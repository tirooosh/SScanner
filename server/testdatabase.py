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
        sqltest TEXT NOT NULL,
        xsstest TEXT NOT NULL,
        url TEXT NOT NULL,
        time_of_taking TEXT NOT NULL,
        email_of_searcher TEXT NOT NULL
    );
    """
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_tests_table)
    else:
        print("Error! Cannot create the database connection.")


def insert_test_result(test1, test2, url, username_of_searcher):
    setup_database()
    """Insert a new test result into the test_results table."""
    conn = create_connection("pentestResults.db")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = conn.cursor()
        sql = '''INSERT INTO test_results(sqltest, xsstest, url, time_of_taking, email_of_searcher)
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


def retrieve_all_test_results():
    setup_database()
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

def retrieve_tests_by_user(email):
    setup_database()
    """Retrieve test results for a specific user identified by their email."""
    conn = create_connection("pentestResults.db")
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM test_results WHERE email_of_searcher=?"
        cursor.execute(sql, (email,))
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(e)
        return None
    finally:
        if conn:
            conn.close()

def get_test_result_by_url(url):
    setup_database()
    """Retrieve the first test result for a specific URL."""
    conn = create_connection("pentestResults.db")
    try:
        cursor = conn.cursor()
        # Select the oldest entry for the given URL
        sql = "SELECT * FROM test_results WHERE url = ? ORDER BY time_of_taking ASC LIMIT 1"
        cursor.execute(sql, (url,))
        result = cursor.fetchone()  # fetchone() retrieves the first row of the query
        if result:
            return True, result
        else:
            return False, "No previous test results found for this URL."
    except sqlite3.Error as e:
        print(e)
        return False, f"Database error: {e}"
    finally:
        if conn:
            conn.close()




def main():
    setup_database()

    # Example usage:
    insert_status, message = insert_test_result("Test1 data", "Test2 data", "http://example.com", "user123@gmail.com")
    print(message)
    print(retrieve_tests_by_user("user123"))




if __name__ == '__main__':
    main()
