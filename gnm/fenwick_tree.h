/*
https://en.wikipedia.org/wiki/Fenwick_tree
Tree to record partial sums.

See this paper https://pubs.acs.org/doi/pdf/10.1021/jp993732q
Particular figure 7 is a good visualization.

*/

class FenwickTree {

public:

    //N: number of rates
    //InitialRate: initial value of leaves
    FenwickTree();
    FenwickTree(int N, double InitialRate);

    //perform initial sum to set up tree structure
    void SumTree();

    //change the rate of event i to value
    void Update(int i, double value);

    int Search(double value);

    //reset entire tree using leaves with Value
    void ResetTree(double Value);

    std::vector<double> tree; 
    int N; //# of rates
    int ntotal; //# of rates (rounded up to power-of-2) + tree          
    int offset; //index where rates start as leaves of tree
    double TotalSum; //store total sum of tree

};
