#!/usr/bin/sh

#SBATCH --job-name=download_uniclust
#SBATCH --output=/projects/ashehu/amoldwin/remote_homologs/logs_slurm/download_uniclust-%j.output
#SBATCH --error=/projects/ashehu/amoldwin/remote_homologs/logs_slurm/download_uniclust-%j.error
#SBATCH --partition=normal
#SBATCH --nodes=1 
#SBATCH --mem=8G 
#SBATCH --time=1-00:00:00

/home/amoldwin/PROJECTS/datasets/uniclust30
wget http://wwwuser.gwdg.de/~compbiol/uniclust/2018_08/uniclust30_2018_08_hhsuite.tar.gz