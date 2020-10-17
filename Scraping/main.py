import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from PIL import Image
import os
import time

chrome_options = webdriver.ChromeOptions()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Whale/2.8.107.16 Safari/537.36"
chrome_options.add_argument("user-agent=" + USER_AGENT)
chrome = webdriver.Chrome(os.getcwd() + '/chromedriver', chrome_options=chrome_options)

def scrap_by_bs(url, min_width, min_height):
    html = urlopen(url)
    html_source = html.read()
    soup = BeautifulSoup(html_source, "html.parser")

    # get image elements from the url
    images_tags = soup.find_all('img')

    #extract src from image elements which are moderately large
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


sample_url = "https://store.musinsa.com/app/product/detail/1108007/0"
sample_url2 = "https://search.shopping.naver.com/search/all?query=%EA%B0%80%EC%9D%84+%EC%9E%90%EC%BC%93&cat_id=&frm=NVSHATC"
sample_url3 = "https://styleman.kr/product/detail.html?product_no=34196&cate_no=968&display_group=2"
sample_url4 = "https://www.brandi.co.kr/"
# scraper(sample_url4, 100, 100)
if len(scrap_by_bs(sample_url, 100, 100)) == 0:
    scrap_by_selenium(sample_url3, 100, 100)