import os
import datetime
import socket
import threading
import os

root_path = 'E:/CN/network-project-phase02-rabbids/Server'
curr_path = 'E:/CN/network-project-phase02-rabbids/Server'

# Sample user data
users = {
    'ilya': 1382,
    'yasna': 1382,
    'admin': 1111
}

report = ""


def handel_command(client_socket, command):
    global curr_path
    global report
    if command[0] == "LIST":
        list_msg = ""
        if len(command) == 1:
            report += "user entered: " + command[0] + "\n"
            for filename in os.listdir(curr_path):
                file_path = os.path.join(curr_path, filename)
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if os.path.isdir(file_path):
                    list_msg = list_msg + str(mod_time) + " " + filename + "\n"
                else:
                    size = os.path.getsize(file_path)
                    list_msg = list_msg + str(mod_time) + " " + filename + " " + str(size) + " bytes" + "\n"
        else:
            report += "user entered: " + command[0] + " " + command[1] + "\n"
            client_path = command[1]
            for filename in os.listdir(client_path):
                file_path = os.path.join(client_path, filename)
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if os.path.isdir(file_path):
                    list_msg = list_msg + str(mod_time) + " " + filename + "\n"
                else:
                    size = os.path.getsize(file_path)
                    list_msg = list_msg + str(mod_time) + " " + filename + " " + str(size) + " bytes" + "\n"
        if len(list_msg) == 0:
            client_socket.send("NO FILE FOUND".encode())
            report += "NO FILE FOUND\n"
        else:
            client_socket.send(list_msg.encode())
            report += list_msg + "\n"
    # .........................................................................
    elif command[0] == "RETR":
        report += "user entered: " + command[0] + " " + command[1] + "\n"
        server_path = command[1]
        try:
            if ".txt" in server_path:
                file = open(server_path, "r")
                file_chunk = file.readline()

                while file_chunk:
                    client_socket.send(file_chunk.encode())
                    file_chunk = file.readline()
                client_socket.send(b'0')

                file.close()
                client_socket.send("File has been sent successfully!".encode())
                report += "File has been successfully sent to the user\n"

            else:
                file = open(server_path, "rb")
                file_chunk = file.read(1024)

                while file_chunk:
                    client_socket.send(file_chunk)
                    file_chunk = file.read(1024)
                client_socket.send(b'0')

                file.close()
                client_socket.send("File has been sent successfully!".encode())
                report += "File has been successfully sent to the user\n"

        except FileNotFoundError:
            client_socket.send("File Not Found".encode())
            client_socket.send("Please try again!".encode())
            report += "File requested by the user was not found\n"

    elif command[0] == "STOR":
        report += "user entered: " + command[0] + " " + command[1] + " " + command[2] + "\n"

        server_path = command[2] + "/" + command[1].split("/")[-1]

        file = open(server_path, "wb")
        file_chunk = client_socket.recv(1024)

        while file_chunk != b'0':
            file.write(file_chunk)
            file_chunk = client_socket.recv(1024)
            if file_chunk == b'0':
                file.close()
                break
        client_socket.send("File has been received!".encode())
        report += "File has been received from client!\n"


    elif command[0] == "DELE":
        report += "user entered: " + command[0] + "\n"
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
            report += "user has deleted a file!\n"
        except FileNotFoundError:
            msg = "No such file or directory!"
            report += "No such file or directory to be deleted!\n"
            client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "MKD":
        report += "user entered: " + command[0] + "\n"
        try:
            if ".." in command[1]:
                temp = command[1].split("/")
                real_path = curr_path + "/" + temp[1]
                os.mkdir(real_path)
            else:
                os.mkdir(command[1])
            msg = "The folder has been made successfully!"
            report += "The folder has been made successfully!\n"
            client_socket.send(msg.encode())
        except FileNotFoundError:
            msg = "No such directory!"
            report += "No such directory!\n"
            client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "RMD":
        report += "user entered: " + command[0] + "\n"
        try:
            if ".." in command[1]:
                temp = command[1].split("/")
                real_path = curr_path + "/" + temp[1]
                os.rmdir(real_path)
            else:
                os.rmdir(command[1])
            msg = "The folder has been removed successfully!"
            report += "The folder has been made successfully!\n"
            client_socket.send(msg.encode())
        except FileNotFoundError:
            msg = "No such directory!"
            report += "No such directory!\n"
            client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "PWD":
        report += "user entered: " + command[0] + "\n"
        client_socket.send(curr_path.encode())
    # .........................................................................
    elif command[0] == "CWD":
        report += "user entered: " + command[0] + "\n"
        if ".." in command[1]:
            temp = command[1].split("/")
            temp2 = curr_path + "/" + temp[1]
            if os.path.isdir(temp2):
                curr_path = temp2
            else:
                msg = "No such directory!"
                report += "No such directory!\n"
                client_socket.send(msg.encode())
        else:
            if os.path.isdir(command[1]):
                curr_path = command[1]
            else:
                msg = "No such directory!"
                report += "No such directory!\n"
                client_socket.send(msg.encode())
        msg = "Directory has been successfully changed to " + curr_path
        report += msg + "\n"
        client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "CDUP":
        report += "user entered: " + command[0] + "\n"
        temp = curr_path.split("/")
        temp.pop(-1)
        curr_path = '/'.join(temp)
        msg = "Directory has been successfully changed to " + curr_path
        report += msg + "\n"
        client_socket.send(msg.encode())
    # .........................................................................
    elif command[0] == "QUIT":
        report += "user entered: " + command[0] + "\n"
        msg = "Auf wiedersehen :)"
        report += msg + "\n"
        client_socket.send(msg.encode())
        client_socket.close()
        return
    elif command[0] == "REPO":
        client_socket.send(report.encode())

    command = check_command(client_socket)
    handel_command(client_socket, command)


def check_command(client_socket):
    global report

    chosen_command = client_socket.recv(1024).decode()
    chosen_command = chosen_command.split()

    while True:
        if not (chosen_command[0] == "LIST" or chosen_command[0] == "RETR" or chosen_command[0] == "STOR" or
                chosen_command[0] == "DELE" or chosen_command[0] == "MKD" or chosen_command[0] == "RMD" or
                chosen_command[0] == "PWD" or chosen_command[0] == "CWD" or chosen_command[0] == "CDUP" or
                chosen_command[0] == "QUIT" or chosen_command[0] == "REPO"):
            msg = "Invalid Command!\nTry Again:"
            report += "user has entered an invalid command\n"
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
    global report
    while True:
        request = client_socket.recv(1024).decode()
        if "PASS" in request:
            password = request.split(" ")[1]
            if int(password) == users[name]:
                msg = "You are logged in"
                client_socket.send(msg.encode())
                report += "\nUser " + name + " has logged in\n"
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
