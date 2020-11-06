"""common

This module has common functionality to both client and server
"""

class GameState:
    def __init__(self):
        self.opponentPos = [OPPONENT_START_X, OPPONENT_START_Y, RACKET_HEIGHT]
        self.ownPos = [OWN_START_X, OWN_START_Y, RACKET_HEIGHT]
        self.ballPos = [0, 0, 0]
        self.ballVelocity = [0, 0, 0]
        self.opponentPoints = 0
        self.ownPoints = 0
        self.gameOver = False
        self.ownRacketTilt = 1.0
        self.ownRacketVelocity = [0,0]
        
