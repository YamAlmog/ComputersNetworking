import socket



def chating(socket):
    while True:
        msg_to_send = input('Ente your msg:\n')
        socket.send(msg_to_send.encode())

        friend_msg = socket.recv(1024).decode('utf-8')
        print("Your friend sent:\n" + friend_msg)

        if msg_to_send or friend_msg == 'Exit':
            socket.close()
            break

def start(socket):
    server_message = socket.recv(1024).decode('utf-8')

    if server_message == "Entre name:":
        name = input('Enter your name:\n')
        socket.send(name.encode())
        print('To exit from the chat room any time, please enter the word: Exit')
        chating(socket)
    
    else:
        print('There was an eror with the server, try next time.')
        socket.close()


def main():
    my_socket = socket.socket()
    my_socket.connect(("0.0.0.0", 8002))
    print("client is connecting\n")
    print("waiting for the server to response\n")
    start(my_socket)