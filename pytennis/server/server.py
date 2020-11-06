# buildt with pyhton 3.8


import socket
import pickle
import selectors

from common.gamestate import GameState
from common import networking


def yield_connections(listen_socket):
    listen_socket.bind((networking.HOST, networking.PORT))
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.listen()

    while True:
        player_one = listen_socket.accept()
        player_two = listen_socket.accept()
        yield (player_one, player_two)


def game_handler(player_pair):
    player_one_socket = player_pair[0][0]
    player_two_socket = player_pair[1][0]

    state = GameState()
    state.gameStarted = True

    with player_one_socket as p1:
        with player_two_socket as p2:
            active = p1
            while True:
                active.sendall(pickle.dumps(state))

                data = active.recv(networking.MAX_PACKET_SIZE)
                if not data:
                    break
                    
                state = pickle.loads(data)
                stateswap(state)
                if active is p1:
                    active = p2
                else:
                    active = p1

def stateswap(state):
    state.ownPos, state.opponentPos = state.opponentPos, state.ownPos
    state.ownPoints, state.opponentPoints = state.opponentPoints, state.ownPoints
    state.ownRacketTilt, state.opponentRacketTilt = state.opponentRacketTilt, state.ownRacketTilt
    state.ownRacketVelocity, state.opponentRacketVelocity = state.opponentRacketVelocity, state.ownRacketVelocity
    


def main():

    from concurrent.futures import ThreadPoolExecutor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        with ThreadPoolExecutor(max_workers=20) as pool:
            pool.map(game_handler, yield_connections(listen_socket))
