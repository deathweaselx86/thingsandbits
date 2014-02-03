#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

def memoize(f):
    """ Simple memoization decorator. """
    cache = {}

    def memoized_f(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]

    return memoized_f

class Node(object):
    def __init__(self, data=None):
        self._data = data

    @property
    def data(self):
        return self._data

    @data.deleter
    def data(self):
        del self._data

    @data.setter
    def data(self, data):
        self._data = data


class ListNode(Node):
    def __init__(self, data=None):
        """ Initialize single node."""
        super(ListNode, self).__init__(data=data)
        self._next = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        if not isinstance(next, ListNode):
            raise TypeError("Attempted to link an object that is not a ListNode.")
        else:
            self._next = next

    @next.deleter
    def next(self):
        del self._next

    def is_tail(self):
        return self._next is None

