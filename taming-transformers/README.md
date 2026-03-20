# Taming Transformers (Custom Data)

This README explains how to install and train on custom data in:
`path-data-augment/taming-transformers`

## Training on CIFAR-10

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

## Training on custom data

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

4. put your .jpg files in a folder `your_folder`

5. create 2 text files a `xx_train.txt` and `xx_test.txt` that point to the files in your training and test set respectively (for example `find $(pwd)/your_folder -name "*.jpg" > train.txt`)

6. adapt `configs/custom_vqgan.yaml` to point to these 2 files

7. Run training:
   ```bash
   python main.py --base configs/custom_vqgan.yaml -t True --gpus 0,1
   ```
   Use `--gpus 0,` (with a trailing comma) to train on a single GPU.

8. Make sure to add the following into configs/custom_vqgan.yaml

```bash
lightning:
  trainer:
    strategy: ddp_find_unused_parameters_true
```

## Training on PathVQA Dataset

1. Download the raw PathVQA parquet shards from Hugging Face:
   ```bash
   cd path-data-augment/taming-transformers

   python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='flaviagiammarino/path-vqa', repo_type='dataset', local_dir='../data/path-vqa-hf')"
   ```
   This downloads the dataset from:
   `https://huggingface.co/datasets/flaviagiammarino/path-vqa`

2. Extract the images and generate the split files used by the training config:
   ```bash
   python scripts/prepare_path_vqa.py --source-dir ../data/path-vqa-hf/data --images-dir data/path_vqa_images --lists-dir data
   ```
   `scripts/prepare_path_vqa.py` extracts unique RGB JPEGs into
   `data/path_vqa_images/{train,validation,test}` and writes the split lists
   `data/path_vqa_train.txt`, `data/path_vqa_validation.txt`, and
   `data/path_vqa_test.txt` used by `configs/path_vqa_vqgan.yaml`.

3. Run training:
   ```bash
   python main.py --base configs/path_vqa_vqgan.yaml -t True --gpus 0,1
   ```
   Use `--gpus 0,` (with a trailing comma) to train on a single GPU.