from tabulate import tabulate
from functions import follow, more_tweets, get_name as gn, select_tweet as st

# enters the select user submenu
# allows the user to view more info on a user, follow them, select a certain tweet, see more tweets.
def select_user(conn, selected_usrid, current_usrID):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE usr = :user;", {"user":selected_usrid})
    result = cursor.fetchone()

    if not result:
        print("User is not a valid user.")
        return
    # Print the user
    while True:
        # see more info about the user
        tids = see_more_info(conn, selected_usrid)
        print("\n\033[1m\033[4mOptions\033[0m\
                \nf\t\t- follow user\
                \nsel <tid>\t- select a tweet and show tweet metrics\
                \nm\t\t- see more tweets\
                \ne\t\t- deselect user")
        
        # get command
        command = input().lower().split()
        if len(command) == 0:
            print("Please enter a command.")
            continue

        if command[0] == "f":   # follow command
            follow.follow(conn, current_usrID, selected_usrid)
        elif command[0] == "sel" and len(command) > 1: # select tweet command
            if int(command[1]) in tids:
                st.select_tweet(conn, current_usrID, command[1]) # select_tweet will check if the tweet exists.
            else:
                print("\nThis is not one of", str(gn.get_name(conn, selected_usrid))+"'s displayed tweets!")    
        elif command[0] == "m": # show more tweets command
            more_tweets.more_tweets(conn, selected_usrid)
        elif command[0] == "e": # exit command
            break
    return

# returns more info on a user
# Includes the users number of tweets, number of followers, and number of folowees, and 3 latest tweets.
# distplays these results into the command line.
def see_more_info(conn, usr):
    c = conn.cursor()

    c.execute('SELECT count(tid) FROM tweets WHERE writer=:usr;', {"usr":usr})   # get count of tweets
    number_of_tweets = c.fetchone()[0]

    c.execute('SELECT count(flwer) FROM follows WHERE flwee=:usr;', {"usr":usr})   # get number of followers
    number_of_followers = c.fetchone()[0]
    
    c.execute('SELECT count(flwee) FROM follows WHERE flwer=:usr;', {"usr":usr})   # get number of users followed
    number_of_followees = c.fetchone()[0]

    c.execute('SELECT tid, tdate, text, replyto FROM tweets WHERE writer=:usr ORDER BY tdate DESC LIMIT 3;', {"usr":usr})   # get 3 most recent tweets
    most_recent_tweets = c.fetchall()
    tids = []
    for tweet in most_recent_tweets:
        tids.append(tweet[0])

    print("\033[1m\033[4mSelected User:\033[0m " + str(gn.get_name(conn, usr)) + " (id: " + str(usr) + ")" + \
            "\nTweets: " + str(number_of_tweets) + \
            "\nFollowers: " + str(number_of_followers) + \
            "\nFollowing: " + str(number_of_followees))
    print("Last three tweets:")
    print(tabulate(most_recent_tweets, headers=['ID', 'Date', 'Text', 'Reply to'], tablefmt='orgtbl'))

    return tids