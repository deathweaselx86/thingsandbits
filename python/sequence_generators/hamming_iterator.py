#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

class HammingInputException(Exception):
    pass

class Hamming(object):
    """
        This is an iterator that gives out the Hamming sequence, one number at a time.

        Axiom 1: 1 is in the Hamming sequence.
        Axiom 2: If x is in the Hamming Sequence, 2x, 3x, and 5x are also in the Hamming
        sequence.
        Axiom 3: The Hamming Sequence contains no other numbers other than those
        attributed to it by Axioms 1 and 2.

        Implication: Hamming numbers must pass one of the following tests:
        x%2 = 0, x%3 = 0, x%5 = 0.
        
        This one is okay if storage is a problem and computation time is not. Can
        be written A LOT shorter as a generator.
    """
    
    def __init__(self, start=1):
        if not isinstance(start,int) or start < 1:
            raise HammingInputException, "Expected non-negative integer for length of sequence."
        self.current = start 

    def __iter__(self):
        return self
    
    def next(self):     
       if self.current == 1:
            self.current = self.current + 1
            return 1
       while (self.current % 2 != 0 and self.current % 3 != 0 and self.current % 5 != 0):
            self.current = self.current + 1
       self.current = self.current + 1
       return self.current - 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "How long shall we count up?"
        sys.exit()

    if len(sys.argv) < 3:
        print "Where shall we start?"
        sys.exit()

    count_to, start_value = int(sys.argv[1]), int(sys.argv[2])
    hamming_object = Hamming(start_value)
    i = 0
    while i < count_to:
        print hamming_object.next()
        i=i+1
