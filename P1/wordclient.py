import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    while True:
        # extract from buffer
        if len(packet_buffer) >= WORD_LEN_SIZE:
            # specially used to convert from b'' to integer
            word_length = int.from_bytes(packet_buffer[:WORD_LEN_SIZE])

            if len(packet_buffer) >= WORD_LEN_SIZE + word_length:
                word_packet = b''
                word_packet += packet_buffer[: WORD_LEN_SIZE + word_length]
                packet_buffer = packet_buffer[WORD_LEN_SIZE + word_length:]
                return word_packet

        # keep adding
        data = s.recv(4096)

        # if no data close connection
        if not data:
            return 

        # append data to the buffer
        packet_buffer += data

    # TODO -- Write me!


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """
    # decode return a string
    word = word_packet.decode()
    return word[WORD_LEN_SIZE:]
    # TODO -- Write me!

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
