from collections import OrderedDict
from operator import itemgetter


def orderByValue(data: dict):
    # data = {1: 'b', 2: 'a'}
    # https://stackoverflow.com/questions/16772071/sort-dict-by-value-python

    d = OrderedDict(sorted(data.items(), key=itemgetter(1)))
    return d