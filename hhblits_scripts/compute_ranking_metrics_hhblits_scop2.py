# export PYTHONPATH=$PYTHONPATH:$pwd/remote_homologs
# conda activate .venv/python311_conda_0
# python scripts/compute_ranking_metrics.py
import os
import sys
home_dir = "../"
sys.path.append(home_dir)


import os
import torch
import pandas as pd
import numpy as np
from joblib import delayed, Parallel
from typing import List
# from torchmetrics.functional import pairwise_cosine_similarity
import remote_homologs.pickle_utils as pickle_utils
from sklearn.metrics import precision_recall_curve, auc, roc_curve

# home_dir = ""

data = pd.read_pickle('../data/SCOPe/contrib_hhblits/scop2_th95_hhsearch_logeval_dct.pk')

# ~ 5mins


def compute_remote_homolog_labels(remote_homologs_df: pd.DataFrame, pos_col: str, neg_col: str):
    # pos_col=superfamily_col, neg_col=family_col
    # pos_col=fold_col, neg_col=superfamily_col

    n_data_points = remote_homologs_df.shape[0]

    def compute_labels(i):
        labels = np.zeros((n_data_points), dtype=int)  # 0 is the negative label
        for j in range(n_data_points):
            if remote_homologs_df.loc[i, neg_col] == remote_homologs_df.loc[j, neg_col]:
                labels[j] = -1  # will not be considered in the metric computation
            elif remote_homologs_df.loc[i, pos_col] == remote_homologs_df.loc[j, pos_col]:
                labels[j] = 1  # positive label
        return labels

        # for j in range(n_data_points):
        #     if (remote_homologs_df.loc[i, pos_col] == remote_homologs_df.loc[j, pos_col]) and (remote_homologs_df.loc[i, neg_col] != remote_homologs_df.loc[j, neg_col]):
        #         labels[j] = 1 # positive label
        # return labels

    with Parallel(n_jobs=os.cpu_count(), verbose=1) as parallel:
        list_of_labels = parallel(delayed(compute_labels)(i) for i in range(remote_homologs_df.shape[0]))

    labels = np.stack(list_of_labels)
    print(f"log: finished computing ground-truth labels {labels.shape}")
    return labels


def compute_auroc(y_true: np.array, y_pred: np.array):
    fpr, tpr, ths = roc_curve(y_true, y_pred)
    return auc(fpr, tpr)


def compute_auprc(y_true: np.array, y_pred: np.array):
    precision, recall, ths = precision_recall_curve(y_true, y_pred)
    return auc(recall, precision)


def compute_hitk(y_true: np.array, y_pred: np.array, k=10):
    """
    y_true (numpy.ndarray): Array of actual values (1 for relevant items, 0 for irrelevant items).
    y_pred (numpy.ndarray): Array of predicted values (1 for recommended items, 0 for non-recommended items).
    """
    top_k_indices = np.argsort(y_pred)[::-1][:k]
    hits = any(y_true[i] == 1 for i in top_k_indices)
    hit_at_k = 1 if hits else 0
    return hit_at_k


def get_data_specific_parameters(data_name):
    # SCOP parameters
    if data_name == "SCOP":
        sep = "\t"
        seq_id_col, family_col, superfamily_col, fold_col = "FA-DOMID", "FA", "SF", "CF"
        data_filepath = home_dir + f"data/{data_name}/processed/SCOP_with_seq.tsv"

    # SCOPe parameters
    elif data_name == "SCOPe":
        sep = ","
        seq_id_col, family_col, superfamily_col, fold_col = "sid", "family", "superfamily", "fold"
        data_filepath = home_dir + f"data/{data_name}/all_sequences.csv"

    return sep, seq_id_col, family_col, superfamily_col, fold_col, data_filepath


if __name__ == "__main__":
    # parameters
    data_name = "SCOP"  # SCOP, SCOPe
    remote_homology_level = "superfamily"  # superfamily, fold
    model_name = "hhblits_hhblits_logeval"
    # random, tapebert, proteinbert, esm1b_t33_650M_UR50S, esm2_t33_650M_UR50D, prottrans_bert_bfd, prottrans_albert_bfd, prottrans_t5_bfd

    sep, seq_id_col, family_col, superfamily_col, fold_col, data_filepath = get_data_specific_parameters(data_name)
    # embeddings_dirpath = home_dir + f"data/{data_name}/embeddings/{model_name}/"
    ths = [10, 20, 30, 40, 70, 95]
    # setting up positive and negative col label based on remote_homology_level
    # superfamily level remote homologs
    if remote_homology_level == "superfamily":
        pos_col, neg_col = superfamily_col, family_col
    # fold level remote homology
    elif remote_homology_level == "fold":
        pos_col, neg_col = fold_col, superfamily_col
    else:
        raise f"remote_homology_level={remote_homology_level} not refined. Option: superfamily, fold"

    # loading data and creating main dicts
    data_df = pd.read_csv(data_filepath, sep=sep)
    int2sid_dict = data_df[seq_id_col].to_dict()
    sid2int_dict = {sid: i for i, sid in int2sid_dict.items()}

    # computing embedding similarities

    def get_similarities_for_sid(sid):
        sims=[]
        if sid not in data.keys():
            return np.array([float(-1)]*len(data_df),dtype=float)
        for sid2 in data_df['sid']:
            if sid2 in data[sid].keys():
                sims.append(float(data[sid][sid2]))
            else:
                sims.append(float(-9999))
        return np.array(sims,dtype=float)

    similarities = data_df['sid'].apply(get_similarities_for_sid)

    similarities = np.array(similarities.tolist())

    for th in ths:
        print(f"----------log:{data_name}|{remote_homology_level}|{model_name}|{th}---------------")
        # th = 10
        # creating output directory and files
        out_dir = home_dir + f"data/{data_name}/ranking_results/{model_name}/{remote_homology_level}/th_{th}/"
        os.makedirs(out_dir, exist_ok=True)
        final_results_per_queries_filepath = f"{out_dir}results_per_query.tsv"
        final_results_per_remhom_filepath = f"{out_dir}results_per_{remote_homology_level}.tsv"
        weighted_results_filepath = f"{out_dir}weighted_results.tsv"
        non_weighted_results_filepath = f"{out_dir}non_weighted_results.tsv"

        # checking whether the outputs are already computed
        if (
            os.path.exists(final_results_per_queries_filepath)
            and os.path.exists(final_results_per_remhom_filepath)
            and os.path.exists(weighted_results_filepath)
            and os.path.exists(non_weighted_results_filepath)
        ):
            continue
            # print("results exists")

        # loading data at th
        remote_homologs_filepath = home_dir + f"data/{data_name}/processed_at_th/th_{str(th)}.tsv"
        remote_homologs_df = pd.read_csv(remote_homologs_filepath, sep="\t")
        remhom_int2sid_dict = remote_homologs_df[seq_id_col].to_dict()
        remhom_sid2int_dict = {sid: i for i, sid in remhom_int2sid_dict.items()}

        # computing ground-truth labels
        labels = compute_remote_homolog_labels(remote_homologs_df, pos_col=pos_col, neg_col=neg_col)

        # filtering out the similarities and lables corresponding to each other
        similarity_indices_to_keep = [sid2int_dict[sid] for sid in remote_homologs_df[seq_id_col] if sid in sid2int_dict]
        print(len(similarity_indices_to_keep))

        label_indices_to_keep = [
            remote_homologs_df[remote_homologs_df[seq_id_col] == int2sid_dict[idx]].index[0] for idx in similarity_indices_to_keep
        ]
        print(len(label_indices_to_keep))

        labels_specific_to_conditions = labels[label_indices_to_keep, :]
        labels_specific_to_conditions = labels_specific_to_conditions[:, label_indices_to_keep]
        print(labels_specific_to_conditions.shape)

        similarities_specific_to_conditions = similarities[similarity_indices_to_keep, :]
        similarities_specific_to_conditions = similarities_specific_to_conditions[:, similarity_indices_to_keep]
        print(similarities_specific_to_conditions.shape)

        assert len(similarity_indices_to_keep) == len(label_indices_to_keep), "number of labels and similarities mismatch"

        # computing results per query
        n_queries = labels_specific_to_conditions.shape[0]
        results = []
        for query_id in range(n_queries):
            # query_id = 50
            mask = labels_specific_to_conditions[query_id] != -1

            n_true_pos = (labels_specific_to_conditions[query_id] == 1).sum()
            n_true_neg = (labels_specific_to_conditions[query_id] == 0).sum()

            y_true, y_pred = labels_specific_to_conditions[query_id][mask], similarities_specific_to_conditions[query_id][mask]

            assert (
                mask.sum() == labels_specific_to_conditions[query_id][mask].shape[0] == similarities_specific_to_conditions[query_id][mask].shape[0]
            ), f"mask did not match for {query_id: sid2int_dict[query_id]}"

            auroc = compute_auroc(y_true, y_pred)  # same as roc_auc_score(y_true, y_pred)
            auprc = compute_auprc(y_true, y_pred)
            hit1 = compute_hitk(y_true, y_pred, k=1)
            hit10 = compute_hitk(y_true, y_pred, k=10)
            # print(auroc, auprc, hit10, n_true_pos, n_true_neg)

            data_point = dict(
                sid=remhom_int2sid_dict[query_id], auroc=auroc, auprc=auprc, hit1=hit1, hit10=hit10, n_true_pos=n_true_pos, n_true_neg=n_true_neg
            )
            results.append(data_point)

            # break
            # if query_id==50: break

            if query_id % 1000 == 0:
                print(f"processed: {query_id}")

        results_df = pd.DataFrame.from_dict(results)

        # removing queries that have no true positives
        print("#-queries of no true positives: ", results_df[results_df["n_true_pos"] == 0].shape[0])
        filtered_results_df = results_df[results_df["n_true_pos"] != 0]

        # non-weighted summary result of superfamily/fold level homology ranking
        non_weighted_results_df = filtered_results_df.drop(columns=["sid"]).describe().reset_index()

        # adding other info with results, and removing seq
        final_results_per_queries_df = filtered_results_df.merge(remote_homologs_df, left_on="sid", right_on=seq_id_col, how="left")
        final_results_per_queries_df.drop(columns=["seq"], inplace=True)
        final_results_per_queries_df.reset_index(drop=True, inplace=True)

        n_queries_per_remhomlevel_df = final_results_per_queries_df[[pos_col, "sid"]].groupby(by=pos_col).count().reset_index()
        # performance per rem-hom level (superfamily/fold)
        final_results_per_remhomlevel_df = (
            final_results_per_queries_df[[pos_col, "auroc", "auprc", "hit1", "hit10", "n_true_pos", "n_true_neg"]]
            .groupby(by=pos_col)
            .mean()
            .reset_index()
        )
        final_results_per_remhomlevel_df.sort_values(pos_col, ascending=True, inplace=True)
        final_results_per_remhomlevel_df = final_results_per_remhomlevel_df.merge(n_queries_per_remhomlevel_df, on=pos_col)
        final_results_per_remhomlevel_df.rename(
            columns={"n_true_pos": "avg_n_true_pos", "n_true_neg": "avg_n_true_neg", "sid": "n_queries"}, inplace=True
        )

        # weighted summary result of superfamily/fold level homology ranking
        weighted_results_df = final_results_per_remhomlevel_df.drop(columns=[pos_col]).describe().reset_index()

        # saving results
        final_results_per_queries_df.to_csv(final_results_per_queries_filepath, sep="\t", index=False, header=True)
        final_results_per_remhomlevel_df.to_csv(final_results_per_remhom_filepath, sep="\t", index=False, header=True)
        weighted_results_df.to_csv(weighted_results_filepath, sep="\t", index=False, header=True)
        non_weighted_results_df.to_csv(non_weighted_results_filepath, sep="\t", index=False, header=True)
print(non_weighted_results_filepath)