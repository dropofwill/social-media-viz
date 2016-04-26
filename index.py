from bottle import Bottle, run, route, get, post, static_file
from os import path

app = Bottle()

pwd = path.dirname(__file__)
static_dir = path.join(pwd, 'static/')

# Serve static assets
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=static_dir)

# Root, only server-side view for the website
# For react router purposes, match it for any route not matched above
@app.route('<:re:.+>')
def home():
    return static_file('index.html', root=pwd)

run(app, host='localhost', port=8080, reloader=True)
