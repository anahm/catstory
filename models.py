# sentence db

from hello import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='game', lazy='dynamic')
    currentRound = db.Column(db.Integer)
    numRounds = db.Column(db.Integer)

    def __repr__(self):
        return '<Game Id = %d>' % self.id

    def getPlayersSerialized(self):
        toReturn = []
        for player in self.players.all():
            toReturn.append(player.serialize())
        return toReturn

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    clientId = db.Column(db.Integer, unique=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    order = db.Column(db.Integer)

    def serialize(model):
        return dict(name = model.name, clientId = model.clientId, gameId = model.game_id)

class TextEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    inResponseTo = db.Column(db.Integer)
    content = db.Column(db.String(120))
    fromId = db.Column(db.Integer, db.ForeignKey('player.id'))
    round = db.Column(db.Integer)

class PictureEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    inResponseTo = db.Column(db.Integer)
    pictures = db.Column(db.String(500))
    fromId = db.Column(db.Integer, db.ForeignKey('player.id'))
    round = db.Column(db.Integer)