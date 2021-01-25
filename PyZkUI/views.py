import os

from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from models import ZK
from PyZkUI.utils import get_zk_node, get_zk_nodes, check_zk_host


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
    # TODO: empty host
    if not check_zk_host(host):
        return jsonify({'status': 'failed', 'message': '<strong>Failed!</strong> Can not connect to <i>{}</i>.'.format(host)})
    zk_obj = ZK(host=host)
    resp = zk_obj.save()
    # if resp['status'] == 'failed':
    #     resp['message'] = '<strong>Failed!</strong> Host <i>{}</i> already exists.'.format(host)
    return jsonify(resp)


@app.route('/load_hosts')
def load_hosts():
    return jsonify(ZK.export())


@app.route('/delete_host')
def delete_host():
    host_id = request.args.get('id')
    if host_id is not None:
        ZK.delete(zk_id=host_id)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'})


@app.route('/zk')
def zk():
    host_id = request.args.get('id')
    if host_id is None:
        return redirect('/')
    zk_obj = ZK.get_by_id(host_id)
    if zk_obj:
        return render_template('tree.html', host=zk_obj.host)
    return redirect('/')


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
        data = get_zk_node(host, path=path)
        if data is not None:
            return jsonify(data)
    return jsonify({'status': 'failed', 'message': 'Get node info failed.'})
