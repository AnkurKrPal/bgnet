import sys
import os
import socket

HOST = "127.0.0.1"
PORT = 28333
SERVER_ROOT = os.path.abspath('.')

# TODO: Add support for JPEG, etc.
mime_types = {
    ".txt": "text/plain; charset=iso-8859-1",
    ".html": "text/html; charset=iso-8859-1"
}

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])

def read_file(filename):
    try:
        with open(filename, "rb") as fp:
            data = fp.read()
            return data
    except (FileNotFoundError, OSError):
        return None

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))

sock.listen()

while True:
    new_conn = sock.accept()
    new_sock = new_conn[0]

    http_req = b"";

    while True:
        data = new_sock.recv(4096)
        http_req += data
        if b"\r\n\r\n" in http_req:
            break


    print(http_req.decode("ISO-8859-1"))
    # perfrom split
    lines_http_req = http_req.split(b"\r\n")
    req_header = lines_http_req[0].decode("ISO-8859-1")
    req_method, req_filepath, _ = req_header.split(" ")

    # only serve files from the webserver dir
    # use stdlibs to make it more portable
    filename = os.path.split(req_filepath)[-1]
    _, extension = os.path.splitext(filename)
    res_content_type = mime_types.get(extension)
    
    filepath = os.path.sep.join((SERVER_ROOT, filename))
    res_payload = read_file(filepath)
    if res_payload is None:
        http_err_res = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 16\r\n"
            "Connection: close\r\n"
            "\r\n"
            "404 not found \r\n"
        )
        new_sock.sendall(http_err_res.encode("ISO-8859-1"))
        new_sock.close()
        continue

    res_content_length = len(res_payload)
    http_res_headers = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Type: {res_content_type}\r\n"
        f"Content-Length: {res_content_length}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    http_res = http_res_headers.encode("ISO-8859-1") + res_payload

    new_sock.sendall(http_res)
    new_sock.close()
