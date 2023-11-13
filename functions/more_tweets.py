import math
from tabulate import tabulate
from functions import select_tweet as st, get_name as gn

# enters the submenu to view more tweets made by some user.
# user can navigate forwards, navigate backward, and select a tweets.
def query_tweets(conn, usr, offset):
    cursor = conn.cursor()
    cursor.execute("SELECT tid, tdate, text, replyto\
                    FROM tweets \
                    WHERE writer=:usr\
                    ORDER BY tdate DESC\
                    LIMIT 5 OFFSET :offset;",
                    {"usr":usr, "offset":offset})
    return cursor.fetchall()

def more_tweets(conn, usr):
    cursor = conn.cursor()
    offset = 0

    tweets = query_tweets(conn, usr, offset)

    cursor.execute('SELECT tid FROM tweets WHERE writer=:usr;', {"usr":usr})

    # list comprehension of all tids that this user wrote.
    tids = [row[0] for row in cursor.fetchall()]

    if len(tweets) == 0:
        print("This user has not tweeted!")
        return

    while True:
        print("\n\033[1m\033[4mTweets by:\033[0m " + str(usr))
        print("Page: " + str(round(offset/5)+1))
        print(tabulate(tweets, headers=['ID', 'Date', 'Text', 'Reply to'], tablefmt='orgtbl'))
        options = ""
        options += "nb\t\t- navigate backwards\n"
        options += "nf\t\t- navigate forward\n"
        options += "sel <tid>\t- select a tweet and show tweet metrics\n"
        options += "e\t\t- exit search\n"
        nav = input(options).lower()
        command = nav.lower().split()
        if nav == "e": # exit command
            break
        elif nav == "nf":
            offset += 5
            tweets = query_tweets(conn, usr, offset)
            # If next page returns empty, revert
            if not (len(tweets) > 0):
                offset -= 5
                tweets = query_tweets(conn, usr, offset)
                print("\nYou are on the last page!")
        elif nav == "nb":
            # Check we are not at page 1
            if offset >= 5:
                offset -= 5
            else:
                print("\nYou are at the first page!")
            tweets = query_tweets(conn, usr, offset)
        elif len(command) > 1 and command[0] == "sel":
            if int(command[1]) in tids:
                st.select_tweet(conn, usr, command[1])
            else:
                print("This is not one of " + gn.get_name(conn, usr) + "'s tweets!")
    return