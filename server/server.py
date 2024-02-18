import socket


# הגדרת פרטי השרת
ip = "127.0.0.1"
port = 8821
MAX_MSG_SIZE = 1024

# יצירת סוקט לשרת
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.bind((ip, port))

print("Server started")

while True:

    # קבלת בקשה מהלקוח
    request, client_address = my_socket.recvfrom(MAX_MSG_SIZE)
    request = request.decode().strip()  # המרת הבקשה למחרוזת והסרת רווחים מתחילתה וסופה
    print("client sent = " + request[3:len(request)])

    if request == 'EXIT':
        # בקשת EXIT - סגירת החיבור עם הלקוח ויציאה מהלולאה
        my_socket.sendto("Goodbye!".encode(), client_address)
        break

    else:
        # בקשה לא מוכרת - שליחת הודעת שגיאה ללקוח
        error_message = "Unknown request"
        my_socket.sendto(error_message.encode(), client_address)

# סגירת הסוקט של השרת
my_socket.close()
