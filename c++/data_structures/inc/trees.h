/* 
 * File:   trees.h
 * Author: jess2
 *
 * Created on February 5, 2012, 7:22 PM
 */

#ifndef TREES_H
#define	TREES_H
/*
 * Tree style datastructures. 
 * Method signatures are taken from Sedgewick and Wayne's Algorithms text.
 */

#include <iostream>

template <class Key, class Value>
class BaseOrderedSymbolTable {
    public:
        OrderedSymbolTable();
        virtual ~OrderedSymbolTable();
        
        //These are pretty self explanatory.
        virtual void put(Key key, Value value) = 0;
        virtual Value get(Key key) = 0;
        virtual void remove(Key key) = 0;
        virtual bool contains(Key key) = 0;
        virtual bool isEmpty() = 0;
        
        int size() = 0; //The number of key, value pairs in this structure
        int size(Key low, Key high) = 0; //The number of key, value pairs in this
                                     //structure between low and high 
        
        Key minimum() = 0; //get Smallest key
        Key maximum() = 0; //get Largest key
        Key floor(Key key) = 0; //get largest key less than or equal to key 
        Key ceiling(Key key) = 0; //get smallest key greater than or equal to key
        
        int rank(Key key) = 0; //number of keys less than key
        Key select(int k) = 0; //get the key of rank k
        
        //These are self explanatory.
        void removeMinimum() = 0; 
        void deleteMaximum() = 0;
        
        Key * keys() = 0; //An array of all of the keys in this structure.
        Key * keys(Key low, Key high) = 0; //An array of all the keys between 
                                           //the keys low and high
};


#endif	/* TREES_H */

