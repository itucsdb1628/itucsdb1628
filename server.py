import datetime
import os
import json
import re
import psycopg2 as dbapi2
from init_database import *
from flask import redirect
from flask.helpers import url_for
from flask import Flask
from flask import render_template

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name  for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    now = datetime.datetime.now()
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

@app.route('/timeline')
def timeline_page():
    return render_template("timeline.html")

@app.route('/activities')
def activities_page():
    return render_template("activities.html")

@app.route('/createtables')
def initialize_database():
    create_post_table()
    firstPost = Post("perfect!",datetime.datetime.now(),1, 1)
    insert_post(firstPost)
    return redirect(url_for('home_page'))
    
        
if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'""" 
    app.run(host='0.0.0.0', port=port, debug=debug)
