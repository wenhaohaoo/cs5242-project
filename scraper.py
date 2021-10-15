import json
import time
import datetime
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm


def init_driver():
    chromedriver = Service(ChromeDriverManager().install())

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--allow-cross-origin-auth-prompt')

    driver = webdriver.Chrome(service=chromedriver, options=options)
    driver.maximize_window()
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

    print('Scrolling down ..')
    while True:
        _scroll()
        try:
            # Try clicking 'Show more results'
            driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/input').click()
            
            # Wait for page to load
            time.sleep(wait_time)
        except:
            print('Reached the end ..')
            
            # Scroll back to top
            driver.execute_script("window.scrollTo(0,0)")
            return


def get_image_url(driver, search_term, dev=False):
    
    base_url = f'https://www.google.com/search?q={search_term}&tbm=isch&ijn=0'
    driver.get(base_url)

    print(f'Search term: {search_term}')

    # Scroll all the way down to load all images
    scroll_down(driver, 2)

    # Get list of image thumbnails to extract
    parent_elem = driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]')
    all_children = parent_elem.find_elements(By.XPATH, '*')
    print(f'Total results found: {len(all_children)}')

    def _scrape(list, retry=False, images = {'date': str(datetime.datetime.now())}, dev=False):

        if dev:
           list = list[:50]

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
                    if img_src.startswith('http'):
                        images[idx] = img_src

            except Exception as e:
                if retry:
                    print(f'appending {idx} to retry list')
                    retry_list.append(all_children[idx])
                pass
        
        return images, retry_list
    
    # First pass
    images, retry_list = _scrape(all_children, retry=True, dev=True)
    print(f'Total image URLs extracted in first pass: {len(images)}')

    # Retry those with ElementClickInterceptedException 
    if retry_list:
        images, _ = _scrape(retry_list, images=images)
        print(f'Total image URLs extracted after retrying: {len(images)}')

    # Write URLs to json file
    with open(f'{search_term}.json', 'w') as f:
        f.write(json.dumps(images))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        default="happy man",
        help="search term to scrape images from",
    )

    args = parser.parse_args()
    driver = init_driver()
    get_image_url(driver, args.s, dev=True)
    driver.close()
