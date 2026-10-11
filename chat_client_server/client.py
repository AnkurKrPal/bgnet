
import sys
import socket
import threading

from chatui.chatuicurses import *

from packet import *


def listen_server(s):
    buffer = b""

    while True:
        data = s.recv(4096)

        if not data:
            break

        buffer += data

        while True:
            payload, remaining = get_next_packet(buffer)

            if payload is None:
                break

            buffer = remaining

            if payload["type"] == "join":
                print_message(f"*** {payload['nick']} joined the chat")
            elif payload["type"] == "leave":
                print_message(f"*** {payload['nick']} left the chat")
            elif payload["type"] == "chat":
                print_message(f"{payload['nick']}: {payload['message']}")

    s.close()


def send_server(s, nick):
    while True:
        message = read_command(f"{nick}> ")

        if message == "/q":
            break

        msg_pckt = {
            "type": "chat",
            "message": message
        }
        s.sendall(make_packet(msg_pckt))

    s.close()


def main(argv):
    if len(argv) != 4:
        print("usage: client.py nickname host port", file=sys.stderr)
        return 1

    nickname = argv[1]
    host = argv[2]
    port = int(argv[3])

    init_windows()

    s = socket.socket()
    s.connect((host, port))

    hello = {
        "type": "hello",
        "nick": nickname
    }

    s.sendall(make_packet(hello))

    listen_thread = threading.Thread(
        target=listen_server,
        args=(s,),
        daemon=True
    )

    listen_thread.start()
    send_server(s, nickname)

    end_windows()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
