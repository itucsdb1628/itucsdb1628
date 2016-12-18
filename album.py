import psycopg2 as dbapi2
from flask import request
from picture import *
from dsn_conf import get_dsn
from dao.album import *
dsn = get_dsn()

def insert_album():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            albumname = request.form['albumname']
            albumcover = int(request.form['albumcover'])
            albumdate = int(request.form['albumdate'])
            query ="""INSERT INTO ALBUM(NAME,ALBUMDATE,ALBUMCOVERID) VALUES(%s,%s,%s)"""
            cursor.execute(query,(albumname,albumdate,albumcover))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def insert_album2(album):
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            albumname = album.name
            albumcover = album.cover_filepath
            albumdate = album.albumdate
            query ="""INSERT INTO ALBUM(NAME,ALBUMDATE,ALBUMCOVERID) VALUES(%s,%s,%s)"""
            cursor.execute(query,(albumname,albumdate,albumcover))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_albums():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ALBUM.NAME, PICTURE.FILEPATH, ALBUM.ALBUMDATE, ALBUM.ID
                       FROM ALBUM INNER JOIN PICTURE ON ALBUM.ALBUMCOVERID = PICTURE.ID
                       ORDER BY ALBUM.ID"""
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                album = Album(val[0],val[1],val[2],val[3])
                content.append(album)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_albums_music():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ALBUM.NAME, PICTURE.FILEPATH, ALBUM.ALBUMDATE, ALBUM.ID
                       FROM ALBUM INNER JOIN PICTURE ON ALBUM.ALBUMCOVERID = PICTURE.ID
                       ORDER BY ALBUM.ID"""
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                album = Album(val[0],val[1],val[2],val[3])
                underscored = val[0].replace(" ", "_")
                content.append((album,underscored))
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()


def delete_album(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM ALBUM WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_album(UPDATEID,newname,newcover,newyear):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE ALBUM SET NAME = '%s', ALBUMDATE = '%s', ALBUMCOVERID = '%s' WHERE ID = %d""" % (newname,newyear,newcover[0],int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def insert_albumandpic(albm,pic,date):
    filename = pic
    insert_picture(Picture(filename,2))
    albumname = albm
    pictureid = select_picture_id(filename)
    newalbum = Album(albumname,pictureid[0],date)
    insert_album2(newalbum)

def insert_sample_albums():
    insert_albumandpic('Best of Vivaldi','http://berkaygiris.com/itucsdb1628/albums/bestofvivaldi.jpg',1991)
    insert_albumandpic('Californication','http://berkaygiris.com/itucsdb1628/albums/californication.jpg',1999)
    insert_albumandpic('Curtain Call','http://berkaygiris.com/itucsdb1628/albums/curtaincall.jpg',2005)
    insert_albumandpic('Random Access Memories','http://berkaygiris.com/itucsdb1628/albums/Random_Access_Memories.jpg',2013)
    insert_albumandpic('Hybrid Theory','http://berkaygiris.com/itucsdb1628/albums/hybridtheory.jpg',2000)
    insert_albumandpic('Minutes to Midnight','http://berkaygiris.com/itucsdb1628/albums/LP-MinutestoMidnight.jpg',2007)
    insert_albumandpic('Master of Puppets','http://berkaygiris.com/itucsdb1628/albums/masterofpuppets.jpg',1986)
    insert_albumandpic('Nevermind','http://berkaygiris.com/itucsdb1628/albums/nevermind.jpg',1991)
    insert_albumandpic('Oral Fixation','http://berkaygiris.com/itucsdb1628/albums/Oral%20Fixation.jpg',2006)
    insert_albumandpic('Reload','http://berkaygiris.com/itucsdb1628/albums/reload.jpg',1997)
    insert_albumandpic('Renaissance','http://berkaygiris.com/itucsdb1628/albums/Renaissance.jpg',2012)
    insert_albumandpic('Scary Monsters and Nice Sprites','http://berkaygiris.com/itucsdb1628/albums/scarymonstersandnicesprites.jpg',2010)
    insert_albumandpic('Stadium Arcadium','http://berkaygiris.com/itucsdb1628/albums/stadium-arcadium.jpg',2006)
    insert_albumandpic('The Wall','http://berkaygiris.com/itucsdb1628/albums/the-walll.jpg',1979)
    insert_albumandpic('The Getaway','http://berkaygiris.com/itucsdb1628/albums/thegetaway.jpg',2016)
    insert_albumandpic('Views','http://berkaygiris.com/itucsdb1628/albums/views.jpg',2016)
    insert_albumandpic('What a Wonderful World','http://berkaygiris.com/itucsdb1628/albums/whatawonderfulworld.jpg',1967)
    insert_albumandpic('Wish You Were Here','http://berkaygiris.com/itucsdb1628/albums/wishyouwerehere.jpg',1975)
    insert_albumandpic('X&Y','http://berkaygiris.com/itucsdb1628/albums/x&y.jpg',2005)





