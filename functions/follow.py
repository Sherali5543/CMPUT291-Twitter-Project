from functions import get_name as gn
import sqlite3

# follows a user.
# takes in a follower and followee. Attempts to add the follows row into the table and if unable, prints a message
def follow(conn, flwer, flwee):
    c = conn.cursor()

    if str(flwer) == str(flwee):
        print("You cannot follow yourself!")
        return

    try:
        c.execute('INSERT INTO follows (flwer, flwee, start_date) VALUES (:flwer, :flwee, date());', {"flwer":flwer, "flwee":flwee})
        conn.commit()
        print("Sucessfully followed", gn.get_name(conn, flwee))
        return

    except sqlite3.IntegrityError as msg: 
        print("You already follow", gn.get_name(conn, flwee))
        return
