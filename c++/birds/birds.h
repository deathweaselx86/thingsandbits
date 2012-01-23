#ifndef BIRDS_H
#define BIRDS_H
//This code is a simple model of evolution based on Darwin's finches.
//Read more: http://en.wikipedia.org/wiki/Darwin's_finches

#include <iostream>
#include <ctime>
#include <cmath>
#include <cstdlib>
#include <string>
#include <vector>

using namespace std;

class Bird{
	public:
		Bird();
		~Bird();
		Bird(const Bird & bird);
                Bird(const Bird & bird1, const Bird & bird2);
                
                void evaluateZeros();
		void setBenefit(int benefit);
                int getNumberOfEggs() const;
                void getGene(string & gene) const;
                void generateRandomGene();
                
                friend ostream & operator<<(ostream & os, const Bird & bird);
                
	private:
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
                Population(vector<T> herd);
                void setInitialPopulationSize(int popSize);
                int getCurrentPopulationSize() const;
                
                void evaluatePopulationBenefit();
                vector<T> & getHerd();
                
                
        private:
                vector<T> herd;
                double averageBenefit;
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
                void setIterations(int iterations=100);
                void randomizeSeed();
                
                const void getCurrentPopulationSize();
                
        private:
                Population<T> * herd;
                int amountOfSeeds;
                int amountOfFlowers;
                int maximumPopulationSize;
                int startingPopulationSize;
                int currentPopulationSize;
                int numberOfIterations;
};
#endif
