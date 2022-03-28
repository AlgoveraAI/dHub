# Code from pytorch image model library (timm)

import os
from urllib.parse import urlsplit

from .huggingface import load_model_config_from_hf
from .ocean import get_algorithms, load_algorithm_from_ocean
from ..utils import parse_name

def create_algorithm(algorithm_name):

    algorithm_source, algorithm_name = parse_name(algorithm_name)

    if algorithm_source == 'ocean':
        algorithm = load_algorithm_from_ocean(algorithm_name)
    
    elif algorithm_source == 'hf-hub':
        pretrained_cfg, algorithm_name = load_model_config_from_hf(algorithm_name)

    return algorithm

def list_algorithms(algorithm_source):
    if algorithm_source == 'ocean':
        algorithms = get_algorithms()
    elif algorithm_source == 'hf-hub':
        pass
    elif algorithm_source == 'activeloop':
        print('ActiveLoop Hub does not currently have algorithms.')
        return None    

    return algorithms