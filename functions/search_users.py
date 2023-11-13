from tabulate import tabulate

import math

from functions import select_usr as sr

def query_users(conn, keyword, offset):
    c = conn.cursor()
    c.execute("\
                SELECT usr, name, city, 1 as rank, LENGTH(name)\
                FROM users \
                WHERE LOWER(name) LIKE :keyword\
                UNION\
                SELECT usr, name, city, 2 as rank, LENGTH(name)\
                FROM users \
                WHERE LOWER(city) LIKE :keyword\
                AND NOT LOWER(name) LIKE :keyword\
                ORDER BY rank, LENGTH(name)\
                LIMIT 5 OFFSET :offset;",
                {"keyword":keyword, "offset":offset})
    temp = c.fetchall()
    users = []
    #get rid of excess columns in result
    for user in temp:
        users.append((user[0:3]))
    
    return users

def search_users(conn, user_id):
    c = conn.cursor()
    offset = 0
    while True:
        print("\n\033[1m\033[4mSearch for users:\033[0m\
                \nsu <term>\t- searches for users matching this name/city\
                \nsel <usr>\t- select user\
                \ne\t\t- exit to menu")
                
        # get commmand.
        action = input()
        if action.startswith("su"):
            if len(action) > 3:
                keyword = "%" + action[3:].lower() + "%"

                users = query_users(conn, keyword, offset)

                if len(users) == 0:
                    print("No matching users found!")
                    continue

                # List users loop
                while len(users) != 0:
                    print("\nPage: " + str(round(offset/5)+1))
                    print(tabulate(users, headers=['usr', 'name', 'city'], tablefmt='orgtbl'))
                    options = "sel <usr>\t- select a user"
                    options += "\nnb\t\t- navigate backwards"
                    options += "\nnf\t\t- navigate forward"
                    options += "\ne\t\t- exit search\n"
                    nav = input(options).lower()
                    if nav == "e":          # exit command.
                        break
                    elif nav == "nf":
                        offset += 5
                        users = query_users(conn, keyword, offset)
                        # If next page returns empty, revert
                        if not (len(users) > 0):
                            offset -= 5
                            users = query_users(conn, keyword, offset)
                            print("\nYou are on the last page!")
                    elif nav == "nb":
                        # Check we are not at page 1
                        if offset >= 5:
                            offset -= 5
                        else:
                            print("\nYou are at the first page!")
                        users = query_users(conn, keyword, offset)
                    elif nav.startswith("sel"):
                        if len(nav) > 4:
                            sr.select_user(conn, nav[4:], user_id)
                        else:
                            print("Missing user.")
            else:   # if the user supplied an invalid command
                print("Missing search term.")
        if action.startswith("sel"):    # select user command. Can select a user before searching for one.
            if len(action) > 4:
                sr.select_user(conn, action[4:], user_id)
            else:
                print("Missing user.")
        elif action.lower() == "e":
            break
            
    return True
