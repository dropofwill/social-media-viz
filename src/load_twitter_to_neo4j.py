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

    # query='''
    # WITH {json} AS tweets
    # UNWIND tweets as t
    # RETURN
    # CASE
    # WHEN t.in_reply_to_status_id <> 'None'
    # THEN t.in_reply_to_status_id
    # END
    # '''

    # query='''
    # WITH {json} AS doc
    # UNWIND doc AS tw
    # UNWIND tw.user AS original_user
    # UNWIND tw.entities AS entities
    # UNWIND entities.user_mentions AS user_mention
    # UNWIND entities.hashtags AS hashtag
    # MERGE (u:User {id: original_user.id_str,
    #                name: original_user.name,
    #                screen_name: original_user.screen_name,
    #                location: original_user.location,
    #                description: original_user.description})
    #
    # MERGE (um:User {id: user_mention.id_str,
    #                name: user_mention.name,
    #                screen_name: user_mention.screen_name,
    #                location: user_mention.location,
    #                description: user_mention.description})
    #
    # MERGE (u)-[:MENTIONED]->(um)
    # '''
    # MERGE (u:User {id:tw.user.id_str}) ON CREATE
    #     SET u.name = tw.user.name,
    #         u.screen_name = tw.user.screen_name,
    #         u.location = tw.user.location,
    #         u.description = tw.user.description

    # FOREACH (um IN tw.entities.user_mentions |
    #     MERGE (um2:User {id:tw.entities.user_mentions.id_str}) ON CREATE
    #         SET um2.name = tw.user.name,
    #             um2.screen_name = tw.user.screen_name
    #     MERGE (u)-[:MENTIONED]->(um2))

    # ou:User {id:tw.user.id_str}

    # MERGE (um:User {id:id_str}) ON CREATE
    #     SET um.name = user_mentions.name,
    #         um.screen_name = user_mentions.screen_name

    # RETURN user_mentions.name, user.name

    # query='''
    # WITH {json} AS data
    # UNWIND data AS tweet
    # UNWIND tweet.user AS user
    # RETURN user.name
    # '''

    print(execute(query, json=json))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input-path",
            default="data/roc.liwc.json", nargs="?",
            help="path to input directory, default: 'data/roc.liwc.json'")

    main(parser.parse_args())
