import shutil
from pathlib import Path

import numpy as np
from box import ConfigBox
from fastai.vision.all import get_files
from ruamel.yaml import YAML


yaml = YAML(typ="safe")


def data_split():
    """
        Splits the image and mask data into train and test directories
        based on the regions specified in the configuration file.
        The function reads the image file paths from the "data/pool_data/images" directory,
        and the corresponding mask file paths from the "data/pool_data/masks" directory.
        It then creates the "data/train_data" and "data/test_data" directories if they
        don't already exist.

        For each image file, if the image path contains any of the test regions
        specified in the configuration file, the image and its corresponding mask are
        copied to the "data/test_data" directory.
        Otherwise, they are copied to the "data/train_data" directory.

        The function uses the random seed specified in the configuration file to
        ensure reproducible data splits.
    """
    params = ConfigBox(yaml.load(open("params.yaml", encoding="utf-8")))
    np.random.seed(params.base.random_seed)
    img_fpaths = get_files(Path("data") / "pool_data" /
                           "images", extensions=".jpg")

    train_data_dir = Path("data") / "train_data"
    train_data_dir.mkdir(exist_ok=True)
    test_data_dir = Path("data") / "test_data"
    test_data_dir.mkdir(exist_ok=True)
    for img_path in img_fpaths:
        msk_path = Path("data") / "pool_data" / \
            "masks" / f"{img_path.stem}.png"
        if any(region in str(img_path) for region in params.data_split.test_regions):
            shutil.copy(img_path, test_data_dir)
            shutil.copy(msk_path, test_data_dir)
        else:
            shutil.copy(img_path, train_data_dir)
            shutil.copy(msk_path, train_data_dir)


"""
Runs the data split process to create train and test data directories.
"""
if __name__ == "__main__":
    data_split()
