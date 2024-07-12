export PYTHONPATH=$PYTHONPATH:$pwd/remote_homologs

```bash
# To remove conda venv
conda info --envs
conda deactivate
conda remove -p path/to/venv --all -y
```

```bash
# Installation of Generic environment (pytorch)
conda create -c conda-forge -p .venv/python311_conda_0 python=3.11 -y
conda activate .venv/python311_conda_0
pip install --upgrade pip
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
pip install pandas joblib matplotlib seaborn scikit-learn
```

### Official TAPE: https://github.com/songlab-cal/tape
```bash
# Installation of TAPE (pytorch)
module load python/3.8.6-generic-x86_64
python -m venv .venv/tape_rao
source .venv/tape_rao/bin/activate
conda deactivate
pip install --upgrade pip
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
pip install tape_proteins --no-cache
```


### Official ProteinBERT: https://github.com/nadavbra/protein_bert
```bash
# Installation of ProteinBERT (tensorflow)
module load python/3.8.6-generic-x86_64
python -m venv .venv/proteinbert_tf_brandes
source .venv/proteinbert_tf_brandes/bin/activate
conda deactivate
pip install --upgrade pip
pip install protein-bert --no-cache
```

### Official Bio Embeddings for Prottrans: https://github.com/sacdallago/bio_embeddings
```bash
# Installation of Bio Embeddings (pytorch)
module load python/3.8.6-generic-x86_64
python -m venv .venv/bioembeddings_dallago
source .venv/bioembeddings_dallago/bin/activate
conda deactivate
pip install --upgrade pip
pip install bio-embeddings[all] --no-cache

Note: This does not properly install pytorch (=">=1.8.0,<=1.10.0"). "bio_embeddings/bio_embeddings/embed/__init__.py" describes that it is build on CUDA 11.1, so manually install the following:
pip install torch==1.9.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html       # this will install compatible torch with cuda 11.1
```

### Official ESM: https://github.com/facebookresearch/esm
```bash
# Installation of ESM (pytorch)
module load python/3.8.6-generic-x86_64 
python -m venv .venv/esm_rives
source .venv/esm_rives/bin/activate
conda deactivate
pip install --upgrade pip
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
pip install fair-esm --no-cache
```

### Official CD-HIT: https://github.com/weizhongli/cdhit-web-server
```bash
# CD-HIT clustering
Install web-server can be found in the following two links: 
    https://sites.google.com/view/cd-hit/web-server?authuser=0 and https://github.com/weizhongli/cdhit-web-server
    sudo snap install docker
    sudo docker run -d -h cdhit-server --name cdhit-server -p 8088:80 weizhongli1987/cdhit-server:latest (this requires super-user permission)
    http://localhost:8088/cdhit-web-server on the browser

# running CD-HIT:
    Sequence identity cut-off: .9 - .1
    And other parameters are per default, such as 
        -G: use global sequence identity: Yes
        -b bandwidth of alignment: 20
        -l length of sequence to skip: 10
    Then we downloaded the cluster file that is sorted by cluster size.
    wget http://localhost:8088/cdhit-web-server/output/1681921330/1681921330.fas.1.clstr.sorted -O data/cdhit_clusters_at_th_family/at_90_seq_identity.txt
    ... and so on (link will be different).

docker ps -a # all list of containers
docker rm container_id # to remove a docker container
sudo docker restart container_id # to restart a docker container
```