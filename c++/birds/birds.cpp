#include "birds.h"


const double eggNumberFactor = 100;
//The above number determines how many eggs a particular Bird produces based on
//fitness



using namespace std;

Bird::Bird()
{
        generateRandomGene();
        benefit=0;
}

Bird::~Bird(){}

Bird::Bird(const Bird& bird)
{
        //Copy constructor
        memcpy(&gene, (void *)(bird.gene), sizeof(int));
        benefit = bird.benefit;
        numberOfEggs = bird.numberOfEggs;
        evaluateZeros();`
}


Bird::Bird(const Bird& bird1, const Bird& bird2)
{
    //This method is using for "breeding",
    //generating new birds (genes) using old birds (genes)
    //from the previous generation.
    //
    //Again, I hope you used srand() first...
    //
    //The idea here is 
    //1. Cut bird1, bird2's genes into 1 character slices to
    //get 8 characters.
    //2. Apply some idea of mutation to the characters so we don't get
    //stuck in a rut.
    //3. Construct the new Bird's gene by concatenating 4 of these
    //characters "randomly".

    int randomGeneIndex, i;
    char chromosomes[8];
    
    benefit = 0;
    numberOfEggs = 0;
    
    memcpy(chromosomes, (void *)(bird1.gene), sizeof(int));
    memcpy(chromosomes+4, (void *)(bird2.gene), sizeof(int));
    
    for(i=0; i<8;i++)
    {
        chromosomes[i] = chromosomes[i]^(rand() % 256);
    }
    
    for (i=0; i<4; i++)
    {
        randomGeneIndex = rand() % 8;
        memcpy((void *)(&gene+i), chromosomes+randomGeneIndex, sizeof(int));
    }

    
}

void Bird::evaluateZeros()
{
        numberOfZeros=0;
        
        for (int i=0; i<32; i++)
        {
            numberOfZeros += (gene << i) & 1;
        }
       
}

inline void Bird::setBenefit(int benefit){
    this->benefit = benefit;
}

inline int Bird::getNumberOfEggs() const{
    //This 60 number is an arbitrary egg factor.
    return int(benefit/60);
    
}

void Bird::getGene(string & gene) const
{
    //I don't know of any way to print the genes out in
    //binary. Hex will do, methinks.
    int success;
    char charGene[5];
    success = sprintf(charGene, "%x", &gene);
    
    gene = string(charGene);
}

void Bird::generateRandomGene()
{
    //I hope you called srand() first. 
    //Your population class should do this for you.
    gene = std::rand();
}

ostream & operator<<(ostream & os, const Bird & bird)
{
    string gene;
    bird.getGene(gene);
    //Realistically only going to be used for manual testing.
    os <<" Bird with genetic material "<<gene<<" has benefit "<<bird.benefit<<" and "<<
            bird.numberOfEggs<<endl;
}
