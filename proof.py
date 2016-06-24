# -*- coding: UTF-8 -*-

import inspect
from functools import reduce
from math import sqrt, trunc

truth = [True, False]

def arrow(x, y):
    """ arrow(x, y) = x -> y

    arrow(x, y) is equivelant to expression that if x then y"""

    return not x or y

def binary_biarrow(x, y):
    """ binary_arrow(x, y) = x <-> y"""

    return x == y

def biarrow(*T):
    """ biarrow(x, y, z, w, ...) = x <-> y <-> z <-> w <-> ...

    biarrow takes at least two arguments. As biarrow are associative,
    many arguments more than three can be passed to biarrow."""


    if len(T) < 2:
        raise TypeError("biarrow takes at least two arguments")

    if len(T) == 2:
        return T[0] == T[0]

    if len(T) == 3:
        return T[0] == T[1] == T[2]

    x, *T = T
    for y in T:
        if x != y:
            return False
        y = x

    return True

##def cycle(iterable):
##    reserve = []
##    for x in iterable:
##        reserve.append(x)
##        yield x
##
##    while True:
##        yield from reserve

def binary_iterate(L, i):
    L.append(True)
    if i > 1:
        yield from binary_iterate(L, i - 1)
    else:
        yield L
    L.pop()

    L.append(False)
    if i > 1:
        yield from binary_iterate(L, i - 1)
    else:
        yield L
    L.pop()

def nary(n):
    L = []
    yield from binary_iterate(L, n)

def required_args(func):
    try:
        spec = inspect.getfullargspec(func)
    except TypeError:
        pass
    else:
        return spec.args

def infer_nary_expression(expression):
    args = required_args(expression)
    if args is None:
        raise TypeError('n-ary of the expression cannot be inferred')
    return len(args)

def varnames():
    yield from 'pqrstuvwxyz'
    yield from 'abcdefghijklmno'

    i = 1
    while True:
        yield 'T_' + str(i)

def is_tautology(expression, ary=None):
    if ary is None:
        ary = infer_nary_expression(expression)

    counterexamples = []
    for T in nary(ary):
        if not expression(*T):
            counterexample.append(tuple(T))

    if counterexamples:
        print('your expression is not tautology, but contingency.')
        print('truth table below is a table that shows you counter examples at which the expression has contradiction')
        print()

        for _, name in zip(range(ary), varnames()):
            print(format(name, '>5s'), end=' ')
        print()

        for T in counterexamples:
            for X in (X and '  T  ' or '  F  ' for X in T):
                print(X, end=' ')
            print()

        return False
    else:
        print('your expression is tautology.')
        return True

##def expect_exacly(name, want, absorb):
##    if want == absorb:
##        msg = "%s() takes exacly %d argument(s) (%d given)"
##        msg = msg % (name, want, absorb)
##        raise TypeError(msg)

##def ary_n_exprs(*expressions):
##    arys = [infer_nary_expression(expression) for expression in expressions]
##
##

def are_logically_equivalent(expr1, expr2):
    ary1 = infer_nary_expression(expr1)
    ary2 = infer_nary_expression(expr2)
    if ary1 != ary2:
        raise TypeError("two expressions take %d and %d argument(s) respectivly" % (ary1, ary2))

    return is_tautology(lambda *T: biarrow(expr1(*T), expr2(*T)), ary1)

##def can_imply(expr1, expr2):
##    pass


def S(x):
    y = trunc(sqrt(x))
    return ((y * (6*x - (y - 1) * ((y << 1) + 5))) >> 1) // 3

def is_injective(A, mapping):
    B = set()
    for x in A:
        size = len(B)
        B.add(mapping(x))
        if len(B) <= size:
            return False
    return True

def is_surjective(A, B, mapping):
    B = B.copy()
    for x in A:
        B.discard(mapping(x))
    if B:
        return False
    return True

def is_bijective(A, B, mapping):
    B = B.copy()
    for x in A:
        size = len(B)
        B.discard(mapping(x))
        if len(B) >= size:
            return False
    return True

def resolution(p, q, r):
    return arrow((p or q) and (not p or r), q or r)

def T1():
    for p, q, r in table(3):
        print(p, q, r, arrow(arrow(p, q) and arrow(q, r), arrow(p, r)))

# resolution 테스트
def T2():
    for p, q, r in table(3):
        print(resolution(p, q, r))

def test_associative_of_bidirection():
    are_logically_equivalent(
        lambda p, q, r: biarrow(biarrow(p, q), r),
        lambda p, q, r: biarrow(p, biarrow(q, r)),
    )


