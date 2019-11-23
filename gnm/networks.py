import numpy as np
from .fenwick_tree import FenwickTree

# perform bidirection connections on nodes i and j
def _connectNodes(i, j, degrees, neighbours):
    
    degrees[i] += 1
    degrees[j] += 1

    neighbours[i].append(j)
    neighbours[j].append(i)

    
def _findNode(tree):
    return tree.search(tree.total_sum*np.random.rand())


# create a scale free network with given alpha
def scale_free_network(n, alpha, avgk):

    m = avgk//2
    m0 = m

    w = (alpha-3)*m

    degrees = [0]
    neighbours = [[]]
    
    tree = FenwickTree(n, 0)

    # set up initial nodes
    for i in range(1,m0):

        degrees.append(0)
        neighbours.append([])

        # connect to nodes before it
        for j in range(i):

            _connectNodes(i, j, degrees, neighbours)
            tree.update(i, degrees[i] + w)
            tree.update(j, degrees[j] + w)

    # add other nodes
    for i in range(m0, n):

        connect_to = []

        for j in range(m):

            # select node based on connectivity
            # and prevent multiple connections
            while True:
                new_connection = _findNode(tree)
                if new_connection not in connect_to:
                    break
            
            connect_to.append(new_connection)


        # connect all of these to the new node
        degrees.append(0)
        neighbours.append([])
        for node in connect_to:
            _connectNodes(i, node, degrees, neighbours)
            tree.update(i, degrees[i] + w)
            tree.update(node, degrees[node] + w)

            
    return neighbours
