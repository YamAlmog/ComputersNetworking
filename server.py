import socket


PORT= 8002
SERVER_IP= socket.gethostbyname(socket.gethostname())
print(SERVER_IP)
BIND=(SERVER_IP,PORT)
HEADER=1024

server=socket.socket()
server.bind(BIND)

server.listen()
print(f"[LISTENING] Server is listenin on {SERVER_IP}")


(client_1, address_1) = server.accept()
print("Client 1 connected")
(client_2, address_2) = server.accept()
print("Client 2 connected")


name_1 = client_1.recv(1024).decode('utf-8')
print(f"Client 1 name: {name_1}")

name_2 = client_2.recv(1024).decode('utf-8')
print(f"Client 2 name: {name_2}")

client_1.send(f'{name_2} has connected to the chat room'.encode('utf-8'))
client_2.send(f'{name_1} has connected to the chat room'.encode('utf-8'))

# ------------------------------------------------------------------------------

while True:
    print(f"Waiting for message from {name_1}")
    message_1 = client_1.recv(1024)

    client_2.send(message_1)
    print(f"{name_1} sent: {message_1}")

    print(f"Waiting for message from {name_2}")
    message_2 = client_2.recv(1024)

    client_1.send(message_2)
    print(f"{name_2} sent: {message_2}")


client_1.close()
client_2.close()
server.close()
