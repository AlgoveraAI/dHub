# Builds on pytorch image models library (timm)

from io import BytesIO
import os
from pathlib import Path
from typing import Union

import torch
from torch.hub import get_dir

from huggingface_hub import HfApi, HfFolder, Repository, cached_download, hf_hub_url
from ..privacy import decrypt_weights

_has_hf_hub = True

def download_cached_file(url, check_hash=True, progress=False):
    parts = urlparse(url)
    filename = os.path.basename(parts.path)
    cached_file = os.path.join(get_cache_dir(), filename)
    if not os.path.exists(cached_file):
        _logger.info('Downloading: "{}" to {}\n'.format(url, cached_file))
        hash_prefix = None
        if check_hash:
            r = HASH_REGEX.search(filename)  # r is Optional[Match[str]]
            hash_prefix = r.group(1) if r else None
        download_url_to_file(url, cached_file, hash_prefix, progress=progress)
    return cached_file


def has_hf_hub(necessary=False):
    if not _has_hf_hub and necessary:
        # if no HF Hub module installed and it is necessary to continue, raise error
        raise RuntimeError(
            'Hugging Face hub model specified but package not installed. Run `pip install huggingface_hub`.')
    return _has_hf_hub


def hf_split(hf_id):
    # FIXME I may change @ -> # and be parsed as fragment in a URI model name scheme
    rev_split = hf_id.split('@')
    assert 0 < len(rev_split) <= 2, 'hf_hub id should only contain one @ character to identify revision.'
    hf_model_id = rev_split[0]
    hf_revision = rev_split[-1] if len(rev_split) > 1 else None
    return hf_model_id, hf_revision


def load_cfg_from_json(json_file: Union[str, os.PathLike]):
    with open(json_file, "r", encoding="utf-8") as reader:
        text = reader.read()
    return json.loads(text)


def _download_from_hf(model_id: str, filename: str):
    url = hf_hub_url(model_id, filename)
    return cached_download(url)


def load_model_config_from_hf(model_id: str):
    assert has_hf_hub(True)
    cached_file = _download_from_hf(model_id, 'config.json')
    pretrained_cfg = load_cfg_from_json(cached_file)
    pretrained_cfg['hf_hub_id'] = model_id  # insert hf_hub id for pretrained weight load during model creation
    pretrained_cfg['source'] = 'hf-hub'
    model_name = pretrained_cfg.get('architecture')
    return pretrained_cfg, model_name


def load_state_dict_from_hf(model_id: str):
    assert has_hf_hub(True)
    cached_file = _download_from_hf(model_id, 'encrypted_pytorch_model.bin')
    decrypted_weights = decrypt_weights(cached_file)
    state_dict = torch.load(BytesIO(decrypted_weights), map_location='cpu')
    return state_dict

def push_to_hf_hub(
    encrypted_weights,
    local_dir,
    commit_message='Add model',
    use_auth_token=True,
    # git_email=None,
    # git_user=None,
    # revision=None,
    # model_config=None,
):
    if isinstance(use_auth_token, str):
        token = use_auth_token
    else:
        token = HfFolder.get_token()

    if token is None:
        raise ValueError(
            "You must login to the Hugging Face hub on this computer by typing `transformers-cli login` and "
            "entering your credentials to use `use_auth_token=True`. Alternatively, you can pass your own "
            "token as the `use_auth_token` argument."
        )

    org = HfApi().whoami(token)['orgs'][0]['name']
    repo_name = Path(local_dir).name

    repo_url = f'https://huggingface.co/{org}/{repo_name}'

    repo = Repository(
        local_dir,
        clone_from=repo_url,
        use_auth_token=use_auth_token,
        # git_user=git_user,
        # git_email=git_email,
        # revision=revision,
    )

    # Prepare a default model card that includes the necessary tags to enable inference.
    # readme_text = f'---\ntags:\n- image-classification\n- timm\nlibrary_tag: timm\n---\n# Model card for {repo_name}'
    with repo.commit(commit_message):
        # Save model weights and config.
        # save_for_hf(model, repo.local_dir, model_config=model_config)

        with open(f"encrypted_pytorch_model.bin", "wb") as f:
            f.write(encrypted_weights)

        # # Save a model card if it doesn't exist.
        # readme_path = Path(repo.local_dir) / 'README.md'
        # if not readme_path.exists():
        #     readme_path.write_text(readme_text)

    return repo.git_remote_url()

def create_model_huggingface(algorithm_name):
    algorithm = None
    return algorithm