# Taming Transformers (Custom Data)

This README explains how to install and train on custom data in:
`path-data-augment/taming-transformers`

## Training on custom data (pip)

Training on your own dataset can be beneficial to get better tokens and better images for your domain.

1. Move into the project:
   ```bash
   cd path-data-augment/taming-transformers
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies with pip:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   pip install -e .
   ```
4. Run training:
   ```bash
   python main.py --base configs/custom_vqgan.yaml -t True --gpus 0,1
   ```
   Use `--gpus 0,` (with a trailing comma) to train on a single GPU.

## Training on custom data (conda)

Training on your own dataset can be beneficial to get better tokens and hence better images for your domain.
Those are the steps to follow to make this work:

1. Install the repo:
   ```bash
   conda env create -f environment.yaml
   conda activate taming
   pip install -e .
   ```
2. Run:
   ```bash
   python main.py --base configs/custom_vqgan.yaml -t True --gpus 0,1
   ```
   This trains on two GPUs. Use `--gpus 0,` (with a trailing comma) to train on a single GPU.
