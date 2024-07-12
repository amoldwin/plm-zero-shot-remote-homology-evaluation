import os
from proteinbert import load_pretrained_model


class ProteinBERTModel:
    def __init__(self, max_seq_len=1024, cache_dir="./cache/proteinbert/"):
        os.makedirs(cache_dir, exist_ok=True)

        self.max_seq_len = max_seq_len + 2  # +2 b/c of '<START>', '<END>'

        pretrained_model_generator, self.tokenizer = load_pretrained_model(
            local_model_dump_dir=cache_dir,
            local_model_dump_file_name="epoch_92400_sample_23500000.pkl",
        )
        self.model = pretrained_model_generator.create_model(self.max_seq_len)
        # from proteinbert.tokenization import token_to_index
        # print(token_to_index["<PAD>"]) 25

    def get_seq_embedding(self, seq_list):
        # seq_list = ["MKTVR", "MKTVR"]
        # print(len(max(seq_list, key=len)), self.max_seq_len)
        token_ids = self.tokenizer.encode_X(seq_list, self.max_seq_len)
        # print(token_ids)
        # print(token_ids[0].shape)
        local_rep, global_rep = self.model.predict(token_ids)
        # print(local_rep.shape, global_rep.shape)
        return global_rep


# m = ProteinBERTModel()
