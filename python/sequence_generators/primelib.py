#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
from math import sqrt, ceil

class PrimeGenerators(object):
    def sundaram(self, n):
        """
        This is a method of sieving prime numbers discovered by the
        Indian mathematics student S.P. Sundaram. This will return
        a sequence of primes between 2 and n, inclusive (if applicable)

        @param n: the upper bound for n

        """
        if n < 2:
            return []

        initial_list = range(1,n) 
        
        for j in range(1,n):
            for i in range(1,n):
                removal_candidate = i+j+2*i*j
                if removal_candidate >= n:
                    continue
                try:    
                    initial_list.remove(removal_candidate)
                except ValueError:
                    pass
        
        prime_list = [2]
        prime_list.extend([2*x+1 for x in initial_list])
        
        # I have to do this because this algorithm will give me
        # all primes less than 2*n + 1 given some integer n.
        # I can solve that to get the idea n to feed this, but then
        # I run into problems mixing floating point math with
        # integer operations.

        prime_list = [p for p in prime_list if p <= n]
        
        return prime_list
    
    def erastosthenes(self, n):
        """
        This is the classic Sieve of Eratosthenes. 
        This will give you a list of all of the prime numbers between
        2 and n, inclusive (if applicable).
        
        They should be emitted in increasing order.
        """
        if n < 2:
            return []
        
        divisor_list = range(2,n+1)       
        
        next_prime_index = 0
        current_prime = divisor_list[0]
        while current_prime < n and len(divisor_list) > next_prime_index:
            # This loop eliminates every composite number between 2 and k
            current_prime = divisor_list[next_prime_index]
            divisor_list = [n for n in divisor_list if
                             n % current_prime != 0 or n == current_prime]
            next_prime_index = divisor_list.index(current_prime)+1
        return divisor_list

    def get_prime_factors(self, n):
        """
            This method returns a list of the prime factors of the number n.
        
            As expected, any number that is less than 2 will return an empty list.
        """
        # First get all prime numbers between 2 and n, inclusive.
        # This is emitted in order.
        prime_factors = []

        primes = self.erastosthenes(int(ceil(sqrt(n))))
        for prime in primes:
            if n % prime == 0:
                prime_factors.append(prime)
    
        return prime_factors


    
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        n = 20
    else:
        n = int(sys.argv[1])

    generator = PrimeGenerators()
    #print generator.sundaram(n)
    print generator.erastosthenes(n)
    print generator.get_prime_factors(n)
