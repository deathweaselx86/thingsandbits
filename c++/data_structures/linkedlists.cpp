/* 
 * File:   linkedlists.h
 * Author: jess2
 *
 *
 * Just for some practice with C++.
 *
 * Created on February 5, 2012, 8:06 PM
 */

#include "linkedlists.h"

using namespace std;

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

