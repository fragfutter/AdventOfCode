from itertools import cycle


def pairwise(sequence1, sequence2=None):
    """return pairwise items of sequence1 and sequence2

    (s1_1, s2_1), (s1_2, s2_2), ...

    if sequence2 is ommited return pairs of sequence1

    (s1_1, s1_2), (s1_3, s1_4), ...

    if sequence2 is an integer it will be an offset for sequence1

    (s1_1, s1_offset), (s1_2, s1_offset+1)

    """
    iter1 = iter(sequence1)
    if sequence2 is None:
        iter2 = iter1
    elif isinstance(sequence2, int):
        iter2 = cycle(sequence1)
        for i in range(sequence2):
            next(iter2)
    else:
        iter2 = iter(sequence2)
    return zip(iter1, iter2)


def duplicates(sequence, values=True):
    """check if there are duplicates in sequence,
    if values is True return them, otherwise only return boolen"""
    s = set(sequence)
    if len(sequence) == len(s):
        return False
    if not values:
        return True  # values are not required
    return filter(lambda x: x not in s, sequence)
