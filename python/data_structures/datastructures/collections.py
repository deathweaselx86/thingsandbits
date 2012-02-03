#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

from abc import ABCMeta, abstractmethod

class BaseCollection(object):
    """
    This is the base class for Bag, (FIFO) Queue, and
    (LIFO) Stack. Yes, I know these are already implemented and
    surely more efficiently than this, but this is for learning purposes.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self):
        """
        We don't necessarily want to implement our collection the
        same way for each class that inherits from this one, so
        make sure that they override __init__() to define 
        self.largest_key properly.
        """
        self.collection = None
    
    @property    
    def size(self):
        """
            Returns the number of objects in this collection.
        """
        return len(self.collection)
    

    def is_empty(self):
        """
            Self-explanatory.
        """
        return len(self.collection) < 1

    def items(self):
        """
            Any BaseCollection subclass must give the user
            the option to review the contents.
        """
        return iter(self.collection)
    
class Bag(BaseCollection):
    """
        An implementation of a classic create 
        and read only unordered set.
    """
    def __init__(self):
        """
            This implementation uses a set because
            order does not matter.
        """
        self.collection = set()
    
    def add(self, item):
        """
            Add an item to this collection. That's all you can do.
        """
        self.collection.add(item)


class Queue(BaseCollection):
    """
        An implementation of the classic FIFO
        queue data structure reminiscent of a checkout line 
        in Walmart.  
    """
    def __init__(self):
        self.collection = list()
    
    def enqueue(self, item):
        """
            Add an item to the end of this queue.
        """
        self.collection.append(item)
    
    def dequeue(self):
        """
            Remove the item at the beginning of this queue.
        """
        if not self.is_empty():
            return self.collection.pop(0)
    
class Stack(BaseCollection):
    """
        An implementation of the classic LIFO 
        queue (stack) data structure.
    """
    def __init__(self):
        """
            Not that this would be used for a large number of
            items, but I think that using a dictionary keyed
            with numbers is more efficient than using a list for
            continuously adding to/removing from the top of 
            this data structure.
        """
        self.collection = dict()
        self.largest_key = -1

    @property
    def size(self):
        return self.largest_key + 1
    
    def is_empty(self):
        return self.largest_key < 0
    
    def push(self, item):
        """
            Put an item at the top of this stack.
        """
        self.collection[self.largest_key+1] = item
        self.largest_key = self.largest_key + 1
    
    def pop(self):
        """
            Take an item off the top of this stack.
            Warning: This will return None if the stack
            is empty.
        """
        if not self.is_empty():
            self.largest_key = self.largest_key - 1
            return self.collection.pop(self.largest_key+1)
        else:
            return None
         
    def items(self):
        return self.collection.itervalues()
    
    
if __name__ == "__main__":
    #Quick and dirty tests.
    #Is this too much item?
    items = ['alpha', 'beta', 'delta', 'gamma']
    
    #Bag
    myBag = Bag()
    assert myBag.size == 0
    assert myBag.is_empty()
    [myBag.add(item) for item in items]
    assert myBag.size == len(items)
    assert myBag.is_empty() == False
    bagContents = [item for item in myBag.items()]
    assert [item for item in bagContents if item not in items] == []
    assert [item for item in items if item not in bagContents] == []
    #Queue
    myQueue = Queue()
    assert myQueue.size == 0
    assert myQueue.is_empty()
    for item in items:
        myQueue.enqueue(item)
    assert myQueue.is_empty() == False
    assert myQueue.size == len(items)
    queueContents = [myQueue.dequeue() for item in items]
    assert queueContents == items
    
    #Stack
    myStack = Stack()
    assert myStack.size == 0
    assert myStack.is_empty()
    for item in items:
        myStack.push(item)
        assert myStack.is_empty() == False
        assert myStack.size == 1
        popped = myStack.pop()
        assert popped == item
        assert myStack.is_empty()
        assert myStack.size == 0
    [myStack.push(item) for item in items]
    assert myStack.size > 0
    assert myStack.size == len(items)
    stackContents = [item for item in myStack.items()]
    assert [item for item in stackContents if item not in items] == []
    assert [item for item in items if item not in stackContents] == []
    
    