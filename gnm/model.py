import numpy as np
from .node import Node
from .fenwick_tree import FenwickTree
from .rates import damage_rate, repair_rate

class Model:
    """
    Generic network model of aging (GNM).

    Parameters
    ----------
    
    network : list of lists or 2d array
        Adjacency list (list of neighbour lists) or adjacency matrix (2d array). 
        Adjacency list must contain no self loops. Adjacency matrix must be square and 
        have zero diagonal.

    gammap : float
        Damage rate parameter.

    gamman : float
        Repair rate parameter.

    R : float
        Ratio of damage rate to repair rate.

    record_deficits : bool, default = True
        If True, outputs recorded node trajectories.

    """
    def __init__(self, network, gammap, gamman, R, record_deficits = True):

        self.n = len(network)

        self.state = []
            
        # adjacency list
        if type(network) == list:

            for i in range(self.n):

                assert i not in network[i], "Error: trying to connect node to itself"
                
                self.state.append(Node(i, create_neighbours = False))
                self.state[i].neighbours = np.array(network[i])
                self.state[i].k = len(self.state[i].neighbours)
        
        # adjacency matrix
        elif type(network) == np.ndarray:
            assert network.shape[0] == network.shape[1], "Error: adjacency matrix not square"
            assert np.all(np.diagonal(network) == 0), "Error: non-zero diagonal of adjacency matrix"
            
            for i in range(self.n):
                self.state.append(Node(i, network))

        else:
            assert False, "Error: network format not recognized"

        # need to find top 2 most connected
        self.m1 = 0
        self.m2 = 1

        self.record_deficits = record_deficits
        
        self.parameters = (gammap, gamman, R)
    

    def _resetState(self):
        
        # reset state variable
        for i in range(self.n):
            self.state[i].reset()

    
    def _calculateRates(self, tree, index):
        
        # calculate the new rates given that node index changed
        for i in self.state[index].neighbours:
            
            self.total_rate -= self.state[i].rate

            if self.state[i].d == 0:
                self.state[i].rate = damage_rate(self.state[i].f, self.parameters)
            else:
                self.state[i].rate = repair_rate(self.state[i].f, self.parameters)

            # update rates on tree
            tree.update(i, self.state[i].rate)

            # update new total rate
            self.total_rate += self.state[i].rate

        # now update index node
        self.total_rate -= self.state[index].rate
        if self.state[index].d == 0:
            self.state[index].rate = damage_rate(self.state[index].f, self.parameters)
        else:
            self.state[index].rate = repair_rate(self.state[index].f, self.parameters)

        # update rate on tree
        tree.update(index, self.state[index].rate)

        # update new total rate
        self.total_rate += self.state[index].rate

    
    def _findRate(self, tree):
        # find index of next event
        val = self.total_rate * np.random.rand()
        index = tree.search(val)
        return index

    
    def _updateState(self, index, run, age, state_changes):
        
        # change state 0->1, 1->0
        self.state[index].d = (self.state[index].d+1)%2

        # update neighbours
        new_f = 0
        for i in self.state[index].neighbours:
            
            new_f += self.state[i].d
            
            if self.state[index].d == 0:
                self.state[i].f -= 1/self.state[i].k
            else:
                self.state[i].f += 1/self.state[i].k
            
        # update this node's local frailty
        self.state[index].f = new_f/self.state[index].k

        # record for output
        if self.record_deficits:
            state_changes.append(np.array([age, index,
                                           self.state[index].d, run]))

        # update time
        return age - 1/self.total_rate * np.log(1 - np.random.rand())

    
    def _mortality(self):
        # evaluate mortality
        return self.state[self.m1].d*self.state[self.m2].d

    
    def simulate(self, num_runs):
        """
        Perform simulation.

        Parameters
        ----------

        num_runs : int
            Number of individuals to simulate.

        Returns
        -------

        death_ages : array, shape = [num_runs]
             Death ages for each simulated individual. Unscaled.

        state_changes : array, shape = [num_runs, 4]
            Returns the state changes of nodes for all simulated individuals. 
            Each row contains [age, node index, new node state, individual id]
            
        """

        state_changes = []
        death_ages = np.zeros(num_runs)
        
        for run in range(num_runs):
            
            tree = FenwickTree(self.n, 1.)
            self._resetState()
            self.total_rate = self.n
            
            age = 0
            alive = True
            
            while alive:

                index = self._findRate(tree)
                age = self._updateState(index, run, age, state_changes)
                self._calculateRates(tree, index)

                if self._mortality() == 1:
                    alive = False
                    death_ages[run] = age

        if self.record_deficits:
            return death_ages, np.array(state_changes)
        else:
            return death_ages
