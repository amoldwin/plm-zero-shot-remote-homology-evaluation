#!/usr/bin/sh
#SBATCH --job-name=multinode_build_MSA
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL


#SBATCH --partition=normal
#SBATCH --constraint=intel
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --mem-per-cpu=3400M

#SBATCH --time=1-00:00:00


module load OneAPI
source $SETVARS

module --ignore_cache load hh-suite



cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits


mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk0.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk0.hhr -scores hhblits_all_th95_query_fast_chunk0.scores -all -noprefilt -noaddfilter

mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk1.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk1.hhr -scores hhblits_all_th95_query_fast_chunk1.scores -all -noprefilt -noaddfilter

mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk2.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk2.hhr -scores hhblits_all_th95_query_fast_chunk2.scores -all -noprefilt -noaddfilter

mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk3.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk3.hhr -scores hhblits_all_th95_query_fast_chunk3.scores -all -noprefilt -noaddfilter

mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk4.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk4.hhr -scores hhblits_all_th95_query_fast_chunk4.scores -all -noprefilt -noaddfilter

## mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk5.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk5.hhr -scores hhblits_all_th95_query_fast_chunk5.scores -all -noprefilt -noaddfilter

## mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk6.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk6.hhr -scores hhblits_all_th95_query_fast_chunk6.scores -all -noprefilt -noaddfilter

## mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk7.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk7.hhr -scores hhblits_all_th95_query_fast_chunk7.scores -all -noprefilt -noaddfilter

## mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk8.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk8.hhr -scores hhblits_all_th95_query_fast_chunk8.scores -all -noprefilt -noaddfilter

## mpirun -np ${SLURM_NTASKS}  hhsearch_mpi -i scope_th95_chunk9.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhsearch_all_th95_query_fast_chunk9.hhr -scores hhblits_all_th95_query_fast_chunk9.scores -all  -noprefilt -noaddfilter

