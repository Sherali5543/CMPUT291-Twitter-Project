import getpass

# registers a user
def register(conn):
    print("\n\033[1m\033[4mRegistering a new user:\033[0m")


    # generate a new user ID. if its valid, get the rest of the user info
    usr = generateUid(conn)
    pwd = getpass.getpass("Enter your password: ", stream=None)
    name = input("Input name: ")
    email = input("Input email: ")
    city = input("Input city: ")
    while True:
        try:
            timezone = float(input("Input timezone: "))
            break
        except ValueError:
            print("error. The input must be a float. Try again.")

    # Write new user to the database.
    c = conn.cursor()
    c.execute('INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (:usr, :pwd, :name, :email, :city, :timezone);', {"usr":usr, "pwd":pwd, "name":name, "email":email, "city":city, "timezone":timezone})

    
    conn.commit()
    print("Finished creating a new user.\
            \nYour userID is: " + str(usr) +" You will need this to login!")
    return usr


# generates a new unique user ID by returning 1+ the max user id in the database.
def generateUid(conn):
    cur = conn.cursor()
    cur.execute("\
                SELECT max(usr)\
                FROM users")
    result = cur.fetchone()
    if result != None:
        ret = result[0]+1
        return ret
    else:
        return 0

