import itertools

__version__ = '0.1'


class Recycleable(object):

    # TODO problem here is that this delays construction of the object
    #      so errors are delayed too. E.g. if the parameter count for the decorated
    #      function is wrong, it won't be raised until __iter__ is called
    def __init__(self, fn):
        self.fn = fn
        self.args = []
        self.kwargs = {}

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def __iter__(self):
        return self.fn(*self.args, **self.kwargs)

    @classmethod
    def map(cls, fn, *iterables):
        return cls(itertools.imap)(fn, *iterables)

    @classmethod
    def chain(cls, *iterables):
        return cls(itertools.chain.from_iterable)(iterables)
