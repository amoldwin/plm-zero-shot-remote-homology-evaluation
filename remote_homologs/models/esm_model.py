import re
import torch
import esm
from typing import List


class ESMModel:
    def __init__(self, model_name, cache_dir="./cache/") -> None:
        # esm2_t33_650M_UR50D, esm1b_t33_650M_UR50S
        self._device = "cuda" if torch.cuda.is_available() else "cpu"

        if model_name == "esm1b_t33_650M_UR50S":
            model, alphabet = esm.pretrained.esm1b_t33_650M_UR50S()  # emb: 1280
        elif model_name == "esm2_t33_650M_UR50D":
            model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()  # emb: 1280
        else:
            raise f"Model name='{model_name}' is not registered"

        self.batch_converter = alphabet.get_batch_converter()
        self.padding_idx = alphabet.padding_idx
        self.unk_token = "X"
        self.model = model.to(self._device)
        self.model.eval()
        self.model_name = model_name

    def get_seq_embedding(self, seq_list: List):
        seq_list_new = []
        for i, seq in enumerate(seq_list):
            if self.model_name == "esm1b_t33_650M_UR50S":
                seq = seq[:1022]  # max len
            seq = re.sub(r"[^LAGVSERTIDPKQNFYMHWCXBUZO]", self.unk_token, seq)
            seq_list_new.append((f"id_{i}", seq))

        batch_labels, batch_strs, batch_tokens = self.batch_converter(seq_list_new)
        batch_tokens = batch_tokens.to(self._device)
        batch_lens = (batch_tokens != self.padding_idx).sum(1)

        results = self.model(batch_tokens, repr_layers=[33], return_contacts=False)
        token_rep = results["representations"][33]

        for i, tokens_len in enumerate(batch_lens):
            seq_rep = token_rep[i, 1 : tokens_len - 1].mean(0)
            seq_rep = seq_rep.detach().cpu().numpy()
            yield seq_rep


# seq_list = ["M1JKT", "KALTA"]
# model = ESMModel("esm1b_t33_650M_UR50S")
# for e in model.get_seq_embedding(seq_list):
#     # print(e)
#     print(e.shape)
