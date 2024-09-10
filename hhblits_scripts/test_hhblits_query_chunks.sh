#!/usr/bin/sh
#SBATCH --job-name=multinode_build_MSA
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL


#SBATCH --partition=bigmem
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --mem=2000000M

#SBATCH --time=5-00:00:00

module load gnu10


source $HOME/miniconda/bin/activate
export PYTHONNOUSERSITE=true
 
conda activate /home/amoldwin/.venv/python39_conda_0


cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits

hhblits_omp -i scope_th95_chunk4.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_all_th95_query_fast_chunk4.hhr -scores hhblits_all_th95_query_fast_chunk4.scores -Z 0 -noprefilt -noaddfilter

hhblits_omp -i scope_th95_chunk5.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_all_th95_query_fast_chunk5.hhr -scores hhblits_all_th95_query_fast_chunk5.scores -Z 0 -noprefilt -noaddfilter

hhblits_omp -i scope_th95_chunk6.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_all_th95_query_fast_chunk6.hhr -scores hhblits_all_th95_query_fast_chunk6.scores -Z 0 -noprefilt -noaddfilter

hhblits_omp -i scope_th95_chunk7.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_all_th95_query_fast_chunk7.hhr -scores hhblits_all_th95_query_fast_chunk_7.scores -Z 0 -noprefilt -noaddfilter

hhblits_omp -i scope_th95_chunk8.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_all_th95_query_fast_chunk8.hhr -scores hhblits_all_th95_query_fast_chunk8.scores -Z 0 -noprefilt -noaddfilter

hhblits_omp -i scope_th95_chunk9.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_all_th95_query_fast_chunk9.hhr -scores hhblits_all_th95_query_fast_chunk9.scores -Z 0 -noprefilt -noaddfilter

