# Code from pytorch image model library (timm)

import os
from urllib.parse import urlsplit

from .ocean import load_dataset_from_ocean
from ..utils import parse_name


def create_dataset(dataset_full):
    dataset_source, dataset_name = parse_name(dataset_full)

    if dataset_source == 'ocean':
        dataset = load_dataset_from_ocean(dataset_full)
    elif dataset_source == 'hf-hub':
        pass

    return dataset