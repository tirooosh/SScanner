import socket
import json  # Import json module for parsing JSON responses

IP = "127.0.0.1"
PORT = 8821
MAX_MSG_SIZE = 1024


def send_request_and_get_response(request_message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.sendto(request_message.encode(), (IP, PORT))
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
    print(response.get("success"))
    return response.get("name", "")


def email_exists(email):
    response = send_request_and_get_response(f"CHECK_EMAIL {email}")
    return response.get("exists", False)

if __name__ == '__main__':
    name = "tirosh"
    email = "tiroshtayouri@gmail.com"
    password = "tirosh45"
    print(get_username(email))
