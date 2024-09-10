#!/usr/bin/sh
#SBATCH --job-name=compile_hhbits_scores
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/compile_hhbits_scores-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/compile_hhbits_scores-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL


#SBATCH --partition=bigmem
#SBATCH --mem=2000000M

#SBATCH --time=5-00:00:00

module load gnu10


source $HOME/miniconda/bin/activate
export PYTHONNOUSERSITE=true
 
conda activate /home/amoldwin/.venv/python39_conda_0

python compile_hhsearch_scores_dict.py