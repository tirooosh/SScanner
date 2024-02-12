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


# Main function to demonstrate functionality
def main():
    setup_database()

    # Signup a new user
    name = "John Doe"
    email = "john@example.com"
    password = "123456"
    signup_status, message = signup(name, email, password)
    print(message)

    # Prompt for login
    email_input = input("Enter email: ")
    password_input = input("Enter password: ")
    login_status, message = login(email_input, password_input)
    print(message)


if __name__ == '__main__':
    main()
