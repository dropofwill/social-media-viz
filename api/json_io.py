import json
from more_itertools import chunked

def read_newline_json(path):
    with open(path, 'rb') as f:
        return [json.loads(line.decode('utf8')) for line in f.readlines()]

def read_chunked_newline_json(path, chunk_size=4000):
    return chunked(read_newline_json(path), chunk_size)

