# checks if a hashtag exists.
# takes in a hashtag and if it is in the sqlite database as stored in the argmet conn then returns true. else false.
def hashtagExists(conn, hashtag):
    cur = conn.cursor()
    cur.execute("\
                SELECT term\
                FROM hashtags\
                WHERE term = :hashtag;",
                {"hashtag":hashtag})
    result = cur.fetchone()
    if result == None:
        return False
    else:
        return True