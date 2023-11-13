from tabulate import tabulate
from functions import select_usr as sr

# enters the list followers submenu
def list_followers(conn, usr):

    print('')

    # get all followers from sql
    c = conn.cursor()
    c.execute('select flwer, name from follows, users WHERE usr = flwer and flwee=:usr', {"usr":usr})
    rows = c.fetchall() 

    flwer_dict = {}

    for row in rows:
        flwer_dict[row[0]] = row[1]

    # enter submenu control flow. display commands, and act on those commands.
    while True:
        print("\n\033[1m\033[4mFollowers:\033[0m")
        print(tabulate(rows, headers=["userId", "Name"], tablefmt='orgtbl'))
        print("\n\033[1m\033[4mChoose an action:\033[0m\
                \nsel <usr>\t- select a follower\
                \ne\t\t- exit to main menu"
        )

        # get command
        command = input().lower().split()
        if len(command) == 0:
            print("Please enter a command.")
            continue
        action = command[0]
        arg1 = None
        if len(command) == 2:
            arg1 = command[1]

        if action == "e":   # exit command
            return
        elif action == "sel":   # select follower command
            if arg1 == None:
                print('"sel" command expects a second argument.')
                continue
            if not arg1.isdigit():
                print('Second argument must be of type int.')
                continue

            arg1 = int(arg1)

            if arg1 not in flwer_dict.keys():
                print(arg1, 'is not your follower.')
                continue
        
            # finally if the user id given is valid, select that user.
            sr.select_user(conn, arg1, usr)
