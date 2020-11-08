"""networking

This module has common functionality regarding networking for both the client and server
"""


# host and port
HOST = "tennis.alepou.no"      # can be any IPv4 address or valid hostname
PORT = 59338            # must be between 1024 and 65535

MAX_PACKET_SIZE = 1024  # max number of bytes that will be sent through a connection at a time
