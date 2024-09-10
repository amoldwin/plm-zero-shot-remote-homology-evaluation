#!/usr/bin/sh
#SBATCH --job-name=multinode_build_MSA
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL

#SBATCH --partition=normal
#SBATCH --constraint=intel
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=48
#SBATCH --mem-per-cpu=3400M


#SBATCH --time=5-00:00:00



module load OneAPI
source $SETVARS

module --ignore_cache load hh-suite

cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/hhblits

mpirun -np ${SLURM_NTASKS} hhblits_mpi -i ~/PROJECTS/remote_homologs/data/SCOPe/hhblits/scope_th95.fas -d ~/PROJECTS/datasets/uniclust30/uniclust30_2018_08/uniclust30_2018_08 -oa3m scope_th95_test_a3m_wo_ss -n 2 -cpu 1 -v 1 -maxmem 3.4
