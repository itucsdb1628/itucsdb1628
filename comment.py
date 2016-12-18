import psycopg2 as dbapi2
from flask import request
from dao.comment import *

from dsn_conf import get_dsn
from flask_login.utils import current_user

dsn = get_dsn()

def select_comments(id):
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COMMENT.COMMENT, USERDATA.USERNAME, AVATAR.FILEPATH, POST.CONTENT, POST.ID,
            COMMENT.ID FROM COMMENT INNER JOIN AVATAR on AVATAR.ID = COMMENT.AVATARID
            INNER JOIN USERDATA on COMMENT.USERID = USERDATA.ID
            INNER JOIN POST ON COMMENT.POSTID = POST.ID where (POST.ID = %s)
            ORDER BY COMMENT.ID"""

            cursor.execute(query,(id,))
            value = cursor.fetchall()
            for val in value:
                comment = Comment(val[0],val[1],val[2],val[3],val[4],val[5])
                content.append(comment)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_comments2():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COMMENT.COMMENT, USERDATA.USERNAME, AVATAR.FILEPATH, POST.CONTENT, POST.ID, COMMENT.ID, PICTURE.FILEPATH,
            POST.USERID FROM COMMENT INNER JOIN AVATAR on AVATAR.ID = COMMENT.AVATARID
            INNER JOIN USERDATA on COMMENT.USERID = USERDATA.ID
            INNER JOIN POST ON COMMENT.POSTID = POST.ID
            INNER JOIN PICTURE ON COMMENT.ALBUMCOVERID = PICTURE.ID
            WHERE(POST.USERID = %s)
            ORDER BY COMMENT.ID""" %current_user.id
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                comment = Comment(val[0],val[1],val[2],val[3],val[4],val[5],val[6])
                content.append(comment)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()


def select_comment_number(postid):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COUNT(*) FROM COMMENT WHERE POSTID = %s """ % postid
            cursor.execute(query)
            return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()


def insert_comment(comment,userid,postid,avatarid,albumcoverid):
    with dbapi2.connect(dsn) as connection:
        try:
           cursor = connection.cursor()
           query = """INSERT INTO COMMENT(COMMENT,USERID,POSTID,AVATARID,ALBUMCOVERID) VALUES(%s,%s,%s,%s,%s)"""
           cursor.execute(query,(comment,userid,postid,avatarid,albumcoverid))
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

def update_comment(comment,UPDATEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE COMMENT SET COMMENT = '%s' WHERE ID = %d""" % (comment,int(UPDATEID))
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()



