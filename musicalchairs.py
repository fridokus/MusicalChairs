import falcon 
import json

size = 4

grid = [[0 for i in range(size)] for j in range(size)]

class GameBoard(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = str(size)

class ScanBoard(object):
    def on_get(self, req, resp, x, y):
        resp.status = falcon.HTTP_200
        x = int(x)
        y = int(y)
        body = {'chairId': grid[x][y]}
        resp.body = json.dumps(body)

class SitDown(object):
    def on_get(self, req, resp, userID, x, y):
        resp.status = falcon.HTTP_200
        

# def addRoute(obj, route):
#     api = falcon.API()
#     api.add_route(route, obj)

# addRoute(GameBoard(), '/board')
# addRoute(ScanBoard(), '/scan/{x}/{y}')

app = falcon.API()
gameBoard = GameBoard()
scanBoard = ScanBoard()
app.add_route('/board', gameBoard)
app.add_route('/scan/{x}:{y}', scanBoard)
