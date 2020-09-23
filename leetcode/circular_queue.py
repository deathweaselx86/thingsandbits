#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# From leetcode:
# https://leetcode.com/problems/design-circular-queue/

class MyCircularQueue:
    def __init__(self, k: int):
        """
        Initialize your data structure here. Set the size of the queue to be k.
        """
        self.max_size = k
        self.current_capacity = 0
        self.rear_index = 0
        self.front_index = -1 # set this to one so we can always increment when we add a new element
        self.circular_queue = [None] * k

    def enQueue(self, value: int) -> bool:
        """
        Insert an element into the circular queue. Return true if the operation is successful.
        """
        if not self.isFull():
            self.front_index = (self.front_index + 1) % self.max_size
            self.circular_queue[self.front_index] = value
            self.current_size = self.current_size + 1
            return True
        return False

            
    def deQueue(self) -> bool:
        """
        Delete an element from the circular queue. Return true if the operation is successful.
        """
        if not self.isEmpty():
            self.circular_queue[self.rear_index] = None
            self.current_size = self.current_size - 1
            self.rear_index = (self.rear_index + 1) % self.max_size
            return True
        return False

    def Front(self) -> int:
        """
        Get the front item from the queue.
        """
        if not self.isEmpty():
            return self.circular_queue[self.front_index]
        return -1

    def Rear(self) -> int:
        """
        Get the last item from the queue.
        """
        if not self.isEmpty():
            return self.circular_queue[self.rear_index]
        return -1

    def isEmpty(self) -> bool:
        """
        Checks whether the circular queue is empty or not.
        """
        return self.current_capacity < 1

    def isFull(self) -> bool:
        """
        Checks whether the circular queue is full or not.
        """
        return self.current_capacity == self.max_size
