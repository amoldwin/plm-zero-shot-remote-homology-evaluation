# source /projects/ashehu/amoldwin/remote_homologs/.venv/proteinbert_tf_brandes/bin/activate
# export PYTHONPATH=$PYTHONPATH:$pwd/remote_homologs
# python scripts/embed_gen_proteinbert.py

import os
import time
import pandas as pd
from joblib import Parallel, delayed

from remote_homologs.models.proteinbert_model import ProteinBERTModel
import remote_homologs.pickle_utils as pickle_utils

model_name = "proteinbert"
data_name = "SCOP"  # SCOP, SCOPe
out_dir = f"./data/{data_name}/embeddings/{model_name}/"
os.makedirs(out_dir, exist_ok=True)
batch_size = 128

if data_name == "SCOPe":
    data_filepath = "./data/SCOPe/all_sequences.csv"
    id_col = "sid"
    seq_col = "sequence"
    sep = ","
elif data_name == "SCOP":
    data_filepath = "./data/SCOP/processed/SCOP_with_seq.tsv"
    id_col = "FA-DOMID"
    seq_col = "seq"
    sep = "\t"

data_df = pd.read_csv(data_filepath, sep=sep)
n_batches = data_df.shape[0] // batch_size
max_seq_len = data_df[seq_col].map(len).max()
print(f"max_seq_len={max_seq_len}, batch_size={batch_size}, n_batches={n_batches}")

data_df_iterator = pd.read_csv(data_filepath, sep=sep, chunksize=batch_size)


protein_bert = ProteinBERTModel(max_seq_len)

for i, data_df in enumerate(data_df_iterator):
    # if i + 1 < 84: # to skip number of batches
    #     continue

    print(f"Log: evaluating {i+1}|{n_batches}...")
    seq_ids = data_df[id_col].tolist()

    are_all_evaluated = True
    for seq_id in seq_ids:
        if not os.path.exists(out_dir + str(seq_id) + ".pkl"):
            are_all_evaluated = False
            break

    # print(are_all_evaluated)
    if are_all_evaluated:
        continue

    seqs = [str(s).strip().upper() for s in data_df[seq_col].tolist()]
    # print(seqs)

    embed = protein_bert.get_seq_embedding(seqs)
    # print(embed.shape)
    # print(embed)

    # saving in parallal, using cpus,
    with Parallel(n_jobs=batch_size) as parallel:
        parallel(delayed(pickle_utils.check_b4_save)(embed[j], out_dir + str(seq_id) + ".pkl") for j, seq_id in enumerate(seq_ids))

    # break
    # if i + 1 == 90:
    #     break

time.sleep(30)
