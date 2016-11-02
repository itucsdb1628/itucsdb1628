import psycopg2 as dbapi2
from flask import request

from dsn_conf import get_dsn

dsn = get_dsn()

def insert_genre(genre):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO GENRE(NAME) VALUES(%s)"""
            cursor.execute(statement,(genre.name,))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_genre(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM GENRE WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_genre(UPDATEID,newname):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE GENRE SET NAME = '%s' WHERE ID = %d""" % (newname,int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_all_genre():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM GENRE""")
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()
