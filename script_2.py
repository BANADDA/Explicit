import os
import time

import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

searchword1 = 'sexy ugandan'
searchword2 = 'hot black girls'
searchword3 = 'sexy ebony'
searchurl = 'https://www.google.com/search?q=' + searchword1 + '+' + searchword2 + '+' + searchword3 + '&source=lnms&tbm=isch'
dirs = 'pictures_2'
maxcount = 1000

chromedriver = 'chromedriver.exe'

if not os.path.exists(dirs):
    os.mkdir(dirs)

def download_google_staticimages():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    print("Initializing WebDriver...")
    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        raise RuntimeError(f'Failed to initialize WebDriver: {e}')

    browser.set_window_size(1280, 1024)
    print("Navigating to search URL...")
    browser.get(searchurl)
    time.sleep(1)

    print(f'Getting you a lot of images. This may take a few moments...')

    element = browser.find_element_by_tag_name('body')

    # Scroll down
    for i in range(50):
        print(f"Scrolling down, iteration {i+1}")
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    print(f'Reached end of page.')

    print("Fetching page source...")
    page_source = browser.page_source 

    print("Parsing HTML...")
    soup = BeautifulSoup(page_source, 'lxml')
    images = soup.find_all('img')

    urls = []
    for image in images:
        try:
            url = image['src']
            if url.startswith('http') and not url.endswith('gstatic.com'):
                urls.append(url)
        except Exception as e:
            print(f'Error extracting image URL: {e}')

    count = 0
    if urls:
        for url in urls:
            try:
                print(f"Downloading image: {url}")
                res = requests.get(url, verify=False, stream=True)
                rawdata = res.raw.read()
                with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                    f.write(rawdata)
                    count += 1
            except Exception as e:
                print(f'Error downloading image: {e}')

    browser.close()
    return count

def main():
    t0 = time.time()
    try:
        count = download_google_staticimages()
    except RuntimeError as e:
        print(e)
        count = 0
    t1 = time.time()

    total_time = t1 - t0
    print(f'\n')
    print(f'Download completed. [Successful count = {count}].')
    print(f'Total time is {str(total_time)} seconds.')

if __name__ == '__main__':
    main()
