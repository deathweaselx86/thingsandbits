#ifndef ZOO_H_
#define ZOO_H_
//Just for fun, an OO exercise.
//We are modeling a zoo with the idea of modelling the
//Cincinnati Zoo. It would be silly to make something so 
//specific when we could abstract it out and make it reusable.
//
//A zoo has AT LEAST
// - A location
// - A name
// - A set of acts
// - a head zookeeper
//An act has AT LEAST
// - a set of animals
// - a catchy name
//Zoo animals have at least the following:
// - a name
// - a size
// - a species
//
// It would also be nice if we could categorize them somehow.

#include <vector>
#include <string>

class Act:
{
	private:
		vector::vector<Animal_T> animals;
		string name;
	public:
		virtual Act();
		virtual ~Act();
		virtual Act(string & name="Catchy name",
			    vector::vector<Animal_T> & animals=vector::vector<Animal_T>);
		//I'm sure there's more here
}


class Zoo {
	private:
		std::string name;
		std::string location;
		std::string zookeeper;
		vector::vector <Act_T> acts;	
	public:
		Zoo(); //default constructor
		Zoo(const Zoo & z); //copy constructor
		Zoo(const std::string & n="Imaginary Zoo", //constructor with default arguments
	            const std::string & l="My head",
		    const vector::vector <Act_T> & a=vector::vector <Act_T>);
		~Zoo();
		Zoo operator=(const Zoo & z);
		void setName(const std::string & name);
		void setLocation(const std::string & location);
		void setZookeper(const std::string & zookeeper);
		string & getName() const;
		string & getLocation() const;
		string & getZookeeper() const;
		void addAct(Act_T &);
		vector::vector <Act_T> & getActs();
}
#endif

