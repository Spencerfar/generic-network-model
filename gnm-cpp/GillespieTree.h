#include <vector>

/*
Gillespie SSA for rates updated with a tree, preserving partial sums
*/

//Time to an event given the rates
double TimeToEvent(double TotalRate) {
    
    using namespace Parameters;
    return -1.0/TotalRate * log(RNG(g1));

}


//repair rate given parameters and local frailty
double DamageRate(double f) {

    using namespace Parameters;
    return exp(gammap * f);

}

//repair rate given parameters and local frailty
double DamageRateDisease(double f) {

    using namespace Parameters;
    return 1.1*exp(gammap * f);

}

//Damage rate given parameters and local frailty
double RepairRate(double f) {

    using namespace Parameters;
    return 1/R * exp(-gamman * f);

}

//calculate and set the rate of a node and all of its neighbours, as well as the
//cumulative rate
void CalculateRates(std::vector<Node> &Network, Node &X, EventTree &tree, int j, double &TotalRate) {

    
    for(int i: X.Neighbours) {

	//remove current from total rate
        TotalRate -= Network[i].Rate;

        //update rates on the network
        if(Network[i].d == 0) Network[i].Rate = DamageRate(Network[i].f); 
        else if(Network[i].d == 1) Network[i].Rate = RepairRate(Network[i].f); 

        //update rates on the tree
        tree.Update(i, Network[i].Rate);

        //update new total rate
        TotalRate += Network[i].Rate;

    }

    //update the X node
    TotalRate -= X.Rate;
    if(X.d == 0) X.Rate = DamageRate(X.f); 
    else if(X.d == 1) X.Rate = RepairRate(X.f); 

    tree.Update(j, Network[j].Rate);

    TotalRate += X.Rate;

}


// loop over all nodes and change the damage rates of all of them
void CalculateRatesFull(std::vector<Node> &Network, EventTree &tree, double &TotalRate) {
    
    // reset total rate
    TotalRate = 0;
    
    int i = 0;
    // loop over all nodes
    for(Node &n: Network ) {
        
        // change damage rates of all nodes that aren't already damaged
        if(n.d == 0) n.Rate = DamageRateDisease(n.f);
        
        // add to total rate
        TotalRate += n.Rate;
        
        // update tree
        tree.Update(i, Network[i].Rate);
        // not sure if I can use i as I am here to index Network
        i += 1;
    }
	
}



//finds rate and returns index of rate to be performed
int FindRate(EventTree &tree, double TotalRate) {

    double val = TotalRate * RNG(g1) ; //temp
    int i = tree.Search(val);
    assert(i < Parameters::N);
    
    return i;

}
