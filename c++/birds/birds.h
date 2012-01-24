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

//Okay, this is getting less and less simple. To make this more reusable.
//let's make an ABC and make Bird a subclass of it.

class AnimalABC{
	protected:
		union gene_t {
				char charGene[8];
				int intGene[2]; };
	 	//This struct is here to make the breeding and mutation easier,
		//at least in the case of Birds.		
		typedef std::map<string,char> foodNameToAlphabet;
		//The simulation class needs to know what the food is called.
		//The animal class needs to know what food maps to which character
		//to know how to calculate fitness . 
	 	virtual void generateRandomGene() = 0;
		virtual void mutateGene() = 0;	
		void getGene() { return & const gene; };
		virtual void combineGeneticMaterial(const & AnimalABC animal1, const & AnimalABC animal2) = 0;
	private:
		gene_t gene;
		int benefit; //this benefit variable is used to calculate the order in which this
			     //animal shares its genetic material. 
	public:
		//default constructors are A-OK
		void setBenefit(int benefit); 
		//This can be set by Population given some information from
		//Simulation.

class Bird : public AnimalABC{
	public:
		Bird();
		~Bird();
		Bird(const Bird & bird);
        	void setBenefit(int benefit);

	private:
                void mutateGene();
		void generateRandomGene();
                void combineGeneticMaterial();
        
	//Population and Simulation don't need "actual" representations of the gene.
	//This is here so the user can see it.
	friend std::ostream & operator<<(std::ostream & os, const Bird & bird);
                
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
