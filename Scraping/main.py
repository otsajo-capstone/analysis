import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def scraper(url, min_width, min_height):
    html = urlopen(url)
    html_source = html.read()
    soup = BeautifulSoup(html_source, "html.parser")

    '''
    get image elements from the url
    '''
    images_origin = soup.find_all('img')

    '''
    extract src from image elements which are moderately large
    '''
    images_src = set([])
    for image in images_origin:
        if type(image.get('width')) == str:
            width = int(image.get('width'))
            if width >= min_width:
                images_src.add(image.get('src'))
            continue

        elif type(image.get('height')) == str:
            height = int(image.get('height'))
            if height >= min_height:
                images_src.add(image.get('src'))

    print("\n".join(images_src))


sample_url = "https://store.musinsa.com/app/product/detail/1108007/0"
scraper(sample_url, 300, 300)
