import os
from flask import Flask, session, render_template, url_for, request, abort
import pusher
import random
import requests
import json
from requests.auth import HTTPBasicAuth

# db boilerplate code?
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = '\xd8\xd0=\x1b\xcf5\xc0\xd7gt\xc1#\xffT\xe1i^*2Bq\x8ad\xd7'

BING_LINK = 'https://api.datamarket.azure.com/Bing/Search/Image?$format=json'
BING_API_KEY = 'N95x+ajghz4OP94AMQgR46/TkWDBwxmtatNd5Wkvkrc'

if 'DATABASE_URL' in os.environ:
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)
from models import Game, Player, TextEntry, PictureEntry

p = pusher.Pusher(
	app_id='50464',
	key='f0690b5e328eda453c5b',
	secret='a6da6bf5e1eea3f480fb'
)

# from join.html, players to join game
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
		curSize = Player.query.filter_by(game_id = gameId).count()
		player.order = curSize
		db.session.add(player)
		# add player to game
		game = Game.query.filter_by(id = gameId).first()
		game.players.append(player)
		game.numRounds = game.numRounds + 1
		db.session.commit()
		
		p['game' + str(gameId)].trigger('playerJoin', {'newPlayer': {'name': username}})
		return "joined"
	abort(401)
	#return "hi"

# from start.html, host to start game
@app.route('/confirmStart')
def confirmStart():
	gameId = session['gameId']
	# get game object
	game = Game.query.filter_by(id = gameId).first()
	#TODO(peter): game start socket call

	return render_template('game.html', gameId=gameId)

# from start.html and join.html, gets a list of players
# params: gameId
@app.route('/getPlayersForGame/<int:gameId>', methods=['POST', 'GET'])
def getPlayersForGame(gameId):
	game = Game.query.filter_by(id = gameId).first()
	return json.dumps(game.getPlayersSerialized())

# from game.html, gets next round's data
# params: clientId
@app.route('/getData', methods=['POST', 'GET'])
def getData():
	if request.method == 'POST':
		# get user
		clientId = request.form['clientId'] # is this a thing?
		player = Player.query.filter_by(clientId = clientId).first()
		# # get game
		gameId = POST['gameId']
		game = Game.query.filter_by(id = gameId).first()
		prevOrder = (player.order - 1) % game.players.count()
		prevPlayer = Player.query.filter_by(game_id = gameId, order = prevOrder)
		# check if text or picture
		if (game.currentRound % 2 == 0): 
			entry = TextEntry.query.filter_by(game = gameId, round = game.currentRound-1, fromId = prevPlayer.id)
		 	return render_template('recieveText.html', content = entry.content, inResponseTo = entry.id)
		else:
		 	entry = PictureEntry.query.filter_by(game = gameId, round = game.currentRound-1, fromId = prevPlayer.id)
		 	return render_template('recievePictures.html', content = entry.pictures, inResponseTo = entry.id)
		return "results"
	abort(401)

# from game.html, send what user has input
# params: clientId, content, inResponseTo 
@app.route('/sendData', methods=['POST', 'GET'])
def sendData():
	if request.method == 'POST':
		# get user
		clientId = request.form['clientId'] # is this a thing?
		player = Player.query.filter_by(clientId = clientId).first()
		# get game
		gameId = POST['gameId']
		game = Game.query.filter_by(id = gameId).first()
		content = request.form['content']
		inResponseTo = request.form['inResponseTo']
		#check if text or picture
		size = 0
		if (game.currentRound % 2 == 0): 
		#make picture/text: game = game, pictures = request.form['pictures/text'], inresponseto = request.form['prevId'], from = user, round = game.round
		 	textEntry = TextEntry(game = gameId, content = content, inResponseTo = inResponseTo, fromId = player.id, round = game.currentRound)
		 	db.session.add(textEntry)
		 	db.session.commit()
		 	size = TextEntry.query.filter_by(gameId = gameId, round=game.currentRound).count()
		else:
		 	pictureEntry = PictureEntry(game = gameId, content = content, inResponseTo = inResponseTo, fromId = player.id, round = game.currentRound)
		 	db.session.add(pictureEntry)
		 	db.session.commit()
		 	size = PictureEntry.query.filter_by(gameId = gameId, round=game.currentRound).count()
		if (size == game.players.size):
		 	game.currentRound = game.currentRound + 1
		 	if (game.currentRound == game.numRounds):
		 		#TODO(peter): sockets call to end
		 		print "end"
		 	else: 
		 		#TODO(peter): sockets call to start new round
		 		print "new"
		return "sent"
	abort(401)

@app.route('/imageSearch/<query>', methods=['POST', 'GET'])
def imageSearch(query):
	r = requests.get(BING_LINK + "&Query=%27" + query + "%27", auth=HTTPBasicAuth(BING_API_KEY, BING_API_KEY))
	return r.text

# =====================
# Actual Pages
# =====================

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/test_words')
def testWords():
	return render_template('testWords.html')

@app.route('/test_pusher')
def testPusher():	
	p['test_channel'].trigger('my_event', {'message': 'hello world'})
	return 'pushed'

@app.route('/makeGame', methods=['POST', 'GET'])
def makeGame():
	if request.method == 'POST':
		username = request.form['username']

		# make player object
		clientId = random.randrange(0, 10000) #TODO(junjun): make random Id
		player = Player(name=username, clientId=clientId, order=0)
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

@app.route('/join/<int:gameId>')
def displayJoin(gameId):
	session['gameId'] = gameId
	return render_template('join.html', gameId=gameId)

# TESTTTTTT
@app.route('/image')
def image():
	return render_template("image.html")

