import socket
import os


PORT = 8820
SERVER_IP = "127.0.0.1"
BIND = (SERVER_IP, PORT)
CHUNK_SIZE = 1024
FILE_NOT_FOUND = "NOFILE"
END_THE_PROGRAM = "DONE"
EMPTY_FILE= "Empty file"
MAGIC_END_FILE_KEY = "$$$<END_OF_FILE>$$$"
server = socket.socket()
server.bind(BIND)


# 2. I want the server to accept request to get files from clients, until the server receives a "DONE" command
# 3. Handle all potential errors that can happen in the program (try/except)


def send_file_to_receiver(user, filename):
    # Reading file and sending data to user
    file = open(filename, "r")
    data = file.read(CHUNK_SIZE) #read the data chank by chank and then send it
    
    if len(data) == 0: #In case of empty file
        print(f"{filename} is empty file")
        user.send(EMPTY_FILE.encode())
    
    while data:
        user.send(data.encode()) # data could be any kind of data, not just text file
        print(f"Sending the data is in progress...")
        data = file.read()  # read the next chunk of data from the file

    file.close()  # File is closed after data is sent
    user.send("MAGIC_END_FILE_KEY".encode())



def main():
    server.listen()
    print(f"[LISTENING] Server is listenin on...")

    (receiver, address) = server.accept()
    print("Receiver is connected")

    while True:
        request_file = receiver.recv(CHUNK_SIZE)
        
        if request_file==END_THE_PROGRAM:
            print("The program has ended")
            break

        elif os.path.exists(request_file):
            print(f"{request_file} is exist")
            send_file_to_receiver(receiver, request_file)
            

        else:
            print(f"{request_file} does not exist") 
            receiver.send(FILE_NOT_FOUND.encode()) # the receiver will asked to try again or otherwise input the key word DONE
            continue


    server.close()
    receiver.close()
