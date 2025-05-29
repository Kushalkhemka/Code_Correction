def flatten(*args, **kwargs):
    return list(_flatten_inner(*args, **kwargs))

def _flatten_inner(arr):
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x