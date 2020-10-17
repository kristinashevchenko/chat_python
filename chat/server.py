from socket import AF_INET, socket, SOCK_STREAM
from typing import Dict, List
from server_logging import server_logger
import datetime
import random
import select
import struct


clients: Dict[socket, str] = {}
players: List[str] = []


HOST = "127.0.0.1"
PORT = 4203
ADDR = (HOST, PORT)

GAME_WIN = {
    ("paper", "rock"),
    ("rock", "scissors"),
    ("scissors", "paper")
}

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def count_participants(client: socket):
    send_str = "Server response: %s participants in chat." % len(clients)

    server_logger.info(send_str)
    send_to_clients(send_str, client)


def get_participants_names(client: socket):
    client_names = list(clients.values())
    send_str = "Server response: Next participants in chat: %s" % client_names

    server_logger.info(send_str)
    send_to_clients(send_str, client)


def current_server_time(client: socket):
    now = datetime.datetime.now()
    serverTime = now.strftime("%d-%m-%Y %H:%M:%S")
    send_str = "Current date and time %s: " % serverTime

    server_logger.info(send_str)
    send_to_clients(send_str, client)


def random_value() -> str:
    return random.choice(["paper", "rock", "scissors"])


def start_game(client: socket):
    name = clients[client]
    send_str = "Let's play game, %s!" \
               " Enter 'paper', rock' or 'scissors' value" % name

    server_logger.info(send_str)
    send_to_clients(send_str, client)
    players.append(name)


def play_game(user_value: str, server_value: str) -> str:
    if user_value not in ["paper", "rock", "scissors"]:
        return "Invalid value. You failed!"
    if user_value == server_value:
        return "50/50"
    if (user_value, server_value) in GAME_WIN:
        return "You win!"
    else:
        return "You failed!"


cmd_handlers = {
    "cmd!count-participants": count_participants,
    "cmd!get-names": get_participants_names,
    "cmd!get-time": current_server_time,
    "cmd!rock-paper-scissors": start_game
}


def handle_cmd(msg: str, client: socket):
    if msg in cmd_handlers.keys():
        cmd_handlers[msg](client)
    else:
        send_str = "This command is not supported"

        server_logger.info(send_str)
        send_to_clients(send_str, client)


def send_to_clients(msg: str, client=""):
    if client:
        send_data(client, msg)
    else:
        for sock in clients:
            send_data(sock, msg)


def receive_message(client: socket):
    try:
        data_size = struct.unpack('>I', client.recv(4))[0]
        # receive data till received data size is equal to data_size received
        received_data = b""
        remaining_data_size = data_size
        while remaining_data_size != 0:
            received_data += client.recv(remaining_data_size)
            remaining_data_size = data_size - len(received_data)
        return received_data.decode("utf-8")
    except ConnectionResetError:
        return False


def send_data(client_socket: socket, data: str):
    data_to_send = bytes(data, "utf-8")
    # send data size and data
    client_socket.send(struct.pack('>I', len(data_to_send)))
    client_socket.send(data_to_send)


def client_joined_event(name: str, client_socket: socket):
    welcome = "Welcome %s! " \
              "If you ever want to quit, press CTRL+C to exit." % name

    message = "%s has joined the chat!" % name

    send_to_clients(welcome, client_socket)
    server_logger.info(message)
    send_to_clients(message)

    clients[client_socket] = name


def client_exited_event(name: str, client_socket: socket):
    readable_sockets.remove(client_socket)
    client_socket.close()
    del clients[client_socket]
    send_str = "%s has left the chat." % name

    server_logger.info(send_str)
    send_to_clients(send_str)


def client_game_event(msg: str, client_socket: socket):
    server_value = random_value()
    game_result = play_game(msg, server_value)
    send_str = "Server choose %s value" % server_value

    server_logger.info(send_str)
    send_to_clients(send_str, client_socket)
    server_logger.info(game_result)
    send_to_clients(game_result, client_socket)


if __name__ == "__main__":
    SERVER.listen()
    server_logger.info("Waiting for connection...")

    with SERVER as server:
        readable_sockets = [server]

        while True:
            r_sockets, w_sockets, e_sockets = select.select(readable_sockets,
                                                            [],
                                                            readable_sockets)

            for r_socket in r_sockets:
                if r_socket is server:
                    # new client connected
                    client, client_address = SERVER.accept()
                    server_logger.info("%s:%s has connected." % client_address)

                    readable_sockets.append(client)

                else:
                    msg = receive_message(r_socket)
                    name = ""

                    # check if client sent username
                    if r_socket in clients:
                        name = clients[r_socket]
                    else:
                        if msg not in list(clients.values()):
                            # client sent uniq name
                            client_joined_event(msg, r_socket)

                        continue

                    # client exit
                    if not msg:
                        client_exited_event(name, r_socket)
                        continue

                    is_cmd = msg.startswith("cmd!")

                    if name in players:
                        client_game_event(msg, r_socket)
                        players.remove(name)
                    elif is_cmd:
                        handle_cmd(msg, r_socket)
                    else:
                        send_str = "%s: %s" % (name, msg)
                        server_logger.info(send_str)
                        send_to_clients(send_str)

            for e_socket in e_sockets:
                readable_sockets.remove(e_socket)
                send_str = "%s has left the chat." % clients[e_socket]

                server_logger.info(send_data)
                send_to_clients(send_str)
                del clients[e_socket]

    SERVER.close()
