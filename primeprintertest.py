"""
unittest for primeprinter.py
Created on Jul 9, 2011
How to verify/break the Sieve of Erastosthenes:
Input: [You should raise on these]

    What if you give it non-standard input?
        -something castable to integer
        -something that is not castable to integer like a
        string
    What if one or both of the primes are zero or negative?
        zero or negative numbers should not be considered here.


Functionality (PrintPrimes):
    What if x,y is given such that x>y?
        [Nominal]
    What if x,y is give such that x<y?
        [Sort such that x>y][Same as above]
    What if x or y is 1?
        [1 is not prime. Immediately drop it.]
    What if the integers you give it are not primes?
        [Print primes between them]
    What if just one integer is prime?
    What if the integers you give it are the same integer?
        [There are no primes between them]
        [If they are primes, print just one of them]
    What if there are no primes between the integers?
        [Print empty list if x and y are not prime otherwise
        print the prime(s) x and/or y]

Return
    What data structure should it return the primes as?
        [int, nonnegative]
    What data structure should this return the primes in?
        [A list]
    What order should this return the primes in?
        [Ascending.]
    How to verify that this actually returns prime numbers?
        [Impractical to test large numbers.
        Test for n,m < 100. ]
    


@author: rossjr
"""
import unittest
import primeprinter

class PrimePrinterInputTests(unittest.TestCase):
    """
    These tests correspond to the list up there labeled 'Input'.
    """
    def setUp(self):
        self.inputs = [1.0, 2.0, 'a', {'should this work': 'nope'}, -2, -5]
        self.prime_printer = primeprinter.PrimePrinter()
    
    def test_nonstandard_castable(self):
        with self.assertRaises(primeprinter.NonIntegerException):
            self.prime_printer.get_primes(self.inputs[0], self.inputs[1])
    
    def test_nonstandard_uncastable(self):
        with self.assertRaises(primeprinter.NonIntegerException):
            self.prime_printer.get_primes(self.inputs[2], self.inputs[3])

    def test_negative_integers(self):
        with self.assertRaises(primeprinter.NonPositiveIntegerException):
            self.prime_printer.get_primes(self.inputs[4], self.inputs[5])
    def test_x_and_y_equal_to_1(self):
        returnValue = self.prime_printer.get_primes(1, 1)
        self.assertEqual([], returnValue)
    def tearDown(self):
        del self.prime_printer
    
    
"""
Functionality:
    What if x,y is given such that x>y?
        [Nominal]
    What if x,y is give such that x<y?
        [Sort such that x>y]
    What if x or y is 1?
        [1 is not prime. Immediately drop it.]
    What if the integers you give it are not primes?
        [Print primes between it]
    What if the integers you give it are the same integer?
        [There are no primes between them]
        [If they are primes, print just one of them]
    What if there are no primes between the integers?
        [Print empty list if x and y are not prime otherwise
        print the prime(s) x and/or y]
"""
class PrimePrinterFunctionalityTests(unittest.TestCase):

    def setUp(self):
        self.prime_printer = primeprinter.PrimePrinter()
        #I am using these inputs pairwise. I apologize for the mess,
        #but otherwise we get huge lines.
        self.inputs =(3, 23, 17, 71, 1, 13, 11, 24, 28)
        self.answers = ([17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71],
                         [2, 3, 5, 7, 11, 13],[11],[])
    def test_is_a_list(self):
        return_value = self.prime_printer.get_primes(self.inputs[0],
                                                     self.inputs[1])
        self.assertIsInstance(return_value, list)
        
    def test_x_greater_than_y(self):
        return_value = self.prime_printer.get_primes(self.inputs[2],
                                                      self.inputs[3])
        self.assertEqual(return_value, self.answers[0])
    
    def test_y_greater_than_x(self):
        return_value = self.prime_printer.get_primes(self.inputs[3],
                                                      self.inputs[2])
        self.assertEqual(return_value, self.answers[0])
    
    def test_x_equal_to_1(self):
        return_value = self.prime_printer.get_primes(self.inputs[4],
                                                      self.inputs[5])
        self.assertEqual(return_value, self.answers[1])

    def test_x_equal_to_y_prime(self):
        return_value = self.prime_printer.get_primes(self.inputs[6],
                                                      self.inputs[6])
        self.assertEqual(return_value, self.answers[2])
        
    def test_x_equal_to_y_nonprime(self):
        return_value = self.prime_printer.get_primes(self.inputs[7],
                                                      self.inputs[7])
        self.assertEqual(return_value, self.answers[3])

    def test_no_primes(self):
        return_value = self.prime_printer.get_primes(self.inputs[8],
                                                      self.inputs[8])
        self.assertEqual(return_value, self.answers[3])
        
    def tearDown(self):
        del self.prime_printer
        del self.inputs
        del self.answers

if __name__ == "__main__":
    unittest.main()