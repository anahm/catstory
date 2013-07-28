import os
from flask import Flask, session, render_template

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

@app.route('/start')
def start():
	# make a game object
	# get game id
	gameId = 1
	session['gameId'] = gameId
	return render_template('start.html', gameId=gameId)

# @app.route('/join/<int:gameId>')
# def join(username, gameId):
