"""gamestate

This module has common functionality regarding gamestate to both client and server
"""

OPPONENT_START_X = 0
OPPONENT_START_Y = 0
RACKET_HEIGHT = 42
OWN_START_X = 0
OWN_START_Y = 0


class GameState:
    """GameState is a class to deal with shared game data between clients"""
    def __init__(self):
        self.opponentPos = [OPPONENT_START_X, OPPONENT_START_Y, RACKET_HEIGHT]
        self.ownPos = [OWN_START_X, OWN_START_Y, RACKET_HEIGHT]
        self.ballPos = [0, 0, 0]
        self.ballVelocity = [0, 0, 0]
        self.opponentPoints = 0
        self.ownPoints = 0
        self.gameStarted = False
        self.gameOver = False
        self.ownRacketTilt = 1.0
        self.ownRacketVelocity = [0,0]


    def __str__(self):
        s = "Game State:\n"
        s += f"\tOpponent position: {self.opponentPos}\n"
        s += f"\tOwn position: {self.ownPos}\n"
        s += f"\tBall position: {self.ballPos}\n"
        s += f"\tBall velocity: {self.ballVelocity}\n"
        s += f"\tOpponents points: {self.opponentsPoints}\n"
        s += f"\tGame started: {self.gameStarted}\n"
        s += f"\tGame over: {self.gameOver}\n"
        s += f"\tOwn racket tilt: {self.ownRacketTilt}\n"
        s += f"\tOwn racket velocity: {self.ownRacketVelocity}\n"

        

        
