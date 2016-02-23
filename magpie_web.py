import json

from flask import Flask, render_template, request
import requests

from config import EXTRACT_URL, WORD2VEC_URL

app = Flask(__name__)

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


@app.route('/', methods=['POST', 'GET'])
def extractor():
    if request.method == 'POST':
        text = request.form.get('text', '')
        extract_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        response = requests.post(EXTRACT_URL, data=json.dumps({'domain': 'hep', 'text': text}), headers=extract_headers)
        print response.text
        contents = json.loads(response.text)
        return render_template('magpie/results.html', results=contents, ctx='extract')

    return render_template('magpie/extractor.html')


@app.route('/word2vec', methods=['POST', 'GET'])
def word2vec():
    if request.method == 'POST':
        positive = request.form.get('positive', None)
        negative = request.form.get('negative', None)

        data = {'domain': 'hep'}
        if positive:
            data['positive'] = positive.split(',')
        if negative:
            data['negative'] = negative.split(',')

        print data

        response = requests.post(WORD2VEC_URL,
                                 data=json.dumps(data),
                                 headers=headers)
        print response.text
        contents = json.loads(response.text)
        return render_template('magpie/results.html', results=contents, ctx='word2vec')
    else:
        return render_template('magpie/word2vec.html')


if __name__ == '__main__':
    app.run(debug=True)
