import itertools

__version__ = '0.1'


class Recycleable(object):
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        return self.fn(*self.args, **self.kwargs)

def recycleable(fn):
    def wrapper(*args, **kwargs):
        return Recycleable(fn, *args, **kwargs)
    return wrapper

@recycleable
def map(fn, *iterables):
    return itertools.imap(fn, *iterables)

@recycleable
def chain(*iterables):
    return itertools.chain.from_iterable(iterables)

chain.from_iterable = lambda iterable: chain(*iterable)
