import socket
import sys
from threading import Thread

HOST = '127.0.0.1'
PORT = 0
USERNAME = ''
BUFSIZE = 1024

# show received data
def receive():
    while (True):
        try:
            msg = client_socket.recv(BUFSIZE).decode('utf-8')
            print(msg)
        except OSError:
            break

# send message to server socket
def send():
    while (True):
        try:
            send_str = input()
            client_socket.send(bytes(send_str, 'utf-8'))
        except EOFError:
            client_socket.close()
            break

if __name__ == '__main__':
    try:
        if len(sys.argv) >= 3:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
            if len(sys.argv) > 3:
                USERNAME = sys.argv[3]

        if not USERNAME:
            USERNAME = input('Enter username: ')

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.bind((HOST, PORT))
        client_socket.connect(('127.0.0.1', 4203))

        client_socket.send(bytes(USERNAME, 'utf-8'))

        receive_thread = Thread(target=receive)
        receive_thread.start()

        send_thread = Thread(target=send)
        send_thread.start()
    except:
        print('Error occured while connecting server')