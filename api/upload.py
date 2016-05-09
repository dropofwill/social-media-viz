'''
For brand new database run:

    graph = authenticated_graph()
    upload_json(graph, path_to_json_file)
    merge_tweet_liwc(graph)
    merge_tweet_emolex(graph)
'''
import os
from py2neo import Graph, Node, Relationship, authenticate

from api import json_io, liwc, emolex

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
    tweet.source = t.source
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
    MERGE (tweet)-[:TAGS]->(tag)
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

def upload_json(graph, path, chunk_size=100):
    n = 0
    for batch in json_io.read_chunked_newline_json(path, chunk_size):
        print('Loaded {0} batches of {1} tweets.'
                .format(str(n), str(len(batch))))
        n = n + 1
        graph.run(upload_query, json=batch)

'''
'''
def merge_tweet_liwc(graph):
    query='''
    MATCH (t:Tweet) WHERE NOT (t)-[:HAS_LIWC]-() AND NOT t.text IS NULL
    RETURN t
    '''
    print('Finding tweets without Liwc data...')
    match_cursor = graph.run(query)

    print('Begin merging tweets with Liwc data...')
    # just for reporting progress
    n = 0
    while match_cursor.forward():
        tx = graph.begin()
        tweet_node = match_cursor.current['t']
        summary = liwc.summarize_string(tweet_node['text'])
        l_n = Node('Liwc', id='liwc:tweet:' + str(tweet_node['id']))

        for k,v in summary.items():
            l_n[k] = v

        tx.merge(l_n, primary_label='Liwc', primary_key='id')

        has_liwc = Relationship(tweet_node, 'HAS_LIWC', l_n)

        tx.merge(has_liwc)
        tx.commit()

        n = n + 1
        if n % 100 is 0:
            print("Updated {} tweets with LIWC information".format(n))

    print("Updated {} tweets with LIWC information".format(n))

def merge_tweet_emolex(graph):
    query='''
    MATCH (t:Tweet) WHERE NOT (t)-[:HAS_EMOLEX]-() AND NOT t.text IS NULL
    RETURN t
    '''
    print('Finding tweets without EmoLex data...')
    match_cursor = graph.run(query)

    print('Begin merging tweets with EmoLex data...')
    # just for reporting progress
    n = 0
    while match_cursor.forward():
        # start a transaction
        tx = graph.begin()

        tweet_node = match_cursor.current['t']
        summary = emolex.summarize_string(tweet_node['text'])
        l_n = Node('EmoLex', id='emolex:tweet:' + str(tweet_node['id']))

        for k,v in summary.items():
            l_n[k] = v

        tx.merge(l_n, primary_label='Liwc', primary_key='id')

        has_emolex = Relationship(tweet_node, 'HAS_EMOLEX', l_n)

        tx.merge(has_emolex)
        tx.commit()

        n = n + 1
        if n % 100 is 0:
            print("Updated {} tweets with EmoLex information".format(n))

    print("Updated {} tweets with EmoLex information".format(n))

# def wipe():
#     return authenticated_graph().delete_all()
