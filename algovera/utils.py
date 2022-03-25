import os
from pathlib import Path
from urllib.parse import urlsplit

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

def parse_name(name):
    name = name.replace('hf_hub', 'hf-hub')  # NOTE for backwards compat, to deprecate hf_hub use
    parsed = urlsplit(name)
    assert parsed.scheme in ('', 'ocean', 'hf-hub')
    if parsed.scheme == 'hf-hub':
        # FIXME may use fragment as revision, currently `@` in URI path
        return parsed.scheme, parsed.path
    else:
        name = os.path.split(parsed.path)[-1]
        return 'ocean', name