import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

from dao.messages import Room, Message
from init_database import reset_database
from post import *

from comment import *

from genre import *
from userdata import *
from dao.genre import *

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


'''*********************************ADMIN PAGE**************************************'''
@app.route('/adminpanel', methods=['GET', 'POST'])
def adminpanel_page():
    if request.method == 'GET':

        return render_template('adminpanel.html',allgenre = select_all_genre(),allgenre2 = select_all_genre())
    else:
        actiontype = int(request.form['actiontype'])
        if actiontype == 1: #addgenre
            genrename = request.form['genrename']
            newgenre = Genre(genrename)
            insert_genre(newgenre)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 2: #updategenre
            genreid = request.form['genreid']
            newname = request.form['newname']
            update_genre(genreid,newname)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 3: #deletegenre
            genreid = request.form['genreid']
            delete_genre(genreid)
            return redirect(url_for('adminpanel_page'))



'''*********************************************************************************'''
'''****************************** USERDATA TABLE OPERATIONS *************************'''
@app.route('/')
def home_page():
    reset_database()
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['lg_username']
    password = request.form['lg_password']
    user_list = select_users_from_login()
    for record in user_list:
        if (record[1] == username and record[2] == password):
            return redirect('/timeline')

    return render_template('signinerror.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['reg_username']
    password = request.form['reg_password']
    insert_user_login(username,password)
    return render_template('successful_signup.html')

@app.route('/update-profile', methods=['POST'])
def update_profile():
    old_username = request.form['old_username']
    username = request.form['new_username']
    password = request.form['new_password']
    update_user_login(username,password,old_username)
    return render_template('home.html')

@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    username = request.form['username']
    password = request.form['password']
    delete_user_login(username,password)
    return render_template('home.html')

'''*********************************************** END OF USERDATA TABLE OPERATIONS ****************************'''


@app.route('/messages')
@app.route('/messages/<int:room_id>')
def messages_page(room_id=None):
    room = None
    if room_id is not None:
        room = Room.get_room_by_id(room_id)
        room.participants = Room.get_participants(room_id)
        room.messages = Message.get_messages(room)

    # todo Rooms=Room.get_room_header(logged_in_userID)
    return render_template('messages.html', Rooms=Room.get_room_headers("pk1"), SelectedRoom=room)


@app.route('/messages/new_room', methods=['POST'])
def messages_new_room():
    room_id = None
    if request.method == 'POST':
        group_name = request.form['group_name']
        participants = request.form.getlist('participants')

        room = Room(name=group_name, participants=participants + ["pk1"])  # todo userID
        room.save()

    return redirect(url_for('messages_page'))


@app.route('/messages/update_room', methods=['POST'])
def messages_update_room():
    return redirect(url_for('messages_page'))


@app.route('/messages/delete_room', methods=['POST'])
def messages_delete_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        Room.delete_room(room_id)
    return redirect(url_for('messages_page'))


@app.route('/messages/new_message', methods=['POST'])
def messages_new_message():
    return redirect(url_for('messages_page'))


@app.route('/profile')
def profile_page():
    return render_template("profile.html")


@app.route('/music')
def music_page():
    return render_template("music.html")

'''Activity Routes-Salih'''
@app.route('/activities')
def activities_page():
    return render_template("activities.html", comments = select_comments())

@app.route('/activities/insert', methods=['GET', 'POST'])
def activities_page_insert():
    actiontype = int(request.form['actiontype'])
    comment = request.form['comment']
    avatar = request.form['avatar']
    postid = request.form['postid']
    userid = request.form['userid']
    if actiontype == 1:
        insert_comment(comment, avatar, postid, userid)
    return redirect(url_for('activities_page'))

@app.route('/activities/delete', methods=['GET', 'POST'])
def activities_page_delete():
    deleteid = int(request.form['commentid'])

    delete_comment(deleteid)
    return redirect(url_for('activities_page'))

@app.route('/activities/update', methods = ['GET','POST'])
def activities_page_update():
    actiontype = int(request.form['actiontype'])
    if actiontype == 2:
        updateid = int(request.form['commentid'])
        update_comment(updateid)
    return redirect(url_for('activities_page'))
'''Activity Routes-Salih'''

@app.route('/createtables')
def initialize_database():
    reset_database()
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.config['dsn'] = get_dsn()

    app.run(host='0.0.0.0', port=port, debug=debug)
