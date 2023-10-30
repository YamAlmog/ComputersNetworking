import socket
import os
import UDP_shared


UDP_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_server.bind(UDP_shared.BIND)


def send_file_to_receiver(user_socket, filename):
    # Reading file and sending data to user
    file = open(filename, "rb")

    # read first chunk of the file
    data = file.read(UDP_shared.CHUNK_SIZE)
    # In case of empty file
    if len(data) == 0: 
        print(f"{filename} is empty file")
        user_socket.sendto(UDP_shared.EMPTY_FILE, UDP_shared.BIND)
    
    while data:
        # data could be any kind of data, not just text file
        user_socket.sendto(data, UDP_shared.BIND)

        # read the rest of the file. chunk by chunk
        data = file.read(UDP_shared.CHUNK_SIZE)
    
    # File is closed after data is sent
    print(f"Finished sending the data...")
    file.close() 
    
    user_socket.sendto(UDP_shared.MAGIC_END_FILE_KEY, UDP_shared.BIND)



def main():
    while True:
        #UDP_server.listen()
        print(f"[LISTENING] UDP_server is listening on...")

        '''(receiver, address) = UDP_server.accept()
        print("Receiver is connected")'''

        request_file = UDP_server.recvfrom(UDP_shared.CHUNK_SIZE)    

        while request_file != UDP_shared.END_THE_PROGRAM:
            print(request_file)
            if request_file == UDP_shared.LIST_DIR.encode():
                list_dir = os.listdir()
                print("Sending dir list")
                UDP_server.sendto(f"{UDP_shared.LIST_DIR}  {str(list_dir)}".encode(), UDP_shared.BIND)
                
            elif os.path.exists(request_file.decode()):
                print(f"{request_file} exist")
                send_file_to_receiver(UDP_server, request_file.decode())
                
            else:
                print(f"{request_file.decode()} does not exist") 
                UDP_server.sendto(UDP_shared.FILE_NOT_FOUND, UDP_shared.BIND) 
        
            print("requesting another file from user:")
            request_file = UDP_server.recvfrom(UDP_shared.CHUNK_SIZE)
            
    
        print("Close the receiver socket")
        UDP_server.close()   

        

if __name__ == "__main__":
    main() 


   