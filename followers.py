import psycopg2 as dbapi2
from flask import request
from dsn_conf import get_dsn
from dao.user import *

dsn = get_dsn()

def insert_follower(username,f_username):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO FOLLOWERS(USERNAME,FOLLOWER) VALUES(%s,%s)"""
            cursor.execute(query,(username,f_username))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def check_follower(username,f_username):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""SELECT USERNAME FROM FOLLOWERS WHERE (USERNAME = %s AND FOLLOWER = %s)"""
            cursor.execute(query,(username,f_username))
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_follower(name,f_name):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM FOLLOWERS WHERE (USERNAME = %s
             AND FOLLOWER = %s)"""
            cursor.execute(query,(name,f_name))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def number_of_followers(name):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COUNT(USERNAME) FROM FOLLOWERS WHERE (USERNAME = '%s')""" %(name)
            cursor.execute(query)
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def number_of_following(name):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COUNT(FOLLOWER) FROM FOLLOWERS WHERE (FOLLOWER = '%s')""" %(name)
            cursor.execute(query)
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def mutual_followup(name,fname):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """select areWeFollowing from (SELECT ff1.follower as followedBy,
                (
           select count(follower)
           from followers as ff2
               where ff2.username = ff1.follower
              and ff2.follower = ff1.username
            ) as areWeFollowing
            FROM followers as ff1
            where username = %s) where follower = %s"""
            cursor.execute(query,(name,fname))
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()



