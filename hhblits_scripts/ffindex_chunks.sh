module load gnu10


source $HOME/miniconda/bin/activate
export PYTHONNOUSERSITE=true
 
conda activate /home/amoldwin/.venv/python39_conda_0

cd ~/PROJECTS/remote_homologs/data/SCOPe/contrib_hhblits/

ffindex_from_fasta -s scope_th95_chunk0.fas.ff{data,index} scope_th95_chunk0.fas
ffindex_from_fasta -s scope_th95_chunk1.fas.ff{data,index} scope_th95_chunk1.fas
ffindex_from_fasta -s scope_th95_chunk2.fas.ff{data,index} scope_th95_chunk2.fas
ffindex_from_fasta -s scope_th95_chunk3.fas.ff{data,index} scope_th95_chunk3.fas
ffindex_from_fasta -s scope_th95_chunk4.fas.ff{data,index} scope_th95_chunk4.fas
ffindex_from_fasta -s scope_th95_chunk5.fas.ff{data,index} scope_th95_chunk5.fas
ffindex_from_fasta -s scope_th95_chunk6.fas.ff{data,index} scope_th95_chunk6.fas
ffindex_from_fasta -s scope_th95_chunk7.fas.ff{data,index} scope_th95_chunk7.fas
ffindex_from_fasta -s scope_th95_chunk8.fas.ff{data,index} scope_th95_chunk8.fas
ffindex_from_fasta -s scope_th95_chunk9.fas.ff{data,index} scope_th95_chunk9.fas