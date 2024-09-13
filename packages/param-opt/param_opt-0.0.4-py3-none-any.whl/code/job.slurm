#!/bin/bash

#SBATCH --job-name=hparam-opt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=small_gpu
#SBATCH --time=5:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ehrhardj@hsu-hh.de
#SBATCH --output=hparam-opt.log

module purge
module load anaconda3/2021.11
module load cuda
eval "$(conda shell.bash hook)"

conda activate paramopt
conda info --envs

python main.py

