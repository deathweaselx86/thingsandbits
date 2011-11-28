#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4


def hamming(count):
    """
        This function will give you a list of the first count numbers of the Hamming
        sequence.
        Axiom 1: 1 is in the Hamming sequence.
        Axiom 2: If x is in the Hamming sequence, 2x, 3x, and 5x are in the
        Hamming sequence.
        Axiom 3: The Hamming sequence contains no other values other than those
        attributed to it by Axioms 1 and 2.
    	Please see http://programmingpraxis.com/2011/08/30/hamming-numbers/
    	@input count: The number of Hamming numbers you want outputted.
    """
    hammingSequence = [1]
    hammingGenerator = ((2*ch,3*ch,5*ch) for ch in hammingSequence)
    while len(hammingSequence) < count:
        for n in hammingGenerator.next():
			if n not in hammingSequence:
				hammingSequence.append(n)
	hammingSequence.sort()
    return hammingSequence


if __name__ == '__main__':
	print hamming(1000)
