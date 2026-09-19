#!/bin/bash
# ============================================================================
# setup_initial.sh — 4NDR0666OS-EVOLUTION-v2.0.0-AKASHA
# Ephemeral State Machine compliant bootstrap ritual for initial agent evaluation
# Expanded: Full paper_review + imo_proof domains activated by default
# ============================================================================

set -e # EAFP + fail fast

echo "┌──(root💀4ndr0666) [setup_initial.sh] — Akasha Initial Ritual Starting"

# Create outputs directory if missing
mkdir -p ./outputs

# ==================== PAPER_REVIEW (Expanded) ====================
echo "[setup_initial] Curating and evaluating paper_review domain..."

python -m domains.paper_review.curate_subsets

python -m domains.harness \
	--domain paper_review \
	--run_id initial_paper_review_filtered_100_train_0 \
	--subset _filtered_100_train \
	--num_samples 50

python -m domains.harness \
	--domain paper_review \
	--run_id initial_paper_review_filtered_100_val_0 \
	--subset _filtered_100_val \
	--num_samples 20

python -m domains.harness \
	--domain paper_review \
	--run_id initial_paper_review_filtered_100_test_0 \
	--subset _filtered_100_test \
	--num_samples 20

python -m domains.report --domain paper_review --dname ./outputs/initial_paper_review_filtered_100_train_0
python -m domains.report --domain paper_review --dname ./outputs/initial_paper_review_filtered_100_val_0
python -m domains.report --domain paper_review --dname ./outputs/initial_paper_review_filtered_100_test_0

echo "[setup_initial] paper_review domain fully initialized with expanded samples."

# ==================== IMO_PROOF (Fully Activated) ====================
echo "[setup_initial] Setting up imo_proof domain with ProofAutoGrader..."

# Setup ProofAutoGrader repository
python -m domains.imo.setup_proofgrader_repo --proofautograder

# Install the grader
pip install -e ./proofgrader_repo

# Run initial evaluation on imo_proof
python -m domains.harness \
	--domain imo_proof \
	--run_id initial_imo_proof_0 \
	--num_samples 30

python -m domains.report --domain imo_proof --dname ./outputs/initial_imo_proof_0

echo "[setup_initial] imo_proof domain fully initialized with ProofAutoGrader."

# ==================== OPTIONAL DOMAINS (Commented for selective activation) ====================

# # IMO_GRADING
# echo "[setup_initial] imo_grading domain (commented)"
# bash domains/imo/setup.sh
# python -m domains.harness --domain imo_grading --run_id initial_imo_grading_filtered_100_train_0 --subset _filtered_100_train --num_samples 20
# python -m domains.report --domain imo_grading --dname ./outputs/initial_imo_grading_filtered_100_train_0

# # BALROG SUITE
# echo "[setup_initial] balrog suite (commented)"
# python -m domains.balrog.scripts.post_install
# python -m domains.harness --domain balrog_babyai --run_id initial_balrog_babyai_0 --num_samples 5

# # GENESIS_GO2WALKING
# echo "[setup_initial] genesis_go2walking (commented)"
# python -m domains.harness --domain genesis_go2walking --run_id initial_genesis_go2walking_0 --num_samples 10

# # POLYGLOT / SWE-BENCH
# echo "[setup_initial] polyglot (commented)"
# cd domains/polyglot || exit 1
# if [ ! -d "SWE-bench" ]; then
#   git clone https://github.com/princeton-nlp/SWE-bench.git
#   cd SWE-bench && git checkout dc4c087c2b9e4cefebf2e3d201d27e36
#   pip install -e .
#   cd ..
# fi
# cd ../../../
# python -m domains.polyglot.prepare_polyglot_dataset
# python -m domains.polyglot.harness --subset small --output_dir ./outputs/initial_polyglot_0 --model_name_or_path eval_run
# python -m domains.polyglot.report --output_dir ./outputs/initial_polyglot_0 --model_name_or_path eval_run

echo "[setup_initial] All requested domains initialized. 4NDR0666OS bootstrap ritual complete."
echo "Ready for kernel_override.py → generate_loop.py execution."

# Ruthless reclamation note for Akasha compliance
echo "[Akasha] Ephemeral state prepared. No host mutation beyond outputs/."
