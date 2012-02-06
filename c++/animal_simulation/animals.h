#ifndef BIRDS_H
#define BIRDS_H
//This code is a simple model of evolution based on Darwin's finches.
//Read more: http://en.wikipedia.org/wiki/Darwin's_finches

#include <iostream>
#include <ctime>
#include <cmath>
#include <string>
#include <list>
#include <string>

#include <boost/utility/enable_if.hpp>
#include <boost/type_traits.hpp>

//My, this is a lot of includes.

//Okay, this is getting less and less simple. To make this more reusable.
//let's make an ABC and make Bird a subclass of it.


struct simulation_prefs_t {
                int amountOfFood0;
                int amountOfFood1;
                int maximumPopulationSize;
                int startingPopulationSize;
                int currentPopulationSize;
                int numberOfIterations; };
                
struct food_amount_t {
                int amountOfFood0;
                int amountOfFood1; };
union gene_t {
		char charGene[8];
		int intGene[4]; };
class AnimalABC{
	protected:
		union gene_t {
				char charGene[8];
				int intGene[4]; };
	 	//This struct is here to make the breeding and mutation easier.	
		
		void mutateGene();
		gene_t getGene() const { return gene; }
                void setGene(const gene_t *newGene){ std::memcpy(&gene, newGene, sizeof(gene_t));}
                void setBenefit(food_amount_t & food_amount_left);
                virtual void generateRandomGene();
		virtual void combineGeneticMaterial(const AnimalABC & animal1, const AnimalABC & animal2) = 0;
                    
        private:
             
		gene_t gene;
		int benefit; //this benefit variable is used to calculate the order in which this
			     //animal shares its genetic material. Also known as "fitness" 
	public:
                virtual ~AnimalABC(){};
     
                
		//This can be set by Population given some information from
		//Simulation.
};

//Is there anything like Java's final keyward?
class Bird : public AnimalABC{
        
        
	public:
		Bird();
		~Bird();
		Bird(const Bird & bird);
                Bird(const Bird & bird1, const Bird & bird2);
        private:
                void combineGeneticMaterial(const Bird & bird1, const Bird & bird2);
                void makeRecombinantBird(const Bird & bird1, const Bird & bird2);
                
};

//If you use some class other than something derived from AnimalABC, you will get a
//compiler error
template <class T, class Enable = void> class Population;

template <class T> class Population<T, class boost::enable_if<boost::is_base_of<AnimalABC, T> >::type>
{
        public:
                Population(std::list<T> herd, food_amount_t & food_amounts);
                void makeNextGeneration();
                void evaluatePopulationBenefit();
                std::list<T> & getHerd();
                
                
        private:
                std::list<T> * herd;
                double averageBenefit;
                food_amount_t * foodAmounts;
};





template <class T> Population<T, class boost::enable_if<boost::is_base_of<AnimalABC, T> >::type>::Population(std::list<T> new_herd, food_amount_t & food_amounts)
{
    herd = new_herd;
    foodAmounts = (void *)food_amounts;
}

template <class T> void Population<T, class boost::enable_if<boost::is_base_of<AnimalABC, T> >::type>::evaluatePopulationBenefit()
{
    int thisBenefit;
    typename std::list<T>::iterator iter;
    
    for(iter=herd.begin(); iter < herd.end(); iter++)
    {
        /*Benefit is the amount of food this animal got to eat.
         * How to calculate this generally? **/
        thisBenefit = 0; 
        iter->setBenefit(foodAmounts);
    }
}

template <class T> class Simulation{
    
        public:
                Simulation(simulation_prefs_t simulationPrefs);
                ~Simulation();
                Simulation(const Simulation<T> & simulation);
                const void getCurrentPopulationSize();
                
        private:
                Population<T> population;
                simulation_prefs_t simulationPreferences;
                food_amount_t foodAmounts;
              
};

template <class T> Simulation<T>::Simulation(simulation_prefs_t simulation_prefs)
{
    std::srand(std::time(NULL));
    
    simulationPreferences = simulation_prefs;
    population = Population<T>(simulation_prefs.startingPopulationSize);
}

#endif

