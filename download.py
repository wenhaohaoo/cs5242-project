import json
import argparse
import requests
from pathlib import Path

from tqdm import tqdm

def download(file_name, output_root=Path('./')):
    print(f'Search term: {file_name}')

    (output_root/f'images/{file_name}').mkdir(parents=True, exist_ok=True)
    with open(output_root/f'{file_name}.json') as f:
        images = json.loads(f.read())
    
    for k, v in tqdm(images.items(), desc=f'search_term={file_name} '):
        name = v.split('/')[-1]
        if not (name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg')):
            name += '.jpg'
        
        if k != 'date': 
            r = requests.get(v)
            if r.status_code == 200:
                with open(output_root/f'images/{file_name}/{name}', 'wb') as f:
                    f.write(r.content)
            else:
                print(f'failed: {k}, {v}, {r.status_code}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        default='happy man',
        help='search term to download images from',
    )
    parser.add_argument(
        '-o',
        default='./',
        help='output root directory',
    )

    args = parser.parse_args()
    Path(args.o).mkdir(parents=True, exist_ok=True)
    download(args.s, output_root=Path(args.o))
