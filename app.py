import json
import base64
from flask import Flask, request
import replicate
from logging.config import dictConfig
import sys

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

@app.route("/query")
def query():
    encoded_data = request.args.get('data', '')
    data = base64.b64decode(encoded_data)
    obj = json.loads(data)
    model = replicate.models.get("paper11667/clipstyler")
    modified_images = []
    app.logger.info(f'Processing {len(obj["images"])} images')

    time_to_wait = 10
    time_counter = 0

    for i in obj["images"]:
        imgurl = i['originalURL']
        print(f"Processing: {imgurl}", file=sys.stderr)
        tmp = []
        for k in model.predict(image=imgurl, text="in the style of Da Vinci", iterations=100):
            tmp.append(k)

        modified_images.append(tmp[:-1])

    app.logger.info(f'Done processing...')
    return modified_images

@app.route("/")
def hello_world():
    return "<p>Hola universo!</p>"

if __name__ == '__main__':
    app.debug = True
    app.run()

