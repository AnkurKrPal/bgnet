# Example usage:
#
# python3 select_server.py 3490

import sys
import socket
import select

def run_server(port):

    sock = socket.socket()
    sock.bind(("localhost", port))
    sock.listen()

    read_set = {sock}

    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})

        for ready_sock in ready_to_read:

            if ready_sock == sock:
                new_conn = sock.accept()
                new_sock = new_conn[0]
                print(f"{new_conn[1]}: connected")
                read_set.add(new_sock)
            else:
                data = ready_sock.recv(4096)

                # remove sock
                if not data:
                    closed_sock_addr = ready_sock.getpeername()
                    print(f"{closed_sock_addr}: disconnected")
                    read_set.discard(ready_sock)
                    break

                len_data = len(data)
                sock_addr = ready_sock.getpeername()
                print(f"{sock_addr} {len_data} {data}")         

    # TODO--fill this in
    pass

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
