import os
from pathlib import Path
import shutil
from urllib import request

DIDs = {
    "AlgoveraAI/CryptoPunks" : "did:op:C9D0568838fa670baEe7195Ea443b32EfCAc2281"
}
    
class Datasets:
    def __init__(self, cfg):
        self.cfg = cfg

    def load_dataset(self, did):
        dataset = self.cfg.ocean.assets.resolve(DIDs[did])

        print(f"Data token info = '{dataset.values['dataTokenInfo']}'")
        print(f"Dataset name = '{dataset.metadata['main']['name']}'")

        return Dataset(dataset)

    def ls(self):
        for DID in DIDs:
            print(DID)

    
class Dataset:
    def __init__(self, dataset):
        self.dataset = dataset

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

    def download(self):
        pass

def list_files(data_dir):
    print("Listing files...")
    data_path = []
    for root, dirs, files in os.walk(data_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            fn = os.path.join(root,file)
            # if fn.split('.')[-1] in ['feather']:
            data_path.append(fn)
            print(len(path) * '---', file)

def check_gdrive_link(link):
    path = Path(link)
    if path.parts[-1] == 'view?usp=sharing':
        return False
    else:
        return True

def convert_gdrive_link(link):
    path = Path(link)
    file_id = path.parts[-2]
    new_link = "https://drive.google.com/uc?export=download&id=" + file_id
    return new_link