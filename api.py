from flask import Flask, request
from scrap import scrap_by_bs, scrap_by_selenium
import requests
import json

app = Flask(__name__)

'''
POST로 scrap할 url을 받으면, 이미지 src를 배열 형태로 반환합니다.
'''
@app.route('/url', methods=['POST'] )
def scraper():
    try:
        url = request.form['url']
        min_width = int(request.form['width'])
        min_height = int(request.form['height'])

        result = scrap_by_bs(url, min_width, min_height)
        if len(result) == 0:
            result = scrap_by_selenium(url, min_width, min_height)

            if len(result) == 0:
                return {'status': 'scrap failed'}

        return {'status': 'success', 'image_urls': list(result)}

    except Exception as e:
        return {'error': str(e)}

@app.route('/url/select', methods=['post'])
def selecter():
    print('')

if __name__ == '__main__':
    app.run(debug=True)
