import psycopg2 as dbapi2
from flask import request
from flask_login import current_user, login_required, login_user, logout_user

from dsn_conf import get_dsn

dsn = get_dsn()

def select_posts(userid):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT POST.ID, POST.CONTENT, POST.SONGID, ALBUMCOVER.FILEPATH,USERDATA.USERNAME,
             POST.LIKECOUNTER AS NUMBER
             FROM POST,ALBUMCOVER,USERDATA
             WHERE(
             ALBUMCOVER.ID = POST.ALBUMCOVERID
             AND POST.USERID = USERDATA.ID
             AND POST.USERID = %s)
             ORDER BY POST.ID""" % userid
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
             query = """SELECT POST.ID, POST.CONTENT, POST.SONGID, ALBUMCOVER.FILEPATH,USERDATA.USERNAME, POST.ALBUMCOVERID
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
            userid = current_user.id
            songid = request.form['songid']
            query ="""INSERT INTO POST(CONTENT,USERID,SONGID,ALBUMCOVERID) VALUES(%s,%s,%s,%s)"""
            cursor.execute(query,(content,userid,songid,albumcover))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
