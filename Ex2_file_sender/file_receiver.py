import socket
import os
import shared

SERV_IP = "127.0.0.1"
# connect and return socket
def connect_to_server():
    try: 
        server_socket = socket.socket()
        server_socket.connect((SERV_IP, shared.PORT))
        return server_socket
    except socket.error as e:
        raise Exception(f"Could not connect: {str(e)}")

# returns file name 
def get_user_request():
   user_input = input("Input filename you want to get, don't forget add the suffix\n"
                      "To exit the program, input the word 'DONE'\n "
                      "Input your request here:")
   return user_input



def get_file_from_server(socket, file_name):
    # Create the folder
    if not os.path.exists(shared.OUTPUT_DIR_NAME):
        os.mkdir(shared.OUTPUT_DIR_NAME)
        print(f"{shared.OUTPUT_DIR_NAME} folder has been created")

    # Create the full path to the file within the folder
    file_path = os.path.join(shared.OUTPUT_DIR_NAME, file_name)
    file = open(file_path, "wb")
    
    # send file name to server to check if exsist
    socket.send(file_name.encode('utf-8'))

    # get chunk by chunk the file from server
    # until the end of file is received
    data = socket.recv(shared.CHUNK_SIZE)
    print(data.decode())
    
    while data != shared.MAGIC_END_FILE_KEY:
        if data.decode('utf-8') == shared.EMPTY_FILE:
            print("The requested file is empty")
            break
        elif data.decode('utf-8') == shared.FILE_NOT_FOUND:
            raise Exception("File not found")
        else:
            file.write(data)
            data = socket.recv(shared.CHUNK_SIZE)
            print(f"geting data from server: {data}")
            continue
        
    print("file get to end")
    file.close()




def main():

    try:
        server_socket = connect_to_server()
        print("receiver is connected")
    except Exception as ex:
        print(f"Connection Error: something went wrong, Apologies for the inconvenience\n {ex}")
        return

    user_request= get_user_request()
    while user_request != shared.END_THE_PROGRAM: 
        try:
            get_file_from_server(server_socket, user_request)
            print("in try block")
        except Exception as e:
            # print(f"Error:{e}, There isn't file named: {user_request}")
            raise e
        finally:    
            print("I'm at finaly, get user request again")
            user_request= get_user_request()

    if user_request== shared.END_THE_PROGRAM:
        server_socket.close()



if __name__ == "__main__":
    main()