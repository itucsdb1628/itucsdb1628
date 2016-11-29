import os

from flask import Flask, app
from flask import redirect
from flask import render_template
from flask.helpers import url_for

# from dao.messages import Room, Message, tempLoggedUser
import dao.messages as Messages
from init_database import reset_database
from post import *
from like import *
from comment import *

from genre import *
from userdata import *
from album import *
from dao.genre import *

from dsn_conf import get_dsn
from flask.globals import request

app = Flask(__name__)

'''********************************TIMELINE ROUTES - ismail*********************************'''

@app.route('/timeline/like/<int:LIKEID>', methods=['GET', 'POST'])
def like_post(LIKEID):
    if(control_like(1,LIKEID)):
        insert_like(1,LIKEID)
    else:
        delete_like(1,LIKEID)
    return redirect(url_for('timeline_page'))

@app.route('/timeline')
def timeline_page():
    return render_template("timeline.html", posts=select_posts(), likes = list(select_user_likes(1)))


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
        albums=[]
        return render_template('adminpanel.html', allgenre=select_all_genre(), allgenre2=select_all_genre(), albums=select_albums())
    else:
        actiontype = int(request.form['actiontype'])
        if actiontype == 1:  # addgenre
            genrename = request.form['genrename']
            newgenre = Genre(genrename)
            insert_genre(newgenre)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 2:  # updategenre
            genreid = request.form['genreid']
            newname = request.form['newname']
            update_genre(genreid, newname)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 3:  # deletegenre
            genreid = request.form['genreid']
            delete_genre(genreid)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 4: #add_album
            insert_album()
            return redirect(url_for('adminpanel_page'))
        if actiontype == 5: #delete_album
            albumid = int(request.form['albumid'])
            delete_album(albumid)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 6: #update_album
            albumname = request.form['albumname']
            albumdate = int(request.form['albumdate'])
            albumcoverid = int(request.form['albumcover'])
            albumid = int(request.form['albumid'])
            update_album(albumid,albumname,albumcoverid,albumdate)
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
    insert_user_login(username, password)
    return render_template('successful_signup.html')


@app.route('/update-profile', methods=['POST'])
def update_profile():
    old_username = request.form['old_username']
    username = request.form['new_username']
    password = request.form['new_password']
    update_user_login(username, password, old_username)
    return render_template('home.html')


@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    username = request.form['username']
    password = request.form['password']
    delete_user_login(username, password)
    return render_template('home.html')


'''*********************************************** END OF USERDATA TABLE OPERATIONS ****************************'''

# ################################################ Messages #################################################


@app.route('/messages')
@app.route('/messages/<int:room_id>')
def messages_page(room_id=None):
    """ Get All Message Rooms """
    room = None

    if room_id is not None:  # room secili

        room = Messages.Room.get_details(room_id)
        if room is None:  # Verilen id'ye sahip bir room yok.
            return redirect(url_for("messages_page"))

    # todo Rooms=Room.get_room_header(logged_in_userID)
    return render_template('messages.html', Rooms=Messages.Room.get_headers(), SelectedRoom=room, User=Messages.get_user_id())


@app.route('/messages/new_room', methods=['POST'])
def messages_new_room():
    """ Create new room """
    room_id = None
    if request.method == 'POST':
        # get form values
        group_name = request.form['group_name']
        participants = request.form.getlist('participants')

        # create room and save to database
        room = Messages.Room(name=group_name, admin=Messages.get_user_id(), participants=participants + [Messages.get_user_id()])
        room_id = room.create()

    return redirect(url_for('messages_page', room_id=room_id))


@app.route('/messages/update_room', methods=['POST'])
def messages_update_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        group_name = request.form['group_name']
        participants = request.form.getlist('participants')

        room = Messages.Room.get_details(room_id)
        if room is not None and room.admin == Messages.get_user_id():
            room.update_name(group_name)
            room.update_participants(participants + [Messages.get_user_id()])

    return redirect(url_for('messages_page', room_id=room_id))


@app.route('/messages/leave_room', methods=['POST'])
def messages_leave_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        room = Messages.Room.get_details(room_id)
        if room is not None:
            room.remove_participant(Messages.get_user_id())
    return redirect(url_for('messages_page'))


@app.route('/messages/delete_room', methods=['POST'])
def messages_delete_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        room = Messages.Room.get_details(room_id)
        if room is not None:
            room.delete()
    return redirect(url_for('messages_page'))


@app.route('/messages/new_message', methods=['POST'])
def messages_new_message():
    if request.method == 'POST':
        room_id = request.form['room_id']
        message_text = request.form['message']
        room = Messages.Room.get_details(room_id)
        room.send_message(message_text)
    return redirect(url_for('messages_page', room_id=room_id))


@app.route('/messages/change_user/<user_id>')
def messages_change_user(user_id=""):
    Messages.tempLoggedUser = user_id
    return redirect(url_for('messages_page'))


# ################################################ End Of Messages ##########################################

@app.route('/profile')
def profile_page():
    return render_template("profile.html")


@app.route('/music')
def music_page():
    return render_template("music.html")


'''Activity Routes-Salih'''
@app.route('/comment/<int:COMMENTID>', methods=['GET','POST'])
def comment_page(COMMENTID):
    if request.method == 'GET':
        comments = []
        return render_template("comments.html", posts=list(select_post(COMMENTID)), comments=select_comments(COMMENTID))
    else:
        actiontype=int(request.form['actiontype'])
        if actiontype == 1:
            commentid=int(request.form['id'])
            delete_comment(commentid)
            postid=int(request.form['postid'])
            return redirect("/comment/" + str(postid))
        if actiontype == 2:
            comment=request.form['comment']
            postid=int(request.form['postid'])
            userid=int(request.form['userid'])
            avatarid=int(request.form['avatarid'])
            albumcoverid=int(request.form['albumcover'])
            insert_comment(comment,userid,postid,avatarid,albumcoverid)
            return redirect("/comment/" + str(postid))
        if actiontype == 3:
            commentid=int(request.form['id'])
            postid=int(request.form['postid'])
            new_comment=request.form['new_comment']
            update_comment(new_comment,commentid)
            return redirect("/comment/" + str(postid))

@app.route('/activities')
def activities_page():
    activity = []
    return render_template("activities.html", activity=select_comments2())


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


@app.route('/activities/update', methods=['GET', 'POST'])
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

    # add get total unread message count function to jinja2 global variables
    # because almost every template must reach it
    app.jinja_env.globals.update(get_unread_message_count=Messages.get_unread_count)

    app.run(host='0.0.0.0', port=port, debug=debug)
