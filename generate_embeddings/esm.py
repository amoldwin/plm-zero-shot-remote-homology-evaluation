# run: python -m generate_embeddings.esm --model_name=esm1b_t33_650M_UR50S --data_name=SCOP

import os
import time
import torch
import argparse
from torch.utils.data import DataLoader
from joblib import Parallel, delayed

from remote_homologs.seq_dataset import SeqDataset
from remote_homologs.models.esm_model import ESMModel
from remote_homologs import pickle_utils as pickle_utils

def parse_args():
    parser=argparse.ArgumentParser(description="ESM embedding generation")
    parser.add_argument("--model_name", default="esm1b_t33_650M_UR50S", choices=["esm2_t33_650M_UR50D", "esm1b_t33_650M_UR50S"], help="An ESM model name")
    parser.add_argument("--data_name", default="SCOPe", choices=["SCOPe", "SCOP"], help="A dataset name")
    args=parser.parse_args()
    return args

def main(model_name, data_name):
    out_dir = f"./data/{data_name}/embeddings/{model_name}/"

    if data_name == "SCOPe":
        ds = SeqDataset(data_filepath="./data/SCOPe/all_sequences.csv", id_col="sid", seq_col="sequence", sep=",")
    elif data_name == "SCOP":
        ds = SeqDataset(data_filepath="./data/SCOP/processed/SCOP_with_seq.tsv", id_col="FA-DOMID", seq_col="seq", sep="\t")
    dl = DataLoader(ds, batch_size=64, shuffle=False, num_workers=1)

    os.makedirs(out_dir, exist_ok=True)
    model = ESMModel(model_name)

    def eval_this_batch(seq_ids):
        for seq_id in seq_ids:
            if not os.path.exists(out_dir + str(seq_id) + ".pkl"):
                return True
        return False

    with torch.no_grad():
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

if __name__ == '__main__':
    args = parse_args()
    main(args.model_name, args.data_name)
