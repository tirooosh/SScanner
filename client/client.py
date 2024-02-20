import socket
import json  # Import json module for parsing JSON responses

ip = "127.0.0.1"
port = 8821
MAX_MSG_SIZE = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def parse_response(response):
    try:
        # Try to parse the JSON response
        return json.loads(response)
    except json.JSONDecodeError:
        # If response is not in JSON format, return the raw response
        return response


def signup(name, email, password):
    my_socket.sendto(f"SIGNUP {name} {email} {password}".encode(), (ip, port))
    response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    my_socket.close()
    return response.decode()


def login(email, password):
    my_socket.sendto(f"LOGIN {email} {password}".encode(), (ip, port))
    response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    my_socket.close()
    return response.decode()


def change_password(email, new_password):
    my_socket.sendto(f"CHANGE_PASSWORD {email} {new_password}".encode(), (ip, port))
    response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    my_socket.close()
    return response.decode()


def change_name(email, new_name):
    my_socket.sendto(f"CHANGE_NAME {email} {new_name}".encode(), (ip, port))
    response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    my_socket.close()
    return response.decode()


def get_user_details(email):
    my_socket.sendto(f"GET_USER_DETAILS {email}".encode(), (ip, port))
    response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    my_socket.close()
    return parse_response(response.decode())


def get_username(email):
    my_socket.sendto(f"GET_USERNAME {email}".encode(), (ip, port))
    response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    my_socket.close()
    return response.decode()


def email_exists(email):
    my_socket.sendto(f"CHECK_EMAIL {email}".encode(), (ip, port))
    response, _ = my_socket.recvfrom(MAX_MSG_SIZE)
    my_socket.close()
    return response.decode()
