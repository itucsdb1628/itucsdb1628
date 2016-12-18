import psycopg2 as dbapi2
from flask import request
from post import *
import datetime
from dsn_conf import get_dsn

dsn = get_dsn()

def delete_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM LIKES WHERE (USERID = %s
             AND POSTID = %s)"""
            cursor.execute(query,(userId,postId))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
        try:
            cursor = connection.cursor()
            query = """UPDATE POST SET LIKECOUNTER = LIKECOUNTER - 1 WHERE (ID = %d)""" % (int(postId),)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()


def insert_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO LIKES(POSTID,USERID,LIKEDATE) VALUES(%s,%s,%s)"""
            cursor.execute(query,(postId,userId,datetime.datetime.now()))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
        try:
            cursor = connection.cursor()
            query = """UPDATE POST SET LIKECOUNTER = LIKECOUNTER + 1 WHERE ID = %d""" % (int(postId),)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT * FROM LIKES WHERE POSTID = %s
             AND USERID = %s """
             cursor.execute(query,(postId,userId))
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_user_likes(userId):
       with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT POSTID,LIKEDATE FROM LIKES
             WHERE USERID = %s
             ORDER BY POSTID"""
             cursor.execute(query,(userId,))
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_like_number(userId):
     with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT COUNT(*) FROM LIKES WHERE
             AND USERID = %s
             GROUP BY POSTID,USERID ORDER BY POSTID"""
             cursor.execute(query,(userId,))
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()

def control_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        cursor = select_like(userId,postId)
        control = cursor.fetchone()

        if control is None:
            return True
        else:
            return False

def select_likeFor_activities(userId):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT POST.ID, POST.USERID, POST.CONTENT, SONG.NAME,ARTIST.NAME,USERDATA.USERNAME,LIKES.POSTID, PICTURE.FILEPATH
             FROM LIKES,USERDATA,POST,PICTURE,SONG,ARTIST
             WHERE (LIKES.USERID = USERDATA.ID
             AND POST.SONGID = SONG.ID
             AND SONG.ARTIST = ARTIST.ID
             AND ARTIST.PICTUREID = PICTURE.ID
             AND LIKES.POSTID = POST.ID
             AND POST.USERID = %s)
             ORDER BY POSTID"""%userId
             cursor.execute(query,(userId,))
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()