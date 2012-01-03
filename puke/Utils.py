#!/usr/bin/env python
# -*- coding: utf8 -*-

import collections
import os, stat,re
import functools
import operator

def quacks_like_dict(object):
    """Check if object is dict-like"""
    return isinstance(object, collections.Mapping)
    
def deepmerge(a, b):
    """Merge two deep dicts non-destructively
    
    Uses a stack to avoid maximum recursion depth exceptions
    
    >>> a = {'a': 1, 'b': {1: 1, 2: 2}, 'd': 6}
    >>> b = {'c': 3, 'b': {2: 7}, 'd': {'z': [1, 2, 3]}}
    >>> c = merge(a, b)
    >>> from pprint import pprint; pprint(c)
    {'a': 1, 'b': {1: 1, 2: 7}, 'c': 3, 'd': {'z': [1, 2, 3]}}
    """
    assert quacks_like_dict(a), quacks_like_dict(b)
    dst = a.copy()
    
    stack = [(dst, b)]
    while stack:
        current_dst, current_src = stack.pop()
        for key in current_src:
            if key not in current_dst:
                current_dst[key] = current_src[key]
            else:
                if quacks_like_dict(current_src[key]) and quacks_like_dict(current_dst[key]) :
                    stack.append((current_dst[key], current_src[key]))
                else:
                    current_dst[key] = current_src[key]
    return dst




_rechmod = re.compile(r"(?P<who>[uoga]?)(?P<op>[+\-=])(?P<value>[ugo]|[rwx]*)")
_stat_prefix = dict(u = "USR", g = "GRP", o = "OTH")

def octalmode(location, symbolic):
    """chmod(location, description) --> None
    Change the access permissions of file, using a symbolic description
    of the mode, similar to the format of the shell command chmod.
    The format of description is
        * an optional letter in o, g, u, a (no letter means a)
        * an operator in +, -, =
        * a sequence of letters in r, w, x, or a single letter in o, g, u
    Example:
        chmod(myfile, "u+x")    # make the file executable for it's owner.
        chmod(myfile, "o-rwx")  # remove all permissions for all users not in the group. 
    See also the man page of chmod.
    """

    mo = _rechmod.match(symbolic)
    who, op, value = mo.group("who"), mo.group("op"), mo.group("value")
    if not who:
        who = "a"
    mode = os.stat(location)[stat.ST_MODE]
    if value in ("o", "g", "u"):
        mask = _ors((_stat_bit(who, z) for z in "rwx" if (mode & _stat_bit(value, z))))
    else:
        mask = _ors((_stat_bit(who, z) for z in value))
    if op == "=":
        mode &= ~ _ors((_stat_bit(who, z) for z in  "rwx"))
    mode = (mode & ~mask) if (op == "-") else (mode | mask)
    
    return mode


# Helper functions

def _stat_bit(who, letter):
    if who == "a":
        return _stat_bit("o", letter) | _stat_bit("g", letter) | _stat_bit("u", letter)
    return getattr(stat, "S_I%s%s" % (letter.upper(), _stat_prefix[who]))

def _ors(sequence, initial = 0):
    return functools.reduce(operator.__or__, sequence, initial)
