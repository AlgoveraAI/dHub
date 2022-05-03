from io import BytesIO
from ocean_lib.assets.asset import Asset
from pathlib import Path
import torch

from dhub.core.storage_provider.storage_provider import StorageProvider
from dhub.core.data_provider.data_service_provider import DataServiceProvider

class Weights():

    def create(user, path, storage_url, private=True):
        byte = Weights.read_bytes(path)

        if private:
            encrypt_response = user.data_provider.encrypt(byte, user.provider_url)
            byte = encrypt_response.content

        # Upload weights to storage
        storage_provider = StorageProvider
        response = StorageProvider.upload(byte, storage_url)

        return response

    def load(user, cid, private=True):
        storage_provider = StorageProvider
        response = StorageProvider.download(cid)
        byte = response.content[5:] # remove "file=" at start

        if private:
            decrypt_response = user.data_provider.decrypt(byte, user.provider_url, user.wallet)
            byte = decrypt_response.content

        state_dict = torch.load(BytesIO(byte), map_location='cpu')

        return state_dict

    def read_bytes(path):
        path = Path(path)
        with open(path, "rb") as f:
            byte = f.read()
        return byte