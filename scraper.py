import ast
import time
import datetime
import argparse
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm


log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

def init_driver():
    chromedriver = Service(ChromeDriverManager().install())

    options = Options()
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--allow-cross-origin-auth-prompt')

    driver = webdriver.Chrome(service=chromedriver, options=options)
    return driver


def scroll_down(driver, wait_time):

    def _scroll():
        # Get scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for page to load
            time.sleep(wait_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height

    logging.info('Scrolling down ..')
    while True:
        _scroll()
        try:
            # Try clicking 'Show more results'
            driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/input').click()
            
            # Wait for page to load
            time.sleep(wait_time)
        except:
            logging.info('Reached the end ..')
            
            # Scroll back to top
            driver.execute_script("window.scrollTo(0,0)")
            return


def get_image_url(driver, search_term, dev=False, output_root=Path('./'), resume=None):

    logging.info(f'Search term: {search_term}')

    images = set()
    try:
        with open(output_root/f'{search_term}.txt', 'r') as f:
            images = ast.literal_eval(f.read())
    except FileNotFoundError:
        logging.info('No prevous results found, starting new search')
        pass

    base_url = f'https://www.google.com/search?q={search_term}&tbm=isch&ijn=0'
    driver.get(base_url)

    # Scroll all the way down to load all images
    scroll_down(driver, 2)

    # Get list of image thumbnails to extract
    parent_elem = driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]')
    all_children = parent_elem.find_elements(By.XPATH, '*')
    logging.info(f'Total results found: {len(all_children)}')

    def _save(images):
        with open(output_root/f'{search_term}.txt', 'w') as f:
            f.write(str(images))

    def _scrape(list, retry=False, images=set(), dev=False, resume=None):

        logging.info(f'is_retry: {not retry}')
        logging.info(f'dev: {dev}')

        original_len = len(list)
        starting_pt = 0

        if dev:
           list = list[:20]

        if resume:
            try:
                resume = int(resume)
                list = list[resume:]
                starting_pt = resume
                logging.info(f'Resuming from {resume}')
            except Exception as e:
                logging.error(f'resume failed: {e}')
                exit(1)

        retry_list = []

        for idx, img in enumerate(tqdm(list, desc=f'search_term={search_term} | is_retry={not retry} ')):
            try:
                # Filter for only image thumbnails
                if img.get_attribute('class') == 'isv-r PNCib MSM1fd BUooTd':
                    
                    # Click on image thumbnail
                    img.click()
                    image = driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img')
                    
                    # Workaround to get original image src
                    image.click()
                    time.sleep(3)

                    # Retrieve 'src' attribute from the element
                    img_src = image.get_attribute('src')
                    if img_src.startswith('http') and img_src not in images:
                        images.add(img_src)

            except Exception as e:
                if retry:
                    logging.warning(f'failed, appending to retry list: {idx}, {e}')
                    retry_list.append(all_children[idx])
                pass

            if idx%10 == 0:
                _save(images)

            # logging.info(f'{starting_pt+idx+1}/{original_len}')
        
        return images, retry_list

    # First pass
    images, retry_list = _scrape(all_children, images=images, retry=True, dev=dev, resume=resume)
    logging.info(f'Total image URLs extracted in first pass: {len(images)}')

    # Retry those with ElementClickInterceptedException 
    if retry_list:
        images, _ = _scrape(retry_list, images=images)
        logging.info(f'Total image URLs extracted after retrying: {len(images)}')

    # Write URLs to txt file
    _save(images)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        default='happy man',
        help='search term to scrape images from',
    )
    parser.add_argument(
        '-o',
        default='./',
        help='output root directory',
    )
    parser.add_argument(
        '-r',
        default=None,
        help='index to resume from',
    )
    parser.add_argument(
        '-d',
        default=None,
        help='whether to run in dev mode',
    )

    args = parser.parse_args()
    driver = init_driver()
    Path(args.o).mkdir(parents=True, exist_ok=True)
    if not args.r:
        if not args.d:
            get_image_url(driver, args.s, dev=False, output_root=Path(args.o))
        else:
            get_image_url(driver, args.s, dev=True, output_root=Path(args.o))
    else:
        if not args.d:
            get_image_url(driver, args.s, dev=False, output_root=Path(args.o), resume=args.r)
        else:
            get_image_url(driver, args.s, dev=True, output_root=Path(args.o), resume=args.r)
    driver.close()
