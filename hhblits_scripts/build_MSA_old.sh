#!/usr/bin/sh

#SBATCH --job-name=build_MSA
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm/download_uniclust-%j.error
#SBATCH --partition=normal
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=48
#SBATCH --mem=128G 
#SBATCH --time=1-00:00:00


module load gnu10
module load openmpi


source $HOME/miniconda/bin/activate
export PYTHONNOUSERSITE=true
 
conda activate /home/amoldwin/.venv/python39_conda_0



cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/hhblits
cores=$(nproc --all)
echo $cores
mpirun -np 48 hhblits_omp -i ~/PROJECTS/remote_homologs/data/SCOPe/hhblits/scope.fa -d ~/PROJECTS/datasets/uniclust30/uniclust30_2018_08/uniclust30_2018_08 -oa3m scope_new_a3m_wo_ss -n 2 -cpu 1 -v 1

