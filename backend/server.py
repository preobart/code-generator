import json
from flask import Flask, request, abort
from flask_cors import cross_origin

from main import create_qrcode, create_barcode

app = Flask(__name__)


@app.post("/qrcode")
@cross_origin()
def send_qrcode():
    try:
        data = json.loads(request.data)

        if not isinstance(data, dict):
            abort(400, 'Request body should be JSON')

        if not 'text' in data or not 'level' in data:
            abort(400, 'Parameters requirements are not met')

        return create_qrcode(data['level'], data['text']), 200
    except:
        abort(400)


@app.post("/barcode")
@cross_origin()
def send_barcode():
    try:
        data = json.loads(request.data)

        if not isinstance(data, dict):
            abort(400, 'Request body should be JSON')

        if not 'text' in data or not 'type' in data:
            abort(400, 'Parameters requirements are not met')

        return create_barcode(data['type'], data['text']), 200
    except:
        abort(400)
    
    