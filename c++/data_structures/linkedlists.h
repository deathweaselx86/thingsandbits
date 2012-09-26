/* 
 * File:   linkedlists.h
 * Author: jess2
 *
 * Created on February 5, 2012, 8:06 PM
 */

#ifndef LINKEDLISTS_H
#define	LINKEDLISTS_H
#include <cstdio>
#include <exception>

class EmptyList: public std::exception {};

template <class Type>
class LinkedList{
    private:
 	template <class Kind>
	class Node{
    		public:
        		explicit Node(Kind & newItem = NULL){
            			if (newItem != NULL) 
					Item = newItem;
				else 
					Item = NULL;
            			next = NULL;
        		}
        		~Node(){
				//deletion of item pointed to by next
				//delegated to that object.
			}

        		Node<Kind> & getNextNode() const { return next; }
			void setNextNode(Node<Kind> * node) { next = node; } 
       			Node<Kind> & getLastNode() const
			{
				Node<Kind> * current = this;
				while(current->getNextNode() != NULL)
					current = current->getNextNode();
				return current;
			}
    			void setItem(Kind & item) { Item = item; }
			Kind & getItem() { return this->Item; }
		private:
        		Type Item;
        		Node<Kind> * next; 

		}; 

       Node<Type> * head;
       int length;
    public:
        LinkedList(Type & item);
        ~LinkedList(); //Same as clear list, except dtor for pointer and int are also called
        bool isEmpty();
        void clearList(); //delete every entry from this list
	void insertInFront(const Type & item);
        void insertInBack(const Type & item);
        Type & removeHead(); //remove and delete head node and relink that node's linked pointer
	Type & removeTail(); //remove and delete the current tail of this list
	void removeItem(Type & Item); //remove specific item from this list
	bool find(Type & item); //If this item exists in this list, return true

};

#endif	/* LINKEDLISTS_H */

