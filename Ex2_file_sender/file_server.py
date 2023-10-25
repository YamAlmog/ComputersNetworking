import socket
import os

PORT = 8020
SERVER_IP = "0.0.0.0"
BIND = (SERVER_IP, PORT)
CHUNK_SIZE = 1024
FILE_NOT_FOUND = "NOFILE"
END_THE_PROGRAM = "DONE"
EMPTY_FILE= "Empty file"
MAGIC_END_FILE_KEY = "$$$<--<@>--->$$$"
server = socket.socket()
server.bind(BIND)


def send_file_to_receiver(user_socket, filename):
    # Reading file and sending data to user
    file = open(filename, "r")
    # read first chunk of the file
    data = file.read(CHUNK_SIZE)
    #In case of empty file
    if len(data) == 0: 
        print(f"{filename} is empty file")
        user_socket.send(EMPTY_FILE)
    
    while data:
        # data could be any kind of data, not just text file
        user_socket.send(data) 
        print(f"Sending the data is in progress...")

        # read the rest of the file. chunk by chunk
        data = file.read(CHUNK_SIZE)
    
    # File is closed after data is sent
    file.close()  
    user_socket.send(MAGIC_END_FILE_KEY)



def main():
    server.listen()
    print(f"[LISTENING] Server is listenin on...")

    (receiver, address) = server.accept()
    print("Receiver is connected")

    request_file = receiver.recv(CHUNK_SIZE)
        
    while request_file !=END_THE_PROGRAM:

        if os.path.exists(request_file):
            print(f"{request_file} is exist")
            send_file_to_receiver(receiver, request_file)
            
        else:
            print(f"{request_file} does not exist") 
            receiver.send(FILE_NOT_FOUND) # the receiver will asked to try again or otherwise input the key word DONE
            continue

    if request_file.encode() == END_THE_PROGRAM:
        print("The program has ended")
        server.close()
        receiver.close()

if __name__ == "__main__":
    main()