import psycopg2 as dbapi2
from flask import request
from dsn_conf import get_dsn
from dao.user import *
from flask_login import current_user, login_required, login_user, logout_user
dsn = get_dsn()


def delete_userdetails():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM USERDETAILS WHERE (USERID = %s)""" %(current_user.id)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def insert_userdetails(userdetails):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO USERDETAILS(USERID,NAME,SURNAME,EMAIL,PHONENUMBER) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(query,(userdetails.userid,userdetails.name,userdetails.surname,userdetails.email,userdetails.phonenumber))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_an_user_userdetails(username):
       with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT * FROM USERDETAILS INNER JOIN USERDATA on USERDATA.ID = USERDETAILS.USERID WHERE USERNAME = '%s' """ %(username)
             cursor.execute(query)
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_userdetails():
       with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT USERNAME, PASSWORD, USERID, NAME, SURNAME, EMAIL, PHONENUMBER FROM USERDETAILS INNER JOIN USERDATA on USERDATA.ID = USERDETAILS.USERID"""
             cursor.execute(query)
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()


def update_myuserdetail(name,surname,email,phonenumber):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """UPDATE USERDETAILS SET  NAME = '%s', SURNAME = '%s', EMAIL = '%s', PHONENUMBER = '%s' WHERE USERID = '%s' """%(name,surname,email,phonenumber,current_user.id)
             cursor.execute(query)
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()


