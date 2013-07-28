# sentence db

from hello import db

class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameId = db.Column(db.Integer, unique=True)
    orderId = db.Column(db.Integer, unique=True)
    text = db.Column(db.String(120), unique=True)

    def __init__(self, gameId, orderId, text):
        self.gameId = gameId
        self.orderId = orderId
        self.text = text

    def __repr__(self):
        return '<User %r>' % self.id

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.Column(db.String(500), unique=True)
    currentRound = db.Column(db.Integer, unique=True)
    numRounds = db.Column(db.Integer, unique=True)

    def __init__(self, players, numRounds):
        self.players = players
        self.currentRound = 0
        self.numRounds = numRounds

    def __repr__(self):
        return '<Game Id = %d>' % self.id

    def getPlayers(self):
        return players

    def getCurrentRound(self):
        return currentRound

    def getNumRounds(self):
        return numRounds

    def addPlayer(self, p1):
        # TODO blargl
        return

    def setCurrentRound(self, newVal):
        self.currentRound = newVal
        return

    def setNumRounds(self, newVal):
        self.numRounds = newVal
        return

