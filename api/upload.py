import os
from py2neo import Graph, authenticate

from api import json_io

upload_query = '''
WITH {json} AS tweets
UNWIND tweets as t
MERGE (tweet:Tweet {id: t.id})
SET tweet.text = t.text,
    tweet.created_at = t.created_at,
    tweet.coordinates = t.coordinates.coordinates,
    tweet.favorited = t.favorited,
    tweet.favorite_count = t.favorite_count,
    tweet.lang = t.lang,
    tweet.retweeted = t.retweeted,
    tweet.retweet_count = t.retweet_count,
    tweet.source = t.source,
MERGE (user:User {id: t.user.id})
SET user.screen_name = t.user.screen_name,
    user.name = t.user.name,
    user.created_at = t.user.created_at,
    user.description = t.user.description,
    user.favourites_count = t.user.favourites_count,
    user.followers_count = t.user.followers_count,
    user.friends_count = t.user.friends_count,
    user.geo_enabled = t.user.geo_enabled,
    user.lang = t.user.lang,
    user.location = t.user.location,
    user.statuses_count = t.user.statuses_count
MERGE (user)-[:POSTS]->(tweet)
FOREACH (h IN t.entities.hashtags |
    MERGE (tag:Hashtag {name:LOWER(h.text)})
    MERGE (tag)-[:TAGS]->(tweet)
)
FOREACH (um IN t.entities.user_mentions |
    MERGE (user_m:User {id: um.id})
    SET user_m.name = um.name,
        user_m.screen_name = um.screen_name
    MERGE (tweet)-[:MENTIONS]->(user_m)
)
FOREACH (_ IN CASE WHEN t.in_reply_to_status_id <> 'None' THEN [1] ELSE [] END |
    MERGE (reply_t:Tweet {id: t.in_reply_to_status_id})
    MERGE (reply_u:User {id: t.in_reply_to_user_id})
    SET reply_u.screen_name = t.in_reply_to_screen_name
    MERGE (reply_u)-[:POSTS]->(reply_t)
    MERGE (tweet)-[:REPLIES_TO]->(reply_t)
)
'''

def authenticated_graph():
    return Graph('http://neo4j:neo4j_password@localhost:7474/db/data/')

def load(path, chunk_size=100):
    graph = authenticated_graph()

    for batch in json_io.read_chunked_newline_json(path, chunk_size):
        print('Loading a batch of ' + len(batch) + ' tweets.')
        graph.run(upload_query, json=batch)

def wipe():
    return authenticated_graph().delete_all()
