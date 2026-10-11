import sys
import socket

HOST = sys.argv[1]
PORT = 80

if len(sys.argv) > 3:
    PORT = sys.argv[3]


sock = socket.socket()
# automates DNS resolution
sock.connect((HOST, PORT))

http_req = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Connection: close\r\n"
    "\r\n\r\n"
)

sock.sendall(http_req.encode("ISO-8859-1"))

response = b""
while True:
    data = sock.recv(4096)
    if len(data) == 0:
        break
    response += data

print(response.decode("ISO-8859-1"))