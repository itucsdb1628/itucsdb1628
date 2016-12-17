import psycopg2 as dbapi2
from flask import request
from flask_login import current_user, login_required, login_user, logout_user
from datetime import date
from dsn_conf import get_dsn

dsn = get_dsn()

def select_suggestions():
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT SUGGESTION.ID,USERDATA.USERNAME, 
             SUGGESTION.ARTIST, SUGGESTION.SONGNAME,SUGGESTION.RELEASEDATE,SUGGESTION.SUGGESTIONDATE,
             SUGGESTION.STATU
             FROM SUGGESTION,USERDATA 
             WHERE(
             USERDATA.ID = SUGGESTION.USERID) 
             ORDER BY SUGGESTION.STATU DESC"""
             cursor.execute(query)
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()
 
def select_suggestions_user():
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT ID,ARTIST,SONGNAME,RELEASEDATE,SUGGESTIONDATE,STATU
             FROM SUGGESTION
             WHERE(
            SUGGESTION.USERID = %s
                ) 
             ORDER BY SUGGESTION.SUGGESTIONDATE""" % current_user.id
             cursor.execute(query)
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()  

def insert_suggestion(userid,artist,songname,releasedate):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """INSERT INTO SUGGESTION(USERID,ARTIST,SONGNAME,SUGGESTIONDATE,RELEASEDATE,STATU)
                            VALUES(%s,%s,%s,%s,%s,%s)"""
            myTime = date.today()
            cursor.execute(query,(userid,artist,songname,date.today(),releasedate,2))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
            
            
def delete_suggestion(deleteId):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM SUGGESTION WHERE ID = %s""", (int(deleteId),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
            
def reject_suggestion(updateId):
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE SUGGESTION SET STATU = 0 WHERE ID = %s"""
            cursor.execute(query, (updateId,))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
            
def approve_suggestion(updateId):
      with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE SUGGESTION SET STATU = 1 WHERE ID = %s"""
            cursor.execute(query, (updateId,))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
            