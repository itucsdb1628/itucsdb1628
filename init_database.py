import psycopg2 as dbapi2

from dao import *


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