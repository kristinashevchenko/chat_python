from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 4203
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def count_participants(client):
    sendToClients(bytes("Server response: %s participants in chat." % len(clients), "utf8"),'',client)
   

def get_participants_names(client):
    clientNames = []
    for i in clients:
        clientNames.append(clients[i])
    sendToClients(bytes("Server response: Next participants in chat: %s" % clientNames, "utf8"),'',client)

def current_server_time(client):
    now = datetime.datetime.now()
    serverTime = now.strftime("%d-%m-%Y %H:%M:%S")
    sendToClients(bytes("Current date and time %s: " % serverTime, "utf8"),'',client)

def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, press CTRL+C or type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    sendToClients(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("count_participants", "utf8"):
            count_participants(client)
        elif msg == bytes("getNames", "utf8"):
            get_participants_names(client)
        elif msg == bytes("getTime", "utf8"):
            current_server_time(client) 
        elif msg == bytes("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            sendToClients(bytes("%s has left the chat." % name, "utf8"))
            break
        else:
            sendToClients(msg, name+": ")


def sendToClients(msg, prefix="", client=""):
    if client:
        client.send(bytes(prefix, "utf8")+msg)
    else:
        for sock in clients:
            sock.send(bytes(prefix, "utf8")+msg)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()