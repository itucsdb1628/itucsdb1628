import psycopg2 as dbapi2
from flask import request

from dsn_conf import get_dsn

dsn = get_dsn()

def select_comments():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COMMENT.ID, COMMENT.COMMENT, COMMENT.CDATE, AVATAR.FILEPATH, USERDATA.USERNAME, POST.ID
            FROM COMMENT INNER JOIN AVATAR ON AVATAR.ID = COMMENT.AVATARID
            INNER JOIN USERDATA ON COMMENT.USERID = USERDATA.ID
            INNER JOIN POST ON POST.ID = COMMENT.POSTID """
            cursor.execute(query)
            return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()


def insert_comment(comment, avatar, postid, userid):
    with dbapi2.connect(dsn) as connection:
        try:
           cursor = connection.cursor()
           query = """INSERT INTO COMMENT(COMMENT,USERID,POSTID,AVATARID) VALUES(%s,%s,%s,%s)"""
           cursor.execute(query,(comment, userid, postid, avatar))
           connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_comment(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM COMMENT WHERE ID = %s""" , (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_comment(UPDATEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            comment = request.form['comment']
            query = """UPDATE COMMENT SET COMMENT = '%s' WHERE ID = %d""" % (comment,int(UPDATEID))
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()


