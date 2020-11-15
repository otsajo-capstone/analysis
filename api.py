from flask import Flask, request, send_file
from scrap import scrap_by_bs, scrap_by_selenium
import os
from datetime import datetime
import urllib.request
from cloth_recognizer import cloth_recognizer
from color_analyzer import color_analyzer
from p_color_classifier import p_color_classifier
from PIL import Image
import copy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
dir_original = os.path.join(os.getcwd(), "original")
server_address = "http://34.105.97.231:5000/"


@app.route('/', methods=['GET'])
def initial():
    return "Analysis Server for Otsajo App!"


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
            original = str(original) + ".png"
            path = os.path.join(dir_original, original)
            file.save(path)

            if file.content_type == 'image/gif':
                img = Image.open(path)
                img.save(path, 'png')

            cloth = cloth_recognizer(path)
            colors = color_analyzer(cloth)
            result = p_color_classifier(colors)
            external_path = server_address + 'image?filename=' + original

            analysis_result.append({'name': original, 'src': external_path, 'colors': list(colors), 'result': result})

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

            src_okay = copy.deepcopy(src)
            if src_okay.find('http:') == -1 and src_okay.find('https:') == -1:
                src_okay = 'http:' + src_okay
            urllib.request.urlretrieve(src_okay, path)

            if src.lower().find('.gif') != -1:
                gif = Image.open(path)
                original = original[:len(original)-4] + ".png"
                path = path[:len(path)-4] + ".png"
                gif.save(path, 'png')

            cloth = cloth_recognizer(path)
            colors = color_analyzer(cloth)
            result = p_color_classifier(colors)

            external_path = server_address + 'image?filename=' + original

            analysis_result.append({'name': original, 'src': external_path, 'colors': list(colors), 'result': result})

        return {'status': 'success', 'analysis_result': list(analysis_result)}

    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run()

