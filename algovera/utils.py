import os
from pathlib import Path

def list_files(data_dir):
    print("Listing files...")
    data_path = []
    for root, dirs, files in os.walk(data_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            fn = os.path.join(root,file)
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