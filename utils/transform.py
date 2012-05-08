from collections import defaultdict


class DictToObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def tree():
    return defaultdict(tree)
