import psycopg2 as dbapi2

dsn = """user='vagrant' password='vagrant'
         host='localhost' port=5432 dbname='itucsdb'"""
         

def create_post_table():
    try:
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS POST(
            ID SERIAL PRIMARY KEY,
            CONTENT VARCHAR(100) NOT NULL,
            POSTDATE DATE NOT NULL,
            USERID INTEGER NOT NULL,
            SONGID INTEGER NOT NULL
            )"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()
    
     
def insert_user(cursor):
    statement= """INSERT INTO USERS(USERNAME,PASSWORD,NAME,SURNAME,EMAIL) VALUES(?,?,?,?,?)"""
    cursor.execute(statement)