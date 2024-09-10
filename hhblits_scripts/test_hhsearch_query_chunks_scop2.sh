#!/usr/bin/sh
#SBATCH --job-name=scop2_hhblits
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/scop2_hhblits-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/scop2_hhblits-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL


#SBATCH --partition=normal
#SBATCH --constraint=intel
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --mem-per-cpu=3400M

#SBATCH --time=2-00:00:00


module load OneAPI
source $SETVARS

module --ignore_cache load hh-suite



cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits


mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i ~/PROJECTS/datasets/scop95/scop95_a3m -d ~/PROJECTS/datasets/scop95/scop95 -o hhsearch_all_th95_query_fast_scop2.hhr -scores hhblits_all_th95_query_fast_scop2.scores -all -noprefilt -noaddfilter
