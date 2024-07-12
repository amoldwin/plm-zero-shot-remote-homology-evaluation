#!/usr/bin/sh
# bash data_count_logs.sh

# ------------SCOP------------
cat data/SCOP/processed/SCOP_with_seq.tsv | wc -l # 31077

ls data/SCOP/embeddings/tapebert/ | wc -l # 31076

ls data/SCOP/embeddings/proteinbert/ | wc -l # 31076

ls data/SCOP/embeddings/esm1b_t33_650M_UR50S/ | wc -l # 31076
ls data/SCOP/embeddings/esm2_t33_650M_UR50D/ | wc -l # 31076

ls data/SCOP/embeddings/prottrans_bert_bfd/ | wc -l # 
ls data/SCOP/embeddings/prottrans_albert_bfd/ | wc -l # 
ls data/SCOP/embeddings/prottrans_t5_bfd/ | wc -l # 


# ------------SCOPe------------
cat data/SCOPe/all_sequences.csv | wc -l # 89131

ls data/SCOPe/embeddings/tapebert/ | wc -l # 89130

ls data/SCOPe/embeddings/proteinbert/ | wc -l # 89130

ls data/SCOPe/embeddings/esm1b_t33_650M_UR50S/ | wc -l # 89130
ls data/SCOPe/embeddings/esm2_t33_650M_UR50D/ | wc -l # 89130

ls data/SCOPe/embeddings/prottrans_bert_bfd/ | wc -l # 89130
ls data/SCOPe/embeddings/prottrans_albert_bfd/ | wc -l # 89130
ls data/SCOPe/embeddings/prottrans_t5_bfd/ | wc -l # 89130