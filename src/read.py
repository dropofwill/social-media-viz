from __future__ import print_function
from builtins import map
from builtins import str
from builtins import range
import argparse
import json
from itertools import combinations_with_replacement, combinations

from pprint import pprint
from collections import defaultdict
from codecs import getreader

import numpy as np
from pandas import DataFrame
import networkx as nx
from networkx.readwrite import json_graph

np.set_printoptions(threshold='nan')

# Keys that are related to LIWC metrics
# Not documented, but I think are the same metrics
LIWC_KEYS=[
    u'humans', u'Numerals', u'inhib', u'cogmech', u'excl', u'incl',
    # Documented metrics
    u'family', u'feel', u'money', u'insight', u'sad', u'anger', u'home',
    u'sexual', u'anx', u'achieve', u'negemo', u'percept', u'certain',
    u'relativ', u'health', u'cause', u'friend', u'relig', u'tentat',
    u'see', u'discrep', u'wordcount', u'leisure', u'death', u'hear', u'bio',
    u'affect', u'work', u'space', u'ingest', u'motion', u'swear',
    u'posemo', u'social']

ALT_LIWC_KEYS=[
    u'humans', u'inhib', u'excl', u'incl',
    # Documented metrics
    # Top level
    u'affect', u'social', u'cogmech', u'percept', u'bio', u'relativ',
    # Secondary
    u'family', u'feel', u'money', u'insight', u'sad', u'anger', u'home',
    u'sexual', u'anx', u'achieve', u'negemo', u'certain',
    u'health', u'cause', u'friend', u'relig', u'tentat',
    u'see', u'discrep', u'leisure', u'death', u'hear',
    u'work', u'space', u'ingest', u'motion', u'swear',
    u'posemo',]

TOP_LEVEL_LIWC_KEYS=[
    u'humans', u'inhib', u'excl', u'incl',
    # Documented metrics
    # Top level
    u'affect', u'social', u'cogmech', u'percept', u'bio', u'relativ',]

HAND_PICKED=[
    'affect', 'relativ', 'cogmech', 'percept', 'social',
    'body', 'health', 'sexual',
    'work', 'leisure', 'money',]

def read_newline_json(path, keys_to_use=LIWC_KEYS):
    with open(path, 'rb') as f:
        return [parse_input_json(line.decode('utf8'), keys_to_use)
                for line in f.readlines()]

def read_valid_json(path):
    with open(path, 'rb') as f:
        return json.load(f)

def write_json_to_file(obj, path):
    with open(path, 'w') as f:
        f.write(json.dumps(obj))

def write_edgelist_to_file(path, list_of_objs):
    with open(path, 'w') as f:
        for line in edgelist_to_str(list_of_objs):
            f.write(line)

def read_edgelist_to_file(path):
    with open(path, 'rb') as f:
        return nx.read_weighted_edgelist(f)

def parse_input_json(line, keys=LIWC_KEYS):
    raw = json.loads(line)
    liwc_obj = extract_keys(raw, keys)
    base_obj = remove_keys(raw, keys)
    base_obj['liwc'] = liwc_obj
    return base_obj

# Thin wrapper around dict comprehensions
# returns a dict where the keys meet some 'methods' criteria
def pluck_keys(obj, method):
    return {k:v for (k,v) in list(obj.items()) if method(k,v)}

# Get an object without an array of keys
def remove_keys(obj, keys):
    return pluck_keys(obj, lambda x,y: x not in keys)

# Get an object with just an array of keys
def extract_keys(obj, keys):
    return pluck_keys(obj, lambda x,y: x in keys)

def non_zero_pairs(k,v):
    return float(v) != 0

# pick a particular key out of an array of objects
# pick([{a: 1, b: 2},...], a) -> [1, ...]
def pick_key(list_of_objs, top_level_key, parse=None):
    if not parse:
        parse = lambda x: x

    return [parse(obj[top_level_key]) for obj in list_of_objs]

# Takes a none or int and converts it to 0 or 1 respectively
def none_or_int(x):
    try:
        int(x)
        return 1
    except:
        return 0

# Takes an array and converts it to 0 (for empty) and 1 (for elements)
def empty_or_val(x):
    if len(str(x)) == 0:
        return 0
    else:
        return 1

def get_year(x):
   return str(x[26:])

def get_month(x):
   return str(x[4:7])

def unique_count(a):
    unique, inverse = np.unique(a, return_inverse=True)
    count = np.zeros(len(unique), np.int)
    np.add.at(count, inverse, 1)
    return np.vstack(( unique, count)).T

def tuple_to_str(tup, delim=','):
    return delim.join(map(str,tup))

def str_to_tuple(string, delim=','):
    return tuple([_f for _f in string.split(delim) if _f])

# [{a:0, b:1, c:1}, ..., {a:1, b:2, c:0}]
# =>
# [{name: a, count: 1}, ..., {name: c, count: 1}]
# [{source: b, target: c, weight: 1}, {source: a, target: b, weight: 1}]

# [[(b,c),...(a,b)],... [(b,c)]]
# [(b,c,2),...(a,b.1)]
def create_graph_of_liwc(list_of_objs):
    G = nx.Graph()
    liwc_data = pick_key(list_of_objs, 'liwc')

    nodes = [key for key in list(liwc_data[0].keys())]
    G.add_nodes_from(nodes)

    # pprint(liwc_data[-1])
    # connected_nodes = pluck_keys(liwc_data[-1], non_zero_pairs)
    # pprint([edge for edge in itertools.combinations_with_replacement(connected_nodes.keys(), 2)])
    # tweets = [pluck_keys(n, non_zero_pairs) for n in liwc_data]
    edges = []
    node_size = []
    both = []

    for tweet in liwc_data:
        connected_nodes = pluck_keys(tweet, non_zero_pairs)
        cur_both = [tuple_to_str(item) for item
                        in itertools.combinations_with_replacement(
                            list(connected_nodes.keys()), 2)]
        both.extend(cur_both)

        cur_edges = [tuple_to_str(edge) for edge
                        in itertools.combinations(
                            list(connected_nodes.keys()), 2)]
        edges.extend(cur_edges)

        cur_nodes = [tuple_to_str(node) for node
                        in itertools.combinations(
                            list(connected_nodes.keys()), 1)]
        node_size.extend(cur_nodes)

    # pprint(str_to_tuple(tuple_to_str(edges[0])))
    # pprint(np.asarray(unique_count(node_size)))
    # pprint(np.asarray(unique_count(edges)))
    pprint(np.asarray(unique_count(both)))

def convert_to_edges(list_of_objs):
    edges = []
    for tweet in pick_key(list_of_objs, 'liwc'):
        connections = pluck_keys(tweet, non_zero_pairs)
        edges.extend([tuple_to_str(n) for n in
            combinations_with_replacement(list(connections.keys()), 2)])
    return unique_count(edges)

def create_adjacency_matrix(json_node_link_data):
    size = len(json_node_link_data['nodes'])
    matrix = [[0 for x in range(size)] for y in range(size)]

    for edge in json_node_link_data['links']:
        matrix[edge['source']][edge['target']] = edge['weight']
        matrix[edge['target']][edge['source']] = edge['weight']

    return matrix

def edgelist_to_str(list_of_objs):
    return [tuple_to_str(str_to_tuple(tup)+(w,), ' ') + '\n' for tup,w
            in convert_to_edges(list_of_objs)]

def print_matrix(matrix):
    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in matrix]))

def main(args):
    pprint(args)

    raw_data = read_newline_json(args.input_path, HAND_PICKED)
    # raw_data = read_valid_json(args.input_path)
    # data = create_graph_of_liwc(raw_data)
    # pprint(convert_to_edges(raw_data))

    # write_edgelist_to_file('data/topic-hand-picked-edgelist.txt', raw_data)
    # weighted_edgelist = read_edgelist_to_file('data/topic-hand-picked-edgelist.txt')
    # # weighted_edgelist.edges(data=True)
    # json_weighted_edgelist = json_graph.node_link_data(weighted_edgelist)
    # pprint(json_weighted_edgelist['nodes'])
    # print create_adjacency_matrix(json_weighted_edgelist)
    # write_json_to_file(json_weighted_edgelist, 'data/topic-hand-picked-edgelist.json')

    # pprint(len(raw_data))
    # pprint(raw_data[-1])

    # flat_data = pick_key(pick_key(raw_data, 'user', empty_or_val), 'id', empty_or_val)
    # flat_data = pick_key(pick_key(raw_data, 'user'), 'location')
    # flat_data = pick_key(raw_data, 'coordinates', empty_or_val)
    # flat_data = pick_key(raw_data, 'created_at', get_month)
    # flat_data = pick_key(data, 'health', float)
    flat_data_ids = pick_key(raw_data, 'in_reply_to_status_id')
    flat_data = pick_key(raw_data, 'in_reply_to_status_id', none_or_int)
    # flat_data = pick_key(pick_key(data, 'entities'), 'user_mentions', empty_or_val)
    # pprint(np.histogram(flat_data, bins=2))

    # print(flat_data)
    # pprint(np.histogram(flat_data, bins=2))
    pprint(unique_count(flat_data))
    pprint([i for i in flat_data_ids if i is not None])

    if args.output_path:
        write_json_to_file(raw_data, args.output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input-path",
            default="data/roc.liwc.json", nargs="?",
            help="path to input directory, default: 'data/roc.liwc.json'")

    parser.add_argument("-o", "--output-path", nargs="?",
            help="path to output directory")

    args = parser.parse_args()
    main(args)
