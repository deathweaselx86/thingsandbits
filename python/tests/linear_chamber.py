#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# The full problem statement for this is not mine to give.
# Seriously, if you need a detailed explanation for this one, you're going
# to have to email me.

# Also, the structure of this class is not quite the way I would have 
# arranged it. I was given a specific set of method signatures.
# Nonetheless, I'm kind of proud of it.

class ParticleAnimation(object):
    """
        This class represents a simulation of a linear particle chamber.
        More details in the docstrings of the methods.
    """
    def __init__(self):
        """
            Initialize an empty linear particle chamber.
        """
        # Might as well explain this here.

        # self.speed is the constant speed that each particle is moving
        self.speed = None;
        
        # self.init is a string representing the initial state that the particle chamber starts in.
        # Each discrete "spot" in the chamber can be occupied with a left-moving (L)
        # particle, a right-moving particle(R), or an empty space (.)
        self.init = ""
        
        # We'll now make two lists that represent the left particles and right particles.
        # We don't need to keep track of how many particles, so we track the fact that there
        # are left (or right) particles in one direction or another.
        self.left_states = []
        self.right_states = []
        # These match up index for index.

    def animate(self, speed, init):
        """
            This is the insertion point for the linear particle chamber.
            speed is an integer between 1 and 10 inclusive
            init is a string with length between 1 and 50, inclusive

        """

        self.speed = speed
        self.init = init
        self.generateStates()
        self.printStates()

    def generateStates(self):
        """
            This method generates the strings representing the intermediate states between the initial
            state and the final state (when the last particle has exited the chamber).
        """
        state_length = len(self.init)
       
        # First turn the initial state consisting of L and R and . into
        # lists of L and . and R and .
        
        # Should we warn if the initial state has junk other than L, R, or .?
        initial_left = ''
        initial_right = ''
        for i in range(0, state_length):
            if self.init[i] == 'L':
                initial_left = initial_left + 'X'
                initial_right = initial_right + '.'
            elif self.init[i] == 'R':
                initial_left = initial_left + '.'
                initial_right = initial_right + 'X'
            else:
                initial_left = initial_left + '.'
                initial_right = initial_right + '.'

        self.left_states.append(initial_left)
        self.right_states.append(initial_right)

        end_condition = '.' * state_length
        
        left_state = ''
        right_state = ''

        while left_state != end_condition  or right_state != end_condition:
            # Left moving particles move left, so shift left and fill right.
            left_state = self.left_states[-1][self.speed:] + '.' * self.speed
            # Right moving particles move right, so shift right and fill left.
            right_state = '.' * self.speed + self.right_states[-1][:state_length-self.speed]
            self.left_states.append(left_state)
            self.right_states.append(right_state)
                           
    def printStates(self):
        """
            This method is used to print the full simulation. We can't show the L and R, so
            this method replaces those with X.
        """
        
        # Arbitrary which one we choose.
        number_states = len(self.left_states) 
        state_length = len(self.init)
        print "{",
        for i in range(number_states):          
            # Clear is better than "clean".
            left_state = self.left_states[i]
            right_state = self.right_states[i]
            for j in range(state_length):
                if left_state[j] == 'X' or right_state[j] == 'X':
                    print 'X',
                else:
                    print '.',
            print ','
        print '}'

if __name__ == "__main__":
    import sys
    # I hope they put this in the right order, or this
    # is going to make a big boom.
    if len(sys.argv) > 2:
        speed = int(sys.argv[1])
        init = sys.argv[2]
        pa = ParticleAnimation().animate(speed, init)
    else:
        print "Not enough arguments."
        
