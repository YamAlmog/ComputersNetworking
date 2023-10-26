import socket
import os
import shared


server = socket.socket()
server.bind(shared.BIND)


def send_file_to_receiver(user_socket, filename):
    # Reading file and sending data to user
    file = open(filename, "rb")
    # read first chunk of the file
    data = file.read(shared.CHUNK_SIZE)
    #In case of empty file
    if len(data) == 0: 
        print(f"{filename} is empty file")
        user_socket.send(shared.EMPTY_FILE.encode('utf-8'))
    
    while data:
        # data could be any kind of data, not just text file
        user_socket.send(data)
        print(f"Sending the data is in progress...")

        # read the rest of the file. chunk by chunk
        data = file.read(shared.CHUNK_SIZE)
    
    # File is closed after data is sent
    print(f"Finish sendin the data...")
    file.close()  
    user_socket.send(shared.MAGIC_END_FILE_KEY.encode('utf-8'))



def main():
    server.listen()
    print(f"[LISTENING] Server is listenin on...")

    (receiver, address) = server.accept()
    print("Receiver is connected")

    request_file = receiver.recv(shared.CHUNK_SIZE)
    print(request_file.decode())
        
    while request_file !=shared.END_THE_PROGRAM:

        if os.path.exists(request_file):
            print(f"{request_file} exist")
            send_file_to_receiver(receiver, request_file)
            
        else:
            print(f"{request_file} does not exist") 
            receiver.send(shared.FILE_NOT_FOUND) 
    
        print("requesting another file from user:")
        request_file = receiver.recv(shared.CHUNK_SIZE)

    if request_file.encode() == shared.END_THE_PROGRAM:
        print("The program has ended")
        server.close()
        receiver.close()

    

if __name__ == "__main__":
    main()