import socket


# CR: Where is main function??? you should always have a 'main' function as entry point to your program
# also I DONT SEE ANY FUNCTIONS IN THIS FILE


# CR: Server IP SHOULD BE CONST, ALSO PORT
my_socket = socket.socket()

# CR: what happends if the server is not running? you should handle this case! and exit the program with a message to the user
# all potential errors should be handled !
my_socket.connect(("127.0.0.1", 8820))

file_name = input("Input filename you want to get: \n")
my_socket.send(file_name.encode())


# output file should be named exactly as the input file name.
# I want the ability to transfer any kind of file, not only text files.

New_file_name = "output.txt"
file = open(New_file_name, "w")
print(f"{New_file_name} has created")


# I want the program to ask users for file names to get from server, until the user enters 'exit' or 'quit'

while True:
    # 1. why do you need to decode the data? you should send the data as bytes and not as string
    #    If I'm transferring a binary file, you will not be able to decode it as string (!)
    # 2. you use 'while True' but when the file ends, you dont know when to stop reading from the socket
    #    and this recv function blocks the code until it gets data from the socket (program will stuck here and never exit !)
    data = my_socket.recv(1024).decode("utf-8")
    if len(data) == 0:
        break

    # all MAGIC STRINGS SHOULD BE DEFINED AS CONSTANTS AT THE BEGINNING OF THE FILE
    if data == "NOFILE":
        print(f"There isn't file named: {file_name}")
        break
    else:
        print(f"{data}")

        # when do you close the file ??? you should close the file after you finish writing to it
        file.write(data)
        continue


my_socket.close()
