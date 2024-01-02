import socket


def send_pass():
    while True:
        inp_pass = input("PASS password: ")
        sock.send(inp_pass.encode())
        msg = sock.recv(1024).decode()

        if msg == "You are logged in":
            return
        else:
            print(msg)


def send_username():
    while True:
        inp_name = input("USER name: ")
        sock.send(inp_name.encode())
        msg = sock.recv(1024).decode()

        if "hello" in msg:
            print(msg)
            send_pass()
            break
        else:
            print(msg)




if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))

    send_username()

    while True:
        print(sock.recv(1024).decode())
        sock.send(input().encode())


