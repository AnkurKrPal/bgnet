import socket

HOST = "127.0.0.1"
PORT = 65432

# socket object is context manager type
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    # can input a backlog value, o.w. default
    # see cat /proc/sys/net/core/somaxconn for max value (4096)
    sock.listen()
    # blocking call
    # creates new socket obj
    # this is of the client
    conn, addr = sock.accept()
    with conn:
        print(f"Connect by {addr}")
        while True:
            data = conn.recv(1024) # buffer size of 1KB, max limit
            if not data:
                break
            conn.sendall(data)