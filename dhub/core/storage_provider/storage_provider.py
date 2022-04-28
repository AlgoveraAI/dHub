from dotenv import load_dotenv
import httpx
from ocean_lib.http_requests.requests_session import get_requests_session
import os
from requests.models import Response

from dhub.core.config import Config

load_dotenv()

class StorageProvider:
    """StorageProvider class."""

    requests_session = get_requests_session()

    def upload(object_to_upload, storage_url) -> Response:

        response = StorageProvider.requests_session.post(
            storage_url,
            data={"file": object_to_upload},
            headers={"Authorization": "Bearer " + os.environ["WEB3_STORAGE_TOKEN"]},
        )

    def get_url(config: Config) -> str:
        """
        Return the DataProvider component url.

        :param config: Config
        :return: str
        """
        return config.storage_url()
