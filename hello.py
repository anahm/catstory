import os
from flask import Flask, session, render_template, request, abort
import pusher, random

# db boilerplate code?
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = '\xd8\xd0=\x1b\xcf5\xc0\xd7gt\xc1#\xffT\xe1i^*2Bq\x8ad\xd7'

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)
from models import Game, Player#, TextEntry, PicturesEntry


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/test_pusher')
def testPusher():
	p = pusher.Pusher(
	  app_id='50464',
	  key='f0690b5e328eda453c5b',
	  secret='a6da6bf5e1eea3f480fb'
	)
	p['test_channel'].trigger('my_event', {'message': 'hello world'})
	return 'pushed'

@app.route('/makeGame', methods=['POST', 'GET'])
def makeGame():
	if request.method == 'POST':
		username = request.form['username']

		# make player object
		clientId = random.randrange(0, 10000) #TODO(junjun): make random Id
		player = Player(name=username, clientId=clientId)
		db.session.add(player)
		# make a game object
		#TODO(junjun): figure out how to make player list
		game = Game(players=[player], currentRound=0, numRounds=1)
		db.session.add(game)
		db.session.commit()
		print game.players.count()
		# get game id
		gameId = game.id
		print gameId
		session['gameId'] = gameId
		session['username'] = username
		session['clientId'] = clientId
		return render_template('start.html')
	abort(401)

@app.route('/confirmStart')
def confirmStart():
	gameId = session['gameId']
	# get game object
	game = Game.query.filter_by(id = gameId).first()
	#TODO(peter): game start socket call

	return render_template('game.html', gameId=gameId)

@app.route('/game/<int:gameId>')
def game(gameId):
	session['gameId'] = gameId
	return render_template('joinGame.html', gameId=gameId)

@app.route('/join', methods=['POST', 'GET'])
def join():
	# get username, gameId from POST
	if request.method == 'POST':
		username = request.form['username']
		session['username'] = username
		clientId = random.randrange(0, 10000)
		session['clientId'] = clientId #TODO(junjun): random id
		gameId = session['gameId']
		# create player
		player = Player(name=username, clientId=clientId)
		db.session.add(player)
		# add player to game
		game = Game.query.filter_by(id = gameId).first()
		game.players.append(player)
		game.numRounds = game.numRounds + 1
		db.session.commit()
		# TODO(peter): socket call to host "friend joined"
		return "joined"
	abort(401)
	#return "hi"

@app.route('/recieveData', methods=['POST', 'GET'])
def receiveData():
	if request.method == 'POST':
		# get user
		clientId = POST['clientId'] # is this a thing?
		user = Player.query.filter_by(clientId = clientId).first()
		# # get game
		gameId = POST['gameId']
		game = Game.query.filter_by(id = gameId).first()
		# # currentPlayerIndex = game.players index of clientId
		# prevPlayer = game.players.get(currentPlayerIndex--) # mod 
		# # check if text or picture
		# if (game.currentRound % 2 == 0): 
		# # from text/pictures, get game = game, round = game.currentRound, from = game.user.previous
		# 	entry = TextEntry.query.filter_by(game = gameId, round = game.currentRound-1, from = prevPlayer)
		# 	# return entry.content + entry._id
		# else:
		# 	entry = PicturesEntry.query.filter_by(game = gameId, round = game.currentRound-1, from = prevPlayer)
		# 	# return entry.pictures + entry._id
		return "results"
	abort(401)

@app.route('/sendText', methods=['POST', 'GET'])
def sendData():
	if request.method == 'POST':
		# # get user
		# clientId = POST['clientId'] # is this a thing?
		# user = User.query.filter_by(clientId = clientId).first()
		# # get game
		# gameId = POST['gameId']
		# game = Game.query.filter_by(id = gameId).first()
		# content = request.form['content']
		# inResponseTo = request.form['prevId']
		# #check if text or picture
		# size = 0
		# if (game.currentRound % 2 == 0): 
		# #make picture/text: game = game, pictures = request.form['pictures/text'], inresponseto = request.form['prevId'], from = user, round = game.round
		# 	textEntry = TextEntry(game._id, content, inResponseTo, clientId, game.currentRound)
		# 	db.session.add(textEntry)
		# 	db.session.commit()
		# 	size = TextEntry.query.filter_by(gameId = game._id, round=game.currentRound).size()
		# else:
		# 	pictureEntry = PicturesEntry(game._id, content, inResponseTo, clientId, game.currentRound)
		# 	db.session.add(pictureEntry)
		# 	db.session.commit()
		# 	size = PictureEntry.query.filter_by(gameId = game._id, round=game.currentRound).size()
		# #size = get all from picture/text: game = game, round = round
		# if (size == game.players.size):
		# 	game.round++
		# 	if (game.round == game.numRounds):
		# 		#TODO(peter): sockets call to end
		# 	else: 
		# 		#TODO(peter): sockets call to start new game
		# else:
		# 	return "sent"
		return "sent"
	abort(401)
