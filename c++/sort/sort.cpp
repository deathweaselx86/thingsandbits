#include <iostream>
#include <cstdlib>
#include <assert.h>

void insertionSort(int * array, int arrayLength);
void quickSort(int *array, int arrayLength);
void quickSortInplace(int *array, int arrayLength);
void qSortInPlace(int *array, int leftIndex, int rightIndex);
int partition(int *array, int leftIndex, int rightIndex);
void swap(int *a, int *b);
void printArray(int *array, int left, int right);

using namespace std;

#define ARRLENGTH 10 
int main()
{
	srand(time(NULL));
	int myArray[ARRLENGTH];
	for (int i=0;i< ARRLENGTH; i++)
		myArray[i] = rand() % 100;	
	printArray(myArray,0,ARRLENGTH);
	quickSortInplace(myArray,ARRLENGTH);
	cout<<endl;
	printArray(myArray,0,ARRLENGTH);
	return 0;
}

void printArray(int *array, int left, int right)
{
	for (int i=left;i<right;i++)
		cout<<array[i]<<" ";
	cout<<endl<<endl;
}

void quickSortInplace(int *array, int arrayLength)
{
	srand(time(NULL));	// seed pseudorandom generator for "random" pivot values
	qSortInPlace(array,0,arrayLength-1);
}

void qSortInPlace(int *array, int leftIndex, int rightIndex)
{
	/*
	 * QuickSort: Recursively sort an array by picking a pivot element,
	 * push all elements greater than that element to one side of the array,
	 * and all elements less than that element to the other.
	 */
	if (leftIndex < rightIndex) {
	
		int pivotIndex = partition(array,leftIndex,rightIndex);
		qSortInPlace(array, leftIndex, pivotIndex-1);
		qSortInPlace(array, pivotIndex+1, rightIndex);
	}
}
int partition(int *array, int leftIndex, int rightIndex)
{
	/*
	 * Partition the array into a set of elements less than
	 * the pivot element, the pivot element, and a set of elements
	 * greater than the pivot element.
	 */
	int pivotValue = array[rightIndex];

	int i = leftIndex-1;
	for (int j=leftIndex;j<rightIndex;j++)
	{
		if (array[j]<= pivotValue)
		{
			i=i+1;
			swap(array[i], array[j]);
		}
	}
	swap(array[i+1], array[rightIndex]);

	cout<<"pivotValue: "<<pivotValue<<endl;
	cout<<"-----"<<endl;
	printArray(array,leftIndex,rightIndex);
	return i+1;
}

void swap(int *a, int *b)
{
	int dummy;
	dummy = *a;
	*a = *b;
	*b = *a;
}
