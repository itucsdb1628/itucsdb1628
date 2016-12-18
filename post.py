import psycopg2 as dbapi2
from flask import request
from flask_login import current_user, login_required, login_user, logout_user
import datetime
from dsn_conf import get_dsn

dsn = get_dsn()

def select_posts(userid):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT POST.ID, POST.CONTENT, POST.POSTDATE ,SONG.NAME, ARTIST.NAME, PICTURE.FILEPATH,
             POST.LIKECOUNTER AS NUMBER,USERDATA.USERNAME
             FROM POST,SONG,ARTIST,USERDATA,PICTURE
             WHERE(
             POST.SONGID = SONG.ID
             AND SONG.ARTIST = ARTIST.ID
             AND PICTURE.ID = ARTIST.PICTUREID
             AND POST.USERID = USERDATA.ID
             AND POST.USERID = %s)
             ORDER BY POST.POSTDATE DESC""" % userid
             cursor.execute(query)
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()





def delete_post(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM POST WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()





def select_post(UPDATEID):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT POST.ID, POST.CONTENT, POST.POSTDATE, SONG.NAME,ARTIST.NAME, PICTURE.FILEPATH,PICTURE.ID,
             USERDATA.USERNAME
             FROM POST,ARTIST,USERDATA,PICTURE,SONG WHERE
             POST.SONGID = SONG.ID
             AND SONG.ARTIST = ARTIST.ID
             AND PICTURE.ID = ARTIST.PICTUREID
             AND POST.USERID = USERDATA.ID
             AND POST.ID = %s  """ %UPDATEID
             cursor.execute(query)
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()



def update_post(UPDATEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            content = request.form['content']
            query = """UPDATE POST SET CONTENT = '%s' WHERE ID = %d""" % (content,int(UPDATEID))
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def insert_post_page():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            content = request.form['content']
            songid = request.form['songid']
            userid = current_user.id
            postdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query ="""INSERT INTO POST(CONTENT,USERID,SONGID,POSTDATE) VALUES(%s,%s,%s,%s)"""
            cursor.execute(query,(content,userid,songid,postdate))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
