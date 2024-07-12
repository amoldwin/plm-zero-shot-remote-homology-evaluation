from torch.utils.data import Dataset
import pandas as pd


class SeqDataset(Dataset):
    def __init__(self, data_filepath, id_col, seq_col, sep=",") -> None:
        super().__init__()
        self.data_df = pd.read_csv(data_filepath, sep=sep)
        self.id_col = id_col
        self.seq_col = seq_col

    def __len__(self):
        return self.data_df.shape[0]

    def get_max_seq_len(self):
        # SCOPe: 1664
        return self.data_df[self.seq_col].map(len).max()

    def __getitem__(self, index):
        row = self.data_df.iloc[index]
        seq_id = str(row[self.id_col])
        seq = str(row[self.seq_col])
        seq = seq.strip().upper()
        # print(seq_id, seq)
        return dict(seq_id=seq_id, seq=seq)


# ds = SeqDataset(
#     data_filepath="./data/SCOPe/all_sequences100.csv", id_col="sid", seq_col="sequence", sep=","
# )
# print(ds.__len__())
# print(ds.__getitem__(99))
# print(ds.get_max_seq_len())  # SCOPe: 1664

# from torch.utils.data import DataLoader

# dl = DataLoader(ds, batch_size=2, num_workers=1)
# for i, b in enumerate(dl):
#     print(b)
#     seq_ids, seq_list = b["seq_id"], b["seq"]
#     print(seq_ids, seq_list)
#     break


# ds = SeqDataset(data_filepath="./data/SCOP/processed/SCOP_with_seq.tsv", id_col="FA-DOMID", seq_col="seq", sep="\t")
# print(ds.__len__())
# print(ds.__getitem__(26294))
