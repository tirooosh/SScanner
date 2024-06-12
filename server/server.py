import ast
import socket
import userdatabase, testdatabase
import json  # Import json module for parsing JSON responses
from datetime import datetime

# Server details
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 8821
MAX_MSG_SIZE = 2028

# Create a UDP socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.bind((ip, port))

print(f"Server started at ip {ip}")

while True:
    # Receive request from the client
    request, client_address = my_socket.recvfrom(MAX_MSG_SIZE)
    request = request.decode().strip()  # Convert the request to string and trim whitespaces
    print(f"Client sent: {request} at: {datetime.now().strftime('%H:%M:%S')}")

    # Parse the request
    parts = request.split(' ')
    cmd = parts[0]

    # Processing commands
    if cmd == 'EXIT':
        payload = json.dumps({"success": True, "message": "Goodbye!"})
        my_socket.sendto(payload.encode(), client_address)
        break
    elif cmd == 'ALIVE?':
        payload = json.dumps("yes")
        my_socket.sendto(payload.encode(), client_address)
        print("sent " + payload)
    elif cmd == 'LOGIN' and len(parts) == 3:
        email, password = parts[1], parts[2]
        success = userdatabase.login(email, password)
        payload = json.dumps({'success': success})
        print("sent " + payload)
        my_socket.sendto(payload.encode(), client_address)
    elif cmd == 'SIGNUP' and len(parts) == 4:
        name, email, password = parts[1], parts[2], parts[3]
        success = userdatabase.signup(name, email, password)
        payload = json.dumps({'success': success})
        my_socket.sendto(payload.encode(), client_address)
    elif cmd == 'GET_USER_DETAILS' and len(parts) == 2:
        email = parts[1]
        details = userdatabase.get_user_details(email)
        if details:
            print("sent " + details)
            response = json.dumps({"success": True, "details": details})
        else:
            response = json.dumps({"success": False})
        my_socket.sendto(response.encode(), client_address)
    elif cmd == 'CHANGE_PASSWORD' and len(parts) == 3:
        email, new_password = parts[1], parts[2]
        success = userdatabase.change_password(email, new_password)
        payload = json.dumps({'success': success})
        my_socket.sendto(payload.encode(), client_address)
    elif cmd == 'GET_USERNAME' and len(parts) == 2:
        email = parts[1]
        name = userdatabase.get_username(email)
        if name:
            response = json.dumps({"success": True, "name": name})
        else:
            response = json.dumps({"success": False, "message": "User not found"})
        print(response)
        my_socket.sendto(response.encode(), client_address)
    elif cmd == 'CHECK_EMAIL' and len(parts) == 2:
        email = parts[1]
        exists = userdatabase.email_exists(email)
        payload = json.dumps({'exists': exists})
        print("sent " + payload)
        my_socket.sendto(payload.encode(), client_address)
    elif cmd == 'CHANGE_NAME' and len(parts) == 3:
        email, new_name = parts[1], parts[2]
        success = userdatabase.change_name(email, new_name)
        payload = json.dumps({'success': success})
        my_socket.sendto(payload.encode(), client_address)
    elif cmd == 'ADD_TEST_RESULT' and len(parts) == 9:
        url, email_of_searcher = parts[7], parts[8]
        # Extract the parts that make up the lists
        list1_str_parts = parts[1:5]
        list2_str_parts = parts[5:7]

        # Join the parts to form complete list representations
        joined_str1 = ' '.join(list1_str_parts)
        joined_str2 = ' '.join(list2_str_parts)

        # Convert the joined strings to actual lists using ast.literal_eval
        list1 = ast.literal_eval(joined_str1)
        list2 = ast.literal_eval(joined_str2)

        success, message = testdatabase.insert_test_result(str(list1), str(list2), url, email_of_searcher)
        payload = json.dumps({'success': success, 'message': message})
        my_socket.sendto(payload.encode(), client_address)
    elif cmd == 'GET_All_TEST_RESULTS':
        results = testdatabase.retrieve_all_test_results()
        results = results[1:10]
        response = json.dumps({"success": True, "results": results})
        my_socket.sendto(response.encode(), client_address)
    elif cmd == 'GET_TEST_RESULT_FOR_USER' and len(parts) == 2:
        email = parts[1]
        results = testdatabase.retrieve_tests_by_user(email)
        response = json.dumps({"success": True, "results": results})
        my_socket.sendto(response.encode(), client_address)
    elif cmd == 'GET_TEST_RESULTS_FOR_URL' and len(parts) == 2:
        url = parts[1]
        exists, result = testdatabase.get_test_result_by_url(url)
        if exists:
            response = json.dumps({"success": True, "results": result})
        else:
            response = json.dumps({"success": False, "message": result})
        my_socket.sendto(response.encode(), client_address)

    else:
            response = json.dumps({"success": False, "message": "Unknown or malformed request"})
            my_socket.sendto(response.encode(), client_address)

# Close the server socket
my_socket.close()
