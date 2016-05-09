from itertools import chain, combinations
from py2neo import Graph, authenticate

emolex_keys = { 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative',
        'positive', 'sadness', 'surprise', 'trust' }

top_level_liwc_keys = { 'affect', 'social', 'cogmech', 'percept', 'bio',
        'relativ' }

'''
EmoLex Queries
'''
def count_emolex_by_thresh(graph, category, thresh=0):
    query='''
    MATCH (t:Tweet)-[:HAS_EMOLEX]->(n:EmoLex)
    WHERE n.{0} > {1}
    RETURN COUNT(t)
    '''.format(category, thresh)

    return graph.evaluate(query)

def general_emolex_counter(graph, where_clause):
    query='''
    MATCH (t:Tweet)-[:HAS_EMOLEX]->(n:EmoLex)
    WHERE {0}
    RETURN COUNT(t)
    '''.format(where_clause)

    print(query)
    return graph.evaluate(query)

def multiple_emolex_counter(graph, where_clauses):
    return [ (k, general_emolex_counter(graph, c)) for k, c in where_clauses ]

'''
LIWC Queries
'''
def count_liwc_by_thresh(graph, category, thresh=0):
    query='''
    MATCH (t:Tweet)-[:HAS_LIWC]->(n:Liwc)
    WHERE n.{0} > {1}
    RETURN COUNT(t)
    '''.format(category, thresh)

    return graph.evaluate(query)

def general_liwc_counter(graph, where_clause):
    query='''
    MATCH (t:Tweet)-[:HAS_LIWC]->(n:Liwc)
    WHERE {0}
    RETURN COUNT(t)
    '''.format(where_clause)

    print(query)
    return graph.evaluate(query)

def multiple_liwc_counter(graph, where_clauses):
    return [ (k, general_liwc_counter(graph, c)) for k, c in where_clauses ]

'''
General helpers
'''

'''
List[Tuple(Tuple(str), int)] -> List[Tuple(Tuple(str), int)]
'''
def top_k_counts(result, k=20):
    return sorted(result, key=lambda x: -x[1])[0:k]

def build_intersect_combinations(keys, thresh=0):
    combos = combinations_from(keys, len(keys))
    return [ (pos_set,
        build_intersect_clause_by_thresh(pos_set, keys - pos_set, thresh))
        for pos_set in combos ]

'''
returns: n.pos_cat1 > thresh AND n.neg_cat <= thresh
'''
def build_intersect_clause_by_thresh(pos_cat, neg_cat, thresh=0):
    return ' AND '.join(chain(
        [ 'n.{0} > {1}'.format(cat, thresh) for cat in pos_cat ],
        [ 'n.{0} <= {1}'.format(cat, thresh) for cat in neg_cat ]
    ))

def combinations_from(cat, n):
    return [ set(x) for x in chain.from_iterable(combinations(cat, i)
        for i in range(1, n+1)) ]
