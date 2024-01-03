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
        msg = sock.recv(1024).decode()

        print(msg)
        if msg == "Auf wiedersehen :)":
            break

        inp = input("---> ")
        sock.send(inp.encode())

        if "STOR" in inp:

            try:
                client_path = inp.split(" ")[1]

                file = open(client_path, "rb")
                file_chunk = file.read(1024)

                while file_chunk:
                    sock.send(file_chunk)
                    file_chunk = file.read(1024)
                sock.send(b'0')

                file.close()
                continue

            except FileNotFoundError:
                print("File Not Found")
                continue


        if "RETR" in inp:
            try:
                file_path = "E:/CN/network-project-phase02-rabbids/clients/" + inp.split("/")[-1]

                file_chunk = sock.recv(1024)
                if file_chunk.decode() == "File Not Found":
                    print("File Not Found")
                    continue
            except:
                file = open(file_path, "wb")

                if file_chunk == b'0':
                    continue

                while True:
                    file.write(file_chunk)
                    file_chunk = sock.recv(1024)
                    if file_chunk == b'0':
                        file.close()
                        break





