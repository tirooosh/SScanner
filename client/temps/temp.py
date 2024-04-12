import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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


def form_details(form):
    """ Extract details from the form """
    details = {
        'action': form.attrs.get("action", ""),
        'method': form.attrs.get("method", "get").lower(),
        'inputs': [{
            "type": input_tag.attrs.get("type", "text"),
            "name": input_tag.attrs.get("name"),
            "value": input_tag.attrs.get("value", "")
        } for input_tag in form.find_all("input")]
    }
    return details


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
    print(f"[+] Detected {len(forms)} forms on {url}.")

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
                    print(f"SQL injection vulnerability detected in form at {target_url}")
                else:
                    print("No SQL injection vulnerability detected.")
            except requests.RequestException as e:
                print(f"Request to {target_url} failed: {e}")


if __name__ == "__main__":
    test_url = "http://testphp.vulnweb.com/artists.php?artist=1"
    sql_injection_scan(test_url)
