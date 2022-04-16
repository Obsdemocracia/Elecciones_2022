import psycopg2

conn = None

def create_tables():

    commands = (
        """
        CREATE TABLE users (
            user_id BIGSERIAL PRIMARY KEY,
            user_username VARCHAR(255) NOT NULL,
            user_screenname VARCHAR(255) NOT NULL,
            user_followers INTEGER NOT NULL,
            user_following INTEGER NOT NULL,
            user_tweet_count INTEGER NOT NULL,
            user_type INTEGER DEFAULT 0
        )
        """,
        """ CREATE TABLE tweets (
                tweet_id INTEGER PRIMARY KEY,
                tweet_text VARCHAR(500) NOT NULL,
                tweet_user INTEGER NOT NULL,
                FOREIGN KEY (tweet_user)
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE 
                )
        """,
        """
        CREATE TABLE retweets (
                retweet_id INTEGER PRIMARY KEY,
                retweet_text VARCHAR(500) NOT NULL,
                retweet_org_user INTEGER NOT NULL,
                retweet_user INTEGER NOT NULL,
                FOREIGN KEY (retweet_user)
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE 
        )
        """,
        """
        CREATE TABLE replies (
                tweet_id INTEGER PRIMARY KEY,
                conversation_id INTEGER NOT NULL,
                in_reply_to_status_id INTEGER NOT NULL,
                in_reply_to_user_id INTEGER NOT NULL,
                reply_user INTEGER NOT NULL,
                FOREIGN KEY (reply_user)
                REFERENCES users (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE 
        )
        """,
        """
        CREATE TABLE candidates_followers (
            user_id BIGSERIAL,
            candidate_id BIGSERIAL,
            PRIMARY KEY(user_id,candidate_id),
            FOREIGN KEY (user_id)
            REFERENCES users (user_id),
            FOREIGN KEY (candidate_id)
            REFERENCES users (user_id)
            ON UPDATE CASCADE ON DELETE CASCADE 
        )
        """)

    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()

def drop_tables():
    commands = (
         "DROP TABLE IF EXISTS candidates_followers",
         "DROP TABLE IF EXISTS replies",
         "DROP TABLE IF EXISTS retweets",
         "DROP TABLE IF EXISTS tweets",
         "DROP TABLE IF EXISTS users"
     )
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()

def add_user(id: int, username: str, screenname: str, followers: int, following: int, tweets: int):
    sql = """INSERT INTO users(
            user_id,
            user_username,
            user_screenname,
            user_followers,
            user_following,
            user_tweet_count)
            VALUES(%s,%s,%s,%s,%s,%s)"""
    user = (id,username,screenname,followers,following,tweets)
    cur = conn.cursor()
    try:
        cur.execute(sql, user)
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cur.close()
        conn.commit()

def add_users(users):
    sql = """INSERT INTO users(
        user_id,
        user_username,
        user_screenname,
        user_followers,
        user_following,
        user_tweet_count) 
        VALUES(%s,%s,%s,%s,%s,%s)"""
    cur = conn.cursor()
    cur.execute(sql, users)
    cur.close()
    conn.commit()

def get_users():
    sql = "SELECT * FROM users"
    cur = conn.cursor()
    cur.execute(sql)
    print("The number of parts: ", cur.rowcount)
    row = cur.fetchone()

    while row is not None:
        print(row)
        row = cur.fetchone()

def connect():
    global conn
    try:
        conn = psycopg2.connect(
        host="",
        port=5432,
        database="postgres",
        user="",
        password=""
        )
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False

def disconnect():
    if conn is not None:
        conn.close()


if __name__ == '__main__':
    if connect():
        #drop_tables()
        create_tables()
        disconnect()
