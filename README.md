# social-media-viz

Social Media ILWC Visualization project

## Requirements

* Python 3.x
* NPM
* Neo4J
* LIWC dataset
* NRC Emolex dataset
* Some JSON Twitter data

```
# Install neo4j, on Mac with homebrew for example:
brew update && brew install neo4j
# start it
neo4j start
# If first time setup with username: neo4j, password: neo4j_password
# By going to localhost:7474

# Install required Python modules
pip install -r requirements.txt

# Install required client side JS modules
npm install

# start the server
python index.py

# start the client
npm start
```

## Ideas

Calculate the overlap between any features
* Threshold
* Boolean

Look at connections
* Geographically
* Temporally
* Mentions
* Direct replies
* Same hashtags

