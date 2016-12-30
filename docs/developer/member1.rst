================================
Parts Implemented by Kağan Özgün
================================

* I developed sign up, sign in, userdata operations, userdetails operations and follow operations part of that project.

.. contents:: Contents
   :local:

***************
Database Design
***************
* I created and use three entity in this part which Userdata table, Userdetails table and Followers table.

Initialization of tables
========================

Userdata Table
--------------

.. code-block :: python

   def drop_user_table():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS    USERDATA"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

* Drop userdata table before creating table for deleting if exist.

.. code-block :: python


    def create_user_table():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS USERDATA(
            ID SERIAL PRIMARY KEY,
            USERNAME  VARCHAR(50) UNIQUE NOT NULL,
            PASSWORD VARCHAR(20) NOT NULL
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

* Create userdata table which contains ID(int), Username (varchar) and password (varchar).

* That table use for login operations and other tables takes id and username's of user using reference.

Userdetails Table
-----------------
.. code-block :: python


   def drop_userdetails_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS USERDETAILS"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Drop userdetails table before creating table for deleting if exist.

.. code-block :: python

    def create_userdetails_table():
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS USERDETAILS(
            ID SERIAL PRIMARY KEY,
            USERID INTEGER NOT NULL REFERENCES USERDATA(ID) ON DELETE CASCADE,
            NAME  VARCHAR(50),
            SURNAME VARCHAR(50),
            EMAIL VARCHAR(50),
            PHONENUMBER VARCHAR(15)
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

* Create userdetails table which contains ID(int), Userid (int) which references user id from userdata table, name(varchar), surname(varchar), email(varchar) and phonenumber(varchar).

* That table using for saving user details like name, surname, email and phonenumber. This table connected to userdata tables using userdata.id as a foreign key.

Followers
---------
.. code-block :: python

   def drop_followers_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS FOLLOWERS"""
            cursor.execute(statement);
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Drop followers table before creating table for deleting if exist.

.. code-block :: python

   def create_followers_table():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS FOLLOWERS(
                ID SERIAL PRIMARY KEY,
                USERNAME VARCHAR(50)  REFERENCES USERDATA(USERNAME) ON DELETE CASCADE ON UPDATE CASCADE,
                FOLLOWER VARCHAR(50) REFERENCES USERDATA(USERNAME) ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE(USERNAME,FOLLOWER)
                )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Create followers table which contains ID(int), Username(varchar) which references userdata.username and Follower(varchar) which references userdata.username

* That table using for saving followers of all users.

**************
Python Objects
**************
* This part include object for transferring data between methods.

User
====

.. code-block :: python

   class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

* Python class for using data from userdata table.

Userdetails
===========
.. code-block :: python

 class Userdetails:
    def __init__(self, userid,name, surname, email,phonenumber):
        self.userid = userid
        self.name = name
        self.surname = surname
        self.email = email
        self.phonenumber = phonenumber

* Python class for using userdetails table data.

*******************
Database Operations
*******************
* This part include database operation methods about Userdata, Userdetails and Followers table.

Userdata Operations
===================

Insert Userdata
---------------
.. code-block :: python

   def insert_user(user):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            statement= """INSERT INTO USERDATA(USERNAME,PASSWORD) VALUES(%s,%s)"""
            cursor.execute(statement,(user.username,user.password))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* This method using for adding new row to the Userdata table.

Select One User
---------------

.. code-block :: python

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

* This method use for taking one user username and password from Userdata table.

Select User List
----------------

.. code-block :: python

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

* Select_users_from_login method using for taking all users login data from Userdata table. Login operation use this method for checking the members of website.

Update User
-----------

.. code-block :: python

    def update_user_login(new_username,new_password,username):
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE USERDATA SET USERNAME = '%s' , PASSWORD = '%s' WHERE USERNAME = '%s'""" %(new_username,new_password,username)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Update user method using for changing user login information.


Delete User
-----------

.. code-block :: python

   def delete_user_login(username,password):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM USERDATA WHERE USERNAME = '%s' AND PASSWORD = '%s'""" %(username,password)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Delete_user_login using for delete a user from database. This methods delete all of the tables and information about user.

Userdetails Operations
======================

Insert Userdetails
------------------

.. code-block :: python

   def insert_userdetails(userdetails):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO USERDETAILS(USERID,NAME,SURNAME,EMAIL,PHONENUMBER) VALUES(%s,%s,%s,%s,%s)"""
            cursor.execute(query,(userdetails.userid,userdetails.name,userdetails.surname,userdetails.email,userdetails.phonenumber))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Insert_userdetails method takes userdetails object and add this object to the Userdetails table.

Select An User Userdetails
--------------------------

.. code-block :: python

   def select_an_user_userdetails(username):
       with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """SELECT * FROM USERDETAILS INNER JOIN USERDATA on USERDATA.ID = USERDETAILS.USERID WHERE USERNAME = '%s' """ %(username)
             cursor.execute(query)
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()

* Select_an_user_userdetails takes an user name, surname, email, phone number information from database using username of the user.

Update Userdetails
------------------

.. code-block :: python

  def update_myuserdetail(name,surname,email,phonenumber):
    with dbapi2.connect(dsn) as connection:
        try:
             cursor = connection.cursor()
             query = """UPDATE USERDETAILS SET  NAME = '%s', SURNAME = '%s', EMAIL = '%s', PHONENUMBER = '%s' WHERE USERID = '%s' """%(name,surname,email,phonenumber,current_user.id)
             cursor.execute(query)
             connection.commit()
             return cursor
        except dbapi2.DatabaseError as e:
             connection.rollback()

* Update_myuserdetails methods using for updating an user's name, surname, email and phone number. Method take name, surname, email, phonenumber.

Delete Userdetails
------------------

.. code-block :: python

   def delete_userdetails():
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """DELETE FROM USERDETAILS WHERE (USERID = %s)""" %(current_user.id)
            cursor.execute(query)
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* This method delete all of the information of the user by users id.

Followers Operations
====================

Insert Follower
---------------

.. code-block :: python

   def insert_follower(username,f_username):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query ="""INSERT INTO FOLLOWERS(USERNAME,FOLLOWER) VALUES(%s,%s)"""
            cursor.execute(query,(username,f_username))
            connection.commit()
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Insert_follower method add username of follower and user name of following to Followers table.

Select Follower
---------------

.. code-block :: python

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

* Check_follower method check following situation of two account using both account username.

Number of Follower
------------------

.. code-block :: python

    def number_of_follower(name):
    with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COUNT(FOLLOWER) FROM FOLLOWERS WHERE (FOLLOWER = '%s')""" %(name)
            cursor.execute(query)
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Number of follower method count followers using username of an user. Methods count number of rows in follower column.

Number of Following
-------------------

.. code-block :: python

   def number_of_following(name):
     with dbapi2.connect(dsn) as connection:
        try:
            cursor = connection.cursor()
            query = """SELECT COUNT(USERNAME) FROM FOLLOWERS WHERE (USERNAME = '%s')""" %(name)
            cursor.execute(query)
            connection.commit()
            return cursor
        except dbapi2.DatabaseError as e:
            connection.rollback()

* Number of following method take username and count number of rows which have this username in username column of Followers table.

Delete Followers
----------------

.. code-block :: python

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

* Delete follower method delete follower from table is user unfollow the other user.




*******
Routing
*******

* This part include methods in server.py which using for sending and getting data between back-end, front-end parts of project.

Sign Up
=======

.. code-block :: python

   @app.route('/signup', methods=['POST'])
   def signup():
    username = request.form['reg_username']
    password = request.form['reg_password']
    insert_user_login(username, password)
    return redirect(url_for('login'))

* Sign up method takes input from homepage.html and add new account to database using this input.

Login
=====

.. code-block :: python

   @app.route('/', methods=['GET','POST'])
   def login():
    form=LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user = get_user(username)
        #user_list = select_users_from_login()
        if user is not None:
            password = form.password.data
            if(password == user.password):
                login_user(user)
                return redirect(url_for('timeline_page'))

    return render_template('home.html',form=form)

* Login method takes input from login page and select user using this input. If user in database method render timeline page and send user login information but if user is not in database method render home page for getting sign in information from user again.



Logout
======

.. code-block :: python

   @app.route('/logout')
   @login_required
   def logout_page():
    logout_user()
    return redirect(url_for('login'))

* Logout method use logout_user() method from flask_login.

Update Profile
==============

.. code-block :: python

   @app.route('/update-profile', methods=['POST'])
   @login_required
   def update_profile():
      form = LoginForm(request.form)
      username = request.form['new_username']
      password = request.form['new_password']
      update_user_login(username, password, current_user.username)
      logout_user()
      return render_template('home.html', form = form)


* Update Profile method takes input from update profile modal and update user information using that information. Old username taking using flask_login module.

* After updating logout operation work and homepage rendered for login with new data.

Delete Profile
==============

.. code-block :: python

   @app.route('/delete-profile', methods=['POST'])
   @login_required
   def delete_profile():
    form=LoginForm(request.form)
    password = request.form['password']
    delete_user_login(current_user.username, password)
    return render_template('home.html',form = form)

* Delete profile operations take password of current user from delete profile modal in layout.html. If password is match delete the users data from all of tables and finally delete the userdata row.


Profile Details
===============

.. code-block :: python

   @app.route('/profiledetails')
   def profiledetails():
        userdetails = select_an_user_userdetails(current_user.username).fetchone()
        check = userdetails
        if(check):
            name =userdetails[2]
            surname = userdetails[3]
            mail = userdetails[4]
            phone = userdetails[5]
        else:
            name =None
            surname = None
            mail = None
            phone = None
        return render_template("profiledetails.html",name = name,surname = surname, mail = mail, phone = phone, users = current_user)

* Profiledetails method select current user data from Userdetails table and render profiledetails.html and send userdetails to profiledetails.html page.

Updating Userdetails
====================

.. code-block :: python

   @app.route('/update_userdetails',methods=['GET','POST'])
 def update_userdetails():
    type = request.form['form_type']
    list = []
    list = select_an_user_userdetails(current_user.username).fetchone()
    name = ""
    surname = ""
    email = ""
    phonenum = ""
    if(type == "1"):
        name = request.form['update_name']
        surname = list[3]
        email = list[4]
        phonenum = list[5]

    elif(type == "2"):
        surname = request.form['update_surname']
        name = list[2];
        email = list[4]
        phonenum = list[5]

    elif(type == "3"):
        email = request.form['update_email']
        name = list[2];
        surname = list[3]
        phonenum = list[5]

    elif(type == "4"):
        phonenum = request.form['update_phone']
        name = list[2];
        surname = list[3]
        email = list[4]
    else:
        name = list[2];
        surname = list[3]
        email = list[4]
        phonenum = list[5]

    update_myuserdetail(name,surname,email,phonenum)
    return redirect(url_for('profiledetails'))

* Update userdetails method using for rendering profiledetails and updating userdetails with input from userdetails.html. User can update one column or multiple column in userdetails table. If else conditions control the user input and send inputs to update_myuserdetails method.


Delete Userdetails
==================

.. code-block :: python

  @app.route('/deleteuserdetails',methods=['GET','POST'])
  def delete_user_details():
    password = request.form['password']
    delete_userdetails()
    return redirect(url_for('timeline_page'))

* Delete userdetails method takes user password from userdetails.html and delete all of the userdetails from table.

Insert Userdetails
==================

.. code-block :: python

   @app.route('/insert_details',methods=['GET','POST'])
   def insert_details():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phonenum = request.form['phonenum']
    userx = Userdetails(current_user.id,name,surname,email,phonenum)
    insert_userdetails(userx)
    return redirect(url_for('profiledetails'))

* Insert details method takes input from userdetails.html and send data to database insert method of userdetails table and render userdetails.html again.


Follower
========

.. code-block :: python

   @app.route('/follow/<string:followusername>')
   def follow(followusername):
    if(check_follower(current_user.username,followusername).fetchone()):
       delete_follower(current_user.username,followusername)
    else:
       insert_follower(current_user.username,followusername)

    user = get_user(followusername)

    return render_template("timeline_search.html", posts=list(select_posts(user.id)), likes = list(select_user_likes(current_user.id)),owner_user = user
                           ,isfollower = check_follower(current_user.username,followusername).fetchone(),
                           follower_number = number_of_follower(user.username).fetchone()[0]
                           ,following_number = number_of_following(user.username).fetchone()[0])

* Follow method using for getting reaction of follow and unfollow button. If user follow another add this information to the followers table and send situation of following for rendering follower and following number.


*******************
Frontend Operations
*******************

* Frontend operations include html file about user interface of operations.

HTML Templates
==============

Home.html
---------

.. code-block :: html

   <div id="signin_modal" class="modal fade" role="dialog">
     <div class="modal-dialog modal-sm">

       <!-- Modal content-->
       <div class="modal-content">
         <div class="modal-header">
           <button type="button" class="close" data-dismiss="modal">&times;</button>
           <h4 class="modal-title">Sign In</h4>
         </div>
         <div class="modal-body">
           <div class="login-form-1">
         <form id="login-form" class="text-left" method="post" action="/">
               {{ form.csrf_token }}
            <div class="login-form-main-message"></div>
            <div class="main-login-form">
               <div class="login-group">
                  <div class="form-group">
                     <label for="lg_username" class="sr-only">Username</label>
                               {{ form.username(autofocus=True,
                              id='lg-username',
                              placeholder='Username') }}

                  </div>
                  <div class="form-group">
                     <label for="lg_password" class="sr-only">Password</label>
                           {{ form.password(id='lg-password', class='form-control',
                              placeholder='Password') }}

                  </div>
               </div>
            </div>
         </form>
      </div>
         </div>
         <div class="modal-footer">
           <button type="submit" value="Send" class="btn btn-default" form="login-form">Sign In</button>
         </div>
       </div>
     </div>
   </div>

* Home.html has two modal for sign up and sign in operation this part for sign in operation. This modal takes input from user and send input to login method in server.py.


.. code-block :: html

      <div id="signup_modal" class="modal fade" role="dialog">
       <div class="modal-dialog modal-sm">

       <!-- Modal content-->
       <div class="modal-content">
         <div class="modal-header">
           <button type="button" class="close" data-dismiss="modal">&times;</button>
           <h4 class="modal-title">Sign Up</h4>
         </div>
         <div class="modal-body">
            <div class="login-form-1">
         <form id="register-form" class="text-left" method="post" action="/signup">
            <div class="login-form-main-message"></div>
            <div class="main-login-form">
               <div class="login-group">
                  <div class="form-group">
                     <label for="reg_username" class="sr-only">Email address</label>
                     <input type="text" class="form-control" id="reg_username" name="reg_username" placeholder="username">
                  </div>
                  <div class="form-group">
                     <label for="reg_password" class="sr-only">Password</label>
                     <input type="password" class="form-control" id="reg_password" name="reg_password" placeholder="password">
                  </div>

               </div>
            </div>
         </form>
      </div>
         </div>
         <div class="modal-footer">
           <button type="submit" class="btn btn-success" value="Send" form="register-form">Sign Up</button>
         </div>
       </div>
     </div>
   </div>

* This part  of Home.html is using for Sign up modal. Modal takes sign up inputs from user and send input to server.py for adding new user to database.

Layout.html
-----------

.. code-block :: html

   <!------------ Profile dropdown ------------>
         <ul class="nav navbar-nav navbar-right">
            <li class="dropdown">
               <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
               <img alt="ProfilePic" src="{{ url_for('static', filename='images/logo/logo_vector.svg') }}"
               width = "50px">Profile<span class="caret"></span></a>
                        <ul class="dropdown-menu">

                           <center><li class="modal_button">  <button type="button" class="btn btn-info " data-toggle="modal" data-target="#update_profile_modal">Update Profile </button>  </li></center>
                           <li role="separator" class="divider"></li>
                           <center><li class ="modal_buton">  <button type="button" class="btn btn-danger " data-toggle="modal" data-target="#delete_profile_modal">Delete Profile </button>  </li></center>
                           <li role="separator" class="divider"></li>
                           <li><a href="{{url_for('profiledetails')}}"><button type="button" class="btn btn-success center-block">Profile Details</button></a></li>

                        <li role="separator" class="divider"></li>
                                <li><a href="{{url_for('suggestion_page')}}"><button type="button" class="btn btn-warning">Suggestions
                                </button></a></li>
                                <li role="separator" class="divider"></li>
                           <li><a href="{{url_for('logout_page')}}"><button type="button" class="btn btn-danger">Logout</button></a></li>
                           <li role="separator" class="divider"></li>
                           <li><a href="#">Separated link</a></li>
                         </ul>
            </li>
            </ul>
            <!------------ Profile dropdown ------------>

* Layout.html file is template for rendering navigation bar of the timeline. Update Profile, Delete Profile, Profile Details and Logout buttons added Profile dropdown list for redirecting relevant html pages or modals.

.. code-block :: python


   <div id="update_profile_modal" class="modal fade" role="dialog">
     <div class="modal-dialog modal-sm">

       <!-- Modal content-->
       <div class="modal-content">
         <div class="modal-header">
           <button type="button" class="close" data-dismiss="modal">&times;</button>
           <h4 class="modal-title">Update Profile</h4>
         </div>
         <div class="modal-body">
           <div class="login-form-1">
            <form id="update-profile" class="text-left" method="post" action="/update-profile">
               <div class="login-form-main-message"></div>
            <div class="main-login-form">
               <div class="login-group">
                  <div class="form-group">
                     New Username
                     <label for="lg_username" class="sr-only">New Username</label>
                     <input type="text" class="form-control" id="new_username" name="new_username" placeholder=" new username">
                  </div>
                  <div class="form-group">
                     New Password
                     <label for="lg_password" class="sr-only"> New Password</label>
                     <input type="password" class="form-control" id="new_password" name="new_password" placeholder="new password">
                  </div>
               </div>
            </div>
         </form>
      </div>
         </div>
         <div class="modal-footer">
           <button type="submit" value="Send" class="btn btn-default" form="update-profile">Update</button>
         </div>
       </div>

     </div>
   </div>


* This part of Layout.html for update profile modal. Modal takes new username, new password and send this input to update_profile method in server.py.

.. code-block :: python



   <div id="delete_profile_modal" class="modal fade" role="dialog">
     <div class="modal-dialog modal-sm">

       <!-- Modal content-->
       <div class="modal-content">
         <div class="modal-header">
           <button type="button" class="close" data-dismiss="modal">&times;</button>
           <h4 class="modal-title">Delete Profile</h4>
         </div>
         <div class="modal-body">
           <div class="login-form-1">
         <form id="delete-profile" class="text-left" method="post" action="/delete-profile">
            <div class="login-form-main-message"></div>
            <div class="main-login-form">
               <div class="login-group">
                  Enter Your Password
                  <div class="form-group">
                     <label for="password" class="sr-only">Password</label>
                     <input type="password" class="form-control" id="password" name="password" placeholder="password">
                  </div>
               </div>
            </div>
         </form>
      </div>
         </div>
         <div class="modal-footer">
           <button type="submit" value="Send" class="btn btn-default" form="delete-profile">Delete</button>
         </div>
       </div>

     </div>
   </div>


* This part of Layout.html for delete profile modal. Modal takes password and send this input to delete_profile method in server.py.

Userdetails.html
----------------

.. code-block :: html

   {%if name == None%}
   {%if surname == None%}
      {%if mail == None%}
         {%if phone == None%}

      <h2>Add User Details</h2>
      <div class="table-responsive">
      <form action = "/insert_details" method = "POST">
      <table class="table">
            <tbody>
                  <tr class="success">
                  <td>Username</td>
               <td></td>
                  <td>{{current_user.username}}</td>
                  </tr>
                  <tr class="info">
                  <td>Name</td>
               <td></td>
                  <td><input type = "text" name = "name" /></td>
                  </tr>
                  <tr class="info">
                  <td>Surname</td>
               <td></td>
                  <td><input type = "text" name = "surname" /></td>
                  </tr>
                  <tr class="info">
                  <td>E-mail</td>
               <td></td>
                  <td><input type = "text" name = "email" /></td>
                  </tr>
                  <tr class = info>
                  <td>Phone Number</td>
               <td></td>
                  <td><input type = "text" name = "phonenum" /></td>
                  </tr>
                  <tr class = info>
                  <td></td>
               <td></td>
                  <td><button type="submit" value = "Add" class="btn btn-danger">Add</button></td>
                  </tr>
             </tbody>
       </table>
            </form>
    </div>

         {%endif%}
      {%endif%}
   {%endif%}


* This part of  userdetails.html using for rendering add userdetails part of page and get input and send that input to inser_useretails method. If else conditions check is all of the useredetails are empty or not.


.. code-block :: html

    {%else%}

     <h2>User Details</h2>
     <div class="table-responsive">
     <table class="table">
       <tbody>
         <tr class="success">
           <td>Username</td>
           <td colspan="2">{{current_user.username}}</td>
         </tr>
         <tr class="info">
           <td>Name</td>
           <td>{{name}}</td>
           <td><button type="button" class="btn-lg btn-info " data-toggle="modal" data-target="#update_name">Update       </button></td>
         </tr>
         <tr class="info">
           <td>Surname</td>
           <td>{{surname}}</td>
           <td><button type="button" class="btn-lg btn-info " data-toggle="modal" data-target="#update_surname">Update </button></td>
         </tr>
         <tr class="info">
           <td>E-mail</td>
           <td>{{mail}}</td>
           <td><button type="button" class="btn-lg btn-info " data-toggle="modal" data-target="#update_email">Update </button></td>
         </tr>
         <tr class = info>
           <td>Phone Number</td>
           <td>{{phone}}</td>
           <td><button type="button" class="btn-lg btn-info " data-toggle="modal" data-target="#update_phone">Update </button></td>
         </tr>
       </tbody>
     </table>
     </div>
     <form action = "/gototimeline" method = "POST">
      <button type="submit" value = "Go to Timeline" class="btn btn-success">Go to Timeline</button>
      </form>
   </br>
   <form action = "/deleteuserdetails" method = "POST">
      <button type="button" class="btn-lg btn-danger" data-toggle="modal" data-target="#delete_details">Delete Userdetails</button>
      </form>
   {%endif%}

* That part of Userdetails.html using for rendering update userdetails and getting input for deleting userdetails and updating user details. Input are taken with modal for each data. If one of the userdetails is in the database for current user, updatedetails part of page is rendering.


Profile.html
------------

.. code-block :: html

   {%if current_user.id != owner_user.id%}
     {%set var = isfollower%}
     {%if var%}
   <a href="{{url_for('follow',followusername = owner_user.username)}}">
   <button type="button" class="btn btn-danger btn-sm">Unfollow</button>
   </a>

     {%else%}
   <a href="{{url_for('follow',followusername = owner_user.username)}}">
   <button type="button" class="btn btn-success btn-sm">Follow</button>
   </a>
     {%endif%}
   {%endif%}

* That part of profile.html using for rendering follow and unfollow button. If current user is not follow searched user follow button is rendering with green color and if current user click follow button hmtl send data to follow method in server.py and follow information adding to Followers table. If current user already follow searched user unfollow button is rendering with red color and user click unfollow button html send that data to follow method and follow row deleted from Followers table.
* If user in its own timeline follow and unfollow buttons are not rendering for preventing follow user itself.

.. code-block :: html


   Followers</a>  <span class="badge">   {{follower_number}}</span>
   </br>
   <a href = "#">
   <i class="glyphicon glyphicon-headphones"></i>
   Following</a> <span class="badge">   {{following_number}}</span>
   </br>

* That part of profile.html put follower and following number of user. Follow method in server.py send number of following and number of follower her for rendering number.


