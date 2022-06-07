from pathlib import Path
import shutil
from urllib import request

from ocean_lib.config import Config
from ocean_lib.ocean.ocean import Ocean

from dhub.core.utils import check_gdrive_link, convert_gdrive_link

config = Config('config.ini')
ocean = Ocean(config)

class Dataset:
    def __init__(self, ddo):
        self.ddo = ddo
        self.did = ddo.did
        self.name = ddo.metadata['main']['name']
        self.token = ocean.get_data_token(ddo.data_token_address)
        self.token_address = self.token.address
        self.service = ddo.get_service('compute')

    def get_sample_link(self):
        sample_link = self.dataset.metadata['additionalInformation']['links'][0]['url']
        dataset_name = Path(sample_link).parts[2]
        return sample_link    

    def untar_sample_data(self):
        path = self.download_sample_data()
        out_dir = Path(path.split('.')[0])
        shutil.unpack_archive(path, out_dir)
        return out_dir

    def download_sample_data(self):
        sample_link = self.get_sample_link()
        if not check_gdrive_link(sample_link):
            sample_link = convert_gdrive_link(sample_link)
        filename = request.urlopen(request.Request(sample_link)).info().get_filename()
        request.urlretrieve(sample_link, filename)
        return filename

    def get_service_type(self):
        return self.dataset.as_dictionary()['service'][1]['type']

    def download(self):
        if get_service_type == 'compute':
            print("Can't download dataset with compute-only access. Try to run an algorithm using C2D.")
            return False