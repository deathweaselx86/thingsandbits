#ifndef BIRDS_H
#define BIRDS_H
//This code is a simple model of evolution based on Darwin's finches.
//Read more: http://en.wikipedia.org/wiki/Darwin's_finches

#include <iostream>
#include <fstream>
#include <algorithm>
#include <ctime>

class Bird{
	public:
		Bird();
		~Bird();
		Bird(const Bird & aBird);
		Bird & operator=(const Bird & aBird);
		void revaluateZeros();                
		void setBenefit(int benefit);
		
	private:
		int gene;
                int benefit;
		int numberOfEggs;
	 	int numberOfZeros;
                
};


template <class T>
class Population {
        public:
                population();
                ~population();
                population(T & herd);
            
        private:
                T * herd;
                double averageFitness;
};

class Simulation {
    
        public:
                Simulation();
                ~Simulation();
                Simulation(const Simulation & simulation);
                Simulation(Population * herds);
                void setSeedAmount(int seedAmount=500);
                void setFlowerAmount(int flowerAmount=500);
                void setMaxPopulationSize(int maxPopulationSize=60);
                void setStartingPopulationSize(int startPopulationSize=15);
                void setNumberOfGenerations(int generationNumber=100);
                void seedRandomizer();
                
                const void getCurrentPopulationSize();
                
        private:
                Population * herd;
                int amountOfSeeds;
                int amountOfFlowers;
                int maximumPopulationSize;
                int startingPopulationSize;
                int currentPopulationSize;
                int numberOfGenerations;
};
#endif
