import socket


def send_req(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8080))
    sock.send(message.encode())
    return sock.recv(1024).decode()


if __name__ == '__main__':
    while(1):
        inp = input("Enter 'Get user_id' or 'POST user_name user_age' to simulate a request: ")
        received_msg = send_req(inp)
        print("Response from the server:")
        print(received_msg)

