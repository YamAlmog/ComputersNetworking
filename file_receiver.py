import socket

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 8820))

file_name = input('Input filename you want to get: \n') 
my_socket.send(file_name.encode())

 
New_file_name = 'output.txt' # Creating a new file
file = open(New_file_name, "w")
print(f"{New_file_name} has created")


while True: 
    data = my_socket.recv(1024).decode('utf-8') 
    if len(data) == 0: 
        break
    if data == "NOFILE":
        print(f"There isn't file named: {file_name}")
        break
    else:
        print(f"{data}")
        file.write(data) 
        continue 


my_socket.close()



