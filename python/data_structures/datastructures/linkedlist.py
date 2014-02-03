#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

from . import common


class LinkedList(object):
    """
        This class represents a standard singly linked list.
   """
    def __init__(self, head=None):
        if isinstance(head, common.ListNode):
            self._head = head

    @property
    def head(self):
        return self._head

    @property.setter
    def head(self, node):
        if not isinstance(node, common.ListNode):
            raise TypeError("Must use a ListNode object as the head of this LinkedList. Tried to use: %s" % node)
        else:
            self._head = node

    @property
    def tail(self):
        """
            The tail of this linked list.
        """
        if self._head == None:
            return None
        else:
            node = self._head
            while not node.is_tail:
                node = node.next
            return node

    def insert(node):
        """
            Insert node into this linked list at the end.

            @param node: An instance of common.ListNode
        """
        if not self._head:
            self.head = node
        else:
	    self.tail.next=node
