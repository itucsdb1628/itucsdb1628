import psycopg2 as dbapi2
from flask import request
from dsn_conf import get_dsn
from flask import current_app
from flask_login import UserMixin
from dao.user import *

dsn = get_dsn()
class UserData(UserMixin):
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.active = True
    
    def get_id(self):
        return self.username
    
    
    @property
    def is_active(self):
        return self.active
        
def get_user(username):
    with dbapi2.connect(dsn) as connection:
        try:
            connection = dbapi2.connect(current_app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""SELECT PASSWORD FROM USERDATA WHERE USERNAME = %s""", (username,))
            values=cursor.fetchone()
            password=values[0]
            connection.commit()
            cursor.close()
            connection.close()
            user = UserData(username, password) if password else None
            return user
        except:
            pass
                  
    
def get_idofuser(username):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT ID FROM USERDATA WHERE USERNAME = %s""", (username,))
            values=cursor.fetchone()
            print(values)
            userid=values[0]
            print(userid)
            return userid
                  
def select_a_user_from_login(userid):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ID,USERNAME,PASSWORD FROM USERDATA WHERE USER.ID = %d""" %userid
            cursor.execute(query)
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

    def select_users_from_login():
        with dbapi2.connect(dsn) as connection:
            try:
                cursor = connection.cursor()
                query = """SELECT ID, USERNAME, PASSWORD FROM USERDATA"""
                cursor.execute(query)
                return cursor
            except dbapi2.DatabaseError as e:
                connection.rollback()

def delete_user_login(username,password):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM USERDATA WHERE USERNAME = '%s' AND PASSWORD = '%s'""" %(username,password)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
    
def update_user_login(new_username,new_password,username):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE USERDATA SET USERNAME = '%s' , PASSWORD = '%s' WHERE USERNAME = '%s'""" %(new_username,new_password,username)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
    
def insert_user_login(username,password):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO USERDATA(USERNAME,PASSWORD) VALUES(%s,%s)"""
            cursor.execute(query,(username,password))
            return connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()