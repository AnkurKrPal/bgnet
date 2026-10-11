
import sys
import socket
import select

from packet import *


def broadcast(read_set, server_sock, payload):
    packet = make_packet(payload)

    for client_sock in read_set:
        if client_sock != server_sock:
            client_sock.sendall(packet)


def run_server(port):
    sock = socket.socket()
    sock.bind(("localhost", port))
    sock.listen()

    read_set = {sock}
    buffers = {}
    nicknames = {}

    while True:
        ready_socks, _, _ = select.select(read_set, [], [])

        for read_sock in ready_socks:
            if read_sock == sock:
                new_sock, address = sock.accept()
                read_set.add(new_sock)
                buffers[new_sock] = b""
                nicknames[new_sock] = None

            else:
                data = read_sock.recv(4096)

                if not data:
                    nickname = nicknames[read_sock]

                    read_set.remove(read_sock)
                    buffers.pop(read_sock)
                    nicknames.pop(read_sock)
                    read_sock.close()

                    if nickname is not None:
                        broadcast(read_set, sock, {
                            "type": "leave",
                            "nick": nickname
                        })

                    continue

                buffers[read_sock] += data

                while True:
                    payload, remaining = get_next_packet(
                        buffers[read_sock]
                    )

                    if payload is None:
                        break

                    buffers[read_sock] = remaining

                    if nicknames[read_sock] is None:
                        if payload["type"] == "hello":
                            nickname = payload["nick"]
                            nicknames[read_sock] = nickname

                            broadcast(read_set, sock, {
                                "type": "join",
                                "nick": nickname
                            })

                    elif payload["type"] == "chat":
                        nickname = nicknames[read_sock]

                        broadcast(read_set, sock, {
                            "type": "chat",
                            "nick": nickname,
                            "message": payload["message"]
                        })


def main(argv):
    if len(argv) != 2:
        print("usage: server.py port", file=sys.stderr)
        return 1

    port = int(argv[1])
    run_server(port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
