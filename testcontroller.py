import sys
import unittest
import requests
import json

class TestController(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_controllerrunning(self):
        try:
            r = requests.get('http://localhost:5000/')
            self.assertEqual(r.status_code, 200)
            self.assertNotEqual(r.json().get('about', 'UNEXPECTED RESPONSE'), 'UNEXPECTED RESPONSE')
        except Exception:
            self.assertEqual('', 'Controller not running!')

    def test_newgame(self):
        r = requests.post('http://localhost:5000/endgame')
        self.assertEqual(r.status_code, 204)
        r = requests.post('http://localhost:5000/startgame')
        error = r.json().get('error', '')
        self.assertEqual(error, '')
        gameID = r.json().get('game_id', '')
        self.assertNotEqual(gameID, '')

    def test_addplayer(self):
        r = requests.post('http://localhost:5000/endgame')
        self.assertEqual(r.status_code, 204)
        r = requests.post('http://localhost:5000/startgame')
        self.assertEqual(r.status_code, 200)
        game_id = r.json().get('game_id', '')
        r = requests.post('http://localhost:5000/addplayer', json={'game_id': game_id, 'name': 'Alice'})
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertNotEqual('', res['player_id'])
        r = requests.get('http://localhost:5000/game/'+game_id)
        status = r.json()
        self.assertIn('players', status)
        self.assertIn('Alice', status['players'])

    def test_newhand(self):
        r = requests.post('http://localhost:5000/endgame')
        self.assertEqual(r.status_code, 204)
        r = requests.post('http://localhost:5000/startgame')
        self.assertEqual(r.status_code, 200)
        game_id = r.json().get('game_id', '')
        r = requests.post('http://localhost:5000/addplayer', json={'game_id': game_id, 'name': 'Alice'})
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertNotEqual('', res['player_id'])
        r = requests.post('http://localhost:5000/addplayer', json={'game_id': game_id, 'name': 'Bob'})
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertNotEqual('', res['player_id'])
        r = requests.post('http://localhost:5000/addplayer', json={'game_id': game_id, 'name': 'Janet'})
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertNotEqual('', res['player_id'])
        r = requests.post('http://localhost:5000/addplayer', json={'game_id': game_id, 'name': 'John'})
        self.assertEqual(r.status_code, 200)
        res = r.json()
        self.assertNotEqual('', res['player_id'])
        r = requests.get('http://localhost:5000/game/'+game_id)
        status = r.json()
        self.assertIn('Alice', status['players'])
        self.assertIn('Bob', status['players'])
        self.assertIn('Janet', status['players'])
        self.assertIn('John', status['players'])
        r = requests.post('http://localhost:5000/newhand', json={'game_id': game_id})
        self.assertEqual(r.status_code, 204)
        r = requests.get('http://localhost:5000/game/'+game_id)
        status = r.json()
        self.assertEqual('pre-flop', status['current_hand']['round'])

if __name__ == '__main__':
    try:
        r = requests.get('http://localhost:5000/')
        if r.status_code != 200:
            raise Exception()
    except:
        print('ERROR: API server not running')
        sys.exit(0)

    unittest.main()
