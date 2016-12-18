import psycopg2 as dbapi2
from flask import request
from dsn_conf import get_dsn
from flask import current_app
from flask_login import UserMixin
from dao.user import *

dsn = get_dsn()
class UserData(UserMixin):
    def __init__(self,id,username,password):
        self.id = id
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
            cursor.execute("""SELECT * FROM USERDATA WHERE USERNAME = %s""", (username,))
            values=cursor.fetchone()
            password=values[2]
            id = values[0]
            connection.commit()
            cursor.close()
            connection.close()
            user = UserData(id,username, password) if password else None
            return user
        except:
            pass


def select_a_user_from_login(userid):
    """Get Userdata by user_id"""
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ID,USERNAME,PASSWORD FROM USERDATA WHERE ID = %d""" %userid
            cursor.execute(query)
            connection.commit()
            res = cursor.fetchone()
            return None if res is None else UserData(res[0], res[1], res[2])
        except dbapi2.DatabaseError as e:
            connection.rollback()


def select_users_from_login():
    """" Get All Users """
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ID, USERNAME, PASSWORD FROM USERDATA"""
            cursor.execute(query)
            connection.commit()
            result = cursor.fetchall()
            users = []
            for res in result:
                users.append(UserData(res[0], res[1], res[2]))
            return users
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