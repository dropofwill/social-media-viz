'''
By convention in Cypher queries:
    t: is the matching Tweet node
    e: is the matching EmoLex node
    l: is the matching Liwc node
'''
from typing import List, Set, Union, Tuple
from itertools import chain, combinations
from py2neo import Graph, authenticate

Num = Union[int, float, complex]

emolex_keys = { 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative',
        'positive', 'sadness', 'surprise', 'trust' }

top_level_liwc_keys = { 'affect', 'social', 'cogmech', 'percept', 'bio',
        'relativ' }

'''
Generate cypher queries for use later, via either pythonic interface:
    graph.evaluate(query)

or over the REST API

POST: localhost:7474/db/data/transaction/commit
Content-Type: "application/json"
Authorization: bmVvNGo6bmVvNGpfcGFzc3dvcmQ=
    {
        "statements": [
            "statement": query
        ]
    }
'''

def count_criteria_by_thresh_query(
        criteria: str,
        category: str,
        thresh: Num = 0) -> str:

    node_name = _parse_single_criteria(criteria)
    return '''
    MATCH (l:Liwc)-[:HAS_LIWC]-(t:Tweet)-[:HAS_EMOLEX]-(e:EmoLex)
    WHERE {0}.{1} > {2}
    RETURN COUNT(t)
    '''.format(node_name, category, thresh)

'''

'''
def count_clause_query(where_clause: str) -> str:
    return '''
    MATCH (l:Liwc)-[:HAS_LIWC]-(t:Tweet)-[:HAS_EMOLEX]-(e:EmoLex)
    WHERE {0}
    RETURN COUNT(t)
    '''.format(where_clause)

'''

'''
def count_multiple_clauses_query(where_clauses: List[str]) -> List[str]:
    return [ (k, count_clause_query(c)) for k, c in where_clauses ]

'''
General helpers
'''

def build_intersect_combinations(
        keys: List[Tuple[str, str]],
        thresh: Num = 0) -> List[Tuple[Set[str], str]]:

    categories = set(_category_to_query_ref(k, l) for k, l in keys)
    combos = _combinations_from(categories, len(categories))
    return [ (pos_set,
        build_intersect_clause_by_thresh(pos_set, categories - pos_set, thresh))
        for pos_set in combos ]

'''
returns: n.pos_cat1 > thresh AND n.neg_cat <= thresh
'''
def build_intersect_clause_by_thresh(
        pos_cat: Set[str],
        neg_cat: Set[str],
        thresh: Num = 0) -> str:

    return ' AND '.join(chain(
        [ '{0} > {1}'.format(cat, thresh) for cat in pos_cat ],
        [ '{0} <= {1}'.format(cat, thresh) for cat in neg_cat ]
    ))

def _combinations_from(
        categories: List[str],
        extent: int) -> List[Set[str]]:

    return [ set(x) for x in chain.from_iterable(combinations(categories, i)
        for i in range(1, extent+1)) ]

def _parse_single_criteria(lexicon_ref: str) -> str:
    if lexicon_ref.lower() == 'emolex':
        return 'e'
    elif lexicon_ref.lower() == 'liwc':
        return 'l'
    else:
        raise NotImplementedError('Only support liwc and emolex lexicon refs')

'''
Given a category and it's lexicon, return a property for a cypher querying
e.g.
_category_to_query_ref('bio', 'liwc') -> 'l.bio'
'''
def _category_to_query_ref(category: str, lexicon_ref: str) -> str:
    print(category, lexicon_ref)
    return '{0}.{1}'.format(_parse_single_criteria(lexicon_ref), category)
