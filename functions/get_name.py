# gets a name from the sqlite database.
# if it exists then it returns the name. Else returns None.
def get_name(conn, uid):
    c = conn.cursor()
    c.execute("\
              SELECT u.name\
              FROM users u\
              WHERE u.usr = :uid",
              {"uid":uid})
    name = c.fetchone()
    return name[0]