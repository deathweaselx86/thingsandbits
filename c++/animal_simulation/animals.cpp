#include "animals.h"



void AnimalABC::setBenefit(food_amount_t & foodAmountLeft)
{
    /*
     This method sets the benefit for each animal. We need this to
     * determine indirectly whether this animal gets to breed.
     */
    int amountOfFood0Desired=0;
    int amountOfFood1Desired;
    
    benefit = 0;
    for (int i=0;i<8;i++)
    {        for (int j=0; j<8;j++)
                   amountOfFood0Desired += (gene.charGene[i] << j) & 1;
    }
    
    amountOfFood1Desired = sizeof(gene_t) - amountOfFood0Desired;
    
    //WTB for var in variables: doSomething() from Python
    //There has to be a way to do this in C++, someone tell me.
    if (amountOfFood0Desired >= foodAmountLeft.amountOfFood0)
    {
        foodAmountLeft.amountOfFood0-=amountOfFood0Desired;
        benefit+=amountOfFood0Desired;
    }
    else
    {
        foodAmountLeft.amountOfFood0 = 0;
        benefit += foodAmountLeft.amountOfFood0;
    }
        
    if (amountOfFood1Desired >= foodAmountLeft.amountOfFood1)
    {
        foodAmountLeft.amountOfFood1-=amountOfFood1Desired;
        benefit+=amountOfFood1Desired;
    }
    else
    {
        foodAmountLeft.amountOfFood1 = 0;
        benefit += foodAmountLeft.amountOfFood1;
    }   
    
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

Bird::Bird()
{
        generateRandomGene();
}

Bird::~Bird(){}

Bird::Bird(const Bird & bird)
{
        gene_t birdGene = bird.getGene();
        setGene(&birdGene);
}

Bird::Bird( const Bird & bird1, const Bird & bird2)
{
    //Let's combine these two Birds to make a new Bird.
    combineGeneticMaterial(bird1, bird2);
}

void Bird::makeRecombinantBird( const Bird & bird1, const Bird & bird2)
{
    combineGeneticMaterial(bird1, bird2);
    mutateGene();
}

void Bird::combineGeneticMaterial(const Bird & bird1, const Bird & bird2)
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
    gene_t bird1Gene = bird1.getGene();
    gene_t bird2Gene = bird2.getGene();
    
    gene_t newGene;
    
    for (int i=0; i<8; i++)
    {
        if (std::rand() % 2 == 1) 
                newGene.charGene[i] = bird1Gene.charGene[i];
        else
                newGene.charGene[i] = bird2Gene.charGene[i];
        
    }
    setGene(&newGene); //This makes a deep copy! Don't worry!    
}
