# social-media-viz

Discover new research topics from social media using LIWC / EmoLex visualizations.

## Requirements

Environment
* Python 3.5 or above
* Node.js/NPM 5.0 or above
* Neo4J graph database

Data / Lexicons
* LIWC lexicon (purchase required)
* NRC Emolex lexicon (free for research use)
* Some JSON Twitter data (freely downloadable, but not for sharing)

```
# Clone the repo
$ git clone git@github.com:dropofwill/social-media-viz.git
$ cd social-media-viz

# Install neo4j, on Mac with homebrew for example:
$ brew update && brew install neo4j
# start it
$ neo4j start
# If first time setup with username: neo4j, password: neo4j_password
# By going to localhost:7474

# Install required Python modules
$ pip install -r requirements.txt

# Install required client side JS modules
$ npm install

# start the server
$ python index.py

# build the client
$ npm run build
```

To do the initial upload of twitter data run the following in the clone project directory (upload via web interface, coming soon!), using iPython for example:

```
$ PYTHONSTARTUP='./config.py' ipython
... in the ipython session

[1]: upload.upload_json(graph, path_to_json_file)
[2]: upload.merge_tweet_liwc(graph)
[3]: upload.merge_tweet_emolex(graph)
```

This might take a while (30 minutes on my machine, with a months worth of regional Tweets).

## Usage

Point your browser to localhost:1339 to view the visualization

Point your browser to localhost:7474 to interact with the Neo4j instance directly


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

