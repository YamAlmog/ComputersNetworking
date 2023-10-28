import socket
import os
import shared
import time


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
        user_socket.send(shared.EMPTY_FILE)
    
    while data:
        # data could be any kind of data, not just text file
        user_socket.sendall(data)

        # read the rest of the file. chunk by chunk
        data = file.read(shared.CHUNK_SIZE)
    
    # File is closed after data is sent
    print(f"Finished sending the data...")
    file.close() 
    
    user_socket.sendall(shared.MAGIC_END_FILE_KEY)



def main():
    while True:
        server.listen()
        print(f"[LISTENING] Server is listening on...")

        (receiver, address) = server.accept()
        print("Receiver is connected")

        request_file = receiver.recv(shared.CHUNK_SIZE)    

        while request_file != shared.END_THE_PROGRAM:

            if request_file == shared.LIST_DIR.encode():
                list_dir = os.listdir()
                print("Sending dir list")
                receiver.send(f"{shared.LIST_DIR}  {str(list_dir)}".encode())
                
            elif os.path.exists(request_file.decode()):
                print(f"{request_file} exist")
                send_file_to_receiver(receiver, request_file.decode())
                
            else:
                print(f"{request_file.decode()} does not exist") 
                receiver.send(shared.FILE_NOT_FOUND) 
        
            print("requesting another file from user:")
            request_file = receiver.recv(shared.CHUNK_SIZE)
            
    
        print("Close the receiver socket")
        receiver.close()   

        

if __name__ == "__main__":
    main() 


    # ask the client what IP to connect