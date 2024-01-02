import socket


def send_req(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
    sock.send(message.encode())
    return sock.recv(1024).decode()


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
    while True:
        print(sock.recv(1024).decode())
        sock.send(input().encode())


