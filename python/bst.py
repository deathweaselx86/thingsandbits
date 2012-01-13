#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
"""
    This is a Binary Search Tree implementation.

"""

class Node:
    """
        This is the base unit that makes up a BST.
        In actuality, a Node is a BST by itself. 
    """
    def __init__(self,value):
        self.value = value
        self.left_child = None
        self.right_child = None

    def add_child(self,child):
        """
            Add a child Node to this BST.
        """
        if not isinstance(Node,child):
            raise TypeError, \
                    "Attempted to add a non-Node object to this BST. Got %r." \
                     % (type(child))
        if child.value == None:
            raise ValueError, \
                    "Attempted to add a Node object to this BST that has an undefined value."
        if type(child.value) != type(self.value):
            raise TypeError, "Attempted to add a Node object to this BST with the wrong data type. Should be %r, got %r." % (type(child.value), type(self.value))
        
        if child.value >= self.value:
            if self.right_value:
                self.right_value.add_child(child)
            else:
                self.right_value = child
        else:
            if self.left_value:
                self.left_value.add_child(child)
            else:
                self.left_child = child

    def add_value(self,value):
        """
            This is here in case we don't want to explicitly
            initialize a Node object.
        """
        self.add_child(Node(value))
    
    def find_value(self,search_value):
    "
        Find a value in the BST.
        If we find it, we'll return the entire Node, that is, the entire
        sub-tree. Otherwise, return None.
    "
        if self.value == search_value:
            return self
        if search_value >= self.value:
            if self.right_value:
                return self.right_value.find_value(search_value)
            else:
                return None
        else:
            if self.left_value:
                return self.left_value.find_value(search_value)
            else:
                return None

    def size(self):
        """
            This method gives the size of this BST.
            
        """
        size = 1
        for node in (self.left_child, self.right_child):
            if node:
                size = size + node.size()
        return size
   
    def min(self):
       """
            This method returns the minimum value in this BST.
       """
       if self.left_node != None:
           return self.left_node.min()
       return self.value
   
    def max(self):
       """
            This method returns the maximum value in this BST.
       """
       if self.right_node != None:
           return self.right_node.max()
       else:
           return self.value
   
    def floor(self,search_value):
        """
            Find the largest value in the BST that is less than or equal to the
            to the value requested.
        """
        if self.right_child and self.value < search_value:
                return self.right_child.floor(search_value)
        if self.left_child and self.value > search_value:
            return self.left_child.floor(search_value)
        return self
   
    def ceiling(self, search_value):
        """
            Find the smallest value in the BST that is greater than or equal to the
            value requested.
        """
        if self.left_child and self.value > search_value:
                return self.left_child.ceiling(search_value):
        if self.right_child and self.value < search_value:
            returns self.right_child.ceiling(search_value)
        return self



    
