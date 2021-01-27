import os

from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from models import ZK
from PyZkUI.utils import get_zk_node, check_zk_host, add_zk_node, delete_zk_node


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
    h, p = host.split(':')
    if not (h and p):
        return jsonify({'status': 'failed', 'message': '<strong>Failed!</strong> Invalid host or port.'})
    if not check_zk_host(host):
        return jsonify({'status': 'failed', 'message': '<strong>Failed!</strong> Can not connect to <i>{}</i>.'.format(host)})
    zk_obj = ZK(host=host)
    resp = zk_obj.save()
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


@app.route('/node', methods=['GET', 'PUT', 'POST', 'DELETE'])
def node():
    if request.method == 'GET':
        host = request.args.get('h')
        path = request.args.get('p')
        if host and path:
            data = get_zk_node(host, path=path)
            if data is not None:
                return jsonify(data)
        return jsonify({'status': 'failed', 'message': 'Get node info failed.'})
    elif request.method == 'POST':
        host = request.form.get('h')
        path = request.form.get('p')
        data = request.form.get('d')
        resp = add_zk_node(host, path, data)
        return jsonify(resp)
    elif request.method == 'DELETE':
        host = request.form.get('h')
        path = request.form.get('p')
        return jsonify(delete_zk_node(host, path))


