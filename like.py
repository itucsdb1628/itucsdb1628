import psycopg2 as dbapi2
from flask import request
from post import *
from dsn_conf import get_dsn

dsn = get_dsn()

def delete_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM LIKES WHERE (USERID = %s
             AND POSTID = %s)"""
            cursor.execute(query,(userId,postId))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
        try:
            cursor = connection.cursor()
            query = """UPDATE POST SET LIKECOUNTER = LIKECOUNTER - 1 WHERE (ID = %d)""" % (int(postId),)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()


def insert_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO LIKES(POSTID,USERID,LIKEDATE) VALUES(%s,%s,%s)"""
            cursor.execute(query,(postId,userId,'10.11.2014'))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
        try:
            cursor = connection.cursor()
            query = """UPDATE POST SET LIKECOUNTER = LIKECOUNTER + 1 WHERE ID = %d""" % (int(postId),)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
        
def select_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT * FROM LIKES WHERE POSTID = %s
             AND USERID = %s """
             cursor.execute(query,(postId,userId))
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()
             
def select_user_likes(userId):
       with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT POSTID,LIKEDATE FROM LIKES 
             WHERE USERID = %s 
             ORDER BY POSTID"""
             cursor.execute(query,(userId,))
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()
             
def select_like_number(userId):
     with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT COUNT(*) FROM LIKES WHERE
             AND USERID = %s 
             GROUP BY POSTID,USERID ORDER BY POSTID"""
             cursor.execute(query,(userId,))
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()
             
def control_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        cursor = select_like(userId,postId)
        control = cursor.fetchone()
    
        if control is None:
            return True
        else: 
            return False