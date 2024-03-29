# source /projects/ashehu/amoldwin/remote_homologs/.venv/bioembeddings_dallago/bin/activate
# export PYTHONPATH=$PYTHONPATH:$pwd/remote_homologs
# python scripts/embed_gen_prottrans.py

import os
import time
import torch
from torch.utils.data import DataLoader
from joblib import Parallel, delayed
import numpy as np

from remote_homologs.seq_dataset import SeqDataset
from remote_homologs.models.prottrans_model import ProttransModel
import remote_homologs.pickle_utils as pickle_utils

# prottrans_bert_bfd, prottrans_albert_bfd, prottrans_t5_bfd
model_name = "prottrans_albert_bfd"
data_name = "SCOP"  # SCOP, SCOPe
out_dir = f"./data/{data_name}/embeddings/{model_name}/"


if data_name == "SCOPe":
    ds = SeqDataset(
        data_filepath="./data/SCOPe/all_sequences.csv",
        id_col="sid",
        seq_col="sequence",
        sep=",",
    )
elif data_name == "SCOP":
    ds = SeqDataset(
        data_filepath="./data/SCOP/processed/SCOP_with_seq.tsv",
        id_col="FA-DOMID",
        seq_col="seq",
        sep="\t",
    )
dl = DataLoader(ds, batch_size=64, shuffle=False, num_workers=1)

os.makedirs(out_dir, exist_ok=True)
model = ProttransModel(model_name)


def eval_this_batch(seq_ids):
    for seq_id in seq_ids:
        if not os.path.exists(out_dir + str(seq_id) + ".pkl"):
            return True
    return False


with torch.no_grad():
    # for some unknown reason [prottrans_albert_bfd, prottrans_t5_bfd] are producing nan embeddings when seq are fed into batch
    # handing those cases manually
    # for i, idx in enumerate(["list of ids goes here"]):
    #     x = ds.__getitem__(idx)
    #     seq_id, seq = x["seq_id"], x["seq"]

    #     for _, embed in enumerate(model.get_seq_embedding([seq])):
    #         print(i, idx, seq_id, np.isnan(embed).any())  # seq, embed
    #         pickle_utils.check_b4_save(embed, out_dir + str(seq_id) + ".pkl")
    #         # raise

    for i, batch in enumerate(dl):
        print(f"Log: evaluating {i+1}|{len(dl)}...")

        seq_ids, seq_list = batch["seq_id"], batch["seq"]
        # print(seq_ids, seq_list)

        if not eval_this_batch(seq_ids):
            continue

        # saving in parallal, using cpus,
        with Parallel(n_jobs=dl.batch_size) as parallel:
            parallel(
                delayed(pickle_utils.check_b4_save)(embed, out_dir + str(seq_ids[j]) + ".pkl")
                for j, embed in enumerate(model.get_seq_embedding(seq_list))
            )

        # break
        # if i + 1 == 2:
        #     break

time.sleep(30)
