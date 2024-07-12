# Welcome to "Zero-shot Remote Homology evaluation of PLMs'" Documentation!

This repository corresponds to the article titled **"In the Twilight Zone: How Well do Protein Language Models Learn Protein Structure?"**.

Protein language models (PLMs) based on the transformer architecture are increasingly improving performance on protein prediction tasks, including secondary structure, subcellular localization, Superfamily and Family membership, and more. Despite being trained only on protein sequences, PLMs appear to implicitly learn protein structure. This paper investigates whether PLM-learned sequence representations encode structural information and to what extent. We address this by evaluating PLMs on remote homology prediction, where identifying remote homologs from sequence information alone requires structural knowledge, especially in the ``twilight zone'' of very low sequence identity. Through rigorous testing at progressively lower sequence identities, we profile the performance of PLMs ranging from a few million to a few billion parameters in a zero-shot setting. Our findings indicate that while transformer-based PLMs outperform traditional sequence alignment methods, they still struggle in the twilight zone. This suggests that current PLMs have not sufficiently learned protein structure to address remote homology prediction when sequence signals are weak. We believe this opens the way for further research both on the problem of remote homology prediction and on the broader goal of learning sequence- and structure-rich representations of protein molecules. All code, data, and models in this paper are made publicly available.

## Resources

- [Paper](https://www.tbd)
- [Data](https://www.tbd)
- [Code](https://github.com/amoldwin/plm-zero-shot-remote-homology-evaluation)
- [Analysis Notebooks](https://github.com/lanl/EPBD-BERT/tree/main/analysis)

## Installation
In this study, we keep individual python virtual environment for each PLM to generate embeddings using that PLM and one generic environment for other things, such as data preprocessing, analysis and so on. It is recommended to follow the corresponding instructions to setup repositories of the PLMs. However, we provide our used setup commands in the [notes](https://github.com/amoldwin/plm-zero-shot-remote-homology-evaluation/tree/main/notes) directory.

```bash
# Generic python environment
conda create -c conda-forge -p .venv/python311_conda_remhom python=3.11 -y
conda activate .venv/python311_conda_remhom
pip install pandas biopython joblib matplotlib seaborn scikit-learn


# To deactivate and remove the venv
conda deactivate
conda remove -p .venv/python311_conda_remhom --all -y
```

## Data Preprocessing Steps
* **Activate venv**: ```conda activate .venv/python311_conda_remhom```.
* **Preprocess SCOPe datasets**: Download SCOPe datasets: SCOPe datasets are publicly available [here](https://scop.berkeley.edu/). Particularly, we download SCOPe 2.08 ASTRAL sequence subsets at different percentage identities (see paper) from [here](https://scop.berkeley.edu/astral/subsets/ver=2.08). Put the downloaded fasta files in "data/SCOPe/downloads_at_ths/" directory.
    - ```data_preprocessing/preprocess_SCOPe_data.ipynb```



## Protein Sequence Embedding Generation

## Remote Homology Analysis

## Authors

* [Anowarul Kabir] (mailto:akabir4@gmu.edu)- Department of Computer Science, George Mason University
* [Asher Moldwin] (mailto:amoldwin@gmu.edu)- Department of Computer Science, George Mason University
* [Yana Bromberg] (mailto:yana@bromberglab.org)- Department of Computer Science, Emory University
* [Amarda Shehu] (mailto:ashehu@gmu.edu)- Department of Computer Science, George Mason University

## How to cite?
```latex
@article{kabir2024advancing,
  title={Advancing Transcription Factor Binding Site Prediction Using DNA Breathing Dynamics and Sequence Transformers via Cross Attention},
  author={Kabir, Anowarul and Bhattarai, Manish and Rasmussen, Kim {\O} and Shehu, Amarda and Bishop, Alan R and Alexandrov, Boian and Usheva, Anny},
  journal={bioRxiv},
  pages={2024--01},
  year={2024},
  publisher={Cold Spring Harbor Laboratory}
}
```

<!-- # plm-zero-shot-remote-homology-evaluation
plm-zero-shot-remote-homology-evaluation


The SCOP dataset can be downloaded here: https://scop2.mrc-lmb.cam.ac.uk/download

SCOPe can be downloaded here: https://scop.berkeley.edu/astral/ver=2.08

ESM models are available here: https://github.com/facebookresearch/esm 

Prottrans models can be found here: https://github.com/agemagician/ProtTrans


Running our code on SCOPe database: 

(1) Download SCOPe data and choose models to evaluate.

(2) Generate embeddings from each model using the appropriate. embed_gen_<model_type>.py script.

(3) Run ipynb notebook preprocess_SCOPe_data.ipynb

(4) Run compute_ranking_metrics.py, making sure to set desired parameters for data_name, remote_homology_level, and model_name in the "main" method. -->

