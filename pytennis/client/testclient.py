from common.gamestate import GameState
from common import networking
import socket

import pickle

def main():

    state = GameState()

    state.gameOver = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((networking.HOST, networking.PORT))
        s.sendall(pickle.dumps(state))
        data = s.recv(1024)

    print('Received', repr(data))
