# buildt with pyhton 3.8


import socket

from common import gamestate
from common import networking


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((networking.HOST, networking.PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


if __name__ == "__main__":
    main()
