import os

from flask import Flask, app
from flask import redirect
from flask import render_template
from flask.helpers import url_for
from flask import current_app, request
from werkzeug.utils import secure_filename ####

# from dao.messages import Room, Message, tempLoggedUser
import dao.messages as Messages
from init_database import reset_database
from init_database import insert_sample_data
from post import *
from like import *
from comment import *
from shared_post import *
from forms import *
from song import *
from artist import *
from genre import *
from userdata import *
from dao.genre import *
from dao.artist import *
from dao.song import *
from picture import *
from album import *
from dao.userdetails import *
from suggestion import *
from userdetails import *
from settings import *
from flask_login import LoginManager
from flask_login import current_user, login_required, login_user, logout_user

from dsn_conf import get_dsn
from flask.globals import request


lm = LoginManager()


app = Flask(__name__)



@lm.user_loader
def load_user(user_id):
    return get_user(user_id)



def create_app():
    app.config.from_object('settings')

    lm.init_app(app)
    lm.login_view='login'

    return app
'''********************************TIMELINE ROUTES - ismail*********************************'''

@app.route('/timeline/like/<int:LIKEID>/<string:USERNAME>', methods=['GET', 'POST'])
@login_required
def like_post(LIKEID,USERNAME):
    if(control_like(current_user.id,LIKEID)):
        insert_like(current_user.id,LIKEID)
    else:
        delete_like(current_user.id,LIKEID)

    if(USERNAME == current_user.username):
          return redirect(url_for('timeline_page'))
    else:
          user = get_user(USERNAME)
          return render_template("timeline_search.html", posts=list(select_posts(user.id)), likes = list(select_user_likes(current_user.id)),owner_user = user)


@app.route('/timeline/search' ,methods=['GET', 'POST'])
@login_required
def search_user():
    content = request.form['content']
    user = get_user(content)
    if(user == None):
         return render_template("error.html" ,posts=list(select_posts(current_user.id)), likes = list(select_user_likes(current_user.id)),error_messages = 'User could not be found.',owner_user = current_user)
    if(current_user.id == user.id):
         return render_template("timeline.html", posts=list(select_posts(current_user.id)), likes = list(select_user_likes(current_user.id)),owner_user = current_user,reposts = list(select_sharedPost(current_user.id)))
    else:
         return render_template("timeline_search.html", posts=list(select_posts(user.id)), likes = list(select_user_likes(current_user.id)), owner_user = user,reposts = list(select_sharedPost(user.id)))


@app.route('/timeline')
@login_required
def timeline_page():
    id = current_user.id
    return render_template("timeline.html", posts=list(select_posts(id)), likes = list(select_user_likes(current_user.id)),owner_user = current_user,reposts = list(select_sharedPost(id)))


@app.route('/timeline/delete/<int:DELETEID>', methods=['GET', 'POST'])
@login_required
def timeline_page_delete(DELETEID):
    delete_post(DELETEID)
    return redirect(url_for('timeline_page'))


@app.route('/timeline/update/<int:UPDATEID>/', methods=['GET', 'POST'])
@login_required
def timeline_page_update(UPDATEID):
    return render_template('timeline_edit.html', posts=select_post(UPDATEID),owner_user = current_user)


@app.route('/timeline/update/<int:UPDATEID>/APPLY', methods=['GET', 'POST'])
@login_required
def timeline_page_apply(UPDATEID):
    update_post(UPDATEID)
    return redirect(url_for('timeline_page'))


@app.route('/timeline/insert', methods=['GET', 'POST'])
@login_required
def timeline_page_insert():
    insert_post_page()
    return redirect(url_for('timeline_page'))

@app.route('/suggestions')
@login_required
def suggestion_page():
    return render_template("suggestions.html",suggestions=list(select_suggestions_user()))

@app.route('/suggestions/insert', methods=['GET', 'POST'])
@login_required
def suggestion_insert_page():
    artist = request.form['artist']
    songname = request.form['song']
    releaseDate = request.form['release_year']
    insert_suggestion(current_user.id,artist,songname,releaseDate)
    return redirect(url_for('suggestion_page'))



@app.route('/suggestions/delete/<int:DELETEID>', methods=['GET', 'POST'])
@login_required
def suggestion_delete_page(DELETEID):
    delete_suggestion(DELETEID)
    return redirect(url_for('suggestion_page'))
'''*********************************************************************************'''

'''*********************************ADMIN PAGE**************************************'''


@app.route('/adminpanel', methods=['GET', 'POST'])
@login_required
def adminpanel_page():
    if request.method == 'GET':
        albums=[]
        allgenre=[]
        allartist=[]
        song_album=[]
        return render_template('adminpanel.html', albums=select_albums(), allgenre=select_all_genre(), allartist=select_all_artist(), song_album=select_song_album(),suggestions =  select_suggestions(), artist_pics= select_artist_pics())
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
        if actiontype == 7:  # addartist
            filename = request.form['filepath']
            insert_picture(Picture(filename,1))
            artistname = request.form['artistname']
            pictureid = select_picture_id(filename)
            newartist = Artist(artistname,pictureid[0])
            insert_artist(newartist)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 8:  # updateartist
            artistid = request.form['artistid']
            newname = request.form['newname']
            update_artist(artistid, newname)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 9:  # deleteartist
            artistid = request.form['artistid']
            delete_artist(artistid)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 10:  # addsong
            songname = request.form['songname']
            albumid = int(request.form['albumid'])
            artistid = int(request.form['artistid'])
            filepath = request.form['filepath']
            genreid = int(request.form['genreid'])
            newsong = Song(songname,albumid,artistid,genreid,filepath)
            insert_song(newsong)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 11:  # updatesong
            UPDATEID = request.form['songid']
            songname = request.form['songname']
            albumid = int(request.form['albumid'])
            artistid = int(request.form['artistid'])
            filepath = request.form['filepath']
            genreid = int(request.form['genreid'])
            update_song(UPDATEID,songname,artistid,albumid,genreid,filepath)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 12:  # deletesong
            songid = request.form['songid']
            delete_song(songid)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 13:
            reset_database()
            insert_sample_data()
            return redirect(url_for('adminpanel_page'))
        if actiontype == 14:
            suggestionId = request.form['id']
            approve_suggestion(suggestionId)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 15:
            suggestionId = request.form['id']
            reject_suggestion(suggestionId)
            return redirect(url_for('adminpanel_page'))
        if actiontype == 16: #add artist pic
            filename = upload_file('adminpanel_page')
            filename = UPLOAD_FOLDER + filename
            insert_picture(Picture(filename,1))
            return redirect(url_for('adminpanel_page'))
        if actiontype == 17: #add album pic
            filename = upload_file('adminpanel_page')
            filename = UPLOAD_FOLDER + filename
            return redirect(url_for('adminpanel_page'))


'''*********************************************************************************'''
'''****************************** USERDATA TABLE OPERATIONS *************************'''


'''@app.route('/')
def home_page():
    return render_template('home.html')'''


@app.route('/', methods=['GET','POST'])
def login():
    form=LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user = get_user(username)
        #user_list = select_users_from_login()
        if user is not None:
            password = form.password.data
            if(password == user.password):
                login_user(user)
                return redirect(url_for('timeline_page'))

    return render_template('home.html',form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['reg_username']
    password = request.form['reg_password']
    insert_user_login(username, password)
    return redirect(url_for('login'))


@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    form=LoginForm(request.form)
    old_username = request.form['old_username']
    username = request.form['new_username']
    password = request.form['new_password']
    update_user_login(username, password, old_username)
    return render_template('home.html', form = form)


@app.route('/delete-profile', methods=['POST'])
@login_required
def delete_profile():
    form=LoginForm(request.form)
    username = request.form['username']
    password = request.form['password']
    delete_user_login(username, password)
    return render_template('home.html',form = form)


'''*********************************************** END OF USERDATA TABLE OPERATIONS ****************************'''

# ################################################ Messages #################################################


@app.route('/messages')
@app.route('/messages/<int:room_id>')
@login_required
def messages_page(room_id=None):
    """ Get All Message Rooms """
    room = None

    if room_id is not None:  # room secili

        room = Messages.Room.get_details(room_id)
        if room is None:  # Verilen id'ye sahip bir room yok.
            return redirect(url_for("messages_page"))

    return render_template('messages.html', Rooms=Messages.Room.get_headers(), SelectedRoom=room, User=Messages.get_user_id())


@app.route('/messages/new_room', methods=['POST'])
@login_required
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
@login_required
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
@login_required
def messages_leave_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        room = Messages.Room.get_details(room_id)
        if room is not None:
            room.remove_participant(Messages.get_user_id())
    return redirect(url_for('messages_page'))


@app.route('/messages/delete_room', methods=['POST'])
@login_required
def messages_delete_room():
    if request.method == 'POST':
        room = Messages.Room()
        room.id = request.form['room_id']
        room.delete()
    return redirect(url_for('messages_page'))


@app.route('/messages/new_message', methods=['POST'])
@login_required
def messages_new_message():
    if request.method == 'POST':
        room = Messages.Room()
        room.id = request.form['room_id']
        room.send_message(request.form['message'])
    return redirect(url_for('messages_page', room_id=room.id))


@app.route('/messages/change_user/<user_id>')
@login_required
def messages_change_user(user_id=""):
    Messages.tempLoggedUser = user_id
    return redirect(url_for('messages_page'))


# ################################################ End Of Messages ##########################################
''' Userdetail Routes- Kağan'''


@app.route('/profiledetails')
@login_required
def profiledetails():
        return render_template("profiledetails.html", userdetails = select_userdetails(), users = select_users_from_login())

@app.route('/delete',methods=['GET','POST'])
@login_required
def showdetails():
    name = request.form['name']
    surname = request.form['surname']
    delete_userdetails(name,surname)
    return redirect(url_for('profiledetails'))

@app.route('/update',methods=['GET','POST'])
@login_required
def update():
    username = request.form['older_name']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phonenum = request.form['phonenum']
    userid = request.form['userid']
    update_userdetails(username,name,userid,surname,email,phonenum)
    return redirect(url_for('profiledetails'))


@app.route('/insert_details',methods=['GET','POST'])
@login_required
def insert_details():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phonenum = request.form['phonenum']
    userid = request.form['userid']
    userx = Userdetails(userid,name,surname,email,phonenum)
    insert_userdetails(userx)
    return redirect(url_for('profiledetails'))

@app.route('/gototimeline',methods=['GET','POST'])
@login_required
def gototimeline():
    return redirect(url_for('timeline_page'))


''' end of userdetails routes -kağan'''
@app.route('/profile')
@login_required
def profile_page():
    return render_template("profile.html")


@app.route('/music')
@login_required
def music_page():
    albums=[]
    return render_template("music.html",albums=select_albums(),allartist=select_all_artist())


'''Activity Routes-Salih'''
@app.route('/comment/<int:COMMENTID>', methods=['GET','POST'])
@login_required
def comment_page(COMMENTID):
    if request.method == 'GET':
        comments = []
        return render_template("comments.html", posts=list(select_post(COMMENTID)), comments=select_comments(COMMENTID))

    else:
        actiontype=int(request.form['actiontype'])
        #if actiontype == 1:
            #commentid=int(request.form['id'])
            #delete_comment(commentid)
            #postid=int(request.form['postid'])
            #return redirect("/comment/" + str(postid))
        if actiontype == 2:
            if request.form['comment']:
                comment=request.form['comment']
                postid=int(request.form['postid'])
                userid=int(request.form['userid'])
                avatarid=int(request.form['avatarid'])
                albumcoverid=int(request.form['albumcover'])
                insert_comment(comment,userid,postid,avatarid,albumcoverid)
                return redirect("/comment/" + str(postid))
            else:
                error = 'Please enter a comment'
                postid=int(request.form['postid'])
                return render_template("comments.html", posts=list(select_post(COMMENTID)), comments=select_comments(COMMENTID), error=error)
        if actiontype == 3:
            commentid=int(request.form['id'])
            postid=int(request.form['postid'])
            new_comment=request.form['new_comment']
            update_comment(new_comment,commentid)
            return redirect("/comment/" + str(postid))

@app.route('/comment/<int:COMMENTID>/<int:C_DELETEID>', methods=['GET', 'POST'])
@login_required
def comment_page_delete(COMMENTID,C_DELETEID):
    delete_comment(C_DELETEID)
    return redirect("/comment/" + str(COMMENTID))

@app.route('/timeline/search/<int:shareID>',methods=['GET','POST'])
@login_required
def post_share_page(shareID):
    insert_sharedPost(shareID)
    return redirect(url_for('timeline_page'))

@app.route('/timeline/delete_r/<int:repost_deleteID>',methods=['GET','POST'])
@login_required
def repost_delete_page(repost_deleteID):
    delete_sharedPost(repost_deleteID)
    return redirect(url_for('timeline_page'))

@app.route('/activities')
@login_required
def activities_page():
    activity = []
    likes_activity=list(select_likeFor_activities(current_user.id))
    return render_template("activities.html", activity=select_comments2(), likes_activity=likes_activity,reposts = list(select_sharedFor_activities(current_user.id)))


@app.route('/activities/insert', methods=['GET', 'POST'])
@login_required
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
@login_required
def activities_page_delete():
    deleteid = int(request.form['commentid'])

    delete_comment(deleteid)
    return redirect(url_for('activities_page'))


@app.route('/activities/update', methods=['GET', 'POST'])
@login_required
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
    insert_sample_data()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app  = create_app()
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.config['dsn'] = get_dsn()

    # add get total unread message count function to jinja2 global variables
    # because almost every template must reach it
    #app.jinja_env.globals.update(get_unread_message_count=Messages.get_unread_count)

    app.run(host='0.0.0.0', port=port, debug=debug)
