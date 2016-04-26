from bottle import Bottle, run, route, get, post, static_file

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

run(app, host='localhost', port=8080)
