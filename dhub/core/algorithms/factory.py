# Code from pytorch image model library (timm)

import os
from urllib.parse import urlsplit

from .huggingface import load_state_dict_from_hf, push_to_hf_hub
from .ocean import get_algorithms, load_algorithm_from_ocean
from ..privacy import encrypt_weights
from ..utils import parse_name

def load_algorithm(algorithm_name):

    algorithm_source, algorithm_name = parse_name(algorithm_name)

    if algorithm_source == 'ocean':
        algorithm = load_algorithm_from_ocean(algorithm_name)
    
    elif algorithm_source == 'hf-hub':
        pretrained_cfg, algorithm_name = load_model_config_from_hf(algorithm_name)

    return algorithm

def load_model(model_name):

    # model_source, model_name = parse_name(model_name)
    # pretrained_cfg, model_name = load_model_config_from_hf(model_name)

    state_dict = load_state_dict_from_hf(model_name)

    return state_dict

def create_model(path, model_name):

    # ALG_ddo = create_algorithm_ocean(algorithm_name, algorithm_url)
    encrypted_weights = encrypt_weights(path)
    model_url = push_to_hf_hub(encrypted_weights, model_name)

    # algorithm_hf, model_url = create_model_huggingface(model_name, encrypted_weights)
    # asset = create_model_token(model_name, model_url)

    return model_url

def list_algorithms(algorithm_source):
    if algorithm_source == 'ocean':
        algorithms = get_algorithms()
    elif algorithm_source == 'hf-hub':
        pass
    elif algorithm_source == 'activeloop':
        print('ActiveLoop Hub does not currently have algorithms.')
        return None    

    return algorithms