from __future__ import print_function
from pprint import pprint
import read
import os
import argparse
import json
from py2neo import Graph, authenticate

def auth():
    authenticate('localhost:7474', 'neo4j', os.environ['NEO4J_PASS'])

def main(args):
    auth()
    graph = Graph()
    execute = graph.cypher.execute

    json = read.read_newline_json(args.input_path, read.ALT_LIWC_KEYS)

    query='''
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
        tweet.wordcount = t.wordcount
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

    print(execute(query, json=json))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input-path",
            default="data/roc.liwc.json", nargs="?",
            help="path to input directory, default: 'data/roc.liwc.json'")

    main(parser.parse_args())
