# sentence db

from hello import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='game', lazy='dynamic')
    currentRound = db.Column(db.Integer)
    numRounds = db.Column(db.Integer)

    def __repr__(self):
        return '<Game Id = %d>' % self.id

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    clientId = db.Column(db.Integer, unique=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))