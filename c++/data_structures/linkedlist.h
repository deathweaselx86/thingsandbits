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
        		~Node(){}
        		Node<Kind> & getNextNode() const { return next; }
     			void setNextNode(Node<Kind> * node) { next = node; } 
         		Node<Kind> & getLastNode() const {
				Node<Kind> * current = this;
				while(current->getNextNode() != NULL)
					current = current->getNextNode();
				return current;
			    }
    			void setItem(Kind & item) { Item = item; }
			    Kind & getItem() { return this->Item; }
		    private:
        		Kind Item;
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

template <class Type>
bool LinkedList<Type>::isEmpty()
{
	if (length < 1)
		return true;
	else 
		return false;
}

template <class Type>
void LinkedList <Type>::clearList()
{
	Node<Type> * temp;
	Node<Type> * current;
	
	head = current;
	while (current->getNextNode() != NULL)
	{
		temp = current->getNextNode();
		delete current;
		current = temp;
	}
	delete current;
	head=NULL;
	length = 0;

}

template <class Type> 
LinkedList <Type>::LinkedList(Type & item = NULL)
{
	if (item != NULL)
	{
		head = new Node<Type>(item);
		length = 1;
	}
	else
	{
		head = NULL;
		length = 0;
	}
}

template <class Type>
LinkedList <Type>::~LinkedList(){
	clearList();
}
template <class Type> 
void LinkedList <Type>::insertInFront(const Type & item){
 
	 //This is technically correct if head == NULL
	 Node<Type> * temp = head;
	 head = new Node<Type>(item);
	 head->setNextNode(temp);
	 length++;
 }

template <class Type>
void LinkedList <Type>::insertInBack(const Type & item)
{
	if (head != NULL)
	{
		Node<Type> * current = head;
		Node<Type> * newNode = new Node<Type>(item);

		while(current->getNextNode() != NULL)
			current = current->getNextNode();
	
		current->setNextNode(newNode);
	}
	else
		head = new Node<Type>(item);
	length++;
}	

template <class Type>
Type & LinkedList <Type>::removeHead()
{
	if (head != NULL)
	{
		Node<Type> * temp = head;
		head = head->getNextNode();
		
		Type value = temp->getItem();
		delete temp;
		length--;
		
		return value;
	}

	throw EmptyList();
}

template <class Type>
Type & LinkedList <Type>::removeTail()
{
	if (head != NULL)
	{
		Node<Type> * current = head;
		Node<Type> * lastNode = NULL;
		
		Type value;	
		while(current != NULL)
		{
			lastNode = current;
			current = current->getNextNode();
		}		
		value = current->getItem();
		lastNode->setNextNode(NULL);
		delete current;
		length--;
		return value;
	}

	throw EmptyList();
}

template <class Type>
bool LinkedList <Type>::find(Type & item)
{
	if (head != NULL)
	{
		Node<Type> * current = head;
		while(current != NULL)
		{
			if (current->getItem() == item)
				return true;
			current = current->getNextNode();
		}
	}

	return false; //return false if head is NULL or item not found
}

template <class Type>
void LinkedList <Type>::removeItem(Type &item)
{
	if (head == NULL)
		throw EmptyList();

	if (head->getItem == item)
 	{
		removeHead();
		length--;
		return;
	}

	Node<Type> * current = head->getNextNode();
	Node<Type> * lastNode = head;

	while(current != NULL)
	{
		if (current->getItem() == item)
		{
			lastNode->setNextNode(current->getNextNode());	
			delete current;
			length--;
			return;
		}
		lastNode = current;
		current = current->getNextNode();
	}
	
	
}
#endif	/* LINKEDLISTS_H */

