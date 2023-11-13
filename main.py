import sys # for CLI
import os # helper for choosing a db file to run.
import sqlite3

from functions import register as reg
from functions import login
from functions import list_followers as lf
from functions import composetweet as ct
from functions import searchTweet as st
from functions import tweet_stats as ts
from functions import search_users


def choose_database():
    if len(sys.argv) == 1:
        print('No filepath given. Defaulting to "test.db"')
        return 'test.db'
    
    database_file = sys.argv[1] # take first arg

    if os.path.exists(database_file):
        print('Selected database "{}"'.format(database_file))
        return database_file
    else:
        print('file "{}" not found. Defaulting to "test.db"'.format(database_file))
        return 'test.db'

def main():
    database = choose_database()

    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys=ON;")
    conn.commit()
    while True:
        # Login/Register Loop
        while True:
            ans = input("\nAre you registered? (y/n/e)").lower()
            user_id = None
            if ans == "y":
                while not user_id:
                    user_id = login.login(conn)
                break
            elif ans == "n":
                user_id = reg.register(conn)
                break
            elif ans == "e":
                conn.close()
                exit("Program Exited")
        # Main Functionality Loop
        while True:
            print("\n\033[1m\033[4mMain Page as usr " + str(user_id) + ":\033[0m\
                                        \nst\t- search for tweets\
                                        \nsu\t- search for users\
                                        \nwt\t- write a tweet\
                                        \nlf\t- list followers\
                                        \nl\t- logout\
                                        \ne\t- exit program")
            command = input().lower().split()
            if len(command) == 0:
                print("Please enter a command.")
                continue
            action = command[0]

            if action == "e":
                conn.close()
                exit("Program Exited")
            elif action == "lf":
                lf.list_followers(conn, user_id)
            elif action == "l":
                break
            elif action == "wt":
                ct.composetweet(conn, user_id)
            elif action == "su":
                search_users.search_users(conn, user_id)
            elif action == "st":
                st.searchTweet(conn, user_id)

if __name__ == '__main__':
  main()