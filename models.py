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
        return '<User %r>' % self.text
