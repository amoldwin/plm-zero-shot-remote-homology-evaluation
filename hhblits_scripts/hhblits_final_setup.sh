#!/usr/bin/sh
#SBATCH --job-name=multinode_build_MSA
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm_asher/download_uniclust-%j.error
#SBATCH --mail-user=<amoldwin@gmu.edu>
#SBATCH --mail-type=BEGIN,END,FAIL

#SBATCH --partition=contrib

#SBATCH --mem=64G

#SBATCH --time=5-00:00:00

module load gnu10
module load openmpi


source $HOME/miniconda/bin/activate
export PYTHONNOUSERSITE=true
 
conda activate /home/amoldwin/.venv/python39_conda_0


cd /home/amoldwin/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits

sort -k3 -n -r  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_cs219.ffindex | cut -f1 > sorting.dat
    
ffindex_order sorting.dat  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm.ff{data,index}  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm_ordered.ff{data,index}
mv  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm_ordered.ffindex  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm.ffindex
mv  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm_ordered.ffdata  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_hhm.ffdata
    
ffindex_order sorting.dat  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_a3m.ff{data,index}  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_a3m_ordered.ff{data,index}
mv  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_a3m_ordered.ffindex  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_a3m.ffindex
mv  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_a3m_ordered.ffdata  ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/scope_th95_test_a3m.ffdata



