from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime
import random

clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 4203
BUFSIZ = 1024
ADDR = (HOST, PORT)

GAME_WIN = {
                ('paper', 'rock'),
                ('rock', 'scissors'),
                ('scissors', 'paper')
            }

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def count_participants(client):
    send_str = "Server response: %s participants in chat." % len(clients)
    print(send_str)
    sendToClients(bytes(send_str, "utf8"), "", client)
   

def get_participants_names(client):
    clientNames = list(clients.values())
    send_str = "Server response: Next participants in chat: %s" % clientNames
    print(send_str)
    sendToClients(bytes(send_str, "utf8"), "", client)

def current_server_time(client):
    now = datetime.datetime.now()
    serverTime = now.strftime("%d-%m-%Y %H:%M:%S")
    send_str = "Current date and time %s: " % serverTime
    print(send_str)
    sendToClients(bytes(send_str, "utf8"), "", client)

def random_value():
    return random.choice(['paper', 'rock', 'scissors'])

def play_game(user_value, server_value):
    if user_value not in ['paper', 'rock', 'scissors']:
        return 'Invalid value. You failed!'
    if user_value == server_value:
        return '50/50'
    if (user_value, server_value) in GAME_WIN:
        return 'You win!'
    else:
        return 'You failed!'

def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = "Welcome %s! If you ever want to quit, press CTRL+C or type {quit} to exit." % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    sendToClients(bytes(msg, "utf8"))
    clients[client] = name
    is_playing_game = False

    while True:
        try:
            msg = client.recv(BUFSIZ).decode("utf-8")

            if is_playing_game:
                server_value = random_value()
                game_result = play_game(msg, server_value)
                send_str = 'Server choose %s value' % server_value
                print(send_str)
                client.send(bytes(send_str, "utf8"))
                print(game_result)
                client.send(bytes(game_result, "utf8"))
                is_playing_game = False
            elif msg == "cmd!count-participants":
                count_participants(client)
            elif msg =="cmd!get-names":
                get_participants_names(client)
            elif msg == "cmd!get-time":
                current_server_time(client) 
            elif msg == "cmd!rock-paper-scissors":
                send_str = "Let's play game, %s! Enter 'paper', rock' or 'scissors' value" % name
                print(send_str)
                client.send(bytes(send_str, "utf8"))
                is_playing_game = True
            elif msg == "{quit}":
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                send_str = "%s has left the chat." % name
                print(send_str)
                sendToClients(bytes(send_str, "utf8"))
                break
            else:
                print("%s: %s" % (name, msg))
                sendToClients(bytes(msg, "utf8"), name+": ")
        except:
            client.close()
            del clients[client]
            send_str = "%s has left the chat." % name
            print(send_str)
            sendToClients(bytes(send_str, "utf8"))
            break


def sendToClients(msg, prefix="", client=""):
    if client:
        client.send(bytes(prefix, "utf8") + msg)
    else:
        for sock in clients:
            sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()