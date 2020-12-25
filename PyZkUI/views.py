import os

from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from PyZkUI.utils import get_zk_node, get_zk_nodes

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
        return redirect('/')
    _history.append(host)
    return render_template('tree.html', host=host)


@app.route('/his')
def history():
    return jsonify(_history)


@app.route('/tree')
def tree():
    host = request.args.get('h')
    data = get_zk_nodes(host)
    if data is None:
        return jsonify({'status': 'failed', 'message': 'Connection Failed.'})
    else:
        return jsonify({'status': 'success', 'data': data})


@app.route('/node')
def node():
    host = request.args.get('h')
    path = request.args.get('p')
    if host and path:
        return jsonify(get_zk_node(host, path=path))
    else:
        return jsonify({'status': 'failed', 'message': 'Get node info failed.'})
