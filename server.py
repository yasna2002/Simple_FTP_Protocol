import socket
import threading

# Sample user data
users = {
    'user1': 1111,
    'user2': 1111,
    'user3': 1111
}


def handle_client(client_socket, client_address):
    pass


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

