import psycopg2 as dbapi2
from flask import request

from dsn_conf import get_dsn
from dao.picture import *
dsn = get_dsn()

def insert_picture(picture):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO PICTURE (FILEPATH,TYPE)
                             VALUES (%s,%s)"""
            cursor.execute(statement,(picture.filepath,picture.type))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_artist_pics():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT PICTURE.ID, PICTURE.FILEPATH, PICTURE.TYPE
                       FROM PICTURE
                       ORDER BY ID"""
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                if val[2] == 1:
                    picture = [val[0],val[1],val[2]]
                    content.append(picture)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_album_pics():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT PICTURE.ID, PICTURE.FILEPATH, PICTURE.TYPE
                       FROM PICTURE
                       ORDER BY ID"""
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                if val[2] == 2:
                    picture = [val[0],val[1],val[2]]
                    content.append(picture)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()
def select_picture_id(filepath):
    content =[]
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT ID FROM PICTURE WHERE FILEPATH = '%s'""" % filepath)
            connection.commit()
            content = list(cursor)
            return content
        except dbapi2.DatabaseError as e:
            connection.rollback()


def delete_picture(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM PICTURE WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_picture(UPDATEID,newfilepath,newtype):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE PICTURE SET FILEPATH = '%s', TYPE = '%s' WHERE ID = %d""" % (newfilepath,newtype,int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
