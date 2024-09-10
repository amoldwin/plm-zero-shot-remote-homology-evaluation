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

hhblits_omp -i scope_th95.fas -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_all_th95_query_fast.hhr -scores hhblits_all_th95_query_fast.scores -Z 0 -noprefilt -noaddfilter


##hhblits -i test_query.a3m -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_test_query.hhr -scores test_query.scores -Z 0 -noprefilt -noaddfilter

##hhsearch -i scope_small_sample_fas.ffdata -d ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test -o hhblits_test_query.hhr -noprefilt -scores test_query.scores -all