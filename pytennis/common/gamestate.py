"""gamestate

This module has common functionality regarding gamestate to both client and server
"""

from pygame.math import Vector2

OPPONENT_START_X = 0
OPPONENT_START_Y = 0
RACKET_HEIGHT = 42
OWN_START_X = 0
OWN_START_Y = 0


class GameState:
    """GameState is a class to deal with shared game data between clients"""
    def __init__(self):
        self.opponentPos = Vector2(OPPONENT_START_X, OPPONENT_START_Y)
        self.ownPos = Vector2(OWN_START_X, OWN_START_Y)
        self.ballPos = Vector2(0, 0)
        self.ballVelocity = Vector2(0, 0)
        self.opponentPoints = 0
        self.ownPoints = 0
        self.gameOver = False
        self.ownRacketYaw = 1
        self.opponentRacketYaw = 1


    def __str__(self):
        s = "Game State:\n"
        s += f"\tOpponent position: {self.opponentPos}\n"
        s += f"\tOwn position: {self.ownPos}\n"
        s += f"\tBall position: {self.ballPos}\n"
        s += f"\tBall velocity: {self.ballVelocity}\n"
        s += f"\tOpponents points: {self.opponentPoints}\n"
        s += f"\tOwn points: {self.ownPoints}\n"
        s += f"\tGame over: {self.gameOver}\n"
        s += f"\tOwn racket yaw: {self.ownRacketYaw}\n"
        s += f"\tOpponent racket yaw: {self.opponentRacketYaw}\n"
        return s
        

        
