import socket
import json  # Import json module for parsing JSON responses

IP = "127.0.0.1"
PORT = 8821
MAX_MSG_SIZE = 1024


def send_request_and_get_response(request_message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.sendto(request_message.encode(), (IP, PORT))
            response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
        return json.loads(response.decode())
    except Exception as e:
        print(f"Error sending or receiving data: {e}")
        return {}


def signup(name, email, password):
    response = send_request_and_get_response(f"SIGNUP {name} {email} {password}")
    return response.get("success", False)


def login(email, password):
    response = send_request_and_get_response(f"LOGIN {email} {password}")
    return response.get("success", False)


def change_password(email, new_password):
    response = send_request_and_get_response(f"CHANGE_PASSWORD {email} {new_password}")
    return response.get("success", False)


def change_name(email, new_name):
    response = send_request_and_get_response(f"CHANGE_NAME {email} {new_name}")
    return response.get("success", False)


def get_user_details(email):
    response = send_request_and_get_response(f"GET_USER_DETAILS {email}")
    # Assuming the server sends back a detailed response for user details
    # You may want to return the entire response or just the success status based on your application logic
    return response


def get_username(email):
    response = send_request_and_get_response(f"GET_USERNAME {email}")
    return response.get("name", "")


def email_exists(email):
    response = send_request_and_get_response(f"CHECK_EMAIL {email}")
    return response.get("exists", False)


def add_test_result(test1, test2, url, email_of_searcher):
    response = send_request_and_get_response(f"ADD_TEST_RESULT {test1} {test2} {url} {email_of_searcher}")
    return response.get("success", False), response.get("message", "")

def get_test_results():
    response = send_request_and_get_response("GET_TEST_RESULTS")
    if response.get("success", False):
        return response.get("results", [])
    else:
        return []


if __name__ == '__main__':
    # Example usage
    email = "tiroshtayouri@gmail.com"
    test1 = "2"
    test2 = "2"
    url = "http://example.com/result1"
    username_of_searcher = "tirosh"

    # Add a test result
    success, message = add_test_result(test1, test2, url, username_of_searcher)
    print((test1, test2, url, username_of_searcher))
    print(f"Add Test Result: Success={success}, Message={message}")

    # # Retrieve test results
    # results = get_test_results()
    # print(f"Test Results: {results}")
