import psycopg2 as dbapi2
from flask import request
from dao.song import *
from dsn_conf import get_dsn

dsn = get_dsn()

def insert_song(song):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """INSERT INTO SONG(NAME,ALBUM,ARTIST,GENRE,FILEPATH) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(song.name,song.album,song.artist,song.genre,song.filepath))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def delete_song(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM SONG WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_all_song2():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT SONG.ID,SONG.NAME,ARTIST.NAME FROM ARTIST,SONG WHERE(SONG.ARTIST = ARTIST.ID)
             ORDER BY ARTIST.NAME """)
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def update_song(UPDATEID,name,artist,album,genre,filepath):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""UPDATE SONG SET NAME = '%s',
                                                ARTIST = '%s',
                                                ALBUM = '%s',
                                                GENRE = '%s',
                                                FILEPATH = '%s'
                                            WHERE ID = %d""" % (name,artist,album,genre,filepath,int(UPDATEID)))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_all_song():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM SONG""")
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_songs_by_artist():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ARTIST.ID, ARTIST.NAME FROM ARTIST"""
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                query = """SELECT SONG.ID, SONG.NAME, SONG.FILEPATH FROM SONG
                            WHERE SONG.ARTIST = %s""" % (int(val[0]))
                cursor.execute(query)
                value2 = cursor.fetchall()
                songs = []
                name1 = val[1]
                artistname = name1.replace (" ", "_")
                for val in value2:
                    id = val[0]
                    songname = val[1]
                    filepath = val[2]
                    song = [id,songname,filepath]
                    songs.append(song)
                artist = (artistname,songs)
                content.append(artist)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_songs_by_album():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT ALBUM.ID, ALBUM.NAME FROM ALBUM"""
            cursor.execute(query)
            value = cursor.fetchall()
            for val in value:
                query = """SELECT SONG.ID, SONG.NAME, SONG.FILEPATH FROM SONG
                            WHERE SONG.ALBUM = %s""" % (int(val[0]))
                cursor.execute(query)
                value2 = cursor.fetchall()
                songs = []
                name1 = val[1]
                albumname = name1.replace (" ", "_")
                for val in value2:
                    id = val[0]
                    songname = val[1]
                    filepath = val[2]
                    song = [id,songname,filepath]
                    songs.append(song)
                album = (albumname,songs)
                content.append(album)
            return content
        except dbapi2.DatabaseError as e:
             connection.rollback()

def select_song_album():
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT  SONG.ID AS ID,
                                      SONG.NAME AS SONG,
                                      ARTIST.NAME AS ARTIST
                                FROM SONG INNER JOIN ARTIST
                                ON ARTIST = ARTIST.ID
                                ORDER BY ARTIST""")
            connection.commit()
            content = list(cursor)
            return content
        except dbapi2.DatabaseError as e:
            connection.rollback()

def select_song_name(id):
    content = []
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT  SONG.NAME  FROM SONG
                                WHERE SONG.ID = %s""" % (int(id)))
            connection.commit()
            content = list(cursor)
            a=content[0]
            return a[0]
        except dbapi2.DatabaseError as e:
            connection.rollback()

def insert_sample_songs():
    #name album artist genre filepath
    insert_song(Song('Fix You'                          ,19 ,1  ,2,'http://berkaygiris.com/itucsdb1628/songs/Coldplay/X&Y/FixYou.mp3'))
    insert_song(Song('Get Lucky'                        ,4  ,2  ,6,'http://berkaygiris.com/itucsdb1628/songs/Daft_Punk/Random_Access_Memories/GetLucky.mp3'))
    insert_song(Song('Lose Yourself To Dance'           ,4  ,2  ,6,'http://berkaygiris.com/itucsdb1628/songs/Daft_Punk/Random_Access_Memories/LoseYourselftoDance.mp3'))
    insert_song(Song('Hotline Bling'                    ,16 ,3  ,2,'http://berkaygiris.com/itucsdb1628/songs/Drake/Views/HotlineBling.mp3'))
    insert_song(Song('Lose Yourself'                    ,3  ,4  ,5,'http://berkaygiris.com/itucsdb1628/songs/Eminem/Curtain_Call/loseyourself.mp3'))
    insert_song(Song('Without Me'                       ,3  ,4  ,5,'http://berkaygiris.com/itucsdb1628/songs/Eminem/Curtain_Call/Withoutme.mp3'))
    insert_song(Song('A Place for my Head'              ,5  ,5  ,1,'http://berkaygiris.com/itucsdb1628/songs/Linkin_Park/Hybrid_Theory/aplaceformyhead.mp3'))
    insert_song(Song('Papercut'                         ,5  ,5  ,1,'http://berkaygiris.com/itucsdb1628/songs/Linkin_Park/Hybrid_Theory/papercut.mp3'))
    insert_song(Song('Bleed It Out'                     ,6  ,5  ,1,'http://berkaygiris.com/itucsdb1628/songs/Linkin_Park/Minutes_to_Midnight/bleeditout.mp3'))
    insert_song(Song('Given Up'                         ,6  ,5  ,1,'http://berkaygiris.com/itucsdb1628/songs/Linkin_Park/Minutes_to_Midnight/givenup.mp3'))
    insert_song(Song('What a Wonderful World'           ,17 ,6  ,4,'http://berkaygiris.com/itucsdb1628/songs/Louis_Armstrong/What_a_wonderful_world/whatawonderfulworld.mp3'))
    insert_song(Song('Detroit'                          ,11 ,7  ,4,'http://berkaygiris.com/itucsdb1628/songs/Marcus_Miller/Renaissance/detroit.mp3'))
    insert_song(Song('February'                         ,11 ,7  ,4,'http://berkaygiris.com/itucsdb1628/songs/Marcus_Miller/Renaissance/february.mp3'))
    insert_song(Song('Master of Puppets'                ,7  ,8  ,1,'http://berkaygiris.com/itucsdb1628/songs/Metallica/Master_of_Puppets/masterofpuppets.mp3'))
    insert_song(Song('Fuel'                             ,10 ,8  ,1,'http://berkaygiris.com/itucsdb1628/songs/Metallica/Reload/mtlc_fuel.mp3'))
    insert_song(Song('Come As You Are'                  ,8  ,9  ,1,'http://berkaygiris.com/itucsdb1628/songs/Nirvana/Nevermind/comeasyouare.mp3'))
    insert_song(Song('Smells Like Teen Spirit'          ,8  ,9  ,1,'http://berkaygiris.com/itucsdb1628/songs/Nirvana/Nevermind/smellsliketeenspirit.mp3'))
    insert_song(Song('Another Brick in the Wall'        ,14 ,10 ,1,'http://berkaygiris.com/itucsdb1628/songs/Pink_Floyd/The_wall/pinkfloyd_anotherbrick.mp3'))
    insert_song(Song('Comfortably Numb'                 ,14 ,10 ,1,'http://berkaygiris.com/itucsdb1628/songs/Pink_Floyd/The_wall/pinkfloyd_comfortably.mp3'))
    insert_song(Song('Wish You Were Here'               ,18 ,10 ,1,'http://berkaygiris.com/itucsdb1628/songs/Pink_Floyd/Wish_you_were_here/pinkfloyd_wishyouwerehere.mp3'))
    insert_song(Song('Scar Tissue'                      ,2  ,11 ,1,'http://berkaygiris.com/itucsdb1628/songs/Red_Hot_Chili_Peppers/Californication/rhcp_scartissue.mp3'))
    insert_song(Song('Dani California'                  ,13 ,11 ,1,'http://berkaygiris.com/itucsdb1628/songs/Red_Hot_Chili_Peppers/Stadium_Arcadium/danicalifornia.mp3'))
    insert_song(Song('Snow'                             ,13 ,11 ,1,'http://berkaygiris.com/itucsdb1628/songs/Red_Hot_Chili_Peppers/Stadium_Arcadium/rhcp_snow.mp3'))
    insert_song(Song('Dark Nescessities'                ,15 ,11 ,1,'http://berkaygiris.com/itucsdb1628/songs/Red_Hot_Chili_Peppers/The_Getaway/rhcp_darknescessities.mp3'))
    insert_song(Song('La Tortura'                       ,9  ,12 ,2,'http://berkaygiris.com/itucsdb1628/songs/Shakira/Oral_Fixation/latortura.mp3'))
    insert_song(Song('Scary Monsters and Nice Sprites'  ,12 ,13 ,6,'http://berkaygiris.com/itucsdb1628/songs/Skrillex/Scary_Monsters_And_Nice_Sprites/scarymonsters.mp3'))
    insert_song(Song('Four Seasons - Spring'            ,1  ,14 ,3,'http://berkaygiris.com/itucsdb1628/songs/Vivaldi/Best of Vivaldi/Fourseasonsspring.mp3'))
    insert_song(Song('Four Seasons - Winter'            ,1  ,14 ,3,'http://berkaygiris.com/itucsdb1628/songs/Vivaldi/Best of Vivaldi/FourseasonsWinter.mp3'))







