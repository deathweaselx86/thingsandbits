#ifndef BIRDS_H
#define BIRDS_H
//This code is a simple model of evolution based on Darwin's finches.
//Read more: http://en.wikipedia.org/wiki/Darwin's_finches

#include <iostream>
#include <fstream>
#include <algorithm>
#include <ctime>
#include <math.h>

class Bird{
	public:
		Bird();
		~Bird();
		Bird(const Bird & bird);
                Bird(const Bird & bird1, const Bird & bird2);
		
                static int getGeneLength();
                
                void evaluateZeros();
		void setBenefit(int benefit);
                int getNumberOfEggs();
                void generateRandomGene();
                
	private:
                static int geneLength;
                int gene;
                int benefit;
		int numberOfEggs;
	 	int numberOfZeros;
                
};


template <class T>
class Population {
        public:
                Population();
                ~Population();
                Population(T & herd);
            
        private:
                T * herd;
                double averageFitness;
};

template <class T>
class Simulation {
    
        public:
                Simulation();
                ~Simulation();
                Simulation(const Simulation & simulation);
                Simulation(Population<T> * herds);
                void setSeedAmount(int seedAmount=500);
                void setFlowerAmount(int flowerAmount=500);
                void setMaxPopulationSize(int maxPopulationSize=60);
                void setStartingPopulationSize(int startPopulationSize=15);
                void setNumberOfGenerations(int generationNumber=100);
                void seedRandomizer();
                
                const void getCurrentPopulationSize();
                
        private:
                Population<T> * herd;
                int amountOfSeeds;
                int amountOfFlowers;
                int maximumPopulationSize;
                int startingPopulationSize;
                int currentPopulationSize;
                int numberOfGenerations;
};
#endif
