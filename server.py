import socket
import threading

def handel_command(client_socket, command):
    if command[0] == "LIST":
        pass
    elif command[0] == "RETR":
        pass
    elif command[0] == "STOR":
        pass
    elif command[0] == "DELE":
        pass
    elif command[0] == "MKD":
        pass
    elif command[0] == "RMD":
        pass
    elif command[0] == "PWD":
        pass
    elif command[0] == "CWD":
        pass
    elif command[0] == "CDUP":
        pass
    elif command[0] == "QUIT":
        pass


def show_commands_list(client_socket):
    welcome_msg = "----You are connected to the sever----\nhere is a list of commands you can send:\n" \
                  "01.LIST\n02.RETR -(RETR /path/file.txt)-\n03.STOR -(STOR /client-path /server-path)-" \
                  "\n04.DELE -(DELE /path/file.txt)-\n05.MKD -(MKD /home/user OR MKD ../folder)-" \
                  "\n06.RMD -(RMD /home/user OR RMD ../folder)-\n07.PWD\n08.CWD -(CWD /home/user OR CWD ../folder)-\n" \
                  "09.CDUP -(CDUP /home/user OR CDUP ../folder)-\n10.QUIT\n--------------------------"
    client_socket.send(welcome_msg.encode())
    chosen_command = client_socket.recv(1024).decode()
    chosen_command = chosen_command.split()

    while True:
        if not (chosen_command[0] == "LIST" or chosen_command[0] == "RETR" or chosen_command[0] == "STOR" or
                chosen_command[0] == "DELE" or chosen_command[0] == "MKD" or chosen_command[0] == "RMD" or
                chosen_command[0] == "PWD" or chosen_command[0] == "CWD" or chosen_command[0] == "CDUP" or
                chosen_command[0] == "QUIT"):
            msg = "Invalid Command!\nTry Again:"
            client_socket.send(msg.encode())
            chosen_command = client_socket.recv(1024).decode()
            chosen_command = chosen_command.split()
        else:
            break
    return chosen_command


def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    # showing the list of commands to the user
    command = show_commands_list(client_socket)

    handel_command(client_socket, command)

    request = client_socket.recv(1024).decode()

    client_socket.close()


if __name__ == '__main__':
    host = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
