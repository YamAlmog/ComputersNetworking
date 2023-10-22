import socket

my_socket = socket.socket()
my_socket.connect(("192.168.1.101", 8002))

print("client is connecting")

name = input('Ente your name:\n')
my_socket.send(name.encode())

print("waiting for the server to response")
server_message = my_socket.recv(1024).decode('utf-8')

print("The server sent:\n" + server_message)

while True:
    msg_to_send = input('Ente msg to your friend:\n')
    my_socket.send(msg_to_send.encode())

    friend_msg = my_socket.recv(1024).decode('utf-8')
    print("Your friend sent:\n" + friend_msg)

my_socket.close()



# def client_send():
#     while True:
#         message = f'{nickname}: {input("")}'
#         client.send(message.encode('utf-8'))


# while True:
#     try:
#         message = client.recv(1024).decode('utf-8')
#         if message == "name?":
#             client.send(nickname.encode('utf-8'))
    


