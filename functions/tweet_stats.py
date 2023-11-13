
# display the number of retweets and the number of replies
def tweet_stats(conn, tid):
    c = conn.cursor()

    c.execute('SELECT count(usr) FROM retweets WHERE tid=:tid', {"tid":tid})
    number_retweets = c.fetchone()[0]
    
    c.execute('SELECT count(tid) FROM tweets WHERE replyto=:tid', {"tid":tid})
    number_replies = c.fetchone()[0]

    return number_retweets, number_replies
