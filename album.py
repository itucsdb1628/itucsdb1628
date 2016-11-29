import psycopg2 as dbapi2
from flask import request

from dsn_conf import get_dsn
from dao.album import *
dsn = get_dsn()

def insert_album():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            albumname = request.form['albumname']
            albumcover = int(request.form['albumcover'])
            albumdate = int(request.form['albumdate'])
            query ="""INSERT INTO ALBUM(NAME,ALBUMDATE,ALBUMCOVERID) VALUES(%s,%s,%s)"""
            cursor.execute(query,(albumname,albumdate,albumcover))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_albums():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ALBUM.NAME, ALBUMCOVER.FILEPATH, ALBUM.ALBUMDATE, ALBUM.ID
                       FROM ALBUM INNER JOIN ALBUMCOVER ON ALBUM.ALBUMCOVERID = ALBUMCOVER.ID
                       ORDER BY ALBUM.ID"""
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                album = Album(val[0],val[1],val[2],val[3])
                content.append(album)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()


def delete_album(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM ALBUM WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_album(UPDATEID,newname,newcover,newyear):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE ALBUM SET NAME = '%s', ALBUMDATE = '%s', ALBUMCOVERID = '%s' WHERE ID = %d""" % (newname,newyear,newcover,int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
