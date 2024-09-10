#!/usr/bin/sh
#SBATCH --job-name=multinode_build_MSA
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL

#SBATCH --partition=contrib
#SBATCH --constraint=intel
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=48
#SBATCH --mem-per-cpu=3400M


#SBATCH --time=5-00:00:00



module load OneAPI
source $SETVARS

module --ignore_cache load hh-suite

cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits

mpirun -np ${SLURM_NTASKS} ffindex_apply_mpi ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_a3m_wo_ss.ff{data,index} -i ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm.ffindex -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm.ffdata -- hhmake -i stdin -o stdout -v 1 -maxmem 3.4
