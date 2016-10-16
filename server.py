import datetime
import os

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html')


@app.route('/messages')
def messages_page():
    return render_template('messages.html')


@app.route('/test')
def test_page():
    return render_template('test.html')


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
