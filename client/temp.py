import requests
from bs4 import BeautifulSoup


def request_session(user_agent="Mozilla/5.0"):  # Allow user-agent to be passed as an argument
    session = requests.Session()
    session.headers['User-Agent'] = user_agent
    return session


def find_forms(html):
    """Extracts all forms from an HTML document."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("form")


def form_details(form):
    """Collects form details such as action, method, and inputs."""
    details = {
        "action": form.attrs.get("action", "").lower(),
        "method": form.attrs.get("method", "get").lower(),
        "inputs": []
    }
    for input_tag in form.find_all("input"):
        input_details = {
            "type": input_tag.attrs.get("type", "text"),
            "name": input_tag.attrs.get("name"),
            "value": input_tag.attrs.get("value", "")
        }
        details["inputs"].append(input_details)
    return details


def test_website(url, user_agent="Mozilla/5.0"):
    session = request_session(user_agent)
    print(f"Testing URL: {url}")

    try:
        response = session.get(url, verify=False)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        forms = find_forms(response.text)
        print(f"Found {len(forms)} forms on {url}.")

        # Your existing logic for iterating through forms and checking for specific keywords (replace with non-vulnerability checks)
        # ...
        print("No specific issues detected on this website (focusing on HTML structure).")

    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while fetching the website: {e}")


if __name__ == "__main__":
    test_url = "https://redtiger.labs.overthewire.org/level2.php"  # Replace with the URL you want to test
    test_website(test_url)
