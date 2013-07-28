import os
from flask import Flask, session, render_template, request, abort
import pusher


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = '\xd8\xd0=\x1b\xcf5\xc0\xd7gt\xc1#\xffT\xe1i^*2Bq\x8ad\xd7'

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
	if request.method = 'POST':
		username = request.form['username']
		# make a game object
		# get game id
		gameId = 1
		username = 'Ali'
		session['gameId'] = gameId
		session['username'] = username
		session['clientId'] = 1 #random id
		#make player object
		return render_template('newGame.html', gameId=gameId)	
	abort(401)

@app.route('/confirmStart')
def confirmStart():
	gameId = session['gameId']
	# get game object
	# game start socket call
	return render_template('game.html', gameId=gameId)

@app.route('/game/<int:gameId>')
def game(gameId):
	session['gameId'] = gameId
	return render_template('start.html', gameId=gameId)

@app.route('/join', methods=['POST', 'GET'])
def join():
	# get username, gameId from POST
	if request.method == 'POST':
		username = request.form['username']
		session['username'] = username
		session['clientId'] = 1 #random id
		gameId = session['gameId']
		# create player
		# add player to game
		# socket call to host "friend joined"
		return "joined"
	abort(401)
	#return "hi"

@app.route('/recieveData')
def receiveData():
	# get user
	# get game
	# check if text or picture
	# from text/pictures, get game = game, round = game.currentRound, from = game.user.previous
	# return pictures or text + text/picture id
	return "HI"

@app.route('/sendText', methods=['POST', 'GET'])
def sendData():
	if request.method == 'POST':
		#get user
		#get game
		#check if text or picture
		#make picture/text: game = game, pictures = request.form['pictures/text'], inresponseto = request.form['prevId'], from = user, round = game.round
		#get all from picture/text: game = game, round = round
			#if size = game.players.size
				#game.round++
				#if game.round = game.numrounds
					#sockets call to end
				#else 
					#sockets call to start new game
	abort(401)