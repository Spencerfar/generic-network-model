import numpy as np


class Node:

    def __init__(self, id, network = [], f = 0, d = 0, rate = 0, create_neighbours = True):

        self.id = id
        self.f = f
        self.d = d
        self.rate = rate
        self.k = 0
        self.neighbours = []
        
        if create_neighbours:
            assert type(network) == np.ndarray, "Error: network not ndarray"
            self.k = network[:,id].sum().astype(int)
            self._setNeighbours(network)
            

    def reset(self):
        self.rate = 1
        self.d = 0
        self.f = 0

    def _setNeighbours(self, network):

        n = network.shape[0]
        self.neighbours = np.zeros(self.k,int)
        
        # fix for directed later
        neighbour_num = 0
        for i in range(n):
            if network[i, self.id] == 1:
                self.neighbours[neighbour_num] = i
                neighbour_num += 1
            
        

