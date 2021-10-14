import time
import datetime
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


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



chromedriver = ChromeDriverManager().install()

options = Options()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-web-security')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--allow-cross-origin-auth-prompt')
driver = webdriver.Chrome(chromedriver, options=options)
driver.maximize_window()
base_url = 'https://www.google.com/search?q={}&tbm=isch&ijn=0'
driver.get(base_url.format('happy man'))

# Scroll all the way down to load all images
scroll_down(driver, 2)

# Get list of image thumnails to extract
parent_elem = driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]')
all_children = parent_elem.find_elements(By.XPATH, '*')
print(f'Total results found: {len(all_children)}')

images = {'date': str(datetime.datetime.now())}
data_list = []

for idx, img in enumerate(all_children):
    try:
        # Filter for only image
        if img.get_attribute('class') == 'isv-r PNCib MSM1fd BUooTd':
            
            # Click on image thumbnail
            img.click()
            image = driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img')
            
            # Workaround to get original image src
            image.click()
            time.sleep(4)

            # Retrieve 'src' attribute from the element
            img_src = image.get_attribute('src')
            print(f'{idx}: {img_src}')
            if img_src.startswith('http'):
                images[idx] = img_src
            else:
                data_list.append(idx)
        else:
            print(f'{idx}: not an image')
    except Exception as e:
        print(f'{idx} error: {e}')
        pass

with open('happy man.json', 'w') as f:
    f.write(json.dumps(images))
driver.close()
