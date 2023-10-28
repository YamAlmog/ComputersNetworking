import socket
import os
import shared
from errors import *
        
# connect and return socket
def connect_to_server():
    SERVER_IP = input("Pleas input the IP to connect with: ")
    try: 
        server_socket = socket.socket()
        server_socket.connect((SERVER_IP, shared.PORT))
        return server_socket
    except socket.error as e:
        raise Exception(f"Could not connect: {str(e)}")

# returns file name 
def get_user_request():
   user_input = input("Input filename you want to get, don't forget add the suffix\n"
                      "To exit the program, input the word 'DONE'\n"
                      "Input your request here:")
   return user_input



def get_file_from_server(socket, file_name):
    # send file name to server to check if exsist
    socket.send(file_name.encode('utf-8'))

    # get first chunk of the file from server
    data = socket.recv(shared.CHUNK_SIZE)

    # print(f"Data received:\n {data}")

    if shared.LIST_DIR.encode() in data:
        print("-" * 10 + "[DIR LIST]" + "-" * 10)
        dir_list = data.decode().replace(shared.LIST_DIR, '')
        print(dir_list)
        return

    if data == shared.EMPTY_FILE:
        print("The requested file is empty")
        return
    
    elif data == shared.FILE_NOT_FOUND:
        raise FileNotFoundException(f"File: {file_name} not found")
    
    else:
        # Create the folder
        if not os.path.exists(shared.OUTPUT_DIR_NAME):
            os.mkdir(shared.OUTPUT_DIR_NAME)
            print(f"{shared.OUTPUT_DIR_NAME} folder has been created")

        # Create the full path to the file within the folder
        file_path = os.path.join(shared.OUTPUT_DIR_NAME, file_name)
        file = open(file_path, "wb")
        
        while shared.MAGIC_END_FILE_KEY not in data:            
            file.write(data)
            data = socket.recv(shared.CHUNK_SIZE)

        
        if data != shared.MAGIC_END_FILE_KEY:
             data = data.replace(shared.MAGIC_END_FILE_KEY, b'')
             file.write(data)
             
        
    print("Finished transferring the file.")
    file.close()


def main():
    
    try:
        server_socket = connect_to_server()
        print("Receiver is connected to the server")
    except Exception as ex:
        print(f"Connection Error: {ex}")
        return

    user_request= get_user_request()
    
    while user_request.encode() != shared.END_THE_PROGRAM: 
        try:
            get_file_from_server(server_socket, user_request)
            
        except FileNotFoundException as e:
            print(f" {e}")
        except socket.error as e:
            print(f"Network Error: {e}")
        #except Exception as e:
        #    print(f"Unknown Error: {e}")

            
        finally:    
            user_request= get_user_request()

    server_socket.send(user_request.encode())
    print("You asked to end the program. Hope to see you soon.")
    server_socket.close()



if __name__ == "__main__":
    main()