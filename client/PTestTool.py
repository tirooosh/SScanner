from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def find_and_search(browser, url, search_query):
    """
    This function attempts to find the search bar on a website and search for a given query.

    Args:
        browser: A Selenium WebDriver instance.
        url: The URL of the website to search.
        search_query: The query to search for in the search bar.

    Returns:
        A boolean indicating whether the search was performed successfully.
    """

    browser.get(url)

    try_methods = [
        ("name", "q"),
        ("id", "search-bar"),
        ("css_selector", "input[type='search']")
    ]

    for method, value in try_methods:
        try:
            search_bar = browser.find_element(getattr(By, method.upper()), value)
            search_bar.send_keys(search_query + Keys.RETURN)  # Type the search query and press Enter
            return True  # Search was successful
        except NoSuchElementException:
            pass  # If not found, continue trying other methods

    # Try searching within a form (fallback)
    try:
        search_form = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        search_input = search_form.find_element(By.NAME, "q")  # Common search input name within form
        search_input.send_keys(search_query + Keys.RETURN)  # Type the search query and press Enter
        return True  # Search was successful
    except (NoSuchElementException, TimeoutException):
        pass  # If not found or form not loaded within timeout

    # No search bar found using any methods
    return False

# Example usage
browser = webdriver.Chrome()
success = find_and_search(browser, "https://redtiger.labs.overthewire.org/level1.php", "tirosh")

if success:
    print("Search performed successfully.")
else:
    print("Search bar not found on this website or search failed.")

# Add a delay or wait here if you want to see the search results before the browser closes
# browser.quit()
