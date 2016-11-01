import psycopg2 as dbapi2
from flask import request

from dsn_conf import get_dsn

dsn = get_dsn()

def select_posts():
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT POST.ID, POST.CONTENT, POST.SONGID, ALBUMCOVER.FILEPATH,USERDATA.USERNAME
             FROM POST INNER JOIN ALBUMCOVER on ALBUMCOVER.ID = POST.ALBUMCOVERID
             INNER JOIN USERDATA on POST.USERID = USERDATA.ID"""
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
             query = """SELECT POST.ID, POST.CONTENT, POST.SONGID, ALBUMCOVER.FILEPATH,USERDATA.USERNAME
             FROM POST INNER JOIN ALBUMCOVER on ALBUMCOVER.ID = POST.ALBUMCOVERID
             INNER JOIN USERDATA on USERDATA.ID=POST.USERID WHERE POST.ID = %s  """ %UPDATEID
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
            albumcover = request.form['albumcover']
            userid = request.form['userid']
            songid = request.form['songid']
            query ="""INSERT INTO POST(CONTENT,USERID,SONGID,ALBUMCOVERID) VALUES(%s,%s,%s,%s)"""
            cursor.execute(query,(content,userid,songid,albumcover))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
