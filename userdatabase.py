import sqlite3


# Database setup and connection
def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def setup_database():
    database = "usersTable.db"
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    email text NOT NULL UNIQUE,
                                    password text NOT NULL
                                );"""
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_users_table)
    else:
        print("Error! Cannot create the database connection.")


# User management
def signup(name, email, password):
    conn = create_connection("usersTable.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email=?"
    cursor.execute(query, (email,))
    if cursor.fetchone():
        return False, "Email already exists."
    insert_sql = '''INSERT INTO users(name, email, password) VALUES(?,?,?)'''
    cursor.execute(insert_sql, (name, email, password))
    conn.commit()
    return True, "User created successfully."


def login(email, password):
    conn = create_connection("usersTable.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email=? AND password=?"
    cursor.execute(query, (email, password))
    record = cursor.fetchone()
    if record:
        return True, "Login successful."
    else:
        return False, "Login failed. Incorrect email or password."


def email_exists(email):
    conn = create_connection("usersTable.db")
    cursor = conn.cursor()
    query = "SELECT 1 FROM users WHERE email=?"
    cursor.execute(query, (email,))
    return cursor.fetchone() is not None


def change_password(email, new_password):
    if not email_exists(email):
        return False, "Email does not exist."
    conn = create_connection("usersTable.db")
    cursor = conn.cursor()
    update_sql = "UPDATE users SET password = ? WHERE email = ?"
    cursor.execute(update_sql, (new_password, email))
    conn.commit()
    return True, "Password changed successfully."


def change_name(email, new_name):
    if not email_exists(email):
        return False, "Email does not exist."
    conn = create_connection("usersTable.db")
    cursor = conn.cursor()
    update_sql = "UPDATE users SET name = ? WHERE email = ?"
    cursor.execute(update_sql, (new_name, email))
    conn.commit()
    return True, "Name changed successfully."


def get_user_details(email):
    """Fetch and return user details by email."""
    conn = create_connection("usersTable.db")
    cursor = conn.cursor()
    query = "SELECT email, password, name FROM users WHERE email=?"
    cursor.execute(query, (email,))
    user_details = cursor.fetchone()

    if user_details:
        # user_details will be a tuple in the format (email, password, name)
        return {
                   "email": user_details[0],
                   "password": user_details[1],
                   "name": user_details[2]
               }, "User details fetched successfully."
    else:
        return None, "User not found."


# Main function to demonstrate functionality
def main():
    setup_database()

    # Signup a new user
    name = "John Doe"
    email = "johnT@example.com"
    password = "123456"
    signup_status, message = signup(name, email, password)
    print(message)
    print("current email and password: " + str(get_user_details(email)))

    # Assume user logged in here and wants to change their password and name
    new_password = "newpassword124"
    change_password(email, new_password)

    print("current email and password: "+str(get_user_details(email)))
    # # Prompt for login with new credentials
    # email_input = input("Enter email: ")
    # password_input = input("Enter new password: ")  # Prompting for the new password
    # login_status, message = login(email_input, password_input)
    # print(message)


if __name__ == '__main__':
    main()
