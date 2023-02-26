import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


def get_images_url():
    url = 'https://wall.alphacoders.com/by_sub_category.php?id=177585&name=Futurama+Wallpapers'
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        thumbs = driver.find_elements(By.CLASS_NAME, 'thumb-container')
        for thumb in thumbs:
            # img_id = thumb.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/big.php?i=')[1]
            # prefix = img_id[:3]
            # img_url = 'https://images.alphacoders.com/{}/{}.png'.format(prefix, img_id)
            src = thumb.find_element(By.CLASS_NAME, 'img-responsive').get_attribute('src')
            yield src

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

if __name__ == '__main__':
    try:
        os.mkdir('images')
    except FileExistsError:
        pass

    count = 0
    for url in get_images_url():
        count += 1
        print("[{}] download {} ...".format(count, url))
        filename = 'images/' + url.split('/')[-1]
        if not os.path.exists(filename):
            img = requests.get(url, headers=headers).content
            with open(filename, 'wb') as f:
                f.write(img)
