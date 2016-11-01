import datetime
import os
import json
import re
import psycopg2 as dbapi2


from init_database import *
from post import *


from flask import redirect
from flask.helpers import url_for
from flask import Flask
from flask import render_template
from flask import request


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


def get_dns():
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        return get_elephantsql_dsn(VCAP_SERVICES)
    else:
        return """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

'''********************************TIMELINE ROUTES - ismail*********************************'''
@app.route('/timeline')
def timeline_page():
    return render_template("timeline.html", posts = select_posts())

@app.route('/timeline/delete/<int:DELETEID>', methods=['GET', 'POST'])
def timeline_page_delete(DELETEID):
     delete_post(DELETEID)
     return redirect(url_for('timeline_page'))

@app.route('/timeline/update/<int:UPDATEID>/', methods=['GET', 'POST'])
def timeline_page_update(UPDATEID):
    return render_template('timeline_edit.html', posts = select_post(UPDATEID))

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


@app.route('/activities')
def activities_page():
    return render_template("activities.html")

@app.route('/createtables')
def initialize_database():
    create_album_cover_table()
    create_post_table()
    firstPost = Post("perfect!",datetime.datetime.now(),1, 1,1)
    insert_post(firstPost)

    create_user_table()
    firstuser = User(1,"user1","password1")
    insert_user(firstuser)

    create_comment_table()
    first_comment = Comment("first",1,1,datetime.datetime.now())
    insert_comment(first_comment)

    create_song_table()
    sample_song = Song(1,"Scar Tissue","Californication","Red Hot Chili Peppers","Rock","imaginary_filepath.mp3")
    insert_song(sample_song)

    create_messages_table()
    insert_bulk_messages()

    return redirect(url_for('home_page'))



if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.config['dsn'] = get_dns()

    app.run(host='0.0.0.0', port=port, debug=debug)
