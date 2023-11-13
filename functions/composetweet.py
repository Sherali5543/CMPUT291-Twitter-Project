from functions import hashtagExists as he

# composes a tweet. Updates the underlying SQL table if successful
def composetweet(conn, uid, replyto = None):
    print("\n\033[1m\033[4mWriting a tweet:\033[0m")
    text = input("Write your tweet (leave blank to exit): ")
    if not(len(text) > 0):
        print('Did not write a tweet!')
        return
    
    hashtags = parseHashtags(text)
    
    tid = generateTid(conn)
    
    if replyto == None:
        #Sql for adding a tweet
        createTweet(conn, tid, uid, text)
    else:
        #Sql for adding a reply
        createReply(conn, tid, uid, text, replyto)
    
    if hashtags:
        for hashtag in hashtags:
            if len(hashtag) > 0:
                hashtagCheck = he.hashtagExists(conn, hashtag)
                if not hashtagCheck:
                    #add hashtag
                    addHashtag(conn, hashtag)
                mentionHashtag(conn, tid, hashtag)
    print("\nYour tweet has been written.")

# add a hashtag into the hashtag table
# helper function
def addHashtag(conn, hashtag):
    cur = conn.cursor()
    cur.execute("\
                INSERT INTO hashtags (term)\
                VALUES (:term)",
                {"term":hashtag})
    conn.commit()

# add a mention to the mention table
# helper function
def mentionHashtag(conn, tid, hashtag):
    cur = conn.cursor()
    cur.execute("\
                INSERT INTO mentions(tid, term)\
                VALUES(:tid, :term)",
                {"tid":tid, "term":hashtag})
    conn.commit()

# create a tweet which isa  reply function 
# helper function
def createReply(conn, tid, uid, text, replyto):
    cur = conn.cursor()
    cur.execute("\
                INSERT INTO tweets (tid, writer, tdate, text, replyto)\
                VALUES (:tid, :writer, date(), :text, :replyto);",
                {"tid":tid, "writer":uid, "text":text, "replyto":replyto})
    conn.commit()

# create a tweet which is not a reply 
# helper function
def createTweet(conn, tid, uid, text):
    cur = conn.cursor()
    cur.execute("\
                INSERT INTO tweets (tid, writer, tdate, text, replyto)\
                VALUES (:tid, :writer, date(), :text, NULL);",
                {"tid":tid, "writer":uid, "text":text})
    conn.commit()

# generate a uniqeu tweet id 
# helper function
def generateTid(conn):
    cur = conn.cursor()
    cur.execute("\
                SELECT max(tid)\
                FROM tweets")
    result = cur.fetchone()
    if result != None:
        ret = result[0]+1
        return ret
    else:
        return 0

# parse hashtags 
# helper function
def parseHashtags(text):
    text = text.split()
    #go through each word and find all hashtags
    hashtags = []
    for word in text:
        hashCheck = word.find("#")
        #incase multiple hashtags in a word
        while(hashCheck != -1):
            endIndex = word.find("#", hashCheck+1)
            if endIndex != -1:
                tag = word[hashCheck+1:endIndex]
                if not(tag in hashtags):
                    hashtags.append(tag)
                hashCheck = word.find("#", endIndex)
            else:
                tag = word[hashCheck+1:]
                if not(tag in hashtags):
                    hashtags.append(tag)
                hashCheck = word.find("#", hashCheck+1)
    return hashtags