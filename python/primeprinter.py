"""
primeprinter.py
Created on Jul 9, 2011

This module finds and prints the prime numbers between x and
y.

TODO: Improve CLI interface for this.
@author: rossjr
"""
import math



class NonIntegerException(Exception):
    pass

class NonPositiveIntegerException(Exception):
    pass

class PrimePrinter(object):
    """
    Use this class to get all prime numbers between positive integers
    greater than 1 x and y. 
    """


    def get_primes(self, x, y):
        """
        Given two integers x and y, this method will print
        primes for you between x and y, inclusive. Please note that 1
        is not a prime number.

        @param x: An integer greater than 0
        @param y: An integer greater than 0
        """
        self._check_inputs(x, y)
        if y > x:
            x, y = y, x
        
        x_prime_list = self._prime_sieve(x)
        prime_list = x_prime_list
        return_list = [n for n in prime_list if n <= x  and n >= y]
        return_list.sort()
        return return_list
       
       
        

    def _prime_sieve(self, x):
        """
        This is the classic Sieve of Eratosthenes. There is an algorithm that
        works better for much larger numbers (10^9 +), but it is very difficult
        and we would be better of whipping out something like numpy or C
        """
	if x < 2:
            return []
        
        upperBound = int(math.sqrt(x)) +1
        divisor_list = range(2,x+1)         
        
        current_prime = 2
        while current_prime < upperBound:
        #This loop eliminates every composite number between 2 and k
            divisor_list = [n for n in divisor_list if
                             n % current_prime != 0 or n == current_prime]
            next_prime_index = divisor_list.index(current_prime)+1
            current_prime = divisor_list[next_prime_index]
        divisor_list.sort()
        return divisor_list
            
    def _check_inputs(self, x, y):
        """ 
        Somehow this is less bad than doing it inline.
        """
        error_msg = 'Invalid parameter. Expected integer greater than 0.'
        for param in (x,y):
            if not isinstance(param, int):
                raise NonIntegerException(error_msg)
            if x < 1:
                raise NonPositiveIntegerException(error_msg)
            
if __name__ == '__main__':
    x = 2
    y = 1000
    print PrimePrinter().get_primes(x,y)
