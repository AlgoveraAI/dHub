# Code from pytorch image model library (timm)

import hub
import os
from urllib.parse import urlsplit

from .ocean import get_datasets, load_dataset_from_ocean
from ..utils import parse_name


def load_dataset(dataset_full):
    dataset_source, dataset_name = parse_name(dataset_full)

    if dataset_source == 'ocean':
        dataset = load_dataset_from_ocean(dataset_name)
    elif dataset_source == 'hf-hub':
        pass
    elif dataset_source == 'hub':
        dataset = hub.load(dataset_full)

    return dataset

def list_datasets(dataset_source):
    if dataset_source == 'ocean':
        datasets = get_datasets()
    elif dataset_source == 'hf-hub':
        pass
    elif dataset_source == 'activeloop':
        datasets = hub.list('activeloop')    

    return datasets