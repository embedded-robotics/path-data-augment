import argparse
import hashlib
import io
from pathlib import Path

import pyarrow.parquet as pq
from PIL import Image


def export_split(parquet_paths, output_dir, list_path):
    output_dir.mkdir(parents=True, exist_ok=True)
    seen = {}

    for parquet_path in sorted(parquet_paths):
        parquet_file = pq.ParquetFile(parquet_path)
        for batch in parquet_file.iter_batches(batch_size=128, columns=["image"]):
            for row in batch.to_pylist():
                image_bytes = row["image"]["bytes"]
                digest = hashlib.sha1(image_bytes).hexdigest()
                if digest in seen:
                    continue

                image_path = output_dir / f"{digest}.jpg"
                with Image.open(io.BytesIO(image_bytes)) as image:
                    image.convert("RGB").save(image_path, format="JPEG", quality=95)
                seen[digest] = image_path.resolve()

    with list_path.open("w") as handle:
        for image_path in seen.values():
            handle.write(f"{image_path}\n")

    return len(seen)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        default="data/path-vqa-hf/data",
        help="Directory containing the downloaded parquet shards.",
    )
    parser.add_argument(
        "--images-dir",
        default="data/path_vqa_images",
        help="Output directory for extracted unique images.",
    )
    parser.add_argument(
        "--lists-dir",
        default="data",
        help="Directory where split text files will be written.",
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    images_dir = Path(args.images_dir).resolve()
    lists_dir = Path(args.lists_dir).resolve()
    lists_dir.mkdir(parents=True, exist_ok=True)

    split_to_pattern = {
        "train": "train-*.parquet",
        "validation": "validation-*.parquet",
        "test": "test-*.parquet",
    }

    for split, pattern in split_to_pattern.items():
        count = export_split(
            parquet_paths=source_dir.glob(pattern),
            output_dir=images_dir / split,
            list_path=lists_dir / f"path_vqa_{split}.txt",
        )
        print(f"{split}: wrote {count} unique images")


if __name__ == "__main__":
    main()
