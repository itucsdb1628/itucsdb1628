import psycopg2 as dbapi2
from flask import request
from picture import *
from dsn_conf import get_dsn
from dao.artist import *
dsn = get_dsn()

def insert_artist(artist):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO ARTIST(NAME,PICTUREID) VALUES(%s,%s)"""
            cursor.execute(statement,(artist.name,artist.pictureid))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_artist(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM ARTIST WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_artist(UPDATEID,newname):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE ARTIST SET NAME = '%s' WHERE ID = %d""" % (newname,int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_all_artist():
    content =[]
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT ARTIST.ID, ARTIST.NAME, PICTURE.FILEPATH
                       FROM ARTIST INNER JOIN PICTURE ON ARTIST.PICTUREID = PICTURE.ID
                       ORDER BY ARTIST.NAME""")
            connection.commit()
            content = list(cursor)
            return content
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_artists_music():
    content =[]
    content2= []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT ARTIST.ID, ARTIST.NAME, PICTURE.FILEPATH
                       FROM ARTIST INNER JOIN PICTURE ON ARTIST.PICTUREID = PICTURE.ID
                       ORDER BY ARTIST.NAME""")
            connection.commit()
            content = list(cursor)
            for val in content:
                val = val + (val[1].replace(" ", "_"),)
                content2.append(val)
            return content2
        except dbapi2.DatabaseError as e:
            connection.rollback()

def insert_artistandpic(artst,pic):
    filename = pic
    insert_picture(Picture(filename,1))
    artistname = artst
    pictureid = select_picture_id(filename)
    newartist = Artist(artistname,pictureid[0])
    insert_artist(newartist)

def insert_sample_artists():
    insert_artistandpic('Coldplay', 'http://berkaygiris.com/itucsdb1628/artists/coldplay.jpg')
    insert_artistandpic('Daft Punk', 'http://berkaygiris.com/itucsdb1628/artists/daftpunk.jpg')
    insert_artistandpic('Drake', 'http://berkaygiris.com/itucsdb1628/artists/drake.jpg')
    insert_artistandpic('Eminem', 'http://berkaygiris.com/itucsdb1628/artists/eminem.jpg')
    insert_artistandpic('Linkin Park', 'http://berkaygiris.com/itucsdb1628/artists/linkinpark.jpg')
    insert_artistandpic('Louis Armstrong', 'http://berkaygiris.com/itucsdb1628/artists/louisarmstrong.jpg')
    insert_artistandpic('Marcus Miller', 'http://berkaygiris.com/itucsdb1628/artists/marcusmiller.jpg')
    insert_artistandpic('Metallica','http://berkaygiris.com/itucsdb1628/artists/metallica.jpg')
    insert_artistandpic('Nirvana', 'http://berkaygiris.com/itucsdb1628/artists/nirvana.jpg')
    insert_artistandpic('Pink Floyd', 'http://berkaygiris.com/itucsdb1628/artists/pink_floyd.jpg')
    insert_artistandpic('Red Hot Chili Peppers', 'http://berkaygiris.com/itucsdb1628/artists/red_hot_chili_peppers.jpg')
    insert_artistandpic('Shakira', 'http://berkaygiris.com/itucsdb1628/artists/shakira.jpg')
    insert_artistandpic('Skrillex', 'http://berkaygiris.com/itucsdb1628/artists/skrillex.jpg')
    insert_artistandpic('Vivaldi', 'http://berkaygiris.com/itucsdb1628/artists/vivaldi.jpg')



