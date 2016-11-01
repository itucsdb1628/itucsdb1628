import psycopg2 as dbapi2

from dao.post import *
from dao.user import *
from dao.comment import *
from dao.song import *
from dao import messages
import datetime


dsn = """user='vagrant' password='vagrant'
         host='localhost' port=5432 dbname='itucsdb'"""


def create_post_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS POST"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS POST(
            ID SERIAL PRIMARY KEY,
            CONTENT VARCHAR(100) NOT NULL,
            POSTDATE TIMESTAMP,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID),
            SONGID INTEGER NOT NULL,
            ALBUMCOVERID INTEGER NOT NULL REFERENCES ALBUMCOVER(ID)
            )"""
            cursor.execute(statement)
            statement = """INSERT INTO POST (CONTENT,POSTDATE,USERID,SONGID,ALBUMCOVERID)
                            VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,('perfect!','1.10.2016',1,1,1));
            statement = """INSERT INTO POST (CONTENT,POSTDATE,USERID,SONGID,ALBUMCOVERID)
                            VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,('great!','1.10.2016',1,2,2));
            statement = """INSERT INTO POST (CONTENT,POSTDATE,USERID,SONGID,ALBUMCOVERID)
                            VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,('excellent!','1.10.2016',1,3,3));
            statement = """INSERT INTO POST (CONTENT,POSTDATE,USERID,SONGID,ALBUMCOVERID)
                            VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,('beatiful!','1.10.2016',1,4,4 ));
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()
        
def create_album_cover_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS ALBUMCOVER"""
            cursor.execute(statement);
            statement = """CREATE TABLE IF NOT EXISTS ALBUMCOVER(
                ID SERIAL PRIMARY KEY,
                FILEPATH VARCHAR(100) NOT NULL
                )"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH) 
                             VALUES ('/static/images/beatles.jpg')"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH) 
                             VALUES ('/static/images/ledzeplin.jpg')"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH) 
                             VALUES ('/static/images/metallica.jpg')"""
            cursor.execute(statement)
            statement = """INSERT INTO ALBUMCOVER (FILEPATH) 
                             VALUES ('/static/images/pinkfloyd.jpg')"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()



def insert_post(post):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO POST(CONTENT,POSTDATE,USERID,SONGID,ALBUMCOVERID) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(post.content,post.postdate,post.userid,post.songid,post.albumcoverid))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def create_user_table():
    with dbapi2.connect(dsn) as connection:
        try:
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



def insert_user(user):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO USERDATA(ID,USERNAME,PASSWORD) VALUES(%s,%s,%s)"""
            cursor.execute(statement,(user.id,user.username,user.password))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()


def create_comment_table():
    with dbapi2.connect(dsn) as connection:
        try:
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


def insert_comment(comment):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """INSERT INTO COMMENT(CONTENT,USERID,POSTID,CDATE) VALUES(%s,%s,%s,%s)"""
            cursor.execute(statement,(comment.content,comment.userid,comment.postid,comment.cdate))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()


#song table
def create_song_table():
    with dbapi2.connect(dsn) as connection:
        try:
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


def insert_song(song):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """INSERT INTO SONG(ID,NAME,ALBUM,ARTIST,GENRE,FILEPATH) VALUES(%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(song.id,song.name,song.album,song.artist,song.genre,song.filepath))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()



def create_messages_table():
    """ Drops(if exits) and Creates all tables for Messages """
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(""" DROP TABLE IF EXISTS MESSAGE_ROOM CASCADE; """)
            cursor.execute(""" CREATE TABLE MESSAGE_ROOM (
                                       ID SERIAL PRIMARY KEY,
                                       NAME TEXT NULL
                                  ); """)

            cursor.execute(""" DROP TABLE IF EXISTS MESSAGE CASCADE; """)
            cursor.execute(""" CREATE TABLE MESSAGE (
                                       ID SERIAL PRIMARY KEY,
                                       TEXT TEXT NOT NULL,
                                       DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                       RoomID INTEGER REFERENCES MESSAGE_ROOM (ID) ON DELETE CASCADE,
                                       SenderID VARCHAR (40) --todo refer to userid ON DELETE SET NULL
                                  ); """)

            cursor.execute(""" DROP TABLE IF EXISTS MESSAGE_PARTICIPANT; """)
            cursor.execute(""" CREATE TABLE MESSAGE_PARTICIPANT (
                                       RoomID INTEGER REFERENCES MESSAGE_ROOM (ID) ON DELETE CASCADE,
                                       UserID VARCHAR (40), --todo refer to userid, ON DELETE SET NULL
                                       PRIMARY KEY (RoomID, UserID)
                                   ); """)

            cursor.execute(""" DROP TABLE IF EXISTS MESSAGE_STATUS; """)
            cursor.execute(""" CREATE TABLE MESSAGE_STATUS (
                                       MessageID INTEGER REFERENCES MESSAGE (ID) ON DELETE CASCADE,
                                       ReceiverID VARCHAR (40), --todo refer to userid ON DELETE CASCADE
                                       STATUS BOOLEAN DEFAULT TRUE,
                                       PRIMARY KEY (MessageID, ReceiverID)
                                   ); """)


def insert_bulk_messages():
    room1 = messages.Room(name="roomName1", participants=["p1", "p2", "p3", "p4", "p5"])  # todo userID
    room1.save()
    room2 = messages.Room(name="roomName2", participants=["p1", "p2", "p3"])  # todo userID
    room2.save()
    room3 = messages.Room(name="roomName3", participants=["p1", "p4", "p5"])  # todo userID
    room3.save()

    message1 = messages.Message("p1", room1, "Hello Room1!")
    message1.save()
    message2 = messages.Message("p1", room2, "Hello Room2!")
    message2.save()
    message3 = messages.Message("p1", room3, "Hello Room3!")
    message3.save()

    # print([room.name for room in Room.get_room_headers("p1")])
    #
    # print([msg.text for msg in Message.get_messages(room1)])
    # print([msg.text for msg in Message.get_messages(room2)])
    # print([msg.text for msg in Message.get_messages(room3)])
