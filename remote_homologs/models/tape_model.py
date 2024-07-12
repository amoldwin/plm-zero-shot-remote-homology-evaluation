import os
import re
import torch
from typing import List
from torch.nn.utils.rnn import pad_sequence


class TAPEModel:
    def __init__(self, model_name="tapebert", cache_dir="./cache/") -> None:
        cache_dir = cache_dir + model_name + "/"
        os.makedirs(cache_dir, exist_ok=True)

        self._device = "cuda" if torch.cuda.is_available() else "cpu"

        if model_name == "tapebert":
            from tape import ProteinBertModel, TAPETokenizer

            self.tokenizer = TAPETokenizer(vocab="iupac")
            self.padding_value = 0  # manually checked the tokenizer
            self.unk_token = "X"
            model = ProteinBertModel.from_pretrained("bert-base", cache_dir=cache_dir)
            # , force_download=True)
        else:
            raise f"Model name='{model_name}' is not registered"

        model.eval()
        self.embedder = model.to(self._device)

    def get_seq_embedding(self, seq_list: List):
        token_ids_list = []
        for seq in seq_list:
            seq = re.sub(r"[^ARNDCQEGHILKMFPSTWYV]", self.unk_token, seq)
            token_ids = self.tokenizer.encode(seq)
            token_ids = torch.tensor(token_ids)
            token_ids_list.append(token_ids)

        token_ids = pad_sequence(
            token_ids_list, batch_first=True, padding_value=self.padding_value
        )
        token_ids = token_ids.to(self._device)

        seq_lens = (token_ids != self.padding_value).sum(1)
        output = self.embedder(token_ids)
        hidden_states = output[0]  # amino acid embedding

        for i, seq_len in enumerate(seq_lens):
            seq_rep = hidden_states[i, 1 : seq_len - 1].mean(0)
            seq_rep = seq_rep.detach().cpu().numpy()
            yield seq_rep


# test
# model = TAPEModel(model_name="tapebert")
# for e in model.get_seq_embedding(["GCTV", "AXS"]):
#     print(e.shape)
