import ast
import argparse
import logging
import requests
import uuid
import urllib3
from pathlib import Path

from tqdm import tqdm


urllib3.disable_warnings()
log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

def download(file_name, output_root=Path('./')):
    logging.info(f'Search term: {file_name}')

    (output_root/f'images/{file_name}').mkdir(parents=True, exist_ok=True)
    with open(output_root/f'{file_name}.txt') as f:
        images = ast.literal_eval(f.read())
    
    for i, v in enumerate(tqdm(images, desc=f'search_term={file_name} ')):
        
        name = v.split('/')[-1]
        if '.png' in name:
            name = name[:name.index('.png')+4]
        elif '.jpg' in name:
            name = name[:name.index('.jpg')+4]
        elif '.jpeg' in name:
            name = name[:name.index('.jpeg')+5]
        else:
            name = uuid.uuid4().hex + '.jpg'
        
        r = requests.get(v, verify=False)
        if r.status_code == 200:
            with open(output_root/f'images/{file_name}/{name}', 'wb') as f:
                f.write(r.content)
        else:
            logging.info(f'failed: {i}, {v}, {r.status_code}')


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
