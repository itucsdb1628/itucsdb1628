===================================
Parts Implemented by İsmail Pamir
===================================


.. rubric:: Developer Guide for Post, Like and Suggestion

.. contents:: Contents
   :local:

*****************************
General View of Entities
*****************************
I implemented 3 entities given below and their operations in this project.


**Entities:**
 Post - Like - Suggestion

* **Post:** A table created to hold songs shared by users.
* **Like:** A table created to hold liked posts by users.
* **Suggestion:** A table created to hold song suggestions for adding to the website.



*************
POST
*************

Initialization of table
===========================

.. code-block:: python
   
   def create_post_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS POST(
            ID SERIAL PRIMARY KEY,
            CONTENT VARCHAR(100) NOT NULL,
            POSTDATE TIMESTAMP,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            SONGID INTEGER NOT NULL REFERENCES SONG(ID) ON DELETE CASCADE,
            LIKECOUNTER INT DEFAULT 0
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()
   
* Post table has following columns as you can see above.
* **ID:**  It is a serial and primary key for this table.
* **CONTENT:** The attribute created to hold the user's idea about own post.
* **POSTDATE:** The attribute created to hold send date of post.
* **USERID:** It is a foreign key. It references id of **USERDATA**. The attribute that holds the post to whom it belongs.
			  I added **ON DELETE CASCADE** so i provided if the user is deleted, posts belong to this user are deleted too.
* **SONGID:** It is a foreign key. It references id of **SONG**. The attribute that holds what song is shared in the post.
			  I added **ON DELETE CASCADE** so i provided if the song is deleted, posts reference this song are deleted too.	


Selection
==========

Selection for Timeline Page
-------------------------------

.. code-block:: python
   
	def select_posts(userid):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT SONG.FILEPATH AS SONGFILEPATH,
             POST.ID, POST.CONTENT, POST.POSTDATE ,
             SONG.NAME,ARTIST.NAME, PICTURE.FILEPATH,
             POST.LIKECOUNTER AS NUMBER,USERDATA.USERNAME
             FROM POST,SONG,ARTIST,USERDATA,PICTURE
             WHERE(
             POST.SONGID = SONG.ID
             AND SONG.ARTIST = ARTIST.ID
             AND PICTURE.ID = ARTIST.PICTUREID
             AND POST.USERID = USERDATA.ID
             AND POST.USERID = %s)
             ORDER BY POST.POSTDATE DESC""" % userid
             cursor.execute(query)
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()
             
* This function gets the user id as an argument. This user id shows which user's posts will be selected from the database.
  All posts of this user are selected from the database. Five tables are joined each others by this select query.
  Because the name of the user, name of artist, picture of artist, file path of song, name of song are necessary for timeline.
  Picture of artist is hold by picture table so we joined picture table. Path of song, song name are hold by song table so
  we joined song table. Artist name is hold by artist table so we joined artist table. User name is hold by userdata table 
  so we joined userdata table.  



             
Selection for Update Page
------------------------------	

.. code-block:: python
   
    def select_post(UPDATEID):
	    with dbapi2.connect(dsn) as connection:
	        try:
	             cursor = connection.cursor()
	             query = """SELECT POST.ID, POST.CONTENT,
	             POST.POSTDATE, SONG.NAME,ARTIST.NAME, 
	             PICTURE.FILEPATH,PICTURE.ID,
	             USERDATA.USERNAME
	             FROM POST,ARTIST,USERDATA,PICTURE,SONG WHERE
	             POST.SONGID = SONG.ID
	             AND SONG.ARTIST = ARTIST.ID
	             AND PICTURE.ID = ARTIST.PICTUREID
	             AND POST.USERID = USERDATA.ID
	             AND POST.ID = %s  """ %UPDATEID
	             cursor.execute(query)
	             connection.commit()
	             return cursor
	        except dbapi2.DatabaseError as e:
	             connection.rollback()

* This function gets the post id as an argument. This post id shows which post will be selected from the database. 
  It returns the post variables to be updated. 


Insertion
==========
.. code-block:: python
   
	def insert_post_page():
	    with dbapi2.connect(dsn) as connection:
	        try:
	            cursor = connection.cursor()
	            content = request.form['content']
	            songid = request.form['songid']
	            userid = current_user.id
	            postdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	            query ="""INSERT INTO POST(CONTENT,USERID,SONGID,POSTDATE) VALUES(%s,%s,%s,%s)"""
	            cursor.execute(query,(content,userid,songid,postdate))
	            connection.commit()
	        except dbapi2.DatabaseError as e:
	            connection.rollback()

* The content,songid which is taken from user thanks to form is assigned to the content and songid of post to be inserted.
  Posting date is taken with "datetime.datetime.now()" when the this function works. Also user id is taken as current user id, because
  only the user who has logged in can send a post. A new row is added to post table by sending these values to the query. 
  
Updation
=========
.. code-block:: python

   def update_post(UPDATEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            content = request.form['content']
            query = """UPDATE POST SET CONTENT = '%s' WHERE ID = %d""" % (content,int(UPDATEID))
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* This function gets the post id as an argument. This post id shows which post will be updated. The new text which is taken from
  user thanks to form is assigned to the content of post to be updated. 
  
Deletion
==========
.. code-block:: python
   
   def delete_post(DELETEID):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM POST WHERE ID = %s""", (int(DELETEID),))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* This function gets the post id as an argument. This post id shows which post will be deleted.

*************
SUGGESTION
*************


Initialization of table
===========================

.. code-block:: python
  
   def create_suggestion_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement =     """CREATE TABLE IF NOT EXISTS SUGGESTION(
            ID SERIAL PRIMARY KEY,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            ARTIST VARCHAR(50) NOT NULL,
            SONGNAME VARCHAR(50) NOT NULL,
            SUGGESTIONDATE DATE,
            RELEASEDATE DATE,
            STATU INT
            CHECK (STATU > -1 AND STATU < 3)
            )"""
            cursor.execute(statement)
            statement = """INSERT INTO SUGGESTION(USERID,ARTIST,SONGNAME,SUGGESTIONDATE,RELEASEDATE,STATU)
                            VALUES(%s,%s,%s,%s,%s,%s)"""
            cursor.execute(statement,(1,"Metallica","Nothing else matters",'1.10.2016','1.10.2016',2));
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()
            
* Suggestion table has following columns as you can see above.
* **ID:** It is a serial and primary key  for this table.
* **USERID:** It is a foreign key. It references id of **USERDATA**. The attribute that holds the which user makes this suggestion.
		      I added **ON DELETE CASCADE** so i provided if the user is deleted, suggestions belongs to this user are deleted too.
* **ARTIST:** The attribute created to hold name of artist who the song belongs to.
* **SONGNAME:** The attribute created to hold name of song.
* **SUGGESTIONDATE:**  The attribute created to hold send date of suggestion.
* **RELEASEDATE:** The attribute created to hold information of when the song was released.
* **STATU:** The attribute created to hold status of suggestion.
			* It is checked whether it is between 1 and 3 or not. Because there are three types status.
			* Two represents Status **Waiting**.
			* One represents Status **Approved**. 
			* Zero represents Status **Denied**.
			
			
Selection
===============

Selection for Admin
--------------------------
.. code-block:: python
   
   def select_suggestions():
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT SUGGESTION.ID,USERDATA.USERNAME, 
             SUGGESTION.ARTIST, SUGGESTION.SONGNAME,SUGGESTION.RELEASEDATE,SUGGESTION.SUGGESTIONDATE,
             SUGGESTION.STATU
             FROM SUGGESTION,USERDATA 
             WHERE(
             USERDATA.ID = SUGGESTION.USERID) 
             ORDER BY SUGGESTION.STATU DESC"""
             cursor.execute(query)
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()
            
* This function selects all suggestions in the database for admin perspective. These selected suggestions is used 
  for approval and rejection of pop-up screen in admin perspective. User and suggestion tables are joined each others by this select query. 
  Because name of user is needed too.


Selection for Regular User
----------------------------
.. code-block:: python
   
   def select_suggestions_user():
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT ID,ARTIST,SONGNAME,RELEASEDATE,SUGGESTIONDATE,STATU
             FROM SUGGESTION
             WHERE(
            SUGGESTION.USERID = %s
                ) 
             ORDER BY SUGGESTION.SUGGESTIONDATE""" % current_user.id
             cursor.execute(query)
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()  
          
* This function selects only suggestions of current user. This select query uses only suggestion table because it does not need any
  attribute from other tables. These selected suggestions is used for viewing own suggestion of current user.


Insertion
=============

.. code-block:: python
   
   def insert_suggestion(userid,artist,songname,releasedate):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """INSERT INTO SUGGESTION(USERID,ARTIST,SONGNAME,SUGGESTIONDATE,RELEASEDATE,STATU)
                            VALUES(%s,%s,%s,%s,%s,%s)"""
            myTime = date.today()
            cursor.execute(query,(userid,artist,songname,date.today(),releasedate,2))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* This function takes user id, artist, song name and release date as argument. This data is provided from user thanks to 
  form expect user id. User id data is user id of current user. Because only current user can suggest a song. The user 
  must be logged in before the user can suggest a song. This data which is taken from the user is assigned the values of suggestion
  to be inserted and the query is executed. 


Updation
=============

Reject Suggestion 
------------------
.. code-block:: python
   
	def reject_suggestion(updateId):
    	 with dbapi2.connect(dsn) as connection:
        	try:
            	cursor = connection.cursor()
            	query = """UPDATE SUGGESTION SET STATU = 0 WHERE ID = %s"""
            	cursor.execute(query, (updateId,))
            	connection.commit()
        	except dbapi2.DatabaseError as e:
            	connection.rollback()

* This function takes suggestion id as argument. This id is id of suggestion to be rejected. This query makes zero the status
  value of desired suggestion. Because zero statu value means "rejected". 
  
  
Approve Suggestion
--------------------

.. code-block:: python
   
	def approve_suggestion(updateId):
	      with dbapi2.connect(dsn) as connection:
	        try:
	            cursor = connection.cursor()
	            query = """UPDATE SUGGESTION SET STATU = 1 WHERE ID = %s"""
	            cursor.execute(query, (updateId,))
	            connection.commit()
	        except dbapi2.DatabaseError as e:
	            connection.rollback()

* This function takes suggestion id as argument. This id is id of suggestion to be approved. This query makes one the status
  value of desired suggestion. Because one statu value means "approved". 

Deletion
=============			


.. code-block:: python
   
	def delete_suggestion(deleteId):
	    with dbapi2.connect(dsn) as connection:
	        try:
	            cursor = connection.cursor()
	            cursor.execute("""DELETE FROM SUGGESTION WHERE ID = %s""", (int(deleteId),))
	            connection.commit()
	        except dbapi2.DatabaseError as e:
	            connection.rollback()
	       
* This function takes suggestion id as argument. This query deletes one row from suggestion table. This row is specified
  by suggestion id.


********
LIKE
********


Initialization of table
===========================

.. code-block:: python 
   
   def create_like_table():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement =     """CREATE TABLE IF NOT EXISTS LIKES(
            ID SERIAL PRIMARY KEY,
            POSTID INTEGER NOT NULL REFERENCES POST(ID) ON DELETE CASCADE,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            LIKEDATE TIMESTAMP
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Like table has following columns as you can see above.
* **ID:** It is a serial and primary key  for this table.
* **POSTID:** It is a foreign key. It references id of **POST**. The attribute that holds the user likes which post.
			  I added **ON DELETE CASCADE** so i provided if the post is deleted, likes belong to this post are deleted too.	
* **USERID:** It is a foreign key. It references id of **USERDATA**. The attribute that holds the which user likes this post.
			  I added **ON DELETE CASCADE** so i provided if the user is deleted, likes belong to this user are deleted too.
* **LIKEDATE:** The attribute created to hold liked date of post


Selection
=============
.. code-block:: python 
   
	def select_user_likes(userId):
	       with dbapi2.connect(dsn) as connection:
	        try:
	             cursor = connection.cursor()
	             query = """SELECT POSTID,LIKEDATE FROM LIKES
	             WHERE USERID = %s
	             ORDER BY POSTID"""
	             cursor.execute(query,(userId,))
	             connection.commit()
	             return cursor
	        except dbapi2.DatabaseError as e:
	             connection.rollback()
	             
* This function takes user id as argument. It selects likes of desired user for controlling. 

Insertion
============

.. code-block:: python 
   
   def insert_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO LIKES(POSTID,USERID,LIKEDATE) VALUES(%s,%s,%s)"""
            cursor.execute(query,(postId,userId,datetime.datetime.now()))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
        try:
            cursor = connection.cursor()
            query = """UPDATE POST SET LIKECOUNTER = LIKECOUNTER + 1 WHERE ID = %d""" % (int(postId),)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
   
* This function takes user id and post id as argument and it inserts row with these values. At last, it incereases by one
  the like counter of post. 
   
Deletion
===========

.. code-block:: python 
   
   
   def delete_like(userId,postId):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM LIKES WHERE (USERID = %s
             AND POSTID = %s)"""
            cursor.execute(query,(userId,postId))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
        try:
            cursor = connection.cursor()
            query = """UPDATE POST SET LIKECOUNTER = LIKECOUNTER - 1 WHERE (ID = %d)""" % (int(postId),)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()
            
* This function takes user id and post id as argument and it deletes row with these values. At last, it decreases by one
  the like counter of post.
  
  
  
*******************
Routing Operations
*******************


Timeline Routing 
===================

Searhing User
-------------------

.. code-block:: python 
   
	@app.route('/timeline/search' ,methods=['GET', 'POST'])
	@login_required
	def search_user():
	    content = request.form['content']
	    user = get_user(content)
	    if(user == None):
	         return render_template("error.html" ,
	         				posts=list(select_posts(current_user.id)),
	         				likes = list(select_user_likes(current_user.id)),
	                                error_messages = 'User could not be found.',
	                                owner_user = current_user,
	                                reposts = list(select_sharedPost(current_user.id)),
	                                songs = select_all_song2(),
	                                follower_number = number_of_follower(current_user.username).fetchone()[0]
	                                ,following_number = number_of_following(current_user.username).fetchone()[0])
	    if(current_user.id == user.id):
	         return render_template("timeline.html", 
	         					posts=list(select_posts(current_user.id)),
	         					likes = list(select_user_likes(current_user.id)),
	                                 owner_user = current_user,
	                                 reposts = list(select_sharedPost(current_user.id)),
	                                 songs = select_all_song2(), 
	                                 isfollower = check_follower(current_user.username,user.username).fetchone(),
	                                 follower_number = number_of_follower(current_user.username).fetchone()[0]
	                                ,following_number = number_of_following(current_user.username).fetchone()[0])
	    else:
	         return render_template("timeline_search.html", 
	         					posts=list(select_posts(user.id)),
	                               likes = list(select_user_likes(current_user.id)), 
	                                 owner_user = user,
	                                 reposts = list(select_sharedPost(user.id)),
	                                 isfollower = check_follower(current_user.username,user.username).fetchone(),
	                                 follower_number = number_of_follower(user.username).fetchone()[0]
	                                ,following_number = number_of_following(user.username).fetchone()[0])
	                                
* This function is routing function of searching user. This function looks for a registered user with the given username
  in the database. If user does not exist, function redirects to timeline page of current user with error message. If user exists, function redirects 
  to timeline of this user. If current user enters own user name, function redirect to timeline page of current user again.    	                                

Like and Dislike a Post
--------------------------

.. code-block:: python 	
   
	@app.route('/timeline/like/<int:LIKEID>/<string:USERNAME>', methods=['GET', 'POST'])
	@login_required
	def like_post(LIKEID,USERNAME):
	    if(control_like(current_user.id,LIKEID)):
	        insert_like(current_user.id,LIKEID)
	    else:
	        delete_like(current_user.id,LIKEID)
	
	    if(USERNAME == current_user.username):
	          return redirect(url_for('timeline_page'))
	    else:
	          user = get_user(USERNAME)
	          return render_template("timeline_search.html", 
	          					posts=list(select_posts(user.id)), 
	          					likes = list(select_user_likes(current_user.id)),
	          					owner_user = user,
	          					isfollower = check_follower(current_user.username,user.username).fetchone())

* This function is routing function of like and dislike post operations. When a user clicks a like button, function checks
  this post is liked before by this user. If it is liked before, function deletes this like. If it is not, function insertes 
  like. After that, if liked post belongs to current user, function redirects to timeline page of current user. If it is
  not, function redirects timeline of owner of liked post.


Control Like
-------------------
.. code-block:: python


	def control_like(userId,postId):
	    with dbapi2.connect(dsn) as connection:
	        cursor = connection.cursor()
	        cursor = select_like(userId,postId)
	        control = cursor.fetchone()
	
	        if control is None:
	            return True
	        else:
	            return False
	            
* This function checks whether the given user likes the given post. If the user liked, function returns false. If the user did not
  liked function return true.	           