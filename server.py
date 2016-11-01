import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

from init_database import initialize_database
from post import *
from dsn_conf import get_dsn

app = Flask(__name__)


'''********************************TIMELINE ROUTES - ismail*********************************'''


@app.route('/timeline')
def timeline_page():
    return render_template("timeline.html", posts=select_posts())


@app.route('/timeline/delete/<int:DELETEID>', methods=['GET', 'POST'])
def timeline_page_delete(DELETEID):
    delete_post(DELETEID)
    return redirect(url_for('timeline_page'))


@app.route('/timeline/update/<int:UPDATEID>/', methods=['GET', 'POST'])
def timeline_page_update(UPDATEID):
    return render_template('timeline_edit.html', posts=select_post(UPDATEID))


@app.route('/timeline/update/<int:UPDATEID>/APPLY', methods=['GET', 'POST'])
def timeline_page_apply(UPDATEID):
    update_post(UPDATEID)
    return redirect(url_for('timeline_page'))


@app.route('/timeline/insert', methods=['GET', 'POST'])
def timeline_page_insert():
    insert_post_page()
    return redirect(url_for('timeline_page'))


'''*********************************************************************************'''


@app.route('/')
def home_page():
    initialize_database()
    return render_template('home.html')


@app.route('/messages')
def messages_page():
    return render_template('messages.html')


@app.route('/profile')
def profile_page():
    return render_template("profile.html")


@app.route('/music')
def music_page():
    return render_template("music.html")


@app.route('/activities')
def activities_page():
    return render_template("activities.html")


@app.route('/createtables')
def initialize_database():
    initialize_database()
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.config['dsn'] = get_dsn()

    app.run(host='0.0.0.0', port=port, debug=debug)
