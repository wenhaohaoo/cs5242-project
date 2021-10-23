import json
import argparse
import requests
from pathlib import Path

from tqdm import tqdm

def download(file_name):
    Path(f'images/{file_name}').mkdir(parents=True, exist_ok=True)
    with open(f'{file_name}.json') as f:
        images = json.loads(f.read())
    
    for k, v in tqdm(images.items(), desc=f'search_term={file_name} '):
        name = v.split('/')[-1]
        if not (name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg')):
            name += '.jpg'
        
        if k != 'date': 
            r = requests.get(v)
            if r.status_code == 200:
                with open(f'images/{file_name}/' + name, 'wb') as f:
                    f.write(r.content)
            else:
                print(r.status_code)
                print(k)
                print(v)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        default='happy man',
        help='search term to download images from',
    )

    args = parser.parse_args()
    download(args.s)
