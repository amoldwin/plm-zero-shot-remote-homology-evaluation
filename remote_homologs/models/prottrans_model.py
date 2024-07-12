import numpy as np
from typing import List


class ProttransModel:
    def __init__(self, model_name, cache_dir="./cache/") -> None:
        """model_name (str): prottrans_bert_bfd, prottrans_albert_bfd, prottrans_t5_bfd"""
        self.embedder = self.__load_embedder(model_name)
        self.tokenizer = self.embedder._tokenizer

    def get_seq_embedding(self, seq_list: List):
        for e in self.embedder.embed_batch(seq_list):
            # print(e.shape)  # np array
            e = np.mean(e, axis=0)
            yield e

    def __load_embedder(self, model_name):
        if model_name == "prottrans_bert_bfd":
            from bio_embeddings.embed import ProtTransBertBFDEmbedder

            model = ProtTransBertBFDEmbedder()  # out shape: [seq_len, 1024]

        elif model_name == "prottrans_albert_bfd":
            from bio_embeddings.embed import ProtTransAlbertBFDEmbedder

            model = ProtTransAlbertBFDEmbedder()  # out shape: [seq_len, 4096]

        elif model_name == "prottrans_t5_bfd":
            from bio_embeddings.embed import ProtTransT5BFDEmbedder

            model = ProtTransT5BFDEmbedder()  # out shape: [seq_len, 1024]

        else:
            raise NotImplementedError()

        return model


# model = ProttransModel(model_name="prottrans_t5_bfd")
# e = model.embedder.embed("AKLKTRRGAAKRFKATANGFKRKQAFKRHILTKKSAKRIRQLRGCVMVHVSDVASVRRMCPYI")  # take 1-seq
# print(e)

# for e in model.embedder.embed_batch(["AKLKTRRGAAKRFKATANGFKRKQAFKRHILTKKSAKRIRQLRGCVMVHVSDVASVRRMCPYI"]):
#     print(e.shape)  # np array

# for i, e in enumerate(model.get_seq_embedding(["AKLKTRRGAAKRFKATANGFKRKQAFKRHILTKKSAKRIRQLRGCVMVHVSDVASVRRMCPYI"])):
#     print(i, e.shape)  # np array
#     print(e)
#     print(np.isnan(e).any())
