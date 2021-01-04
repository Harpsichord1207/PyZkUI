import os

from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from PyZkUI.utils import get_zk_node, get_zk_nodes, check_zk_host, HostHistory

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/add_host')
def add_host():
    host = str(request.args.get('host')).strip().lower()
    if not check_zk_host(host):
        return jsonify({'status': 'failed'})
    data = HostHistory.add(host)
    return jsonify(**data, **{'status': 'success'})


@app.route('/load_hosts')
def load_hosts():
    return jsonify(HostHistory.export())


@app.route('/delete_host')
def delete_host():
    host_id = request.args.get('id')
    if host_id is not None:
        try:
            HostHistory.data.pop(int(host_id)-1)
            return jsonify({'status': 'success'})
        except IndexError:
            pass
    return jsonify({'status': 'failed'})


@app.route('/zk')
def zk():
    host_id = request.args.get('id')
    if host_id is None:
        return render_template('tree.html', host='Null')
    return render_template('tree.html', host=HostHistory.data[int(host_id)-1]['host'])


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
