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


class Player(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    clientId = db.Column(db.String(20), unique=True)

    def __init__(self, name, clientId):
        self.name = name
        self.clientId = clientId

    def __repr__(self):
        return self.name


class TextEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer, unique=True)
    inResponseTo = db.Column(db.Integer, unique=True)
    content = db.Column(db.String(120), unique=True)

    def __init__(self, gameId, orderId, text):
        self.game = gameId
        self.inResponseTo = orderId
        self.content = text

    def __repr__(self):
        return id

class PictureEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer, unique=True)
    inResponseTo = db.Column(db.Integer, unique=True)
    pictures = db.Column(db.String(500), unique=True)

    def __init__(self, gameId, orderId, pic):
        self.game = gameId
        self.inResponseTo = orderId
        self.pictures = pic

    def __repr__(self):
        return id


