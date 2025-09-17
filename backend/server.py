import json
import os

from flask import Flask, abort, request, send_from_directory
from flask_cors import cross_origin
from main import create_barcode, create_qrcode

# Путь к папке с фронтендом
frontend_path = os.path.join(os.path.dirname(__file__), '../frontend/public')
app = Flask(__name__, static_folder=frontend_path)

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.post("/qrcode")
@cross_origin()
def send_qrcode():
    try:
        data = json.loads(request.data)
        if not isinstance(data, dict):
            abort(400, 'Request body should be JSON')
        if 'text' not in data or 'level' not in data:
            abort(400, 'Parameters requirements are not met')
        return create_qrcode(data['level'], data['text']), 200
    except:
        abort(400)

@app.post("/barcode")
@cross_origin()
def send_barcode():
    try:
        data = json.loads(request.data)
        print("Received /barcode:", data)  # Лог
        if not isinstance(data, dict):
            abort(400, 'Request body should be JSON')
        if 'text' not in data or 'type' not in data:
            abort(400, 'Parameters requirements are not met')

        return create_barcode(data['type'], data['text']), 200
    except Exception as e:
        print("Error:", e)
        abort(400)