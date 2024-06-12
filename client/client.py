import socket
import json  # Import json module for parsing JSON responses
import hashlib

IP = "localhost"
PORT = 8821
MAX_MSG_SIZE = 2028


def send_request_and_get_response(request_message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.sendto(request_message.encode(), (IP, PORT))
            response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
        return json.loads(response.decode())
    except Exception as e:
        print(f"Error sending or receiving data: {e}")
        return {}


def check_server():
    try:
        response = send_request_and_get_response("ALIVE?")
        if response == "yes":
            return True
    except Exception as e:
        return False


def hash_password(password):
    # Encode the password to bytes, then hash it and get a hexadecimal digest
    return hashlib.sha224(password.encode()).hexdigest()


def signup(name, email, password):
    hashed_password = hash_password(password)
    # Constructing the signup request string
    response = send_request_and_get_response(f"SIGNUP {name} {email} {hashed_password}")
    return response.get("success", False)


def login(email, password):
    hashed_password = hash_password(password)
    response = send_request_and_get_response(f"LOGIN {email} {hashed_password}")
    return response.get("success", False)


def change_password(email, new_password):
    hashed_password = hash_password(new_password)
    response = send_request_and_get_response(f"CHANGE_PASSWORD {email} {hashed_password}")
    return response.get("success", False)


def change_name(email, new_name):
    response = send_request_and_get_response(f"CHANGE_NAME {email} {new_name}")
    return response.get("success", False)


def get_user_details(email):
    response = send_request_and_get_response(f"GET_USER_DETAILS {email}")
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


def get_all_test_results():
    response = send_request_and_get_response("GET_All_TEST_RESULTS")
    if response.get("success", False):
        return response.get("results", [])
    else:
        return []


def get_results_from_user(email):
    response = send_request_and_get_response(f"GET_TEST_RESULT_FOR_USER {email}")
    if response.get("success", False):
        return response.get("results", [])
    else:
        return []


def get_results_from_url(url):
    response = send_request_and_get_response(f"GET_TEST_RESULTS_FOR_URL {url}")
    if response.get("success", True):
        res = response.get('results', [])
        res = res[1:3]
        return res
    else:
        return None


if __name__ == '__main__':
    # Example usage
    # email = "user123@gmail.com"
    # test1 = [False, None, False, False]
    # test2 = [True, True]
    # url = "http://testphp.vulnweb.com/artists.php?artist=1"
    # username_of_searcher = "tirosh"
    #
    # add_test_result(test1, test2, url, email)

    # Retrieve test results
    # results = get_results_from_url(url)
    # print(f"Test Results: {results}")
    print(get_all_test_results())