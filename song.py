import psycopg2 as dbapi2
from flask import request

from dsn_conf import get_dsn

dsn = get_dsn()

def insert_song(song):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """INSERT INTO SONG(NAME,ALBUM,ARTIST,GENRE,FILEPATH) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(song.name,song.album,song.artist,song.genre,song.filepath))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_song(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM SONG WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
            
def select_all_song2():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT SONG.ID,SONG.NAME,ARTIST.NAME FROM ARTIST,SONG WHERE(SONG.ARTIST = ARTIST.ID)
             ORDER BY ARTIST.NAME """)
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_song(UPDATEID,name,artist,album,genre,filepath):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE SONG SET NAME = '%s',
                                                ARTIST = '%s',
                                                ALBUM = '%s',
                                                GENRE = '%s',
                                                FILEPATH = '%s'
                                            WHERE ID = %d""" % (name,artist,album,genre,filepath,int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_all_song():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM SONG""")
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_song_album():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT  SONG.ID AS ID,
                                      SONG.NAME AS SONG,
                                      ARTIST.NAME AS ARTIST
                                FROM SONG INNER JOIN ARTIST
                                ON ARTIST = ARTIST.ID
                                ORDER BY ARTIST""")
            connection.commit()
            content = list(cursor)
            return content
        except dbapi2.DatabaseError as e:
            connection.rollback()







