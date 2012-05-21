from collections import defaultdict


class DictToObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def tree():
    return defaultdict(tree)


def unflatten_dict(dictionary):
    resultDict = dict()
    for key, value in dictionary.iteritems():
        parts = key.split(".")
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return resultDict


def unflatten_dictx(flat_dict):
    #result = tree()
    result = {}
    for key, val in flat_dict.iteritems():
        chunks = key.split('.')
        if len(chunks) == 1:
            result[key] = val
        else:
            result[chunks[0]] = unflatten_dict({'.'.join(chunks[1:]): val})
    return result


#{"this.first.try": "first_try"}
#"this.first.try", "first_try"
#0, "this"
#result["this"] = unflatted_dict({"first": "first"})

#"first", "first"
#result["first"] = "first"
