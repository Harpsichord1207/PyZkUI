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
    return render_template('tree.html')


@app.route('/his')
def history():
    return jsonify(_history)


@app.route('/tree')
def tree():
    data = [{"text": "Inbox", "icon": "fa fa-inbox", "nodes": [{"text": "Office", "icon": "fa fa-inbox",
                                                                "nodes": [{"icon": "fa fa-inbox", "text": "Customers"},
                                                                          {"icon": "fa fa-inbox",
                                                                           "text": "Co-Workers"}]},
                                                               {"icon": "fa fa-inbox", "text": "Others"}]},
            {"icon": "fa fa-archive", "text": "Drafts"}, {"icon": "fa fa-calendar", "text": "Calendar"},
            {"icon": "fa fa-address-book", "text": "Contacts"}, {"icon": "fa fa-trash", "text": "Deleted Items"}]
    return jsonify(data)
