import getpass

# Argument is the database connection
# Returns if the login has succeeded and the username of the account that was logged into
def login(conn):
    print("\n\033[1m\033[4mLogging in:\033[0m")
    username = input("Enter your user id: ")
    password = getpass.getpass("Enter your password: ", stream=None)
 
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE usr = ? AND pwd = ?", (username, password))
    result = cursor.fetchone()

    if result:
        print("Login successful!")
        return username
    else:
        print("Login failed. Please try again.")
        return None
