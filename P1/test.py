import os

server_root = os.path.abspath('.')
print(server_root)

n =  3490
bytes = n.to_bytes(2)

for b  in bytes:
    print(b)