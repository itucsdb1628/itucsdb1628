import psycopg2 as dbapi2
from flask import request
import datetime
from dsn_conf import get_dsn
from flask_login.utils import current_user

dsn = get_dsn()

def insert_sharedPost(postID):
    with dbapi2.connect(dsn) as connection:
        try:
           cursor = connection.cursor()
           query = """INSERT INTO SHARE(POSTID,REPOSTERID,SHAREDATE) VALUES(%s,%s,%s)"""
           repostdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           cursor.execute(query,(postID,current_user.id,repostdate))
           connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_sharedPost(repostID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM SHARE WHERE ID = %s""", (int(repostID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_sharedPost(reposterID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT SHARE.ID,POST.CONTENT,SONG.NAME,ARTIST.NAME,PICTURE.FILEPATH,USERDATA.USERNAME,
            POST.POSTDATE,SHARE.SHAREDATE FROM POST,PICTURE,USERDATA,SHARE,SONG,ARTIST
            WHERE(
            SHARE.POSTID = POST.ID
            AND POST.SONGID = SONG.ID
            AND SONG.ARTIST = ARTIST.ID
            AND ARTIST.PICTUREID = PICTURE.ID
            AND POST.USERID = USERDATA.ID
            AND SHARE.REPOSTERID = %s)
            ORDER BY SHARE.ID""" %reposterID
            cursor.execute(query)
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_sharedFor_activities(userID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT POST.CONTENT,PICTURE.FILEPATH,USERDATA.USERNAME,SONG.NAME,ARTIST.NAME
            FROM POST,USERDATA,SHARE,SONG,PICTURE,ARTIST
            WHERE(
            SHARE.POSTID = POST.ID
            AND POST.SONGID = SONG.ID
            AND SONG.ARTIST = ARTIST.ID
            AND ARTIST.PICTUREID = PICTURE.ID
            AND SHARE.REPOSTERID = USERDATA.ID
            AND POST.USERID = %s)
            ORDER BY SHARE.ID""" %userID
            cursor.execute(query)
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()