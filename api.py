from flask import Flask, request, send_file
from scrap import scrap_by_bs, scrap_by_selenium
import json
import os
from datetime import datetime
import urllib.request
from cloth_recognizer import cloth_recognizer
from color_analyzer import color_analyzer
from PIL import Image
import copy

app = Flask(__name__)
dir_original = os.path.join(os.getcwd(), "original")


@app.route('/image', methods=['GET'])
def serve_image():
    filename = request.args.get('filename')
    path = os.path.join(dir_original, filename)

    if path[-4:] == '.gif':
        return send_file(path, mimetype='image/gif')
    else:
        return send_file(path, mimetype='image/png')


@app.route('/image/analyze', methods=['POST'])
def analyze_uploaded():
    try:
        files = request.files.getlist("files")

        analysis_result = []

        for file in files:
            now = datetime.now()
            original = now.strftime("%Y%m%d_%H_%M_%S")
            print(file.content_type)
            original = str(original) + ".png"
            path = os.path.join(dir_original, original)
            file.save(path)

            if file.content_type == 'image/gif':
                img = Image.open(path)
                img.save(path, 'png')

            cloth = cloth_recognizer(path)
            colors = color_analyzer(cloth)
            external_path = 'http://34.82.152.172:5000/image?filename=' + original

            analysis_result.append({'name': original, 'src': external_path, 'colors': list(colors)})

        return {'status': 'success', 'analysis_result': list(analysis_result)}

    except Exception as e:
        return {'error': str(e)}


@app.route('/url', methods=['POST'])
def scraper():
    try:
        url = request.form['url']
        min_width = 100
        min_height = 100
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
        src_list = request.json['src_list']

        analysis_result = []

        for src in src_list:
            now = datetime.now()
            original = now.strftime("%Y%m%d_%H_%M_%S")
            if src.lower().find('.gif') != -1:
                original = str(original) + ".gif"
            else:
                original = str(original) + ".png"
            path = os.path.join(dir_original, original)
            path_to_remove = copy.deepcopy(path)

            urllib.request.urlretrieve(src, path)

            if src.lower().find('.gif') != -1:
                gif = Image.open(path)
                original = original[:len(original)-4] + ".png"
                path = path[:len(path)-4] + ".png"
                gif.save(path, 'png')

            cloth = cloth_recognizer(path)
            colors = color_analyzer(cloth)

            external_path = 'http://34.82.152.172:5000/image?filename=' + original

            analysis_result.append({'name': original, 'src': external_path, 'colors': list(colors)})

        return {'status': 'success', 'analysis_result': list(analysis_result)}

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0')

