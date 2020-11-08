# buildt with pyhton 3.8


import socket
import pickle
import selectors
import logging

from common.gamestate import GameState
from common import networking


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

    state = GameState()


    with player_one_socket as p1:
        with player_two_socket as p2:
            active = p1
            initial_runs = 2

            while True:
                if initial_runs:
                    active.sendall(networking.CONNECTED_MSG)
                    initial_runs -= 1
                    
                active.sendall(pickle.dumps(state))

                data = active.recv(networking.MAX_PACKET_SIZE)
                if not data:
                    break
                    
                state = pickle.loads(data)

                # swapping players
                stateswap(state)
                if active is p1:
                    active = p2
                else:
                    active = p1

def stateswap(state):
    try:
        state.ownPos, state.opponentPos = state.opponentPos, state.ownPos
        state.ownPoints, state.opponentPoints = state.opponentPoints, state.ownPoints
        state.ownRacketYaw, state.opponentRacketYaw = state.opponentRacketYaw, state.ownRacketYaw
    except Exception as e:
        print(e)
        raise e
    


def main():

    from concurrent.futures import ThreadPoolExecutor

    # listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # conn = listen_socket.accept()
    # conn.sendall(bytes("a test", "utf-8"))
    # return


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        with ThreadPoolExecutor(max_workers=20) as pool:
            pool.map(game_handler, yield_connections(listen_socket))
