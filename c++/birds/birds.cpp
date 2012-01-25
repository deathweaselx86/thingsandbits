#include "birds.h"




void AnimalABC::setGene(const gene_t & newGene) {
    memcpy(&gene, &newGene, sizeof(gene_t) );
}

void AnimalABC::setBenefit(int benefit)
{
    this->benefit = benefit;
}

void AnimalABC::mutateGene() 
{
    //Have Simulation class call srand() first!...
    for(int i=0; i < 8; i++)
    {
        gene.charGene[i] = gene.charGene[i]^(std::rand()%256);
    }
    
}

void AnimalABC::generateRandomGene()
{
    //Have Simulation class call srand() first!...
    gene.intGene[0] = std::rand();
    gene.intGene[1] = std::rand();
}

const std::map<std::string, char> AnimalABC::getFoodMap()
{
    return foodNameToAlphabet;
}

Bird::Bird()
{
        generateRandomGene();
        setBenefit(0);
}

Bird::~Bird(){}

Bird::Bird(Bird & bird)
{
        gene_t otherGene = bird.getGene();
        setGene(otherGene);
        setBenefit(0);
}

Bird::Bird(Bird & bird1, Bird & bird2)
{
    //Let's combine these two Birds to make a new Bird.
    combineGeneticMaterial(bird1, bird2);
}

void Bird::makeRecombinantBird(Bird & bird1, Bird & bird2)
{
    combineGeneticMaterial(bird1, bird2);
    mutateGene();
}

void Bird::combineGeneticMaterial(Bird & bird1, Bird & bird2)
{
    //This method is using for "breeding",
    //Generating new birds (genes) using old birds (genes)
    //from the previous generation.
    //
    //Again, I hope you used srand() first...
    //
    //The idea here is 
    //1. Cut bird1, bird2's genes into 1 character slices to
    //get 8 characters.
    //2. Construct the new Bird's gene by concatenating 4 of these
    //characters "randomly".
    
    //You really should use Bird::makeRecombinantBird() to avoid
    //getting stuck in a rut.
    int i;
    const gene_t bird1Gene = bird1.getGene();
    const gene_t bird2Gene = bird2.getGene();
    
    gene_t newGene;
    
    for (int i=0; i<8; i++)
    {
        if (std::rand() % 2 == 1) 
                newGene.charGene[i] = bird1Gene.charGene[i];
        else
                newGene.charGene[i] = bird2Gene.charGene[i];
        
    }
    setGene(newGene); //This makes a deep copy! Don't worry!    
}
