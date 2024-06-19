# plm-zero-shot-remote-homology-evaluation
plm-zero-shot-remote-homology-evaluation


The SCOP dataset can be downloaded here: https://scop2.mrc-lmb.cam.ac.uk/download

SCOPe can be downloaded here: https://scop.berkeley.edu/astral/ver=2.08

ESM models are available here: https://github.com/facebookresearch/esm 

Prottrans models can be found here: https://github.com/agemagician/ProtTrans


Running our code on SCOPe database: 
(1) Download SCOPe data and choose models to evaluate.
(2) Generate embeddings from each model using the appropriate. embed_gen_<model_type>.py script.
(3) Run ipynb notebook preprocess_SCOPe_data.ipynb
(4) Run compute_ranking_metrics.py, making sure to set desired parameters for data_name, remote_homology_level, and model_name in the "main" method.
