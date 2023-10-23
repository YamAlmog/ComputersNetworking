import socket
import os


PORT= 8820
SERVER_IP= "127.0.0.1"
BIND=(SERVER_IP,PORT)
HEADER=1024
server=socket.socket()
server.bind(BIND)
server.listen()
print(f"[LISTENING] Server is listenin on...")


def send_file_to_receiver(user ,filename):
   
    # Reading file and sending data to user 
    file = open(filename, "r")    
    data = file.read() 
    if not data: 
        print(f"{filename} is empty file")
        
    while data: 
        print(f'{data}')
        user.send(str(data).encode()) 
        data = file.read() # read the next chunk of data from the file
        
    file.close() # File is closed after data is sent   

  
def search_file(user_socket,file_name, search_path="."):
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            print(f'{file_name} is exist')
            
            send_file_to_receiver(user_socket ,file_name)

        else:
            print(f'{file_name} is Not exist')
            user_socket.send("NOFILE".encode())
            return 
        


(receiver, address) = server.accept()
print("Receiver is connected")
file_name=receiver.recv(1024).decode('utf-8')
search_file(receiver,file_name, search_path=".")


server.close()
receiver.close()
