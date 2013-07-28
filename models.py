# sentence db

from hello import db

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



