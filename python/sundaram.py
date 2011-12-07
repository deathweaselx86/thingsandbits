#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
from math import sqrt

def sundaram(count):
    """
        This is an alternative prime sieve.
    """
    prime_list = range(count)
    i,j=1,1
    while i+j+2*i*j <= count:
        for i in range(1, int(sqrt((float(count)-j)/2))):
            try:
                prime_list.remove(i+j+2*i*j)
            except ValueError:
                pass
        j=j+1

    prime_list = [2*p+1 for p in prime_list]
    return prime_list 
if __name__ == '__main__':
	print sundaram(20)
