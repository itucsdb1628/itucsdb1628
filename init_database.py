import psycopg2 as dbapi2

from dao.post import *
from dao.user import *
from dao.comment import *
from dao.song import *


dsn = """user='vagrant' password='vagrant'
         host='localhost' port=5432 dbname='itucsdb'"""


def create_post_table():
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS POST(
            ID SERIAL PRIMARY KEY,
            CONTENT VARCHAR(100) NOT NULL,
            POSTDATE TIMESTAMP,
            USERID INTEGER NOT NULL,
            SONGID INTEGER NOT NULL
            )"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()


def insert_post(post):
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement= """INSERT INTO POST(CONTENT,POSTDATE,USERID,SONGID) VALUES(%s,%s,%s,%s)"""
        cursor.execute(statement,(post.content,post.postdate,post.userid,post.songid))
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError as e:
        connection.rollback()
    finally:
        connection.close()

def create_user_table():
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS USERDATA(
            ID SERIAL PRIMARY KEY,
            USERNAME  VARCHAR(50) UNIQUE NOT NULL,
            PASSWORD VARCHAR(20) NOT NULL
            )"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()


def insert_user(user):
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement= """INSERT INTO USERDATA(ID,USERNAME,PASSWORD) VALUES(%s,%s,%s)"""
        cursor.execute(statement,(user.id,user.username,user.password))
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError as e:
        connection.rollback()
    finally:
        connection.close()

def create_comment_table():
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS COMMENT(
            ID SERIAL PRIMARY KEY,
            CONTENT VARCHAR(150) NOT NULL,
            USERID INTEGER NOT NULL,
            POSTID INTEGER NOT NULL,
            CDATE TIMESTAMP
            )"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()

def insert_comment(comment):
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO COMMENT(CONTENT,USERID,POSTID,CDATE) VALUES(%s,%s,%s,%s)"""
        cursor.execute(statement,(comment.content,comment.userid,comment.postid,comment.cdate))
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError as e:
        connection.rollback()
    finally:
        connection.close()
        
#song table     
def create_song_table():
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS SONG(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(50) NOT NULL,
            ALBUM VARCHAR(30),
            ARTIST VARCHAR(30) NOT NULL,
            GENRE VARCHAR(20),
            FILEPATH VARCHAR(64) UNIQUE NOT NULL
            )"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()

def insert_song(song):
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO SONG(ID,NAME,ALBUM,ARTIST,GENRE,FILEPATH) VALUES(%s,%s,%s,%s,%s,%s)"""
        cursor.execute(statement,(song.id,song.name,song.album,song.artist,song.genre,song.filepath))
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError as e:
        connection.rollback()
    finally:
        connection.close()