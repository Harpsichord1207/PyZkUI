import os

from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
from PyZkUI.models import ZK
from PyZkUI.utils import zk_node_ops


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
    check_res = zk_node_ops(host, 'check')
    if check_res['status'] == 'failed':
        check_res['message'] = '<strong>Failed!</strong> Can not connect to <i>{}</i>.'.format(host)
        return jsonify(check_res)
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
    # TODO: request.method related to zk operations
    if request.method == 'GET':
        host = request.args.get('h')
        path = request.args.get('p')
        resp = zk_node_ops(host, 'get', path=path)
        return jsonify(resp)
    elif request.method == 'POST':
        host = request.form.get('h')
        path = request.form.get('p')
        data = request.form.get('d')
        resp = zk_node_ops(host, 'add', path=path, data=data)
        return jsonify(resp)
    elif request.method == 'DELETE':
        host = request.form.get('h')
        path = request.form.get('p')
        resp = zk_node_ops(host, 'delete', path=path)
        return jsonify(resp)
