# Code from pytorch image model library (timm)

import os
from urllib.parse import urlsplit

from .huggingface import load_model_config_from_hf
from .ocean import load_model_from_ocean

def create_model(model_name):

    model_source, model_name = parse_model_name(model_name)

    if model_source == 'ocean':
        model = load_model_from_ocean(model_name)
    
    elif model_source == 'hf-hub':
        pretrained_cfg, model_name = load_model_config_from_hf(model_name)

    return model