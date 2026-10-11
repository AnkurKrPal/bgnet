import json

def make_packet(payload: dict):

    json_bytes = json.dumps(payload).encode()

    header = len(json_bytes).to_bytes(2)
    return header + json_bytes

def get_next_packet(buffer: bytes):

    if len(buffer) < 2:
        return None, buffer

    payload_length = int.from_bytes(buffer[:2])

    packet_length = 2 + payload_length

    if len(buffer) < packet_length:
        return None, buffer

    payload_bytes = buffer[2: packet_length]
    remaining_buffer = buffer[packet_length: ]

    payload = json.loads(payload_bytes.decode())

    return payload, remaining_buffer
    
