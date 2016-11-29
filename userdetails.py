import psycopg2 as dbapi2
from flask import request
from dsn_conf import get_dsn
from dao.user import *

dsn = get_dsn()


def delete_userdetails(name,surname):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM USERDETAILS WHERE (NAME = %s
             AND SURNAME = %s)"""
            cursor.execute(query,(name,surname))
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
             query = """SELECT * FROM USERDETAILS INNER JOIN USERDATA on USERDATA.ID = USERDETAILS.USERID
             WHERE USERNAME = %s """ %(username)
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


def update_userdetails(older_name,name,userid,surname,email,phonenumber):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """UPDATE USERDETAILS SET USERID = '%s', NAME = '%s', SURNAME = '%s', EMAIL = '%s', PHONENUMBER = '%s' WHERE NAME = '%s' """%(userid,name,surname,email,phonenumber,older_name)
             cursor.execute(query)
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()



