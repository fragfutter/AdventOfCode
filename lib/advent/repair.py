import itertools

class Placeholder(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<P %s>' % self.value


def bestpair(sequence):
    """return pair with the highest occurance rate in sequence"""
    result = 0, None
    for offset in range(len(sequence) - 1):
        pair = sequence[offset:offset + 2]
        i = offset + 2
        count = 0
        while i < len(sequence) - 1:
            if sequence[i:i + 2] == pair:
                count += 1
                i += 2
            else:
                i += 1
        if count > result[0]:
            result = count, pair
    if result[0] > 0:
        return result[1]
    else:
        return None


def replace(sequence, placeholder):
    """replace every non overlapping occurance of pair with replacement"""
    result = sequence[:]
    i = 0
    while i < len(result):
        if result[i:i+2] == placeholder.value:
            result = result[:i] + [placeholder] + result[i+2:]
        else:
            i += 1
    return result


def compress(data):
    """compress data (a list) using repair
    https://en.wikipedia.org/wiki/Re-Pair
    yield compressed data and expansion table
    placeholders
    """
    data = data[:]  # copy
    placeholders = []
    pair = bestpair(data)
    while pair:
        placeholder = Placeholder(pair)
        placeholders.append(placeholder)
        data = replace(data, placeholder)
        pair = bestpair(data)
    # expand placeholders
    expanded = {}  # dictionary for fast lookup
    for p in placeholders:
        value = [expanded.get(v, v) for v in p.value]
        value = list(itertools.chain(*value))  # flatten nested list
        p.value = value
        expanded[p] = value
    # drop all placeholders not used in compressed data
    expanded = [x for x in expanded.keys() if x in data]
    return data, expanded
