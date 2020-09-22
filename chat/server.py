from socket import AF_INET, socket, SOCK_STREAM
import datetime
import random
import select

clients = {}
players = []

HOST = "127.0.0.1"
PORT = 4203
BUFSIZ = 1024
ADDR = (HOST, PORT)

GAME_WIN = {
                ("paper", "rock"),
                ("rock", "scissors"),
                ("scissors", "paper")
            }

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def count_participants(client):
    send_str = "Server response: %s participants in chat." % len(clients)

    print(send_str)
    send_to_clients(send_str, client)


def get_participants_names(client):
    client_names = list(clients.values())
    send_str = "Server response: Next participants in chat: %s" % client_names

    print(send_str)
    send_to_clients(send_str, client)


def current_server_time(client):
    now = datetime.datetime.now()
    serverTime = now.strftime("%d-%m-%Y %H:%M:%S")
    send_str = "Current date and time %s: " % serverTime

    print(send_str)
    send_to_clients(send_str, client)


def random_value():
    return random.choice(["paper", "rock", "scissors"])


def play_game(user_value, server_value):
    if user_value not in ["paper", "rock", "scissors"]:
        return "Invalid value. You failed!"
    if user_value == server_value:
        return "50/50"
    if (user_value, server_value) in GAME_WIN:
        return "You win!"
    else:
        return "You failed!"


def handle_cmd(msg, client):
    if msg == "cmd!count-participants":
        count_participants(client)
    elif msg =="cmd!get-names":
        get_participants_names(client)
    elif msg == "cmd!get-time":
        current_server_time(client) 
    elif msg == "cmd!rock-paper-scissors":
        name = clients[client]
        send_str = "Let's play game, %s! Enter 'paper', rock' or 'scissors' value" % name

        print(send_str)
        send_to_clients(send_str, client)
        players.append(name)
    else:
        send_str = "This command is not supported"

        print(send_str)
        send_to_clients(send_str, client)


def send_to_clients(msg, client=""):
    msg = bytes(msg, "utf8")
    if client:
        client.send(msg)
    else:
        for sock in clients:
            sock.send(msg)

def receive_message(client):
    try:
        msg = client.recv(BUFSIZ).decode("utf-8")
        return msg
    except:
        return False


if __name__ == "__main__":
    SERVER.listen()
    print("Waiting for connection...")

    with SERVER as server:
        readable_sockets = [server]
        
        while True:
            r_sockets, w_sockets, e_sockets = select.select(readable_sockets, [], readable_sockets)

            for r_socket in r_sockets:
                if r_socket is server:
                    # new client connected
                    client, client_address = SERVER.accept()
                    print("%s:%s has connected." % client_address)   

                    readable_sockets.append(client)

                else:    
                    msg = receive_message(r_socket)
                    name = ""

                    try:
                        # check if client sent username
                        name = clients[r_socket]
                    except:
                        if msg in list(clients.values()):
                            continue
                        # client sent uniq name
                        name = msg
                        welcome = "Welcome %s! If you ever want to quit, press CTRL+C to exit." % name
                        message = "%s has joined the chat!" % name

                        send_to_clients(welcome, r_socket)
                        print(message)
                        send_to_clients(message)

                        clients[r_socket] = name
                        continue

                    
                    # client exit
                    if not msg:
                        readable_sockets.remove(r_socket)
                        r_socket.close()
                        del clients[r_socket]
                        send_str = "%s has left the chat." % name

                        print(send_str)
                        send_to_clients(send_str)
                        continue                    

                    is_cmd = msg.startswith("cmd!")

                    if name in players:
                        server_value = random_value()
                        game_result = play_game(msg, server_value)
                        send_str = "Server choose %s value" % server_value

                        print(send_str)
                        send_to_clients(send_str, r_socket)
                        print(game_result)
                        send_to_clients(game_result, r_socket)

                        players.remove(name)
                    elif is_cmd:
                        handle_cmd(msg, r_socket)
                    else:
                        send_str = "%s: %s" % (name, msg)
                        print(send_str)
                        send_to_clients(send_str)

            for e_socket in e_sockets:
                readable_sockets.remove(e_socket)
                send_str = "%s has left the chat." % clients[e_socket]
                
                print(send_str)
                send_to_clients(send_str)
                del clients[e_socket]
                        

                   

    SERVER.close()