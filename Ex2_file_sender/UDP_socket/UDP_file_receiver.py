import socket
import os
import UDP_shared
from UDP_errors import *
        
# connect and return socket
def connect_to_server():
    # asking the client to input IP 
    #SERVER_IP = input("Pleas input the IP to connect with: ")
    try: 
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #server_socket.connect((SERVER_IP, UDP_shared.PORT))
        return server_socket
    except socket.error as e:
        raise Exception(f"Could not connect: {str(e)}")

# returns file name 
def get_user_request():
   user_input = input("Input filename you want to get, don't forget add the suffix\n"
                      "To exit the program, input the word 'DONE'\n"
                      "Input your request here:")
   return user_input



def get_file_from_server(socket, file_name, server_ip):
    # send file name to server to check if exsist
    socket.sendto(file_name.encode('utf-8'), (server_ip, UDP_shared.PORT))

    # get first chunk of the file from server
    data = socket.recvfrom(UDP_shared.CHUNK_SIZE)
    print(data)

    if UDP_shared.LIST_DIR.encode() in data:
        print("-" * 10 + "[DIR LIST]" + "-" * 10)
        dir_list = data.decode().replace(UDP_shared.LIST_DIR, '')
        print(dir_list)
        return

    if data == UDP_shared.EMPTY_FILE:
        print("The requested file is empty")
        return
    
    elif data == UDP_shared.FILE_NOT_FOUND:
        raise FileNotFoundException(f"File: {file_name} not found")
    
    else:
        # Create the folder
        if not os.path.exists(UDP_shared.OUTPUT_DIR_NAME):
            os.mkdir(UDP_shared.OUTPUT_DIR_NAME)
            print(f"{UDP_shared.OUTPUT_DIR_NAME} folder has been created")

        # Create the full path to the file within the folder
        file_path = os.path.join(UDP_shared.OUTPUT_DIR_NAME, file_name)
        file = open(file_path, "wb")
        
        while UDP_shared.MAGIC_END_FILE_KEY not in data:            
            file.write(data)
            data = socket.recvfrom(UDP_shared.CHUNK_SIZE)

        
        if data != UDP_shared.MAGIC_END_FILE_KEY:
             data = data.replace(UDP_shared.MAGIC_END_FILE_KEY, b'')
             file.write(data)
             
        
    print("Finished transferring the file.")
    file.close()


def main():
    
    try:
        SERVER_IP = input("Pleas input the IP to connect with: ")

        server_socket = connect_to_server()
        print("Receiver is connected to the server")
    except Exception as ex:
        print(f"Connection Error: {ex}")
        return

    user_request= get_user_request()
    
    while user_request.encode() != UDP_shared.END_THE_PROGRAM: 
        try:
            get_file_from_server(server_socket, user_request, SERVER_IP)
            
        except FileNotFoundException as e:
            print(f" {e}")
        except socket.UDP_error as e:
            print(f"Network Error: {e}")
        except Exception as e:
            print(f"Unknown Error: {e}")

            
        finally:    
            user_request= get_user_request()

    server_socket.sendto(user_request.encode(), (SERVER_IP, UDP_shared.PORT))
    print("You asked to end the program. Hope to see you soon.")
    server_socket.close()



if __name__ == "__main__":
    main()