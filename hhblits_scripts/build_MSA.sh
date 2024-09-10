#!/usr/bin/sh

#SBATCH --job-name=multinode_build_MSA
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL


#SBATCH --partition=bigmem
#SBATCH --ntasks=1280
#SBATCH --time=7-00:00:00




module load gnu10 openmpi
module --ignore_cache load hh-suite
 

cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/hhblits
num_nodes=$(scontrol show job $SLURM_JOB_ID | grep -oP 'NumNodes=\K\d+')

srun -m NoPack -n ${SLURM_NTASKS} -N 10 hhblits_mpi -i ~/PROJECTS/remote_homologs/data/SCOPe/hhblits/scope_th95.fas -d ~/PROJECTS/datasets/uniclust30/uniclust30_2018_08/uniclust30_2018_08 -oa3m scope_th95_a3m_wo_ss -n 2 -cpu 1 -v 1