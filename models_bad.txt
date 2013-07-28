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

class Player(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    clientId = db.Column(db.String(20), unique=True)

    def __init__(self, name, clientId):
        self.name = name
        self.clientId = clientId

    def __repr__(self):
        return self.name

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def setName(self, n):
        self.name = n
        return

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

    def getGame(self):
        return self.game

    def getInResponseTo(self):
        return self.inReponseTo

    def getContent(self):
        return content

    def setGame(self, g):
        self.game = g
        return

    def setInReponseTo(self, i):
        self.inReponseTo = i
        return

    def setContent(self, c):
        self.content = c

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

    def getGame(self):
        return self.game

    def getInResponseTo(self):
        return self.inReponseTo

    def getPictures(self):
        return pictures

    def setGame(self, g):
        self.game = g
        return

    def setInReponseTo(self, i):
        self.inReponseTo = i
        return

    def setPictures(self, c):
        self.pictures = c

