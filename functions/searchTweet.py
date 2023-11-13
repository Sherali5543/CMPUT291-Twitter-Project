from functions import select_tweet
from functions import composetweet as ct

from tabulate import tabulate

# builds a query helper function for building a SQlite query which can search for many keywords.
def buildQuery(searchTerms):
    hashtags = []
    terms = []
    for x in searchTerms:
        if x[0] == '#':
            hashtags.append(x[1:])
        else:
            terms.append(x)


    # wrap each term in percent signs.
    termsOrdered = []
    for x in terms:
        termsOrdered.append("%" + x + "%")
    for x in hashtags:
        termsOrdered.append("%" + x + "%")

    # build the first part of the query
    tweetQuery = '''SELECT t1.tid, t2.writer, t2.tdate, t2.text FROM ( 
            SELECT tid FROM tweets WHERE 0 = 1 OR ''' #term string
    
    # add placeholders for all the terms
    for i in terms:
        tweetQuery += "text LIKE ? OR "
    tweetQuery = tweetQuery[0:len(tweetQuery) - 4] # removing last OR

    # build second part of the query
    hashtagQuery = '''SELECT tid FROM mentions WHERE 0 = 1 OR ''' # hashtags

    # add placeholders for all the hashtags
    for i in hashtags:
        hashtagQuery += "term LIKE ? OR "
    hashtagQuery = hashtagQuery[0:len(hashtagQuery) - 4] # removing last OR

    # make final query by adding two halves
    query = tweetQuery + " UNION " + hashtagQuery + ")t1 JOIN tweets t2 ON t1.tid = t2.tid \
        ORDER BY t2.tdate DESC LIMIT 5 OFFSET ?"
    
    return query, termsOrdered

# search the sqlite database with the query made using buildQuery()
def searchQuery(c, searchTerm, offset = 0):
    query, termsOrdered = buildQuery(searchTerm)
    termsOrdered.append(str(offset))
    
    c.execute(query, termsOrdered)

    rows = c.fetchall()
    return rows

# enter the search tweet submenu
# Hehre the user can search for tweets by term.
def searchTweet(con, usrID):
    c = con.cursor()

    while True:
        print("\n\033[1m\033[4mSearch for a Tweet:\033[0m")
        print("st <terms>\t- searches for tweets with matching text or hashtags")
        print("e\t\t- return to main menu")

        while True:
            command = input().lower().split()
            if len(command) > 0:
                break
            print("Please enter a command.")

        if command[0] == "st" and len(command) > 1:
            # search for a tweet
            terms = command[1:]
            rows = searchQuery(c, terms, 0)

            offset = 0
            if len(rows) == 0:
                print("No tweets to display.")
                continue
            
            while True:
                print("\n\033[1m\033[4mMatching Tweets for Terms:\033[0m " + str(terms) +
                      "\nPage: " + str(round(offset/5)+1))
                if (len(rows) > 0):
                    print(tabulate(rows, headers=['tid', 'usr', 'date', 'tweet'], tablefmt='orgtbl')) 
                else:
                    print("No tweets to display.")
                print("\n\033[1m\033[4mOptions:\033[0m\
                      \nnf\t\t- navigate forward\
                      \nnb\t\t- navigate backward\
                      \nsel <tid>\t- select a tweet and show metrics\
                      \ne\t\t- return to search for new tweet")
                while True:
                    command = input().split()
                    if len(command) > 0:
                        break
                    print("Please enter a command.")
                if command[0] == "nf":
                    offset += 5
                    rows = searchQuery(c, terms, offset)
                    if not (len(rows) > 0):
                        offset -= 5
                        rows = searchQuery(c, terms, offset)
                        print("\nYou are on the last page!")
                elif command[0] == "nb":
                    if offset >= 5:
                        offset -= 5
                    else:
                        print("\nYou are at the first page!")
                    rows = searchQuery(c, terms, offset)
                elif command[0] == "sel" and len(command) > 1:
                    select_tweet.select_tweet(con, usrID, command[1])
                elif command[0] == "e":
                    break
        
        elif command[0] =="e":
            break

