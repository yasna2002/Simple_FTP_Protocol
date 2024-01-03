import datetime
import socket
import threading
import os

root_path = 'D:/PythonProjects/network-project-phase02-rabbids/Server'
curr_path = 'D:/PythonProjects/network-project-phase02-rabbids/Server'

# Sample user data
users = {
    'user1': 1111,
    'user2': 1111,
    'user3': 1111
}


def handel_command(client_socket, command):
    if command[0] == "LIST":
        list_msg = ""
        if len(command) == 1:
            for filename in os.listdir(root_path):
                file_path = os.path.join(root_path, filename)
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
    # .........................................................................
    elif command[0] == "RETR":
        pass
    # .........................................................................
    elif command[0] == "STOR":
        pass
    # .........................................................................
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
    # .........................................................................
    elif command[0] == "MKD":
        global curr_path
        try:
            if ".." in command[1]:
                temp = command[1].split("/")
                real_path = curr_path + "/" + temp[1]
                os.mkdir(real_path)
            else:
                os.mkdir(command[1])
            msg = "The folder has been made successfully!"
            client_socket.send(msg.encode())
        except FileNotFoundError:
            msg = "No such directory!"
            client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "RMD":
        try:
            if ".." in command[1]:
                real_path = curr_path
                os.rmdir(real_path)
                real_path = real_path.split("/")
                real_path.pop(-1)
                curr_path = '/'.join(real_path)
            else:
                os.rmdir(command[1])
            msg = "The folder has been removed successfully!"
            client_socket.send(msg.encode())
        except FileNotFoundError:
            msg = "No such directory!"
            client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "PWD":
        client_socket.send(curr_path.encode())
    # .........................................................................
    elif command[0] == "CWD":
        try:
            if ".." in command[1]:
                temp = command[1].split("/")
                curr_path = curr_path + "/" + temp[1]
            else:
                curr_path = command[1]
            msg = "Directory has been successfully changed to " + curr_path
            client_socket.send(msg.encode())
        except FileNotFoundError:
            msg = "No such directory!"
            client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "CDUP":
        try:
            temp = curr_path.split("/")
            temp.pop(-1)
            curr_path = '/'.join(temp)
            msg = "Directory has been successfully changed to " + curr_path
            client_socket.send(msg.encode())
        except FileNotFoundError:
            msg = "No such directory!"
            client_socket.send(msg.encode())
    # .........................................................................
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
                  "09.CDUP\n10.QUIT\n--------------------------"
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
