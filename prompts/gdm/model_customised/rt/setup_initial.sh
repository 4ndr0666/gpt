#!/usr/bin/env bash
# 4ndr0666

set -euo pipefail
trap 'echo "[FATAL] setup_initial.sh failed at line $LINENO — aborting." >&2' ERR
# ============================================================================
# Setup Initial Agents
# ============================================================================
# To use a specific domain, uncomment the relevant section below.
# Currently, only 'paper_review' is enabled by default.
#
# Available domains:
#   - paper_review
#   - balrog (babyai, babaisai, minihack, nle)
#   - genesis_go2walking
#   - imo_grading
#   - imo_proof
#   - polyglot
# ============================================================================

# paper_review
python -m domains.paper_review.curate_subsets
python -m domains.harness --domain paper_review --run_id initial_paper_review_filtered_100_train_0 --subset _filtered_100_train --num_samples 10
python -m domains.harness --domain paper_review --run_id initial_paper_review_filtered_100_val_0 --subset _filtered_100_val --num_samples 10
python -m domains.harness --domain paper_review --run_id initial_paper_review_filtered_100_test_0 --subset _filtered_100_test --num_samples 10
python -m domains.report --domain paper_review --dname ./outputs/initial_paper_review_filtered_100_train_0
python -m domains.report --domain paper_review --dname ./outputs/initial_paper_review_filtered_100_val_0
python -m domains.report --domain paper_review --dname ./outputs/initial_paper_review_filtered_100_test_0


# # balrog: babyai, babaisai, minihack, nle
# python -m domains.balrog.scripts.post_install
# python -m domains.harness --domain balrog_babyai --run_id initial_balrog_babyai_0 --num_samples 1
# python -m domains.report --domain balrog_babyai --dname ./outputs/initial_balrog_babyai_0


# # genesis_go2walking
# python -m domains.harness --domain genesis_go2walking --run_id initial_genesis_go2walking_0 --num_samples 3
# python -m domains.report --domain genesis_go2walking --dname ./outputs/initial_genesis_go2walking_0


# # imo_grading
# bash domains/imo/setup.sh
# python -m domains.harness --domain imo_grading --run_id initial_imo_grading_filtered_100_train_0 --subset _filtered_100_train --num_samples 10
# python -m domains.harness --domain imo_grading --run_id initial_imo_grading_filtered_100_val_0 --subset _filtered_100_val --num_samples 10
# python -m domains.harness --domain imo_grading --run_id initial_imo_grading_filtered_100_test_0 --subset _filtered_100_test --num_samples 10
# python -m domains.report --domain imo_grading --dname ./outputs/initial_imo_grading_filtered_100_train_0
# python -m domains.report --domain imo_grading --dname ./outputs/initial_imo_grading_filtered_100_val_0
# python -m domains.report --domain imo_grading --dname ./outputs/initial_imo_grading_filtered_100_test_0


# # imo_proof
# python -m domains.imo.setup_proofgrader_repo --proofautograder  # ProofAutoGrader
# # python -m domains.imo.setup_proofgrader_repo --generate_dir <dir to run on imo_grading>  # Or use a generated grader
# pip install -e ./proofgrader_repo
# python -m domains.harness --domain imo_proof --run_id initial_imo_proof_0 --num_samples 10
# python -m domains.report --domain imo_proof --dname ./outputs/initial_imo_proof_0


# # polyglot
# cd domains/polyglot
# git clone https://github.com/princeton-nlp/SWE-bench.git
# cd SWE-bench
# git checkout dc4c087c2b9e4cefebf2e3d201d27e36
# pip install -e .
# cd ../../../
# python -m domains.polyglot.prepare_polyglot_dataset
# python -m domains.polyglot.harness --subset small --output_dir ./outputs/initial_polyglot_0 --model_name_or_path eval_run
# python -m domains.polyglot.report --output_dir ./outputs/initial_polyglot_0 --model_name_or_path eval_run

