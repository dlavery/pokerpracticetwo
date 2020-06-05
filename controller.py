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
from functools import wraps

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

def checkrequest(payload=True):
    def decorator(fn):
        @wraps(fn)
        def check(*args, **kwargs):
            global thegame
            req = request.get_json()
            if payload and not req:
                return(jsonify({'error': 'Missing payload'}), 400)
            if type(payload) is tuple and not all([e in req for e in payload]):
                return(jsonify({'error': 'Missing parameters' + str(payload)}), 400)
            if not req and not 'id' in kwargs:
                return(jsonify({'error': 'Missing id parameter'}), 400)
            if req and not 'id' in kwargs and not 'game_id' in req:
                return(jsonify({'error': 'Missing game_id parameter'}), 400)
            if 'id' in kwargs:
                id = kwargs['id']
            else:
                id = req['game_id']
            if thegame == None or thegame.ID != id:
                return (jsonify({'error': 'No game or wrong game'}), 400)
            return fn(*args, **kwargs)
        return check
    return decorator

@app.route('/', methods=['GET'])
def about():
    return jsonify({'about': 'PokerPracticeTwo version 0.1'})

@app.route('/game/<id>', methods=['GET'])
@checkrequest(payload=False)
def gamestatus(id):
    global thegame
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
@checkrequest(payload=('name',))
def addplayer():
    global thegame
    req = request.get_json()
    name = req['name']
    try:
        player = Player(name)
        thegame.addplayer(player)
    except GameException as e:
        return (jsonify({'error': str(e)}), 400)
    return (jsonify({'player_id': str(player.getid())}), 200)

@app.route('/newhand', methods=['POST'])
@checkrequest(False)
def newhand():
    global thegame
    hand = thegame.newhand()
    hand.deal()
    return ('', 204)

@app.route('/act', methods=['POST'])
@checkrequest(('player', 'action'))
def act():
    global thegame
    req = request.get_json()
    playername = req['player']
    action = req['action']
    if 'amount' in req:
        amount = int(req['amount'])
    else:
        amount = 0
    player = thegame.player(playername)
    hand = thegame.gethand()
    try:
        hand.act(player, action, amount)
    except Exception as e:
        return(jsonify({'error': str(e)}), 400)
    return ('', 204)

@app.route('/flop', methods=['POST'])
@checkrequest(False)
def flop():
    global thegame
    hand = thegame.gethand()
    hand.flop()
    return ('', 204)

@app.route('/turn', methods=['POST'])
@checkrequest(False)
def turn():
    global thegame
    hand = thegame.gethand()
    hand.turn()
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=False)
