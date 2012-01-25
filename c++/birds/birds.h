#ifndef BIRDS_H
#define BIRDS_H
//This code is a simple model of evolution based on Darwin's finches.
//Read more: http://en.wikipedia.org/wiki/Darwin's_finches

#include <iostream>
#include <ctime>
#include <cmath>
#include <string>
#include <vector>
#include <map>
#include <string>

//My, this is a lot of includes.

//Okay, this is getting less and less simple. To make this more reusable.
//let's make an ABC and make Bird a subclass of it.

class AnimalABC{
	protected:
		union gene_t {
				char charGene[8];
				int intGene[2]; };
	 	//This struct is here to make the breeding and mutation easier,
		//at least in the case of Birds.		
		
		void mutateGene();
		gene_t getGene() { return gene; };
                void setGene(const gene_t &newGene);
                virtual void generateRandomGene();
		virtual void combineGeneticMaterial(AnimalABC & animal1, AnimalABC & animal2) = 0;

                
                
        private:
		gene_t gene;
		int benefit; //this benefit variable is used to calculate the order in which this
			     //animal shares its genetic material. 
                static std::map<std::string, char> foodNameToAlphabet;
                //The simulation class needs to know what the food is called.
		//The animal class needs to know what food maps to which character
		//to know how to calculate fitness . 
	public:
                virtual ~AnimalABC();
		void setBenefit(int benefit);
                std::map<std::string, char> & setFoodMap(std::map<std::string, char> thisFoodMap)
                {
                    return foodNameToAlphabet;
                }
                const std::map<std::string, char> getFoodMap();
                
		//This can be set by Population given some information from
		//Simulation.
};

//Is there anything like Java's final keyward?
class Bird : public AnimalABC{
        
        
	public:
		Bird();
		~Bird();
		Bird(Bird & bird);
                Bird(Bird & bird1, Bird & bird2);
        private:
                void combineGeneticMaterial(Bird & bird1, Bird & bird2);
                void makeRecombinantBird(Bird & bird1, Bird & bird2);
                
};


template <class T>
class Population {
        public:
                Population();
                ~Population();
                Population(std::vector<T> herd);
                void setInitialPopulationSize(int popSize);
                int getCurrentPopulationSize() const;
                
                void evaluatePopulationBenefit();
                std::vector<T> & getHerd();
                
                
        private:
                std::vector<T> herd;
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

