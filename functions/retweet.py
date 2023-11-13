import sqlite3

# compose a retweet with a writer, and unique tweet id
def retweet(conn, usr, tid):
    try:
        cur = conn.cursor()
        
        cur.execute("\
                    INSERT INTO retweets\
                    VALUES (:usr, :tid, date())",
                    {"usr":usr, "tid":tid})
        
        conn.commit()
        print("Succesfully retweeted", str(tid))
    except sqlite3.IntegrityError as msg:
        print("You have already retweeted", str(tid))