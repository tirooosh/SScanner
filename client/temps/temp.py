import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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

if __name__ == "__main__":
    test_url = "http://testphp.vulnweb.com/artists.php?artist=1"
    session = request_session()
    scan_sql_injection(test_url, session)
