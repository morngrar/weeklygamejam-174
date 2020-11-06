

class GameState:
    def __init__(self):
        self.opponentPos = [OPPONENT_START_X, OPPONENT_START_Y, RACKET_HEIGHT]
        self.ownPos = [OWN_START_X, OWN_START_Y, RACKET_HEIGHT]
        self.ballPos = [0, 0, 0]
        self.opponentPoints = 0
        self.ownPoints = 0
        self.gameOver = False