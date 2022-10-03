import json
import base64
from flask import Flask, request
import replicate
from logging.config import dictConfig
import sys
from flask_cors import CORS, cross_origin
from flask import jsonify

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/query")
@cross_origin()
def query():
    encoded_data = request.args.get('data', '')
    print(f"Got encoded data: {encoded_data}", file=sys.stderr)

    encoded_data = encoded_data[1:-1]
    print(f"MORE MORE encoded data: {encoded_data}", file=sys.stderr)

    data = base64.b64decode(encoded_data)
    obj = json.loads(data)
    model = replicate.models.get("paper11667/clipstyler")
    app.logger.info(f'Processing {len(obj["images"])} images')

    objects = []

    for i in obj["images"]:
        imgurl = i['originalURL']
        print(f"Processing: {imgurl}", file=sys.stderr)
        tmp = []
        for k in model.predict(image=imgurl, text=obj["artist"], iterations=100):
            tmp.append(k)

        objects.append({
            "originalURL": i['originalURL'],
            "description:": i['description'],
            "cachedImage": tmp[-1:][0]
        })

    finalobj = {
        "images": objects,
        "prompt": obj["prompt"],
        "artist": obj["artist"]
    }

    # jobj = json.dumps(finalobj)
    # print(f"jobj: {jobj}", file=sys.stderr)
    # bj = base64.b64encode(bytes(jobj, 'utf-8'))
    app.logger.info(f'Done processing...')
    return jsonify(
        body= finalobj
    )

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hola universo!</p>"

if __name__ == '__main__':
    app.debug = True
    app.run()

