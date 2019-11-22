import numpy as np
from fenwick_tree import FenwickTree

import sys

sys.path.append(sys.path)


class Model:
    def __init__(self, network, gammap, gamman, R):

        self.network = network #add symmetric-size check
        self.parameters = parameters

        self.state = []
        
        self.n = network.shape[0]
        
    def _neighbours():
        #find neigbours of each node in network

    def _resetState(self):
        # reset state variable

    def _calculateRates(self, tree, index):
        
        # calculate the new rates given that node index changed
        for i in self.neighbours[index]:
            
            self.total_rate -= self.state[i].rate

            if self.state[i].d == 0:
                self.state[i].rate = damage_rate(self.state[i].f)
            else:
                self.state[i].rate = repair_rate(self.state[i].f)

            # update rates on tree
            tree.update(i, self.state[i].rate)

            # update new total rate
            self.total_rate += self.state[i].rate

        # now update index node
        self.total_rate -= self.state[index].rate
        if self.state[index].d == 0:
            self.state[index].rate = damage_rate(self.state[index].f)
        else:
            self.state[index].rate = repair_rate(self.state[index].f)

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
        for i in self.neighbours[index]:
            
            new_f += self.state[i].d
            
            if self.state[index].d == 0:
                self.state[i].f -= 1/self.state[i].k
            else:
                self.state[i].f += 1/self.state[i].k
            
        # update this node's local frailty
        self.state[index].f = new_f/self.state[index].k

        # record for output
        state_changes.append(np.array([age, index,
                                           self.state[index].d, run]))

        # update time
        return age - 1/self.total_rate * np.log(1 - np.random.rand())

    def _mortality(self):
        return self.state[self.m1].d*self.state[self.m2].d
            
    def simulate(self, num_runs):
        # perform simulation

        state_changes = []
        death_ages = np.zeros(num_runs)
        
        for run in range(num_runs):
            
            self.tree = FenwickTree(n, 1.)
            self._resetState()
            self.total_rate = n
            
            age = 0
            alive = True

            while alive:

                index = _findRate(tree)
                self._updateState(index, run, age, state_changes)
                self._calculateRates(tree, index)

                if self._mortality() == 1:
                    alive = False
                    death_ages[run] = age

        return death_ages, np.array(state_changes)
            
            
    
