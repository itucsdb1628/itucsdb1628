
=======================================
Parts Implemented by Salih Can Yurtkulu
=======================================


**In this project, COMMENT, ALBUM AND SHARE tables are implemented by me.**


.. contents:: Contents
   :local:


*************
Comment Table
*************

Comments kept in a table which has 7 columns:


* **Comment ID** -> **Primary Key**: Represents the id of every comment.
* **Comment**                  : It is a string value that represents comments.
* **Userid**     -> **Foreign Key**: This variable references **USERDATA** table
* **Postid**     -> **Foreign Key**: This variable references **POST** table
* **Avatarid**   -> **Foreign Key**: This variable references **AVATAR** table and it is used to reach the commenter's photo.
* **Albumcoverid** -> **Foreign Key**: This variable references **PICTURE** table and it is used to reach related post's content picture.
* **Cdate**                    : It is a timestamp value that represents when the comment was made.


Create Comment Table
====================


.. code-block:: sql

         CREATE TABLE IF NOT EXISTS COMMENT(
            ID SERIAL PRIMARY KEY,
            COMMENT VARCHAR(150) NOT NULL,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            POSTID INTEGER NOT NULL REFERENCES POST(ID) ON DELETE CASCADE,
            AVATARID INTEGER NOT NULL REFERENCES AVATAR(ID) ON DELETE CASCADE,
            ALBUMCOVERID INTEGER NOT NULL REFERENCES PICTURE(ID) ON DELETE CASCADE,
            CDATE TIMESTAMP
            )


* Comment table references several tables such as, userid, postid, avatarid and albumcoverid.


Select Comment
==============

**In this part, two different selection is implemented**


.. code-block:: python


        def select_comments(id):
         content = []
         with dbapi2.connect(dsn) as connection:
            try:
               cursor = connection.cursor()
               query = """SELECT COMMENT.COMMENT, USERDATA.USERNAME, AVATAR.FILEPATH, POST.CONTENT, POST.ID,
               COMMENT.ID FROM COMMENT INNER JOIN AVATAR on AVATAR.ID = COMMENT.AVATARID
               INNER JOIN USERDATA on COMMENT.USERID = USERDATA.ID
               INNER JOIN POST ON COMMENT.POSTID = POST.ID where (POST.ID = %s)
               ORDER BY COMMENT.ID"""

               cursor.execute(query,(id,))
               value = cursor.fetchall()
               for val in value:
                  comment = Comment(val[0],val[1],val[2],val[3],val[4],val[5])
                  content.append(comment)
               return content
            except dbapi2.DatabaseError as e:
                 connection.rollback()


* This select function takes postid as an argument and returns list of comment objects. This id shows which post's comments will be selected from database. Four tables are joined each other
  to select username, user's profile picture, post's content, comment and post's id from comment table. This select function is used for the comment page.


.. code-block:: python


         def select_comments2():
             content = []
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     query = """SELECT COMMENT.COMMENT, USERDATA.USERNAME, AVATAR.FILEPATH, POST.CONTENT, POST.ID, COMMENT.ID, PICTURE.FILEPATH,
                     SONG.NAME,ARTIST.NAME,POST.USERID FROM COMMENT INNER JOIN AVATAR on AVATAR.ID = COMMENT.AVATARID
                     INNER JOIN USERDATA on COMMENT.USERID = USERDATA.ID
                     INNER JOIN POST ON COMMENT.POSTID = POST.ID
                     INNER JOIN PICTURE ON COMMENT.ALBUMCOVERID = PICTURE.ID
                     INNER JOIN SONG ON POST.SONGID = SONG.ID
                     INNER JOIN ARTIST ON SONG.ARTIST = ARTIST.ID
                     WHERE(POST.USERID = %s)
                     ORDER BY COMMENT.ID""" %current_user.id
                     cursor.execute(query)
                     value = cursor.fetchall()
                     for val in value:
                         comment = Comment(val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8])
                         content.append(comment)
                     return content
                 except dbapi2.DatabaseError as e:
                      connection.rollback()


* This select function is used for the selecting comments, usernames, post's contents, user's profile pictures, album covers, song names and artist names
  from comment table for printing notifications on activities page.


Insert Comment
==============


.. code-block:: python

         def insert_comment(comment,userid,postid,avatarid,albumcoverid):
             with dbapi2.connect(dsn) as connection:
                 try:
                    cursor = connection.cursor()
                    query = """INSERT INTO COMMENT(COMMENT,USERID,POSTID,AVATARID,ALBUMCOVERID) VALUES(%s,%s,%s,%s,%s)"""
                    cursor.execute(query,(comment,userid,postid,avatarid,albumcoverid))
                    connection.commit()
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* **"Comment"** variable is taken from user, others taken as hidden inputs. These datas which are taken from user are inserted into comment table.


Delete Comment
==============


.. code-block:: python

         def delete_comment(DELETEID):
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     cursor.execute("""DELETE FROM COMMENT WHERE ID = %s""" , (int(DELETEID),))
                     connection.commit()
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* Takes comment id as a parameter and deletes the corresponding row from comment table. Comment id shows which comment will be deleted from comment table.


Update Comment
==============


.. code-block:: python


         def update_comment(comment,UPDATEID):
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     query = """UPDATE COMMENT SET COMMENT = '%s' WHERE ID = %d""" % (comment,int(UPDATEID))
                     cursor.execute(query)
                     connection.commit()
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* Takes new comment and comment's id to be updated as parameter and updates the comment.


Input Validations
=================

.. code-block:: python

         if request.form['comment']:
                   comment=request.form['comment']
                   postid=int(request.form['postid'])
                   userid=int(request.form['userid'])
                   avatarid=int(request.form['avatarid'])
                   albumcoverid=int(request.form['albumcover'])
                   insert_comment(comment,userid,postid,avatarid,albumcoverid)
                   return redirect("/comment/" + str(postid))
               else:
                   error = 'Comment can not be blank'
                   postid=int(request.form['postid'])
                   return render_template("comments.html", posts=list(select_post(COMMENTID)), comments=select_comments(COMMENTID), error=error)

* This function is added to handle validation. If inputs are not valid, it returns an error message and nothing is inserted into comment table.

.. code-block:: python

         if request.form['new_comment']:
                commentid=int(request.form['id'])
                postid=int(request.form['postid'])
                new_comment=request.form['new_comment']
                update_comment(new_comment,commentid)
                return redirect("/comment/" + str(postid))
            else:
                error = 'Comment can not be blank'
                postid=int(request.form['postid'])
                return render_template("comments.html", posts=list(select_post(COMMENTID)), comments=select_comments(COMMENTID), error=error)

* Same arrangements are made for the comment update operations.

Comment Class
=============

.. code-block:: python

         class Comment:
             def __init__(self, comment, username, avatarpath, content=None, postid = None ,commentid=None, albumcover=None, songname=None, artistname=None,cdate=None):
                 self.comment = comment
                 self.username = username
                 self.avatarpath = avatarpath
                 self.content = content
                 self.albumcover = albumcover
                 self.songname = songname
                 self.artistname = artistname
                 self.postid = postid
                 self.commentid=commentid
                 self.cdate = cdate

* **Comment** class to handle and process the information when it is necessary.




***********
Share Table
***********

Share table keeps reposted posts:


* **ID** -> **Primary Key**: Represents the id of every repost.
* **Reposterid**     -> **Foreign Key**: This variable references **USERDATA** table and it is used to reach username of reposter.
* **Postid**     -> **Foreign Key**: This variable references **POST** table and it is used to reach reposted post.
* **Sharedate**                    : It is a timestamp value that represents when the repost was made.


Create Share Table
==================


.. code-block:: sql

         CREATE TABLE IF NOT EXISTS SHARE(
            ID SERIAL PRIMARY KEY,
            POSTID INTEGER NOT NULL REFERENCES POST(ID) ON DELETE CASCADE,
            REPOSTERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            SHAREDATE TIMESTAMP
            )

* Share table references post and userdata tables.


Select Share
============


.. code-block:: python

         def select_sharedPost(reposterID):
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     query = """SELECT SHARE.ID,POST.CONTENT,SONG.NAME,ARTIST.NAME,PICTURE.FILEPATH,USERDATA.USERNAME,
                     POST.POSTDATE,SHARE.SHAREDATE FROM POST,PICTURE,USERDATA,SHARE,SONG,ARTIST
                     WHERE(
                     SHARE.POSTID = POST.ID
                     AND POST.SONGID = SONG.ID
                     AND SONG.ARTIST = ARTIST.ID
                     AND ARTIST.PICTUREID = PICTURE.ID
                     AND POST.USERID = USERDATA.ID
                     AND SHARE.REPOSTERID = %s)
                     ORDER BY SHARE.ID""" %reposterID
                     cursor.execute(query)
                     return cursor
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* This method takes reposter's id as a parameter and returns repost id, post content, song name in the post, artist name in the post, artist picture in the post,
  post-owner username, post sharing time, and post's repost time. It is used to show every user's reposts.

.. code-block:: python

         def select_sharedFor_activities(userID):
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     query = """SELECT POST.CONTENT,PICTURE.FILEPATH,USERDATA.USERNAME,SONG.NAME,ARTIST.NAME
                     FROM POST,USERDATA,SHARE,SONG,PICTURE,ARTIST
                     WHERE(
                     SHARE.POSTID = POST.ID
                     AND POST.SONGID = SONG.ID
                     AND SONG.ARTIST = ARTIST.ID
                     AND ARTIST.PICTUREID = PICTURE.ID
                     AND SHARE.REPOSTERID = USERDATA.ID
                     AND POST.USERID = %s)
                     ORDER BY SHARE.ID""" %userID
                     cursor.execute(query)
                     return cursor
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* This method takes current user's id as a parameter and returns post content, artist picture in the post, reposter username, song name in the post
  and artist name in the post. It is used to show which user has shared the current user's post.

Insert Share
============

.. code-block:: python

      def insert_sharedPost(postID):
          with dbapi2.connect(dsn) as connection:
              try:
                 cursor = connection.cursor()
                 query = """INSERT INTO SHARE(POSTID,REPOSTERID,SHAREDATE) VALUES(%s,%s,%s)"""
                 repostdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                 cursor.execute(query,(postID,current_user.id,repostdate))
                 connection.commit()
              except dbapi2.DatabaseError as e:
                  connection.rollback()

* Takes post id which is reposted by current user as parameter and inserts into share table.


Delete Share
============

.. code-block:: python

         def delete_sharedPost(repostID):
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     cursor.execute("""DELETE FROM SHARE WHERE ID = %s""", (int(repostID),))
                     connection.commit()
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* Takes repost id as parameter and deletes the corresponding row from table. Repost id shows which repost will be deleted.


***********
Album Table
***********

Albums kept in a table which has 4 columns:


* **ID** -> **Primary Key**: Represents the id of every album.
* **Name**                  : It is a string value that represents album's name.
* **Albumdate**    : It is an integer value that represents album's release year.
* **Albumcoverid**     -> **Foreign Key**: This variable references **PICTURE** table and it is used to reach album covers.


Create Album Table
==================


.. code-block:: sql

         CREATE TABLE IF NOT EXISTS ALBUM(
                  ID SERIAL PRIMARY KEY,
                  NAME VARCHAR(40) NOT NULL,
                  ALBUMDATE INTEGER,
                  ALBUMCOVERID INTEGER NOT NULL REFERENCES PICTURE(ID)
                  )

* Album table references picture table and album table is also referenced by song table.


Select Album
============

.. code-block:: python


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

* Returns a list of album objects.

Insert Album
============

.. code-block:: python


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

* Inserts the given album object which is taken as parameter into album table.


Delete Album
============

.. code-block:: python


         def delete_album(DELETEID):
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     cursor.execute("""DELETE FROM ALBUM WHERE ID = %s""", (int(DELETEID),))
                     connection.commit()
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* Takes album id as parameter and deletes the corresponding row from album table. Album id shows which album will be deleted.

Update Album
============

.. code-block:: python


         def update_album(UPDATEID,newname,newcover,newyear):
             with dbapi2.connect(dsn) as connection:
                 try:
                     cursor = connection.cursor()
                     cursor.execute("""UPDATE ALBUM SET NAME = '%s', ALBUMDATE = '%s', ALBUMCOVERID = '%s' WHERE ID = %d""" % (newname,newyear,newcover[0],int(UPDATEID)))
                     connection.commit()
                 except dbapi2.DatabaseError as e:
                     connection.rollback()

* Takes album id and to be updated informations as an argument and updates the corresponding row from album table. Album id shows which album will be updated.


Input Validations
=================

.. code-block:: python

         def validate_album_data(form):
             form.data = {}
             form.errors = {}

             if len(form['albumname'].strip()) == 0:
                 form.errors['albumname'] = 'Albumname can not be blank.'
             else:
                 form.data['albumname'] = form['albumname']

             if len(form['filepath'].strip()) == 0:
                 form.errors['filepath'] = 'URL can not be blank.'
             else:
                 form.data['filepath'] = form['filepath']

             if not form['albumdate']:
                 form.errors['albumdate'] = 'Year can not be blank'
             elif not form['albumdate'].isdigit():
                 form.errors['albumdate'] = 'Year must consist of digits only.'
             else:
                 albumdate = int(form['albumdate'])
                 if (albumdate < 1887) or (albumdate > 2017):
                     form.errors['albumdate'] = 'Year not in valid range.'
                 else:
                     form.data['albumdate'] = albumdate

             return len(form.errors) == 0

* This function is added to handle validation. If inputs are not valid, it returns an error message in front-end and nothing is inserted into album table.


.. code-block:: python

         def validate_UpdateAlbum_data(form):
             form.data1 = {}
             form.errors1 = {}

             if len(form['albumname'].strip()) == 0:
                 form.errors1['albumname'] = 'Albumname can not be blank.'
             else:
                 form.data1['albumname'] = form['albumname']

             if len(form['filepath'].strip()) == 0:
                 form.errors1['filepath'] = 'URL can not be blank.'
             else:
                 form.data1['filepath'] = form['filepath']

             if not form['albumdate']:
                 form.errors1['albumdate'] = 'Year can not be blank'
             elif not form['albumdate'].isdigit():
                 form.errors1['albumdate'] = 'Year must consist of digits only.'
             else:
                 albumdate = int(form['albumdate'])
                 if (albumdate < 1887) or (albumdate > 2017):
                     form.errors1['albumdate'] = 'Year not in valid range.'
                 else:
                     form.data1['albumdate'] = albumdate

             return len(form.errors1) == 0

* Same arrangements are made for the album update operations.


Album Class
===========

.. code-block:: python

         class Album:
             def __init__(self, name, cover_filepath, albumdate=None, albumid=None):
                 self.name = name
                 self.cover_filepath = cover_filepath
                 self.albumdate = albumdate
                 self.albumid = albumid

* **Album** class to handle and process the information when it is necessary.

