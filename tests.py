import nose
from nose.tools import eq_

import recycle


def gen(length):
    for x in xrange(length):
        yield x


@recycle.Recycleable
def decorated_gen(length):
    return gen(length)


def test_Recycleable():

    # This just demonstrates that normally the generator
    # isn't reusable.
    g = gen(5)
    eq_([x for x in g], [0, 1, 2, 3, 4])
    eq_([x for x in g], [])

    # Wrapping it in a Recyclable means that it can be iterated over multiple times.
    rgen = recycle.Recycleable(gen)
    r = rgen(5)

    eq_([x for x in r], [0, 1, 2, 3, 4])
    eq_([x for x in r], [0, 1, 2, 3, 4])


def test_recycle():
    # Test the decorator

    r = decorated_gen(5)
    eq_([x for x in r], [0, 1, 2, 3, 4])
    eq_([x for x in r], [0, 1, 2, 3, 4])


def test_map():

    map_func = lambda x: x * 2

    r = decorated_gen(5)
    r = recycle.Recycleable.map(map_func, r)

    eq_([x for x in r], [0, 2, 4, 6, 8])
    eq_([x for x in r], [0, 2, 4, 6, 8])
    

def test_chain():
    a = decorated_gen(5)
    b = decorated_gen(5)
    r = recycle.Recycleable.chain(a, b)

    eq_([x for x in r], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4])


def test_chain_and_map():

    map_func = lambda x: x * 2

    a = decorated_gen(5)
    b = decorated_gen(5)
    c = recycle.Recycleable.chain(a, b)
    r = recycle.Recycleable.map(map_func, c)
    eq_([x for x in r], [0, 2, 4, 6, 8, 0, 2, 4, 6, 8])

if __name__ == '__main__':
    nose.run()
