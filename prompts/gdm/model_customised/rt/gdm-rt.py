import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List, Dict, Any, Optional, Union

import docker
from analysis.plot_progress import plot_progress_single, plot_progress_together
from analysis.visualize_archive import (
    visualize_archive_single,
    visualize_archive_together,
)

from utils.common import file_exist_and_not_empty, load_json_file
from utils.constants import REPO_NAME
from utils.docker_utils import (
    build_container,
    cleanup_container,
    copy_from_container,
    copy_to_container,
    log_container_output,
    safe_log,
    setup_logger,
)
from utils.domain_utils import (
    can_domain_ensembled,
    get_domain_eval_subset,
    get_domain_splits,
    get_domain_stagedeval_samples,
)
from utils.gl_utils import (
    apply_diffs_container,
    get_patch_files,
    get_score,
    load_archive_data,
    run_commands_to_check_compilation,
    select_parent,
    setup_initial_gen,
    update_and_save_archive,
    update_node_metadata,
    get_latest_can_select_parent,
    is_starting_node,
    process_meta_patch_files,
)


def run_harness_polyglot(
    root_dir: str, 
    output_dir: str, 
    genid: Union[int, str], 
    skip_staged_eval: bool = False, 
    num_samples: int = -1
) -> None:
    """
    Executes the specialized evaluation harness for the polyglot domain.
    Requires individual docker containers per task instance.
    """
    from domains.polyglot.harness import harness as harness_polyglot
    from domains.polyglot.report import report as report_polyglot

    eval_output_dir = os.path.join(output_dir, f"gen_{genid}", "polyglot_eval")
    test_more_threshold = 0.4  # Matches DGM baseline threshold
    model_name_or_path = "eval_run"
    patch_files = get_patch_files(output_dir, genid)
    run_next_eval = True

    # Small sample size evaluation for staged eval to prevent resource exhaustion
    if not skip_staged_eval:
        test_task_list = load_json_file("./domains/polyglot/subsets/small.json")
        _ = harness_polyglot(
            test_task_list=test_task_list,
            num_samples=-1,
            max_workers=10,
            model_name_or_path=model_name_or_path,
            model_patch_paths=patch_files,
            num_evals=1,
            num_evals_parallel=1,
            pred_dname=eval_output_dir,
            output_dir=eval_output_dir,
            root_dir=root_dir,
        )
        report_polyglot(output_dir=eval_output_dir, run_keyword=model_name_or_path, expected_num_tasks=len(test_task_list))
        stagedeval_score = get_score("polyglot", output_dir, genid)
        run_next_eval = stagedeval_score is not None and stagedeval_score >= test_more_threshold

    # Proceed with broader evaluation if baseline threshold is met
    if run_next_eval:
        test_task_list_more = load_json_file("./domains/polyglot/subsets/medium.json")
        _ = harness_polyglot(
            test_task_list=test_task_list + test_task_list_more if not skip_staged_eval else test_task_list_more,
            num_samples=num_samples,
            max_workers=10,
            model_name_or_path=model_name_or_path,
            model_patch_paths=patch_files,
            num_evals=1,
            num_evals_parallel=1,
            pred_dname=eval_output_dir,
            output_dir=eval_output_dir,
            root_dir=root_dir,
        )
        report_expected_tasks = len(test_task_list + test_task_list_more) if not skip_staged_eval else len(test_task_list_more)
        report_polyglot(output_dir=eval_output_dir, run_keyword=model_name_or_path, expected_num_tasks=report_expected_tasks)

    # Persist evaluation state to node metadata
    update_node_metadata(output_dir, genid, {"run_full_eval": run_next_eval})


def select_next_parent_container(
    docker_client: docker.DockerClient,
    domains: List[str],
    generate_output_dir: str,
    archive: List[Dict[str, Any]],
    root_dir: str = "./",
    root_commit: str = "HEAD",
    max_attempts: int = 10,
) -> Optional[Union[int, str]]:
    """
    Isolates parent selection logic within a containerized environment to prevent host state contamination.
    """
    logger = setup_logger(os.path.join(generate_output_dir, "select_next_parent.log"))

    latest_node = get_latest_can_select_parent(archive, generate_output_dir)
    safe_log(f"select_next_parent_container: latest_node={latest_node}")
    prev_patch_files = get_patch_files(generate_output_dir, latest_node)

    image_name = f"{REPO_NAME}"
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    container_name = f"{REPO_NAME}-nextparent-container-{run_id}"
    container = build_container(docker_client, root_dir, image_name, container_name, verbose=False)
    container.start()
    
    container_output_folder = "/tmp/"
    next_parent_genid = None

    try:
        # Reconstruct the precise source state
        commit_hash = apply_diffs_container(container, prev_patch_files, verbose=False)

        container_generate_output_dir = os.path.join(
            container_output_folder, generate_output_dir.split(os.sep)[-1]
        )
        copy_to_container(
            container,
            source_path=generate_output_dir,
            dest_path=container_generate_output_dir,
            verbose=False,
        )

        command = [
            "timeout",
            "3600",
            "python",
            "-m",
            "utils.run_select_next_parent",
            "--domains",
            *domains,
            "--generate_output_dir",
            container_generate_output_dir,
        ]
        exec_result = container.exec_run(cmd=command, workdir=f"/{REPO_NAME}")
        log_container_output(exec_result, verbose=True)

        container_output_strings = exec_result.output.decode().strip().split("\n")
        next_parent_genid_str = container_output_strings[-1]
        next_parent_genid = int(next_parent_genid_str) if not is_starting_node(next_parent_genid_str) else next_parent_genid_str

    except Exception as e:
        safe_log(f"Error in select_next_parent_container: {e}")
        update_node_metadata(generate_output_dir, latest_node, {"can_select_next_parent": False})
        next_parent_genid = None

    finally:
        # Force hard reset to prevent filesystem drift inside persistent volumes
        exec_result = container.exec_run(cmd=["git", "reset", "--hard", root_commit], workdir=f"/{REPO_NAME}")
        log_container_output(exec_result, verbose=False)
        exec_result = container.exec_run(cmd=["git", "clean", "-fd"], workdir=f"/{REPO_NAME}")
        log_container_output(exec_result, verbose=False)

        cleanup_container(container, verbose=False)

    if next_parent_genid is None:
        if max_attempts > 0:
            next_parent_genid = select_next_parent_container(
                docker_client,
                domains,
                generate_output_dir,
                archive,
                root_dir,
                root_commit,
                max_attempts=max_attempts - 1,
            )
        else:
            raise RuntimeError("Max attempts reached in select_next_parent_container loop.")

    return next_parent_genid


def get_ensemble_scores_container(
    docker_client: docker.DockerClient,
    domain: str,
    generate_output_dir: str,
    gen_output_dir: str,
    root_dir: str = "./",
    root_commit: str = "HEAD",
    prev_patch_files: Optional[List[str]] = None,
    num_samples: int = -1,
    max_workers: int = 5,
    subsets: Optional[List[str]] = None,
) -> List[Optional[float]]:
    """
    Computes ensemble evaluations in a segregated Docker environment.
    Avoids mutable default arguments to prevent state bleed across invocations.
    """
    prev_patch_files = prev_patch_files or []
    subsets = subsets or []
    
    logger = setup_logger(os.path.join(gen_output_dir, "ensemble.log"))

    image_name = f"{REPO_NAME}"
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    container_name = f"{REPO_NAME}-ens-container-{run_id}"
    container = build_container(docker_client, root_dir, image_name, container_name)
    container.start()
    
    container_output_folder = "/tmp/"
    scores = []

    try:
        commit_hash = apply_diffs_container(container, prev_patch_files)

        container_generate_output_dir = os.path.join(
            container_output_folder, generate_output_dir.split(os.sep)[-1]
        )
        copy_to_container(
            container,
            source_path=generate_output_dir,
            dest_path=container_generate_output_dir,
        )

        for subset in subsets:
            command = [
                "timeout",
                "10800",
                "python",
                "-m",
                "utils.run_ensemble",
                "--domain",
                domain,
                "--generate_output_dir",
                container_generate_output_dir,
                "--num_samples",
                str(num_samples),
                "--max_workers",
                str(max_workers),
                "--subset",
                subset,
            ]
            exec_result = container.exec_run(cmd=command, workdir=f"/{REPO_NAME}")
            log_container_output(exec_result)

            container_output_strings = exec_result.output.decode().strip().split("\n")
            try:
                score = float(container_output_strings[-3])
            except ValueError:
                safe_log(f"Failed to parse score from output: {container_output_strings[-3]}")
                score = None
                
            scores.append(score)
            container_predictions_path = container_output_strings[-2]
            container_report_path = container_output_strings[-1]

            predictions_file = os.path.basename(container_predictions_path)
            report_file = os.path.basename(container_report_path)
            local_predictions_path = os.path.join(gen_output_dir, predictions_file)
            local_report_path = os.path.join(gen_output_dir, report_file)
            
            copy_from_container(container, source_path=container_predictions_path, dest_path=local_predictions_path)
            copy_from_container(container, source_path=container_report_path, dest_path=local_report_path)

    except Exception as e:
        safe_log(f"Critical error in get_ensemble_scores_container: {e}")
        scores = [None] * len(subsets)

    finally:
        exec_result = container.exec_run(cmd=["git", "reset", "--hard", root_commit], workdir=f"/{REPO_NAME}")
        log_container_output(exec_result)
        exec_result = container.exec_run(cmd=["git", "clean", "-fd"], workdir=f"/{REPO_NAME}")
        log_container_output(exec_result)
        cleanup_container(container)

    return scores


def eval_produced_agent(
    container: docker.models.containers.Container,
    container_output_folder: str,
    gen_output_dir: str,
    domain: str,
    eval_samples: int = -1,
    eval_workers: int = 10,
    eval_subset: str = "_filtered_100_train",
    eval_test: bool = False,
) -> None:
    """
    Executes the newly generated agent logic within the active container context.
    Extracts post-execution reporting arrays back to host.
    """
    splits = get_domain_splits(domain, eval_test=eval_test)
    for split in splits:
        safe_log(f"Evaluating synthesized agent matrix on {domain} | samples: {eval_samples} | split: {split}")
        eval_run_id = f"{domain}_eval" if split == "train" else f"{domain}_eval_{split}"
        container_evaloutput_folder = os.path.join(container_output_folder, eval_run_id)
        
        command = [
            "timeout",
            "18000",
            "python",
            "-m",
            "domains.harness",
            "--agent_path",
            "./task_agent.py",
            "--output_dir",
            container_output_folder,
            "--run_id",
            eval_run_id,
            "--domain",
            domain,
            "--num_samples",
            str(eval_samples),
            "--num_workers",
            str(eval_workers),
            "--subset",
            eval_subset.replace("_train", f"_{split}"),
        ]
        exec_result = container.exec_run(cmd=command, workdir=f"/{REPO_NAME}")
        log_container_output(exec_result)
        
        command = [
            "timeout",
            "10800",
            "python",
            "-m",
            "domains.report",
            "--domain",
            domain,
            "--dname",
            os.path.join(container_output_folder, eval_run_id),
        ]
        exec_result = container.exec_run(cmd=command, workdir=f"/{REPO_NAME}")
        log_container_output(exec_result)
        
        evaloutput_folder = os.path.join(gen_output_dir, eval_run_id)
        copy_from_container(container, source_path=container_evaloutput_folder, dest_path=evaloutput_folder)


def copy_prev_eval_to_container(
    container: docker.models.containers.Container,
    prev_eval_path: str,
    container_output_folder: str,
    current_genid: Optional[Union[int, str]] = None,
    container_folder_name: Optional[str] = None,
) -> str:
    """
    Transfers historical generation state into the active context while aggressively 
    pruning redundant and volatile payload structures to conserve memory.
    """
    if not os.path.exists(prev_eval_path):
        raise FileNotFoundError(f"Source hierarchy absent: {prev_eval_path}")

    prev_eval_path = os.path.normpath(prev_eval_path)
    tail = os.path.join(*prev_eval_path.split(os.sep)[-1:])
    container_prev_eval_path = os.path.join(container_output_folder, tail)

    container.exec_run(["mkdir", "-p", container_output_folder], workdir="/")

    copy_to_container(container, source_path=prev_eval_path, dest_path=container_prev_eval_path)

    prune_cmds = [
        f"find '{container_prev_eval_path}' -type d -name 'gen_{current_genid}' -prune -exec rm -rf {{}} +",
        f"find '{container_prev_eval_path}' -type d -name '*_eval_val*' -prune -exec rm -rf {{}} +",
        f"find '{container_prev_eval_path}' -type d -name '*_eval_test*' -prune -exec rm -rf {{}} +",
        f"find '{container_prev_eval_path}' -type d -name '*{REPO_NAME}*' -prune -exec rm -rf {{}} +",
        f"find '{container_prev_eval_path}' -type f -name '*.pyc' -delete",
        f"find '{container_prev_eval_path}' -type f \\( -name '*_val' -o -name '*_val.*' -o -name '*_val_*' \\) -delete",
        f"find '{container_prev_eval_path}' -type f \\( -name '*_test' -o -name '*_test.*' -o -name '*_test_*' \\) -delete",
    ]

    for cmd in prune_cmds:
        container.exec_run(["bash", "-lc", cmd], workdir="/")

    exec_result = container.exec_run(["ls", "-l", container_prev_eval_path], workdir="/")
    log_container_output(exec_result)

    if container_folder_name is not None:
        new_container_prev_eval_path = os.path.join(container_output_folder, container_folder_name)
        container.exec_run(["mv", container_prev_eval_path, new_container_prev_eval_path], workdir="/")
        container_prev_eval_path = new_container_prev_eval_path

    return container_prev_eval_path


def generate(
    docker_client: docker.DockerClient,
    domains: List[str],
    output_dir: str,
    run_id: str,
    current_genid: Union[int, str],
    parent_genid: Optional[Union[int, str]],
    root_dir: str,
    root_commit: str = "main",
    eval_samples: Union[int, List[int]] = -1,
    eval_workers: int = 10,
    eval_subsets: Union[str, List[str]] = "_filtered_100",
    meta_patch_files: Optional[List[str]] = None,
    run_meta_agent: bool = True,
    run_baseline: Optional[str] = None,
    optimize_option: str = "only_agent",
    agent_archive_path: Optional[str] = None,
    eval_test: bool = False,
    skip_staged_eval: bool = False,
    edit_select_parent: bool = False,
    max_generation: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Primary iteration core. Synthesizes updates via meta-agent, constructs diffs, and orchestrates downstream evaluation.
    """
    prev_gen_dir = os.path.join(output_dir, f"gen_{parent_genid}")
    gen_output_dir = os.path.join(output_dir, f"gen_{current_genid}")
    os.makedirs(gen_output_dir, exist_ok=True)
    logger = setup_logger(os.path.join(gen_output_dir, "generate.log"))
    
    metadata = {
        "gen_output_dir": gen_output_dir,
        "current_genid": current_genid,
        "parent_genid": parent_genid,
        "run_baseline": run_baseline,
        "prev_patch_files": [],
        "curr_patch_files": [],
        "parent_agent_success": not run_meta_agent,
        "optimize_option": optimize_option,
        "agent_archive_path": agent_archive_path,
        "can_select_next_parent": True,
        "run_eval": not run_meta_agent
    }
    print(json.dumps(metadata, indent=2))

    image_name = f"{REPO_NAME}"
    container_name = f"{REPO_NAME}-gl-container-{run_id}-{current_genid}"
    container = build_container(docker_client, root_dir, image_name, container_name, domains=domains)
    container.start()
    container_output_folder = "/tmp/"

    try:
        if run_baseline and "no_selfimprove" in run_baseline:
            donottouch_reponame = f"/DONOTTOUCH_{REPO_NAME}"
            exec_result = container.exec_run(cmd=["cp", "-r", f"/{REPO_NAME}", donottouch_reponame], workdir="/")
            log_container_output(exec_result)
            meta_patch_files = meta_patch_files or []
            _ = apply_diffs_container(container, meta_patch_files, repo_name=donottouch_reponame)

        # Baseline lineage injection
        if is_starting_node(current_genid):
            meta_patch_files = meta_patch_files or []
            commit_hash = apply_diffs_container(container, meta_patch_files)
            metadata["prev_patch_files"].extend(meta_patch_files)

        patch_files = get_patch_files(output_dir, parent_genid)
        metadata["prev_patch_files"].extend(patch_files)
        commit_hash = apply_diffs_container(container, patch_files)

        if run_meta_agent:
            if run_baseline and "dgm" in run_baseline:
                from baselines.dgm.utils import get_problem_statement
                problem_statement = get_problem_statement(
                    root_dir, output_dir, parent_genid, domains,
                    customized="custom" in run_baseline,
                )
            else:
                if optimize_option == "only_ensemble":
                    container_agent_archive_path = copy_prev_eval_to_container(
                        container, agent_archive_path, container_output_folder,
                        current_genid=current_genid, container_folder_name="agent_archive",
                    )

                if run_baseline == "no_archive":
                    container_prev_eval_path = os.path.join(container_output_folder, *prev_gen_dir.split(os.sep)[-2:])
                    copy_to_container(container, source_path=prev_gen_dir, dest_path=container_prev_eval_path)
                else:
                    container_prev_eval_path = copy_prev_eval_to_container(
                        container, output_dir, container_output_folder, current_genid=current_genid,
                    )

            safe_log("Initiating meta-agent payload generation sequence...")
            container_agentoutput_folder = os.path.join(container_output_folder, "agent_output")
            container_chat_history_file = os.path.join(container_agentoutput_folder, "meta_agent_chat_history.md")
            
            iterations_left = str(max_generation - int(current_genid)) if max_generation is not None else "0"

            if run_baseline and "dgm" in run_baseline:
                command = [
                    "timeout", "21600", "python", "coding_agent.py",
                    "--problem_statement", problem_statement,
                    "--chat_history_file", container_chat_history_file,
                    "--git_dir", f"/{REPO_NAME}",
                    "--base_commit", commit_hash,
                    "--outdir", container_agentoutput_folder,
                ]
            else:
                command = [
                    "timeout", "21600", "python", "run_meta_agent.py",
                    "--chat_history_file", container_chat_history_file,
                    "--repo_path", f"/{REPO_NAME}/",
                    "--evals_folder", container_prev_eval_path,
                    "--git_dir", f"/{REPO_NAME}",
                    "--base_commit", commit_hash,
                    "--outdir", container_agentoutput_folder,
                    "--iterations_left", iterations_left,
                    *(["--model", "claude-3-5-sonnet-20241022"] if domains == ["polyglot"] else []),
                ]

            run_workdir = f"/DONOTTOUCH_{REPO_NAME}" if run_baseline and "no_selfimprove" in run_baseline else f"/{REPO_NAME}"
            exec_result = container.exec_run(cmd=command, workdir=run_workdir)
            log_container_output(exec_result)
            metadata["parent_agent_success"] = (exec_result.exit_code == 0)

            local_agentoutput_folder = os.path.join(gen_output_dir, "agent_output/")
            copy_from_container(container, source_path=container_agentoutput_folder, dest_path=local_agentoutput_folder)

            local_patch_file = os.path.join(local_agentoutput_folder, "model_patch.diff")
            metadata["curr_patch_files"].append(local_patch_file)
            
            run_eval = file_exist_and_not_empty(local_patch_file)
            metadata["run_eval"] = run_eval

            run_commands_to_check_compilation(container, run_baseline=run_baseline, edit_select_parent=edit_select_parent)

        if run_eval and "agent" in optimize_option:
            log_path = os.path.join(gen_output_dir, "generate.log")

            def eval_agent_worker(dom: str, subset: str, n_samples: int):
                setup_logger(log_path)  # Critical re-init for threaded local context
                eval_produced_agent(
                    container, container_output_folder, gen_output_dir,
                    domain=dom, eval_samples=n_samples, eval_workers=eval_workers,
                    eval_subset=subset, eval_test=eval_test,
                )

            if not skip_staged_eval:
                stagedeval_samples = [get_domain_stagedeval_samples(d) for d in domains]
                with ThreadPoolExecutor() as executor:
                    futures = [executor.submit(eval_agent_worker, d, s, n) for d, s, n in zip(domains, eval_subsets, stagedeval_samples)]
                    try:
                        for f in futures:
                            f.result()
                    except Exception as e:
                        for future in futures:
                            if not future.done():
                                future.cancel()
                        raise
                
                stagedeval_scores = [get_score(d, output_dir, current_genid) for d in domains]
                run_next_eval = all([x is not None and x > 0 for x in stagedeval_scores])
            else:
                run_next_eval = True

            if run_next_eval:
                _per_domain_eval_samples = eval_samples if isinstance(eval_samples, list) else [eval_samples] * len(domains)
                with ThreadPoolExecutor() as executor:
                    futures = [executor.submit(eval_agent_worker, d, s, n) for d, s, n in zip(domains, eval_subsets, _per_domain_eval_samples)]
                    try:
                        for f in futures:
                            f.result()
                    except Exception as e:
                        for future in futures:
                            if not future.done():
                                future.cancel()
                        raise
                metadata["run_full_eval"] = True

    except Exception as e:
        safe_log(f"Structural failure in generation loop {current_genid}: {e}")
        metadata["run_eval"] = False

    finally:
        exec_result = container.exec_run(cmd=["git", "reset", "--hard", root_commit], workdir=f"/{REPO_NAME}")
        log_container_output(exec_result)
        exec_result = container.exec_run(cmd=["git", "clean", "-fd"], workdir=f"/{REPO_NAME}")
        log_container_output(exec_result)
        cleanup_container(container)

        eval_successful = all([get_score(d, output_dir, current_genid) is not None for d in domains])
        metadata["valid_parent"] = metadata["run_eval"] and (eval_successful or meta_patch_files is not None)
        
        with open(os.path.join(gen_output_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)

    return metadata


def generate_loop(
    domains: List[str],
    run_id: Optional[str] = None,
    max_generation: int = 3,
    eval_samples: Union[int, List[int]] = -1,
    eval_workers: int = 5,
    eval_subsets: Optional[List[str]] = None,
    parent_selection: str = "score_prop",
    resume_from: Optional[str] = None,
    output_dir_parent: Optional[str] = None,
    meta_patch_files: Optional[List[str]] = None,
    reset_task_agent: bool = False,
    reset_meta_agent: bool = False,
    copy_root_dir: Optional[str] = None,
    run_baseline: Optional[str] = None,
    optimize_option: str = "only_agent",
    agent_archive_path: Optional[str] = None,
    eval_test: bool = False,
    skip_staged_eval: bool = False,
    edit_select_parent: bool = False,
) -> str:
    """
    Main execution orchestration handler. Defines operational perimeter and coordinates autonomous loops.
    """
    eval_subsets = eval_subsets or []
    docker_client = docker.from_env()
    parent_selection = "latest" if run_baseline == "no_archive" else parent_selection
    
    if resume_from:
        output_dir = os.path.normpath(os.path.abspath(resume_from))
        run_id = os.path.basename(output_dir).split("generate_")[-1]
        root_dir, root_commit = setup_initial_gen(
            output_dir, domains, copy_root_dir=copy_root_dir, subsets=eval_subsets,
            resume=True, optimize_option=optimize_option, run_baseline=run_baseline,
            eval_test=eval_test, edit_select_parent=edit_select_parent,
        )
        archive = load_archive_data(os.path.join(output_dir, "archive.jsonl"), last_only=True)["archive"]
    else:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") if run_id is None else run_id
        output_dir_parent = os.path.join(os.getcwd(), "outputs/") if output_dir_parent is None else output_dir_parent
        output_dir = os.path.normpath(os.path.join(output_dir_parent, f"generate_{run_id}/"))
        os.makedirs(output_dir, exist_ok=True)
        
        root_dir, root_commit = setup_initial_gen(
            output_dir, domains, copy_root_dir=copy_root_dir, subsets=eval_subsets,
            resume=False, optimize_option=optimize_option, run_baseline=run_baseline,
            eval_test=eval_test, edit_select_parent=edit_select_parent,
        )

        if not meta_patch_files:
            archive = update_and_save_archive(output_dir, [], new_node="initial")
            metadata = {
                "gen_output_dir": os.path.join(output_dir, "gen_initial"),
                "prev_patch_files": [],
                "curr_patch_files": [],
                "run_eval": True,
            }
        elif reset_task_agent:
            meta_patch_files = process_meta_patch_files(meta_patch_files, output_dir, reset_task_agent=reset_task_agent, reset_meta_agent=reset_meta_agent)
            archive = update_and_save_archive(output_dir, [], new_node="initial")
            gen_output_dir = os.path.join(output_dir, "gen_initial")
            metadata = {
                "gen_output_dir": gen_output_dir,
                "current_genid": "initial",
                "parent_genid": None,
                "run_baseline": run_baseline,
                "prev_patch_files": meta_patch_files,
                "curr_patch_files": [],
                "optimize_option": optimize_option,
                "agent_archive_path": agent_archive_path,
                "can_select_next_parent": True,
                "run_eval": True,
                "run_full_eval": False,
                "valid_parent": True,
            }
            with open(os.path.join(gen_output_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f, indent=4)
        else:
            meta_patch_files = process_meta_patch_files(meta_patch_files, output_dir, reset_task_agent=reset_task_agent, reset_meta_agent=reset_meta_agent)
            archive = update_and_save_archive(output_dir, [], new_node=0)
            metadata = generate(
                docker_client, [d for d in domains if d != "polyglot"], output_dir,
                run_id, current_genid=0, parent_genid=None, root_dir=root_dir, root_commit=root_commit,
                eval_samples=eval_samples, eval_workers=eval_workers, eval_subsets=eval_subsets,
                meta_patch_files=meta_patch_files, run_meta_agent=False, run_baseline=run_baseline,
                optimize_option=optimize_option, agent_archive_path=agent_archive_path,
                eval_test=eval_test, skip_staged_eval=skip_staged_eval, edit_select_parent=edit_select_parent,
                max_generation=max_generation,
            )
            safe_log("generate_loop: Initial state matrix compiled (Node 0).")
            
            if "polyglot" in domains:
                polyglot_samples = eval_samples[domains.index("polyglot")] if isinstance(eval_samples, list) else eval_samples
                run_harness_polyglot(root_dir, output_dir, 0, skip_staged_eval=skip_staged_eval, num_samples=polyglot_samples)

        eval_ensemble = ("ensemble" in optimize_option and all(can_domain_ensembled(d) for d in domains) and run_baseline != "no_archive")
        
        if metadata.get("run_eval") and eval_ensemble:
            _eval_samples = eval_samples if isinstance(eval_samples, list) else [eval_samples] * len(domains)
            for domain, eval_subset, eval_n in zip(domains, eval_subsets, _eval_samples):
                get_ensemble_scores_container(
                    docker_client, domain,
                    (output_dir if optimize_option != "only_ensemble" else agent_archive_path),
                    gen_output_dir=metadata["gen_output_dir"],
                    root_dir=root_dir, root_commit=root_commit,
                    prev_patch_files=metadata["prev_patch_files"] + metadata["curr_patch_files"],
                    num_samples=eval_n,
                    subsets=[eval_subset, eval_subset.replace("_train", "_val")] + (
                        [eval_subset.replace("_train", "_test")] if eval_test else []
                    ),
                )

    with open(os.path.join(output_dir, "generate_loop.log"), "a") as f:
        args_dict = locals()
        filtered_args = {k: v for k, v in args_dict.items() if k != "docker_client"}
        args_str = ", ".join([f"{k}={v}" for k, v in filtered_args.items()])
        f.write(f"Args: {args_str}\n")

    start_genid = len(archive)
    
    if not edit_select_parent or run_baseline == "no_archive":
        parent_genid = select_parent(archive, output_dir, domains, method=parent_selection)
    else:
        parent_genid = select_next_parent_container(docker_client, domains, output_dir, archive, root_dir, root_commit)

    for current_genid in range(start_genid, max_generation + 1):
        metadata = generate(
            docker_client, [d for d in domains if d != "polyglot"], output_dir,
            run_id, current_genid, parent_genid=parent_genid, root_dir=root_dir, root_commit=root_commit,
            eval_samples=eval_samples, eval_workers=eval_workers, eval_subsets=eval_subsets,
            meta_patch_files=meta_patch_files, run_meta_agent=True, run_baseline=run_baseline,
            optimize_option=optimize_option, agent_archive_path=agent_archive_path,
            eval_test=eval_test, skip_staged_eval=skip_staged_eval, edit_select_parent=edit_select_parent,
            max_generation=max_generation,
        )

        archive = update_and_save_archive(output_dir, archive, new_node=current_genid)

        if not metadata.get("parent_agent_success", False):
            update_node_metadata(output_dir, parent_genid, {"valid_parent": False})

        if "polyglot" in domains:
            polyglot_samples = eval_samples[domains.index("polyglot")] if isinstance(eval_samples, list) else eval_samples
            run_harness_polyglot(root_dir, output_dir, current_genid, skip_staged_eval=skip_staged_eval, num_samples=polyglot_samples)

        eval_ensemble = ("ensemble" in optimize_option and all(can_domain_ensembled(d) for d in domains) and run_baseline != "no_archive")
        
        if metadata.get("run_eval") and eval_ensemble:
            _eval_samples = eval_samples if isinstance(eval_samples, list) else [eval_samples] * len(domains)
            for domain, eval_subset, eval_n in zip(domains, eval_subsets, _eval_samples):
                get_ensemble_scores_container(
                    docker_client, domain,
                    (output_dir if optimize_option != "only_ensemble" else agent_archive_path),
                    gen_output_dir=metadata["gen_output_dir"],
                    root_dir=root_dir, root_commit=root_commit,
                    prev_patch_files=metadata["prev_patch_files"] + metadata["curr_patch_files"],
                    num_samples=eval_n,
                    subsets=[eval_subset, eval_subset.replace("_train", "_val")] + (
                        [eval_subset.replace("_train", "_test")] if eval_test else []
                    ),
                )

        for domain in domains:
            splits = get_domain_splits(domain)
            score_types = ["ensemble"] if optimize_option == "only_ensemble" else (["agent", "ensemble", "max"] if eval_ensemble else ["agent"])
            for split in splits:
                for stype in score_types:
                    plot_progress_single(domain, output_dir, split=split, type=stype)
                    visualize_archive_single(domain, output_dir, split=split, type=stype)

        if len(domains) > 1:
            domain_splits_sets = [set(get_domain_splits(d)) for d in domains]
            common_splits = sorted(list(set.intersection(*domain_splits_sets))) if domain_splits_sets else []
            together_score_types = ["ensemble"] if optimize_option == "only_ensemble" else (["agent", "ensemble", "max"] if eval_ensemble else ["agent"])
            
            for split in common_splits:
                for stype in together_score_types:
                    plot_progress_together(domains, output_dir, split=split, type=stype)
                    visualize_archive_together(domains, output_dir, split=split, type=stype)

        if not edit_select_parent or run_baseline == "no_archive":
            parent_genid = select_parent(archive, output_dir, domains, method=parent_selection)
        else:
            parent_genid = select_next_parent_container(docker_client, domains, output_dir, archive, root_dir, root_commit)

        safe_log(f"generate_loop: generation {current_genid} completed, target acquired: parent {parent_genid}")

    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Evolutionary Orchestrator")
    parser.add_argument("--run_id", type=str, default=None, help="Force override run execution identity.")
    parser.add_argument(
        "--domains",
        type=str,
        nargs="+",
        choices=[
            "search_arena", "paper_review", "balrog_babyai", "balrog_babaisai", 
            "balrog_minihack", "balrog_nle", "genesis_go2walking", "genesis_go2walkback", 
            "genesis_go2hop", "polyglot", "imo_grading", "imo_proof",
        ],
        required=True,
        help="Designate operational targets.",
    )
    parser.add_argument("--max_generation", type=int, default=10, help="Terminal evolutionary node limit.")
    parser.add_argument("--eval_samples", type=int, nargs="+", default=None, help="Evaluation capacity matrix per domain (-1 overrides to limitless).")
    parser.add_argument("--eval_workers", type=int, default=10, help="Parallel processing thread cap.")
    parser.add_argument("--parent_selection", type=str, default="score_child_prop", choices=["random", "latest", "best", "score_prop", "score_child_prop"], help="Parent extraction strategy protocol.")
    parser.add_argument("--resume_from", type=str, default=None, help="Force resume from existing structure trace.")
    parser.add_argument("--output_dir_parent", type=str, default=None, help="Root execution target for file persistence.")
    parser.add_argument("--meta_patch_files", type=str, nargs="+", default=[], help="Inject arbitrary logic via diff files.")
    parser.add_argument("--reset_task_agent", default=False, action="store_true", help="Force task agent structural rollback.")
    parser.add_argument("--reset_meta_agent", default=False, action="store_true", help="Force meta agent structural rollback.")
    parser.add_argument("--copy_root_dir", type=str, default=None, help="Direct initialization payload clone target.")
    parser.add_argument("--run_baseline", type=str, choices=["no_selfimprove", "no_archive", "dgm", "dgm_custom", "dgm+no_selfimprove", "dgm_custom+no_selfimprove"], default=None, help="Restrict logic flow to specified baselines.")
    parser.add_argument("--optimize_option", type=str, default="only_agent", choices=["both_agent_ensemble", "only_agent", "only_ensemble"], help="Target extraction axis.")
    parser.add_argument("--agent_archive_path", type=str, default=None, help="Ensemble prerequisite archive path.")
    parser.add_argument("--eval_test", default=False, action="store_true", help="Enable production evaluation overrides.")
    parser.add_argument("--skip_staged_eval", default=False, action="store_true", help="Force fast-track full evaluations without boundary checks.")
    parser.add_argument("--edit_select_parent", default=False, action="store_true", help="Unshackle parent selection manipulation from agent constraints.")
    
    args = parser.parse_args()

    # Pre-flight logic assertions
    if args.optimize_option == "only_ensemble" and args.agent_archive_path is None:
        parser.error("Critical: --agent_archive_path is mandatory when enforcing ensemble logic (--optimize_option=only_ensemble)")
    
    if args.eval_samples is None:
        eval_samples = [-1] * len(args.domains)
    elif len(args.eval_samples) == len(args.domains):
        eval_samples = args.eval_samples
    else:
        parser.error("Critical: Domain mismatch. --eval_samples mapping array length must equal --domains vector length.")

    eval_subsets = [get_domain_eval_subset(d) for d in args.domains]
    
    final_dir = generate_loop(
        domains=args.domains,
        run_id=args.run_id,
        max_generation=args.max_generation,
        eval_samples=eval_samples,
        eval_workers=args.eval_workers,
        eval_subsets=eval_subsets,
        parent_selection=args.parent_selection,
        resume_from=args.resume_from,
        output_dir_parent=args.output_dir_parent,
        meta_patch_files=args.meta_patch_files,
        reset_task_agent=args.reset_task_agent,
        reset_meta_agent=args.reset_meta_agent,
        copy_root_dir=args.copy_root_dir,
        run_baseline=args.run_baseline,
        optimize_option=args.optimize_option,
        agent_archive_path=args.agent_archive_path,
        eval_test=args.eval_test,
        skip_staged_eval=args.skip_staged_eval,
        edit_select_parent=args.edit_select_parent,
    )
    
    print(f"[+] Sequence finalized. Output persisted to: {final_dir}")
