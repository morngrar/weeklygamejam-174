# buildt with pyhton 3.8


import socket
import pickle

from common.gamestate import GameState
from common import networking


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((networking.HOST, networking.PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                # all data received, chekc it
                state = pickle.loads(data)


                conn.sendall(bytes(f"The game is over: {state.gameOver}", "utf-8"))


if __name__ == "__main__":
    main()
