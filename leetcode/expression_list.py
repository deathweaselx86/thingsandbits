#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
# ughhhh

import sys

operators = ')(*/+-'
NUMBERS = [str(i) for i in range(10)]
OPERATORS = {operators[i]:i for i in range(len(operators))}

class Node:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f'val={self.val}, left={self.left.val}, right={self.right.val}'

    def in_order(self):
       print(self.val, end=" ")
       if self.left: 
           self.left.in_order()

       if self.right:
           self.right.in_order()

def infix_to_postfix(infix):
    operator_stack = []
    output = []
    for ch in infix:
        if ch in NUMBERS:
            output.append(ch)
        elif ch == '(':
            operator_stack.append(ch)
        elif ch == ')':
            next_op = operator_stack.pop()
            while next_op != '(':
                output.append(next_op)
                next_op = operator_stack.pop()
        else: # it's a regular operation
            while len(operator_stack) > 0 and OPERATORS[ch] <= OPERATORS[operator_stack[-1]]:
                output.append(operator_stack.pop())
            operator_stack.append(ch)

    while len(operator_stack) > 0:
        output.append(operator_stack.pop())
    return output


def construct(postfix):
    my_favorite_stack = []
   
   # 2-3/(5*2)+1
   # ['2', '3', '-', '5', '2', '*', '1', '+', '/']
    for ch in postfix:
        if ch not in operators:
            my_favorite_stack.append(Node(val=ch))
        else:
            # pop two operands
            right = my_favorite_stack.pop()
            left = my_favorite_stack.pop()
            my_favorite_stack.append(Node(val=ch, right=right, left=left))
    return my_favorite_stack.pop()

if __name__ == "__main__":
    string = sys.argv[1]
    postfix = infix_to_postfix(string)
    print(string)
    print(postfix)
    tree = construct(postfix)
    print(tree)
    tree.in_order()

