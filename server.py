import os
import datetime
import socket
import threading
import os


# Sample user data
users = {
    'user1': 1111,
    'user2': 1111,
    'user3': 1111
}


def handel_command(client_socket, command):
    path = 'E:/CN/network-project-phase02-rabbids/Server'

    if command[0] == "LIST":
        list_msg = ""
        if len(command) == 1:
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if os.path.isdir(file_path):
                    list_msg = list_msg + str(mod_time) + " " + filename + "\n"
                else:
                    size = os.path.getsize(file_path)
                    list_msg = list_msg + str(mod_time) + " " + filename + " " + str(size) + " bytes" + "\n"
        else:
            client_path = command[1]
            for filename in os.listdir(client_path):
                file_path = os.path.join(client_path, filename)
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if os.path.isdir(file_path):
                    list_msg = list_msg + str(mod_time) + " " + filename + "\n"
                else:
                    size = os.path.getsize(file_path)
                    list_msg = list_msg + str(mod_time) + " " + filename + " " + str(size) + " bytes" + "\n"
        client_socket.send(list_msg.encode())

    elif command[0] == "RETR":

        server_path = command[1]
        try:
            if ".txt" in server_path:
                file = open(server_path, "r")
                file_chunk = file.read()

                while file_chunk:
                    client_socket.send(file_chunk.encode())
                    file_chunk = file.read()
                client_socket.send(b'0')
                print("sent")

                file.close()
                client_socket.send("File has been sent successfully!".encode())

            else:
                file = open(server_path, "rb")
                file_chunk = file.read(1024)

                while file_chunk:
                    client_socket.send(file_chunk)
                    file_chunk = file.read(1024)
                client_socket.send(b'0')
                print("sent")

                file.close()
                client_socket.send("File has been sent successfully!".encode())

        except FileNotFoundError:
            print("File not found!")
            client_socket.send("File Not Found".encode())
            client_socket.send("Please try again!".encode())

    elif command[0] == "STOR":
        pass

    elif command[0] == "DELE":
        try:
            msg = "Do you really wish to delete? Y/N"
            client_socket.send(msg.encode())
            response = client_socket.recv(1024).decode()
            if response == "Y" or response == "y":
                os.remove(command[1])
                msg = "File has been successfully deleted!"
                client_socket.send(msg.encode())
            elif response == "N" or response == "n":
                msg = "Command has been canceled successfully!"
                client_socket.send(msg.encode())
        except FileNotFoundError:
            msg = "No such file or directory!"
            client_socket.send(msg.encode())

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
        msg = "Auf wiedersehen :)"
        client_socket.send(msg.encode())
        client_socket.close()
        return


    command = check_command(client_socket)
    handel_command(client_socket, command)


def check_command(client_socket):
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

    welcome_msg = "\n----You are connected to the server----\nhere is a list of commands you can send:\n" \
                  "01.LIST\n02.RETR -(RETR /path/file.txt)-\n03.STOR -(STOR /client-path /server-path)-" \
                  "\n04.DELE -(DELE /path/file.txt)-\n05.MKD -(MKD /home/user OR MKD ../folder)-" \
                  "\n06.RMD -(RMD /home/user OR RMD ../folder)-\n07.PWD\n08.CWD -(CWD /home/user OR CWD ../folder)-\n" \
                  "09.CDUP -(CDUP /home/user OR CDUP ../folder)-\n10.QUIT\n--------------------------"
    client_socket.send(welcome_msg.encode())

    # showing the list of commands to the user
    command = check_command(client_socket)

    handel_command(client_socket, command)


def get_password(client_socket, client_address, name):
    while True:
        request = client_socket.recv(1024).decode()
        if "PASS" in request:
            password = request.split(" ")[1]
            if int(password) == users[name]:
                msg = "You are logged in"
                client_socket.send(msg.encode())
                handle_client(client_socket, client_address)
                break
            else:
                msg = "wrong password"
                client_socket.send(msg.encode())
        else:
            msg = "please send your password"
            client_socket.send(msg.encode())


def get_username(client_socket, client_address):
    while True:
        request = client_socket.recv(1024).decode()
        name = request.split(" ")[1]
        if "USER" in request:
            if name in users.keys():
                msg = "hello " + name + " Please enter your password"
                client_socket.send(msg.encode())
                get_password(client_socket, client_address, name)
                break
            else:
                msg = "user does not exist"
                client_socket.send(msg.encode())
        else:
            msg = "In order to login please enter your username first"
            client_socket.send(msg.encode())


if __name__ == '__main__':
    host = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server is listening on http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=get_username, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

