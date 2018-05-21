import re
import os
import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool


def get_images_url(page):
    url = 'https://wall.alphacoders.com/by_sub_category.php?id=177585&name=Futurama+Wallpapers&page=' + str(page)

    soup = BS(requests.get(url).text, 'lxml')
    download_buttons = soup.select('.download-button')
    for button in download_buttons:
        img_url = button['data-href']
        yield img_url


def download_imgae(url):
    print('Downloading', url)
    img = requests.get(url)
    return img.content


def main(i):
    for url in get_images_url(i):
        filename = os.getcwd() + '/' + url.split('/')[-4] + '.' + url.split('/')[-2]
        print(filename)
        if not os.path.exists(filename):
            img = download_imgae(url)
            with open(filename, 'wb') as f:
                f.write(img)
                print('OK')


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, range(1, 9))
            

