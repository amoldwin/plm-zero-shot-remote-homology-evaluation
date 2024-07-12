# Welcome to "Zero-shot Remote Homology evaluation of PLMs'" Documentation!

This repository corresponds to the article titled **"In the Twilight Zone: How Well do Protein Language Models Learn Protein Structure?"**.

Protein language models (PLMs) based on the transformer architecture are increasingly improving performance on protein prediction tasks, including secondary structure, subcellular localization, Superfamily and Family membership, and more. Despite being trained only on protein sequences, PLMs appear to implicitly learn protein structure. This paper investigates whether PLM-learned sequence representations encode structural information and to what extent. We address this by evaluating PLMs on remote homology prediction, where identifying remote homologs from sequence information alone requires structural knowledge, especially in the ``twilight zone'' of very low sequence identity. Through rigorous testing at progressively lower sequence identities, we profile the performance of PLMs ranging from a few million to a few billion parameters in a zero-shot setting. Our findings indicate that while transformer-based PLMs outperform traditional sequence alignment methods, they still struggle in the twilight zone. This suggests that current PLMs have not sufficiently learned protein structure to address remote homology prediction when sequence signals are weak. We believe this opens the way for further research both on the problem of remote homology prediction and on the broader goal of learning sequence- and structure-rich representations of protein molecules. All code, data, and models in this paper are made publicly available.

## Resources

- [Paper](https://www.tbd) Will be added soon.
- [Data](https://github.com/amoldwin/plm-zero-shot-remote-homology-evaluation/tree/main/data)
- [Code](https://github.com/amoldwin/plm-zero-shot-remote-homology-evaluation)
- [Analysis](https://github.com/lanl/EPBD-BERT/tree/main/analysis)

## Installation
In this study, we keep individual python virtual environment for each PLM to generate embeddings using that PLM and one generic environment for other things, such as data preprocessing, analysis and so on. It is recommended to follow the corresponding instructions to setup repositories of the PLMs. However, we provide our used setup commands in the [notes](https://github.com/amoldwin/plm-zero-shot-remote-homology-evaluation/tree/main/notes) directory.

```bash
# Generic python environment
conda create -c conda-forge -p .venv/python311_conda_remhom python=3.11 -y
conda activate .venv/python311_conda_remhom
pip install pandas biopython pyfastx joblib matplotlib seaborn scikit-learn torchmetrics
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


# To deactivate and remove the venv
conda deactivate
conda remove -p .venv/python311_conda_remhom --all -y
```

## Data Preprocessing Steps
* **Activate venv**: ```conda activate .venv/python311_conda_remhom```.

* **Preprocess SCOPe datasets**: SCOPe datasets are publicly available [here](https://scop.berkeley.edu/). Particularly, we download SCOPe 2.08 ASTRAL sequence subsets at different percentage identities (see paper) from [here](https://scop.berkeley.edu/astral/subsets/ver=2.08). Put the downloaded fasta files in "data/SCOPe/downloads_at_ths/" directory. The following notebook will process the data.
    - ```data_preprocessing/preprocess_SCOPe_data.ipynb```

* **Preprocess SCOP2 datasets**: SCOP2 datasets are publicly available [here](https://www.ebi.ac.uk/pdbe/scop/). We download SCOP domain classification and definitions (files: scop-cla-latest.txt, scop-des-latest.txt, scop_fa_represeq_lib_latest.fa ([link](https://www.ebi.ac.uk/pdbe/scop/files))) and put into the "data/SCOP/downloads/" directory. The following notebook will process the downloaded data.
    - ```data_preprocessing/preprocess_SCOP_data.ipynb```

    Next we cluster the processed protein sequences using CD-HIT at different sequence identities. The CD-HIT commands are summarized in "[notes/cdhit_with_blast_setup.txt]()". The clusters at different sequence identity thresholds are in "[data/SCOP/clusters_fa_represeq]()". Next we process the clusters using the following notebook.
    - ```data_preprocessing/preprocess_SCOP_clusters.ipynb```

## Protein Sequence Embedding Generation
**Requirements**: Different PLM may have dependencies on different python or pytorch or tensorflow version. Therefore, we keep separate virtual environment. Follow specific PLM insallation guide from their official github pages given in notes/plm_venvs_setup.md. Example commands for generating embeddings using different models are given below.
```bash
    python -m generate_embeddings.proteinbert --data_name=SCOPe
    python -m generate_embeddings.tapebert --data_name=SCOPe
    python -m generate_embeddings.esm --model_name=esm1b_t33_650M_UR50S --data_name=SCOPe
    python -m generate_embeddings.prottrans --model_name=prottrans_t5_bfd --data_name=SCOPe
```
## HHblits Alignment-based Homology Detection
HHblits predictions can be generated on SCOPe by following the directions [here](https://github.com/soedinglab/hh-suite) and [here](https://github.com/soedinglab/hh-suite/wiki). The step-by step instructions for doing this are as follows, but note that some settings may need to be changed depending on your available resources.
(1) Install HHblits using the linked instructions and download Uniclust30. MPI is prefferable to OpenMP when multiple CPUs are needed such as when computing Multiple Sequence Alignments, but we also used OpenMP for querying, when multithreading on a singleCPU was needed.
(2) Following [this](https://github.com/soedinglab/hh-suite/wiki#1-creating-a-database-of-hhblits-compatible-msas): Using the SCOPe FASTA file (we used the entire database) and convert to an FFIndex database: ```ffindex_from_fasta -s scope_fas.ff{data,index} scope.fa```
(3) Create Multiple Sequence Alignments for SCOPe. When using the entire database this becomes very computationally intensive and requires trial and error to find the correct settings. For example, we had access to 10 intel nodes that could be used in parallel. Each node had a maximum RAM allocation of 3.4GB, which required us to use the "maxmem" option to ensure that the job could complete successfully. See ```hhblits_scripts/build_MSA_n3.sh``` for our script.
(4) Run ```compute HHMs.sh``` and ```compute_context_states.sh```
(5) Run ```HHblits_final_setup.sh```
(6) Split SCOPe into chunks as in cell 10 of ```compute_ranking_metrics_debug_hhblits.ipynb```
(7) Run ```ffindex_chunks.sh```
(8) Run ```test_hhblits_query_chunks.sh```
(9) Run ```compile_hhblits_scores_dct.sh```
(10) Run ```compute_ranking_metrics_hhblits.py```

## Remote Homology Analysis
* **Activate venv**: ```conda activate .venv/python311_conda_remhom```.
```bash
    # To compute performance metrics
    python -m analysis.compute_performance_metrics --model_name=esm1b_t33_650M_UR50S --data_name=SCOPe --remote_homology_level=superfamily
    # All results and weighted/unweighted performance metrics across all thresholds 
    analysis/all_results_and_dataset_statistics.ipynb
    # To analyze models performance metrics 
    analysis/plot_performance_comparison.ipynb
    # To compare models aggrement
    analysis/plot_performance_aggrement_comparison_with_hhblits.ipynb
``` 

## Raw Performance Metric Scores
* data/SCOPe/ranking_results
* data/SCOP/ranking_results_cdhit_repseq
* data/SCOP/ranking_results_random_repseq

## Authors

* [Anowarul Kabir] (mailto:akabir4@gmu.edu)- Department of Computer Science, George Mason University
* [Asher Moldwin] (mailto:amoldwin@gmu.edu)- Department of Computer Science, George Mason University
* [Yana Bromberg] (mailto:yana@bromberglab.org)- Department of Computer Science, Emory University
* [Amarda Shehu] (mailto:ashehu@gmu.edu)- Department of Computer Science, George Mason University

## How to cite?
```latex
@article{?,
  title={In the Twilight Zone: How Well do Protein Language Models Learn Protein Structure?},
  author={Kabir, Anowarul and Moldwin, Asher and Bromberg, Yana and Shehu, Amarda},
  journal={?},
  pages={?},
  year={2024},
  publisher={?}
}
```

