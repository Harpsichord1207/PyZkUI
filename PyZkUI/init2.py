import os

from flask import Flask, send_from_directory, redirect
from flask_admin import Admin

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

admin = Admin(app, name='PyZkUI', template_mode='bootstrap4')
# Add administrative views here


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/')
def index():
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
