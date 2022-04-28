from ocean_lib.config import Config

NAME_STORAGE_URL = "storage.url"

SECTION_STORAGE = "storage"

class Config(Config):
    """Class to manage the dhub configuration."""

    def storage_url(self) -> str:
        return self.get(SECTION_STORAGE, NAME_STORAGE_URL)