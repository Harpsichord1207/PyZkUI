import os

from flask import Flask, render_template, send_from_directory, request, jsonify


app = Flask(__name__)
_history = []


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/zk')
def zk():
    host = request.args.get('h')
    if host is None:
        return "Error"
    _history.append(host)
    return "Ok"


@app.route('/his')
def history():
    return jsonify(_history)
