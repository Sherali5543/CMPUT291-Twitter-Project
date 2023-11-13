from functions import tweet_stats as ts, retweet, composetweet
from tabulate import tabulate

# enter the select tweet submenu.
# the user can reply to the tweet, retweet the tweet.
def select_tweet(conn, usr, tid):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Tweets WHERE tid = :tid", {"tid":tid})
    result = cursor.fetchone()
    if not result:
        print("Tweet does not exist!")
        return

    while True:
        print("\n\033[1m\033[4mSelected Tweet:\033[0m ")
        numRetweets, numReplies = ts.tweet_stats(conn, tid)
        print(tabulate([result + (numRetweets, numReplies)], headers=["tid", "Writer", "Date", "Text", "Reply to", "# Retweets", "# Replies"], tablefmt='orgtbl'))
        print("rep\t- reply to this tweet\
              \nret\t- retweet this tweet\
              \ne\t- deselect this tweet")
        
        # get command
        inp = input()
        
        if inp == 'e': # exit command
            break
        elif inp == "rep": # reply command
            composetweet.composetweet(conn, usr, tid)
        elif inp == "ret": # retweet command
            retweet.retweet(conn, usr, tid)
    return