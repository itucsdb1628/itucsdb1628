=================================
Parts Implemented by Berkay Giriş
=================================

.. rubric:: Developers Guide for Berkay Giriş's part.

.. contents:: Contents
   :local:

***************
Database Design
***************


Song Table
==========

                +---------------+------------+
                | Attribute     | Type       |
                +===============+============+
                |id             | INTEGER    |
                +---------------+------------+
                |name           | VARCHAR    |
                +---------------+------------+
                |artist         | INTEGER    |
                +---------------+------------+
                |album          | INTEGER    |
                +---------------+------------+
                |genre          | INTEGER    |
                +---------------+------------+
                |filepath       | VARCHAR    |
                +---------------+------------+

Create
------

.. code-block:: sql

   DROP TABLE IF EXISTS SONG
   CREATE TABLE IF NOT EXISTS SONG(
            ID          SERIAL PRIMARY KEY,
            NAME        VARCHAR(50)                             NOT NULL,
            ARTIST      INTEGER REFERENCES ARTIST(ID) ON DELETE CASCADE,
            ALBUM       INTEGER REFERENCES ALBUM(ID)  ON DELETE CASCADE,
            GENRE       INTEGER REFERENCES GENRE(ID)  ON DELETE SET NULL,
            FILEPATH    VARCHAR(200)                  UNIQUE    NOT NULL
            )


Insert
------

.. code-block:: sql

   INSERT INTO SONG
             (NAME, ALBUM, ARTIST, GENRE, FILEPATH)
       VALUES(%s,   %s,    %s,     %s,    %s)

Update
------

.. warning:: All values will be changed.

.. code-block:: sql

   UPDATE SONG SET NAME = '%s',
                   ARTIST = '%s',
                   ALBUM = '%s',
                   GENRE = '%s',
                   FILEPATH = '%s'
               WHERE ID = %d


Select
------

* Function to select all songs

.. code-block:: python

   def select_all_song():

* Function to select songs by artists

.. code-block:: python

   def select_songs_by_artist():

* Function to select songs by albums

.. code-block:: python

   def select_songs_by_album():

* Function to select songs with their artist names

.. code-block:: python

   def select_song_album():

* Function to find a song with given id

.. code-block:: python

   def select_song_name(id):

Delete
------
* Function that deletes a song with given id

.. code-block:: python

   def delete_song(DELETEID):


Artist Table
============
                +---------------+------------+
                | Attribute     | Type       |
                +===============+============+
                |id             | INTEGER    |
                +---------------+------------+
                |pictureid      | INTEGER    |
                +---------------+------------+
                |name           | VARCHAR    |
                +---------------+------------+

Create
------
.. code-block:: sql

   DROP TABLE IF EXISTS ARTIST
   CREATE TABLE IF NOT EXISTS ARTIST(
            ID          SERIAL PRIMARY KEY,
            PICTUREID   INTEGER     REFERENCES PICTURE(ID) ON DELETE SET NULL,
            NAME        VARCHAR(64)                            UNIQUE NOT NULL
            )

Insert
------
* Function to select add an artist with its picture

.. code-block:: python

   def insert_artistandpic(artst,pic):

.. code-block:: sql

   INSERT INTO ARTIST
                     (NAME, PICTUREID)
             VALUES  (%s,   %s)


Select
------
* Function to select all artists with their pictures

.. code-block:: python

   def select_all_artist():

* Function to select artists for music page

This function is created for the need of unique div tags

.. code-block:: python

   def select_artists_music():

Delete
------
* Function that deletes an artist with given id

.. code-block:: python

   def delete_artist(DELETEID):


Genre Table
===========
                +---------------+------------+
                | Attribute     | Type       |
                +===============+============+
                |id             | INTEGER    |
                +---------------+------------+
                |name           | VARCHAR    |
                +---------------+------------+

Create
------
.. code-block:: sql

   DROP TABLE IF EXISTS GENRE
   CREATE TABLE IF NOT EXISTS GENRE(
            ID    SERIAL PRIMARY KEY,
            NAME  VARCHAR(20)    UNIQUE NOT NULL
            )

Insert
------
.. code-block:: sql

   INSERT INTO GENRE(NAME) VALUES(%s)

Update
------
.. code-block:: sql

   UPDATE GENRE SET NAME = '%s'
                WHERE ID = %d

Select
------
* Function that selects all genres

.. code-block:: python

   def select_all_genre():

Delete
------
* Function that deletes an artist with given id

.. code-block:: python

   def delete_genre(DELETEID):


Picture Table
=============
                +---------------+------------+
                | Attribute     | Type       |
                +===============+============+
                |id             | INTEGER    |
                +---------------+------------+
                |type           | INTEGER    |
                +---------------+------------+
                |filepath       | VARCHAR    |
                +---------------+------------+

Create
------
.. code-block:: sql

   DROP TABLE IF EXISTS PICTURE
   CREATE TABLE IF NOT EXISTS PICTURE(
                ID         SERIAL PRIMARY KEY,
                TYPE       INTEGER           NOT NULL,
                FILEPATH   VARCHAR(200)      NOT NULL
                )



Insert
------
.. code-block:: sql

   INSERT INTO PICTURE
                  (FILEPATH, TYPE)
          VALUES  (%s,       %s)

Update
------
.. code-block:: sql

   UPDATE PICTURE SET FILEPATH = '%s',
                  TYPE = '%s'
             WHERE ID = %d

Select
------
* Function that returns picture id of the given URL

.. code-block:: python

   def select_picture_id(filepath):


Delete
------
* Function that deletes picture with given id

.. code-block:: python

   def delete_picture(DELETEID):


