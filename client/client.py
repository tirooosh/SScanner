import socket
import json  # Import json module for parsing JSON responses

ip = "127.0.0.1"
port = 8821
MAX_MSG_SIZE = 1024


def send_request_and_get_response(request_message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.sendto(request_message.encode(), (ip, port))
        response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    return json.loads(response.decode())


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
    # Depending on how you want to handle the response, you might directly return it
    # or extract specific fields like success or username
    return response.get("username", "")


def email_exists(email):
    response = send_request_and_get_response(f"CHECK_EMAIL {email}")
    return response.get("exists", False)
