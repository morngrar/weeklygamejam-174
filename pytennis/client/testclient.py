from common.gamestate import GameState
from common import networking
import socket

import pickle

# for terminal testing
import os
import curses
#############

def communicate(win):

    state = GameState()

    schemes = {
        "left" : {
            "up" : "w",
            "left" : "a",
            "right" : "d",
            "down" : "s",
        },
        "right" : {
            "up" : curses.KEY_UP,
            "left" : curses.KEY_LEFT,
            "right" : curses.KEY_RIGHT,
            "down" : curses.KEY_DOWN,
        },
    }
    

    win.nodelay(True)
    key = ""
    win.clear()
    win.addstr("Waiting for opponent...")

    scheme = schemes["right"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((networking.HOST, networking.PORT))
        server.sendall(pickle.dumps(state))

        while True:
            data = server.recv(networking.MAX_PACKET_SIZE)
            if not data:
                break

            state = pickle.loads(data)
            win.clear()
            win.addstr(str(state))
            try:
                key = win.getkey()
                if key == os.linesep:
                    break
                if key == "l":
                    scheme = schemes["left"]
                if key == "q":
                    break
                if key == "r":
                    scheme = schemes["right"]
                if key == scheme["up"]:
                    state.ownPos[1] += 1
                if key == scheme["down"]:
                    state.ownPos[1] -= 1
                if key == scheme["left"]:
                    state.ownPos[0] -= 1
                if key == scheme["right"]:
                    state.ownPos[0] += 1
            except Exception as e:
                pass

            server.sendall(pickle.dumps(state))


def main():
    # state = GameState()
    # print(state)

    curses.wrapper(communicate)
