from dhub.core.storage_provider.storage_provider import StorageProvider
from ocean_lib.assets.asset import Asset
from pathlib import Path

class ModelWeights(Asset):

    def create(path, storage_url):

        byte = ModelWeights.read_bytes(path)

        # encrypt_response = data_provider.encrypt(files, self._config.provider_url)
        
        # Upload weights to storage
        storage_provider = StorageProvider
        response = StorageProvider.upload(byte, storage_url)

        return response

    def read_bytes(path):
        path = Path(path)
        with open(path, "rb") as f:
            byte = f.read()
        return byte