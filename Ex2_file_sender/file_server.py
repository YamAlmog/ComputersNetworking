import socket
import os


PORT = 8820
SERVER_IP = "127.0.0.1"
BIND = (SERVER_IP, PORT)
HEADER = 1024
server = socket.socket()
server.bind(BIND)
server.listen()
print(f"[LISTENING] Server is listenin on...")


# 1. Where is main function??? you should always have a 'main' function as entry point to your program
#    also I DONT SEE ANY FUNCTIONS IN THIS FILE
# 2. I want the server to accept request to get files from clients, until the server receives a "DONE" command
# 3. Handle all potential errors that can happen in the program (try/except)


def send_file_to_receiver(user, filename):
    # Reading file and sending data to user
    file = open(filename, "r")
    data = file.read()
    if not data:
        print(f"{filename} is empty file")

    while data:
        print(f"{data}")
        user.send(str(data).encode())
        data = file.read()  # read the next chunk of data from the file

    file.close()  # File is closed after data is sent


def search_file(user_socket, file_name, search_path="."):
    # you dont need to to do that . (I bet you dont understand what you did here, but you just copied it from stackoverflow)
    # you can use os.path.exists(file_name) to check if the file exists (which is simpler and more readable)
    # or you can use open() function with 'try/except' to check if the file exists

    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            print(f"{file_name} is exist")

            send_file_to_receiver(user_socket, file_name)

        else:
            # does not exist !!!!!!!  ()
            print(f"{file_name} is Not exist")
            # all MAGIC STRINGS SHOULD BE DEFINED AS CONSTANTS AT THE BEGINNING OF THE FILE
            user_socket.send("NOFILE".encode())
            return


(receiver, address) = server.accept()
print("Receiver is connected")
# 1. why do you need to decode the data? you should send the data as bytes and not as string
#    If I'm transferring a binary file, you will not be able to decode it as string (!)
file_name = receiver.recv(1024).decode("utf-8")
search_file(receiver, file_name, search_path=".")


server.close()
receiver.close()
