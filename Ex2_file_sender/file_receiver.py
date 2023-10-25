import socket

PORT = 8820
SERVER_IP = "127.0.0.1"
CHUNK_SIZE = 1024
FILE_NOT_FOUND = "NOFILE"
END_THE_PROGRAM = "DONE"
EMPTY_FILE= "Empty file"
MAGIC_END_FILE_KEY = "$$$<END_OF_FILE>$$$"

# connect and return socket
def connect_to_server(socket):
    try: 
        socket = socket.socket()
        socket.connect((SERVER_IP, PORT))
        return socket
    except:
        raise Exception("Could not connect")

# returns file name 
def get_user_request():
   user_input = input("Input filename you want to get, don't forget add the suffix\n"
                      "To exit the program, input the word 'DONE'\n "
                      "Input your request here:")
   return user_input



def get_file_from_server(socket, file_name):
    # create copy file 
    file = open(file_name, "w")
    print(f"{file_name} has created")

    # send file name to server to check if exsist
    socket.send(file_name.encode())

    # get chunk by chunk the file from server
    # until the end of file is received
    data = socket.recv(CHUNK_SIZE)

    while data != MAGIC_END_FILE_KEY:
        if data == EMPTY_FILE:
            print("The requested file is empty")
            break
        elif data == FILE_NOT_FOUND:
            raise Exception("File not found")
        else:
            file.write(data)
            data = socket.recv(CHUNK_SIZE)
            continue
    
    file.close()


def main():

    try:
        server_socket = connect_to_server()
    except Exception:
        print("Connection Error: something went wrong, Apologies for the inconvenience.")
        return

    user_request= get_user_request()
    while user_request != END_THE_PROGRAM: 

        try:
            get_file_from_server(server_socket, user_request)
        except Exception:
            print(f"There isn't file named: {user_request}")


        user_request= get_user_request()

    server_socket.close()





