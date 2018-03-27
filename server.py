# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, Response
import json
from predict.predict import Predict

app = Flask(__name__)
pred = Predict()

@app.route('/')
def index():
    title = "Ping Pong"
    return render_template('index.html', title=title)

@app.route('/', methods=['POST'])
def get_AI_action():
    json = request.json
    state_array = []
    state_array.append(json["paddle_x"])
    state_array.append(json["x"])
    state_array.append(json["y"])
    state_array.append(json["dx"])
    state_array.append(json["dy"])
    action = pred.predict(state_array)
    return Response(str(action))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
