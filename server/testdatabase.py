import sqlite3
from datetime import datetime


def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def setup_database():
    database = "pentestResults.db"
    sql_create_tests_table = """
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY,
        test1 TEXT NOT NULL,
        test2 TEXT NOT NULL,
        url TEXT NOT NULL,
        time_of_taking TEXT NOT NULL,
        username_of_searcher TEXT NOT NULL
    );
    """
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_tests_table)
    else:
        print("Error! Cannot create the database connection.")


def insert_test_result(test1, test2, url, username_of_searcher):
    """Insert a new test result into the test_results table."""
    conn = create_connection("pentestResults.db")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = conn.cursor()
        sql = '''INSERT INTO test_results(test1, test2, url, time_of_taking, username_of_searcher)
                 VALUES(?,?,?,?,?)'''
        cursor.execute(sql, (test1, test2, url, timestamp, username_of_searcher))
        conn.commit()
        return True, "Test result added successfully."
    except sqlite3.Error as e:
        print(e)
        return False, "Failed to add test result."
    finally:
        if conn:
            conn.close()


def retrieve_test_results():
    """Retrieve all test results from the test_results table."""
    conn = create_connection("pentestResults.db")
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM test_results"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    finally:
        if conn:
            conn.close()


def main():
    setup_database()

    # Example usage:
    insert_status, message = insert_test_result("Test1 data", "Test2 data", "http://example.com", "user123")
    print(message)

    results = retrieve_test_results()
    for result in results:
        print(result)


if __name__ == '__main__':
    main()
