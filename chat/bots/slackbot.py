import os
from slack import WebClient
from dotenv import load_dotenv  # type: ignore
from flask import Flask
from slackeventsapi import SlackEventAdapter  # type: ignore
from socket import socket, AF_INET, SOCK_STREAM
import struct
from json import dumps, loads
from threading import Thread
from typing import List
from slackbot_logging import bot_logger
import logging
import random


for key in logging.Logger.manager.loggerDict:  # type: ignore
    if key != "botLogger":
        logging.getLogger(key).setLevel(logging.WARNING)

load_dotenv()
app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(
    os.environ.get("SLACK_SIGNING_SECRET"), "/slack/events", app
)

client_socket: socket
CHANNEL_NAME = "C01ERR6BUD9"
clients: List[str] = []
greetings: List[str] = []

slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
bot_id = slack_client.api_call("auth.test")["user_id"]  # type: ignore


def check_users_status():
    for user in clients:
        if user == bot_id:
            continue

        presence = slack_client.users_getPresence(user=user)
        bot_logger.info(f"Presence: {presence}")

        if presence["presence"] == "away":
            clients.remove(user)
            send_data({"message_text": user, "message_type": "user_removed"})

    bot_logger.info(f"Clients: {clients}")


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    bot_logger.info(f"New event: {event}")
    channel_type = event.get("channel_type")

    if channel_type == "im":
        private_chat(event)
    elif channel_type == "channel":
        user_id = event.get("user")

        if user_id and user_id not in clients:
            clients.append(user_id)
            send_data({"message_text": user_id, "message_type": "user_added"})

        text = event.get("text")

        if text == "/quit":
            clients.remove(user_id)
            send_data({"message_text": user_id,
                       "message_type": "user_removed"})
        elif user_id != bot_id:
            send_data({"message_text": text,
                       "message_type": "text",
                       "sender": user_id})


def private_chat(event):
    user_id = event.get("user")
    channel_id = event.get("channel")

    if user_id != bot_id:
        greeting = random.choice(greetings)
        text = f"{greeting}, {user_id}"
        slack_client.chat_postMessage(channel=channel_id, text=text)


def send_data(data: object) -> None:
    check_users_status()
    msg_obj = dumps(data)
    bot_logger.info(f"Send data: {data}")
    data_to_send = bytes(msg_obj, "utf-8")
    # send data size and data
    client_socket.send(struct.pack(">I", len(data_to_send)))
    client_socket.send(data_to_send)


def receive_data() -> str:
    check_users_status()

    data_size = struct.unpack(">I", client_socket.recv(4))[0]
    received_data = b""
    remaining_data_size = data_size

    while remaining_data_size != 0:
        received_data += client_socket.recv(remaining_data_size)
        remaining_data_size = data_size - len(received_data)
    decoded_data = received_data.decode("utf-8")
    return loads(decoded_data)


def receive_messages():
    while True:
        msg_obj = receive_data()

        if not msg_obj:
            break
        bot_logger.info(f"Received data: {msg_obj}")
        if "sender" in msg_obj:
            if msg_obj["sender"] in clients:
                continue
        text = msg_obj["message_text"]
        slack_client.chat_postMessage(channel=CHANNEL_NAME, text=text)


if __name__ == "__main__":
    try:
        with open("greetings.json", encoding="utf-8") as f:
            greetings = loads(f.read())

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.bind(("127.0.0.1", 0))
        client_socket.connect(("127.0.0.1", 4203))

        send_data({"message_text": bot_id, "message_type": "username"})

    except FileNotFoundError:
        bot_logger.info("File was not found")
    except ConnectionRefusedError:
        bot_logger.info("Can not connect to server")
    except BaseException:
        bot_logger.info("Error occurred while connecting server")

    receive_thread = Thread(target=receive_messages, daemon=True)
    receive_thread.start()
    app.run(debug=True, port=8085, use_reloader=False)
