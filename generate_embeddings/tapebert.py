import os
import time
import torch
import argparse
from torch.utils.data import DataLoader
from joblib import Parallel, delayed

from remote_homologs.seq_dataset import SeqDataset
from remote_homologs.models.tape_model import TAPEModel
import remote_homologs.pickle_utils as pickle_utils


def parse_args():
    parser=argparse.ArgumentParser(description="ESM embedding generation")
    parser.add_argument("--model_name", default="tapebert", choices=["tapebert"], help="An TAPE-BERT model name")
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
    model = TAPEModel(model_name)


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

            break
            # if i + 1 == 1:
            #     break

    time.sleep(30)


if __name__ == '__main__':
    args = parse_args()
    # print(args.model_name, args.data_name)
    main(args.model_name, args.data_name)

# source /projects/ashehu/amoldwin/remote_homologs/.venv/tape_rao/bin/activate
# export PYTHONPATH=$PYTHONPATH:$pwd/remote_homologs
# python scripts/embed_gen_tapebert.py
# python -m generate_embeddings.tapebert --data_name=SCOP
