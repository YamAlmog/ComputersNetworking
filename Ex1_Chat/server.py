import socket
import logging
import threading

HEADER=1024
PORT= 8020
SERVER_IP= 'localhost'
BIND=(SERVER_IP,PORT)
server=socket.socket()
server.bind(BIND)

logging.basicConfig(filename='app.log', filemode='w',  level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# -----------------handle_client func------------------------------------------
def handle_first_client(server, client_1, client_2, name_1):
    try:
        while True:
            logging.info(f"Waiting for message from {name_1}")
            message_1 = client_1.recv(1024).decode('utf-8')

            client_2.send(message_1.encode('utf-8'))
            print(f"{name_1} sent: {message_1}")

            if message_1 == 'EXIT':
                print('This correspondence has ended.')
                break
            else:
                continue
    except OSError as ex:
        raise OSError(f"Socket error: {ex}")
    finally:
        client_1.close()
        client_2.close()
        server.close() 
    
def handle_second_client(server, client_1, client_2, name_2):
    try:
        while True:  
            logging.info(f"Waiting for message from {name_2}")
            message_2 = client_2.recv(1024).decode('utf-8')

            client_1.send(message_2.encode('utf-8'))
            print(f"{name_2} sent: {message_2}")

            if message_2 == 'EXIT':
                print('This correspondence has ended.')
                break
            else:
                continue

    except OSError as ex:
        raise OSError(f"Socket error: {ex}")
    finally:
        client_1.close()
        client_2.close()
        server.close() 

# ---------------------start func--------------------------------------------
def start(server):
    try:   
        (user_1, address_1) = server.accept()
        logging.info("User 1 connected")
        (user_2, address_2) = server.accept()
        logging.info("User 2 connected")

        server_msg = "Entre name:"
        user_1.send(f'{server_msg}'.encode('utf-8'))
        user_2.send(f'{server_msg}'.encode('utf-8'))

        name_1 = user_1.recv(1024).decode('utf-8')
        logging.info(f"User 1 name: {name_1}")

        name_2 = user_2.recv(1024).decode('utf-8')
        logging.info(f"User 2 name: {name_2}")

        user_1.send(name_2.encode('utf-8'))
        user_2.send(name_1.encode('utf-8'))

        user1_handler_thread = threading.Thread(target=handle_first_client, args=(server, user_1, user_2, name_1))
        user2_handler_thread = threading.Thread(target=handle_second_client, args=(server, user_1, user_2, user_2))

        user1_handler_thread.start()
        user2_handler_thread.start()

        user1_handler_thread.join()  
        user2_handler_thread.join()
        
    except OSError as ex:
        raise OSError(f"Socket error: {ex}")
    


def main():
    try:    
        server.listen()
        logging.info(f"[LISTENING] Server is listenin on...")
        start(server)
    except OSError as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()