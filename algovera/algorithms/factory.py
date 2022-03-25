# Code from pytorch image model library (timm)

import os
from urllib.parse import urlsplit

from .huggingface import load_model_config_from_hf
from .ocean import load_algorithm_from_ocean
from ..utils import parse_name

def create_algorithm(algorithm_name):

    algorithm_source, algorithm_name = parse_name(algorithm_name)

    if algorithm_source == 'ocean':
        algorithm = load_algorithm_from_ocean(algorithm_name)
    
    elif algorithm_source == 'hf-hub':
        pretrained_cfg, algorithm_name = load_model_config_from_hf(algorithm_name)

    return algorithm