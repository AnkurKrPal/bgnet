import sys
import os

def get_bytes_for_IPv4(s: str) -> bytes:
    num_ip = [int(x) for x in s.split('.')]
    return bytes(num_ip)

def checksum(ip_pseudo_header, tcp_zero_cksum):
    data = ip_pseudo_header + tcp_zero_cksum
    offset = 0
    total = 0

    while offset < len(data):
        word = int.from_bytes(data[offset : offset + 2], "big")
        total += word
        total = (total & 0xffff) + (total >> 16)
        offset += 2

    return (~total) & 0xffff

    
ip_pseudo_header = b''

file_num = sys.argv[1]
content = b''

with open(f"tcp_data/tcp_data_{file_num}.dat", "rb") as fd:
    content = fd.read()
    content_length = len(content)
    original_cksum = int.from_bytes(content[16:18], "big")
    tcp_zero_cksum = content[:16] + b'\x00\x00' + content[18:]
    if len(tcp_zero_cksum) % 2 == 1:
        tcp_zero_cksum += b'\x00'


with open(f"tcp_data/tcp_addrs_{file_num}.txt", "rb") as fd:
    content = fd.read()

source_ip_str, destination_ip_str = content.decode().split()

source_ip = get_bytes_for_IPv4(source_ip_str)
destination_ip = get_bytes_for_IPv4(destination_ip_str)


ip_pseudo_header += source_ip + destination_ip + b"\x00\x06" + content_length.to_bytes(2, "big")
# print(" ".join(f"{b:02x}" for b in ip_pseudo_header))

found_cksum = checksum(ip_pseudo_header, tcp_zero_cksum)

if found_cksum == original_cksum:
    print("PASS")
else: print("FAIL")
