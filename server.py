import socket

PORT= 20
SERVER_IP= '192.168.1.101'
BIND=(SERVER_IP,PORT)
HEADER=1024
server=socket.socket()
server.bind(BIND)


# -----------------handle_client func------------------------------------------
def handle_client(client_1, client_2, name_1, name_2):

    while True:
        print(f"Waiting for message from {name_1}")
        message_1 = client_1.recv(1024).decode('utf-8')

        client_2.send(message_1.encode('utf-8'))
        print(f"{name_1} sent: {message_1}")

        print(f"Waiting for message from {name_2}")
        message_2 = client_2.recv(1024).decode('utf-8')

        client_1.send(message_2.encode('utf-8'))
        print(f"{name_2} sent: {message_2}")

        if message_1 or message_2 == 'Exit':
            break


    client_1.close()
    client_2.close()
    server.close()

# ---------------------start func--------------------------------------------
def start():
    (user_1, address_1) = server.accept()
    print("User 1 connected")
    (user_2, address_2) = server.accept()
    print("User 2 connected")

    server_msg = "Entre name:"
    user_1.send(f'{server_msg}'.encode('utf-8'))
    user_2.send(f'{server_msg}'.encode('utf-8'))

    name_1 = user_1.recv(1024).decode('utf-8')
    print(f"User 1 name: {name_1}")

    name_2 = user_2.recv(1024).decode('utf-8')
    print(f"User 2 name: {name_2}")

    user_1.send(f'{name_2} has connected to the chat room'.encode('utf-8'))
    user_2.send(f'{name_1} has connected to the chat room'.encode('utf-8'))

    handle_client(user_1, user_2, name_1, name_2)


server.listen()
print(f"[LISTENING] Server is listenin on...")
start()
