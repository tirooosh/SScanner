import socket

ip = "127.0.0.1"
port = 8821
MAX_MSG_SIZE = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter a message ('exit' to quit): ")
    if message == 'exit':
        break

    my_socket.sendto(message.encode(), (ip, port))
    response, remote_address = my_socket.recvfrom(MAX_MSG_SIZE)
    data = response.decode()
    print("The server sent: " + data)

my_socket.close()
