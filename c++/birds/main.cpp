/* 
 * File:   main.cpp
 * Author: jess2
 *
 * Created on January 21, 2012, 10:09 PM
 */
#include <iostream>
#include "birds.h"

using namespace std;

int main()
{
    Bird * testBird = new Bird;
    cout<< * testBird; 
    
    delete testBird;
    return 0;
}
/*
int main()
{
	int rand, flag,l,m,tsharef,tshares;
	Bird swap;
	
	srandom(time(NULL));
	
	double* avg = new double[numberOfGenerations];
	Bird* population = new Bird[maximumPopulationSize]; //this generation
	Bird* tpopulation = new Bird[maximumPopulationSize]; //next generation
	int* flower = new int[geneLength];  
	int* seed = new int[geneLength];
	int* gensize = new int[numberOfGenerations];
	int tsize, skip;
	
	for(int i = 0; i < geneLength; i++)
	{
		seed[i] = 0;
		flower[i] = 1;	
	}
	
	for(int j = 0; j < numberOfGenerations; j++)
	{
		tshares=0; //Suitability to eat seeds
		tsharef=0; //Suitability to eat from flowers. By definition tshares - 20
		avg[j] = 0;
		gensize[j] = 0;
		//evaluate fitness
		for(int i = 0; i < current_size; i++)
		{
			tshares=0;
			tsharef=0;
			for(int k = 0; k < geneLength; k++)
			{
				population[k].evaluateZeros();
				tshares += population[k].numberOfZeros;
				tsharef += geneLength - population[k].numberOfZeros;
			}

			for(int k = 0; k < geneLength; k++)
			{
				population[k].benefit = amountOfFlower*((20-population[k].numberOfZeros)/(double)tsharef) + amountOfSeed*(population[k].numberOfZeros/(double)tshares);
				population[k].numberOfEggs =int(population[k].benefit/eggNumberFactor);	
			}
		}

		//Defined in algorithm:
		sort(population, population + current_size);
/*
		//now to organize by "benefit"
		do{
			flag = 0;
			for(int i = 0; i < current_size; i++)
			{
				if (population[i].benefit < population[i+1].benefit)
				{
					swap = population[i];
					population[i] = population[i+1];
					population[i + 1] = swap;
					flag = 1;
				}
		  	}
		} while(flag);	
*/
		//uhh, going to try to make this work for a fixed populationulation
		//first
		//
/*
		tsize = 0;
		for(int k=0;k<current_size;k++)
		{
			skip = 1;
			while((tsize < maximumPopulationSize)&&(population[k].numberOfEggs))
			{
			if(population[k].numberOfEggs)
			  {
			  
			 	 if(population[k+skip].numberOfEggs)
			 	  {
					tpopulation[tsize] = population[k];
					tpopulation[tsize+1] = population[k+skip];
				
					l = random() % geneLength;
					do {
					m = random() % geneLength;
					} while(l = m);
					//I am a bad coder. About to use the var flag as a temp var:-/
					if (l > m)
					{
						flag = l;
						l = m;
						m = flag;
					}
			
					for (int i = l; i < m; i++)
					{
						flag = tpopulation[tsize].gene[i];
						tpopulation[tsize].gene[i] = tpopulation[tsize+1].gene[i];
						tpopulation[tsize+1].gene[i] = flag;
					}
				//mutation
					for (int i = 0; i < 2; i++)
					{
						l = random() % geneLength;
						tpopulation[tsize].gene[l] = 1 - population[tsize].gene[l];
						l = random() % geneLength;
						tpopulation[tsize+1].gene[l] = 1 - population[tsize+1].gene[l];
					}
				population[k+skip].numberOfEggs--;
				population[k].numberOfEggs--;
				tsize=tsize+2;
				}
				else
					skip = skip+1;
			}
		     }
		   }//end of for loop for breeding
		for (int i = 0; i < current_size; i++) {
			avg[j] += population[i].getBenefit();
			}
		for(int i=0;i<tsize;i++)
		{
			population[i] = tpopulation[i];
		}
		gensize[j] = current_size;
		current_size = tsize;
	}
	
	for (int j = 0; j < numberOfGenerations; j++) {
		
		cout <<"Generation "<<j<<" : "<<avg[j]/gensize[j]<<" "<< gensize[j]<< endl;
	}

	delete[] avg;
	delete[] population;	
	delete[] tpopulation;
	delete[] flower;
	delete[] seed;

	return 0;
}

*/