import falcon 
import json
import psycopg2

size = 4

grid = [[0 for i in range(size)] for j in range(size)]

class GameBoard(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = str(size)

class ScanBoard(object):
    def on_get(self, req, resp, playerId, x, y):
        resp.status = falcon.HTTP_200
        SQL = "SELECT scans_left FROM player WHERE id=(%s)"
        data = str(playerId)
        cur.execute(SQL, data)
        row = cur.fetchone()
        scansLeft = row[0]
        if scansLeft <= 0:
            body = {'status': 'No scans left', 'chairId': -1}
        else:
            SQL = "SELECT id FROM chair WHERE coordinates='{%s,%s}'"
            x = 2
            y = 3
            data = (x, y)
            cur.execute(SQL, data)
            row = cur.fetchone()
            if row:
                chairId = row[0]
                body = {'status': 'Chair found', 'chairId': chairId}
            else:
                body = {'status': 'No chair found', 'chairId': 0}

        resp.body = json.dumps(body)

class SitDown(object):
    def on_get(self, req, resp, userID, x, y):
        resp.status = falcon.HTTP_200
        

# def addRoute(obj, route):
#     api = falcon.API()
#     api.add_route(route, obj)

# addRoute(GameBoard(), '/board')
# addRoute(ScanBoard(), '/scan/{x}/{y}')

conn = psycopg2.connect(dbname = 'musicalchairs', user = 'oskar', password = 'bajs', host = 'localhost')
cur = conn.cursor()
cur.execute("""select * from player""")
rows = cur.fetchall()
for row in rows:
    print(row)

playerId = 1
SQL = """SELECT scans_left FROM player WHERE id=(%s)"""
data = str(playerId)
cur.execute(SQL, data)
rows = cur.fetchall()
for row in rows:
    print(row)

SQL = "SELECT id FROM chair WHERE coordinates='{%s,%s}'"
x = 2
y = 3
data = (x, y)
cur.execute(SQL, data)
row = cur.fetchone()
if row:
    chairId = row[0]
    body = {'status': 'Chair found', 'chairId': chairId}
else:
    body = {'status': 'No chair found', 'chairId': 0}
print(body)

app = falcon.API()
gameBoard = GameBoard()
scanBoard = ScanBoard()
app.add_route('/board', gameBoard)
app.add_route('/scan/{x}:{y}', scanBoard)
