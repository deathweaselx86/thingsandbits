#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

class HammingInputException(Exception):
    pass


def hamming(length):
    """
        This function will give you a list of the first length numbers of the Hamming
        sequence.
        Axiom 1: 1 is in the Hamming sequence.
        Axiom 2: If x is in the Hamming sequence, 2x, 3x, and 5x are in the
        Hamming sequence.
        Axiom 3: The Hamming sequence contains no other values other than those
        attributed to it by Axioms 1 and 2.
    	Please see http://programmingpraxis.com/2011/08/30/hamming-numbers/
    	@input length: The number of Hamming numbers you want generated.
    """
    if not isinstance(length,int) or length < 1:
        raise HammingInputException, "Expected non-negative integer for length of sequence."
    number = 1
    sequence_length = 0
    while sequence_length < length:
        if number == 1:
            yield 1
            number = number + 1
        while (number % 2 != 0 and number % 3 != 0 and number % 5 != 0):
            number = number + 1
        yield number
        number = number + 1
        sequence_length = sequence_length + 1
    raise StopIteration

if __name__ == '__main__':
    for i in hamming(20):
        print i
