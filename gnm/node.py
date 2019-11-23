import numpy as np


class Node:
    """
    Node class. Contains all info we need in the nodes for the simulation.
    
    Paremeters
    ----------

    id : int
        Network id of this node.

    network : list of lists or 2d array, optional, default = []
        Network to create node from. 
        If 2d array (adjacency matrix), must have create_neighbours = True.
        If list of lists (adjacency list), create_neighbours needs to be False, 
        and neighbours need to be set separately.

    f : float, default = 0
        Local frailty of node (proportion of damaged neighbours).
        
    d : int, default = 0
        Binary value (0,1) of node.
        
    rate : float, default = 0
        Node damage/repair rate.

    create_neighbours : bool, default = True
        If True, creates neighbours from adjacency matrix.

    """
    def __init__(self, id, network = [], f = 0, d = 0, rate = 0, create_neighbours = True):

        self.id = id
        self.f = f

        assert d == 0 or d == 1, "Error: Node value needs to be binary."
        self.d = d
        
        self.rate = rate
        self.k = 0
        self.neighbours = []
        
        if create_neighbours:
            assert type(network) == np.ndarray, "Error: network not ndarray"
            self.k = network[:,id].sum().astype(int)
            self._setNeighbours(network)
            

    def reset(self):
        """Reset nodes to rate = 1, d = 0, f = 0"""
        self.rate = 1
        self.d = 0
        self.f = 0

    def _setNeighbours(self, network):
        """Set neighbours of network (adjacency list)"""
        n = network.shape[0]
        self.neighbours = np.zeros(self.k,int)
        
        # fix for directed later
        neighbour_num = 0
        for i in range(n):
            if network[i, self.id] == 1:
                self.neighbours[neighbour_num] = i
                neighbour_num += 1
            
        

