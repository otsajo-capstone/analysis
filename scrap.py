import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from PIL import Image
import os
import time

def scrap_by_bs(url, min_width, min_height):
    html = urlopen(url)
    html_source = html.read()
    soup = BeautifulSoup(html_source, "html.parser")

    # get image elements from the url
    images_tags = soup.find_all('img')

    # extract src from image elements which are moderately large
    image_src = set([])
    for image in images_tags:
        src = image.get('src')

        if type(image.get('width')) == str:
            width = int(image.get('width'))
            if width >= min_width:
                image_src.add(src)
            continue

        elif type(image.get('height')) == str:
            height = int(image.get('height'))
            if height >= min_height:
                image_src.add(src)

    return image_src

def scrap_by_selenium(url, min_width, min_height):
    chrome_options = webdriver.ChromeOptions()
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.107.16 Safari/537.36"
    chrome_options.add_argument("user-agent=" + USER_AGENT)
    chrome = webdriver.Chrome(os.getcwd() + '/chromedriver', chrome_options=chrome_options)

    path = './' + str(time.time())
    os.mkdir(path)

    chrome.get(url)
    image_elements = chrome.find_elements_by_tag_name('img')
    image_src = set([])
    for e in image_elements:
        size = e.size

        if size["width"] >= min_width and size["height"] >= min_height:
            image_src.add(e.get_attribute('src'))

    chrome.close()

    return image_src