from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify
from flask import request
import configparser
import logging
import uuid
from game import Game
from gameexception import GameException
from player import Player
from hand import Hand

# Value mapping
LOG_LEVELS = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG,
              'WARN': logging.DEBUG, 'ERROR': logging.ERROR}

# Create application
app = Flask(__name__)

# Read external config
config = configparser.ConfigParser()
config.read('app.cfg')
app.config['MONGO_DBNAME'] = config['DATABASE']['dbName']
app.config['MONGO_URI'] = config['DATABASE']['dbURI']
logfile = config['LOGGING']['logFile']
loglevel = LOG_LEVELS[config['LOGGING']['logLevel']]
runPort = config['PORT']['port']

# Set up logging
#fh = logging.FileHandler(logfile, mode='a', encoding='utf8', delay=False)
#fmt = logging.Formatter(
#    '%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s')
#fh.setFormatter(fmt)
#app.logger.setLevel(loglevel)
#app.logger.addHandler(fh)

# Set up database
#ongo = PyMongo(app)

thegame = None

@app.route('/', methods=['GET'])
def about():
    return jsonify({'about': 'PokerPracticeTwo version 1.0'})

@app.route('/game/<id>', methods=['GET'])
def gamestatus(id):
    global thegame
    if thegame == None or thegame.ID != id:
        return (jsonify({'error': 'No game or wrong game'}), 400)
    status = thegame.summarise()
    return (jsonify(status), 200)

@app.route('/startgame', methods=['POST'])
def startgame():
    global thegame
    if thegame != None and thegame.ID != None:
        return (jsonify({'error': 'Game already started'}), 400)
    game_id = str(uuid.uuid4())
    thegame = Game()
    thegame.ID = game_id
    return (jsonify({'game_id': thegame.ID}), 200)

@app.route('/endgame', methods=['POST'])
def endgame():
    global thegame
    thegame = None
    return ('', 204)

@app.route('/addplayer', methods=['POST'])
def addplayer():
    global thegame
    req = request.get_json()
    id = req['game_id']
    if thegame == None or thegame.ID != id:
        return (jsonify({'error': 'No game or wrong game'}), 400)
    name = req['name']
    try:
        player = Player(name)
        thegame.addplayer(player)
    except GameException as e:
        return (jsonify({'error': str(e)}), 400)
    return (jsonify({'player_id': str(player.getid())}), 200)

@app.route('/newhand', methods=['POST'])
def newhand():
    global thegame
    req = request.get_json()
    id = req['game_id']
    if thegame == None or thegame.ID != id:
        return (jsonify({'error': 'No game or wrong game'}), 400)
    hand = thegame.newhand()
    hand.deal()
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=False)
