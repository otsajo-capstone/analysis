from flask import Flask, request
from scrap import scrap_by_bs, scrap_by_selenium
import json
import os
from datetime import datetime
import urllib.request
from cloth_recognizer import cloth_recognizer
from color_analyzer import color_analyzer

app = Flask(__name__)
dir_original = os.path.join(os.getcwd(), "original")


@app.route('/test_analyze', methods=['GET'])
def test():
    original = "233356.png"

    try:
        now = datetime.now()
        filename = now.strftime("%Y%m%d_%H_%M_%S")
        cloth = cloth_recognizer(original)
        color = color_analyzer(cloth)

        return {'color': color}

    except Exception as e:
        return {'error': str(e)}


@app.route('/image/analyze', methods=['POST'])
def analyze_uploaded():
    try:
        files = request.files.getlist("files")

        analysis_result = []

        for file in files:
            now = datetime.now()
            original = now.strftime("%Y%m%d_%H_%M_%S")
            original = str(original) + ".png"
            path = os.path.join(dir_original, original)
            file.save(path)

            cloth = cloth_recognizer(path)
            colors = color_analyzer(cloth)

            analysis_result.append({'src': path, 'colors': list(colors)})

        return {'status': 'success', 'analysis_result': list(analysis_result)}

    except Exception as e:
        return {'error': str(e)}


@app.route('/url', methods=['POST'])
def scraper():
    try:
        url = request.form['url']
        min_width = 150
        min_height = 150
        if request.form['width']:
            min_width = int(request.form['width'])
        if request.form['height']:
            min_height = int(request.form['height'])

        result = scrap_by_bs(url, min_width, min_height)
        if len(result) == 0:
            result = scrap_by_selenium(url, min_width, min_height)

            if len(result) == 0:
                return {'status': 'cannot scrap this site'}

        return {'status': 'success', 'src_list': list(result)}

    except Exception as e:
        return {'error': str(e)}


@app.route('/url/analyze', methods=['POST'])
def analyze_selected():
    try:
        src_list_string = request.form['src_list']
        src_list = json.loads(src_list_string)

        analysis_result = []

        for src in src_list:
            now = datetime.now()
            original = now.strftime("%Y%m%d_%H_%M_%S")
            if src.lower().find('.gif') != -1:
                original = str(original) + ".gif"
            else:
                original = str(original) + ".png"
            path = os.path.join(dir_original, original)
            urllib.request.urlretrieve(src, path)

            cloth = cloth_recognizer(path)
            colors = color_analyzer(cloth)

            analysis_result.append({'src': original, 'colors': list(colors)})

        return {'status': 'success', 'analysis_result': list(analysis_result)}

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0')

