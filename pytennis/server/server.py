# buildt with pyhton 3.8


import socket
import pickle
import selectors
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from common.gamestate import GameState
from common import networking
from server import servermechanics


def yield_connections(listen_socket):
    listen_socket.bind(("", networking.PORT))
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.listen()

    print("Listening...")

    while True:
        player_one = listen_socket.accept()
        player_two = listen_socket.accept()
        yield (player_one, player_two)


def game_handler(player_pair):
    player_one_socket = player_pair[0][0]
    player_two_socket = player_pair[1][0]

    with player_one_socket as p1:
        with player_two_socket as p2:
            p1.sendall(networking.CONNECTED_MSG)
            p2.sendall(networking.CONNECTED_MSG)

            try:
                servermechanics.main(p1, p2)
            except Exception as e:
                logger.error(e)

                    


    


def main():

    from concurrent.futures import ThreadPoolExecutor
    import threading

    # listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # conn = listen_socket.accept()
    # conn.sendall(bytes("a test", "utf-8"))
    # return


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        for pair in yield_connections(listen_socket):
            game_handler(pair)
            #threading.Thread(target=game_handler, args=(pair,)).start()
        # with ThreadPoolExecutor(max_workers=20) as pool:
        #     pool.map(game_handler, yield_connections(listen_socket))
