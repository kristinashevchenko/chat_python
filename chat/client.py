import socket
import sys
from threading import Thread
import struct
import json

HOST = "127.0.0.1"
PORT = 0
USERNAME = ""


def send_data(message_text: str, message_type: str = "text"):
    message_obj = json.dumps({"message_text": message_text,
                              "message_type": message_type})

    data_to_send = bytes(message_obj, "utf-8")
    # send data size and data
    client_socket.send(struct.pack(">I", len(data_to_send)))
    client_socket.send(data_to_send)


def receive_data() -> str:
    # receive first 4 bytes of data as size of data
    data_size = struct.unpack(">I", client_socket.recv(4))[0]
    # receive data till received data size is equal to data_size received
    received_data = b""
    remaining_data_size = data_size
    while remaining_data_size != 0:
        received_data += client_socket.recv(remaining_data_size)
        remaining_data_size = data_size - len(received_data)
    decoded_data = received_data.decode("utf-8")
    return json.loads(decoded_data)


# show received data
def receive():
    while True:
        try:
            msg = receive_data()
            msg_text = "" if "message_text" not in msg else msg["message_text"]
            print(msg_text)

            if msg_text == "/quit":
                client_socket.close()
                break

        except OSError:
            break


# send message to server socket
def send():
    while True:
        try:
            send_str = input()
            send_data(message_text=send_str)

            if send_str == "/quit":
                break

        except EOFError:
            client_socket.close()
            break
        except ConnectionError:
            print("You have connection error. Seems server is unavailable")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 3:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
            if len(sys.argv) > 3:
                USERNAME = sys.argv[3]

        if not USERNAME:
            USERNAME = input("Enter username: ")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.bind((HOST, PORT))
        client_socket.connect(("127.0.0.1", 4203))

        send_data(message_text=USERNAME, message_type="username")

        receive_thread = Thread(target=receive)
        receive_thread.start()

        send_thread = Thread(target=send)
        send_thread.start()
    except BaseException:
        print("Error occurred while connecting server")
