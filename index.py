from bottle import Bottle, run, route, get, post, static_file
from os import path

app = Bottle()

pwd = path.dirname(__file__)
static_dir = path.join(pwd, 'static/')

# Serve static assets
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=static_dir)

'''
Filter query strings:

start=MM-DD-YYYY        Date range
end=MM-DD-YYYY          Date range
conversations=bool      Whether two report on tweets or conversations
hashtags=list[str]      By a list of hashtags
keywords=list[str]      By a list of strings in the text of a tweet or conversation

/api/upload

/api/meta

/api/raw

# 
@app.post('/api/meta/counts')

'''

# Root, only server-side view for the website
# For react router purposes, match it for any route not matched above
@app.route('<:re:.+>')
def home():
    return static_file('index.html', root=pwd)

run(app, host='localhost', port=8080, reloader=True)
