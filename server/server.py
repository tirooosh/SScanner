import socket
import userdatabase
import json  # Import json module for parsing JSON responses


# Server details
ip = "127.0.0.1"
port = 8821
MAX_MSG_SIZE = 1024

# Create a UDP socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.bind((ip, port))

print("Server started")

while True:
    # Receive request from the client
    request, client_address = my_socket.recvfrom(MAX_MSG_SIZE)
    request = request.decode().strip()  # Convert the request to string and trim whitespaces
    print(f"Client sent: {request}")

    # Parse the request
    parts = request.split(' ')
    cmd = parts[0]

    # Processing commands
    if cmd == 'EXIT':
        my_socket.sendto("Goodbye!".encode(), client_address)
        break
    elif cmd == 'LOGIN' and len(parts) == 3:
        email, password = parts[1], parts[2]
        success = userdatabase.login(email, password)
        my_socket.sendto(success.encode(), client_address)
    elif cmd == 'SIGNUP' and len(parts) == 4:
        name, email, password = parts[1], parts[2], parts[3]
        success = userdatabase.signup(name, email, password)
        my_socket.sendto(success.encode(), client_address)
        # Inside the server loop, adjust the response construction:

    elif cmd == 'GET_USER_DETAILS' and len(parts) == 2:
        email = parts[1]
        details, message = userdatabase.get_user_details(email)
        if details:
            response = json.dumps({"success": True, "name": details['name'], "email": details['email']})
        else:
            response = json.dumps({"success": False, "message": message})
        my_socket.sendto(response.encode(), client_address)

    elif cmd == 'CHANGE_PASSWORD' and len(parts) == 3:  # Assuming correct format now includes old_password
        email, new_password = parts[1], parts[2]
        success = userdatabase.change_password(email, new_password)
        my_socket.sendto(success.encode(), client_address)
    elif cmd == 'GET_USERNAME' and len(parts) == 2:
        email = parts[1]
        name = userdatabase.get_username(email)
        my_socket.sendto(name.encode(), client_address)
    else:
        response = json.dumps({"success": False, "message": "Unknown or malformed request"})
        my_socket.sendto(response.encode(), client_address)

# Close the server socket
my_socket.close()
