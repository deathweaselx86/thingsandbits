#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
import array


#I do not want my datastore to wrap.
class DatastoreOverflow(Exception):
    pass

class DatastoreUnderflow(Exception):
    pass

class MismatchedBracketException(Exception):
    pass

def bf_interpreter(bf_program):
    """
    This is an interpreter for Brainfuck. 
    The valid symbols are ><+-.,[]; all else are ignored.
    We start with a tape (I refer to it as a datastore) of length
    300000.
    
    Please see http://programmingpraxis.com/2011/10/04/brainfuck
    for a full explanation of this problem. 
    """
    datastore = array.array('b', (0 for i in xrange(300000)))
    data_pointer = 0
    instruction_pointer = 0

    program_length = len(bf_program)
    output = [] 
     

    while instruction_pointer < program_length:
        if bf_program[instruction_pointer] == '<':
            data_pointer = data_pointer - 1
            if data_pointer < 0:
                raise DatastoreUnderflow, "We have run off the beginning of the datastore. Please check the program and try again."
        elif bf_program[instruction_pointer] == '>':
            data_pointer = data_pointer + 1
            if data_pointer > 300000:
                raise DatastoreOverflow, "We have run off the end of the datastore. Please check the program and try again."
        elif bf_program[instruction_pointer] == '+':
            datastore[data_pointer] = datastore[data_pointer] + 1
        elif bf_program[instruction_pointer] == '-':
            datastore[data_pointer] = datastore[data_pointer] - 1
        elif bf_program[instruction_pointer] == '.':
            output.append(chr(datastore[data_pointer]))
        elif bf_program[instruction_pointer] == ',':
            datastore[data_pointer] = bf_program[instruction_pointer+1]
        elif bf_program[instruction_pointer] == '[':
            try:
                if datastore[data_pointer] == 0:
                    instruction_pointer = bf_program[instruction_pointer:].index(']')
            except ValueError:
                raise MismatchedBracketException, "Program is missing a right bracket. Please check the program and try again." 
        elif bf_program[instruction_pointer] == ']':
            try:
                if datastore[data_pointer] != 0:
                    instruction_pointer = bf_program[:instruction_pointer].index('[') 
            except ValueError:
                raise MismatchedBracketException, "Program is missing a left bracket. Please check the program and try again." 
        else:
            pass    
        instruction_pointer = instruction_pointer + 1
    del datastore
    return ''.join(output)


if __name__ == '__main__':
   import sys
   if len(sys.argv) > 1:
        bf_filehandler = open(sys.argv[1])
        bf_program = ''.join(bf_filehandler.readlines())
        bf_filehandler.close()
        print bf_interpreter(bf_program)
  
