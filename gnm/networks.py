import numpy as np
from .fenwick_tree import FenwickTree

# perform bidirection connections on nodes i and j
def _connectNodes(i, j, degrees, neighbours):
    
    degrees[i] += 1
    degrees[j] += 1

    neighbours[i].append(j)
    neighbours[j].append(i)

    
def _findNode(tree):
    val = tree.total_sum*np.random.rand()
    assert val >= 0, "Error: Trying to find negative value in tree for network creation."
    return tree.search(val)


def scale_free_network(n, alpha, avgk):
    """
    Create a scale free network with a given exponent alpha by shifted linear
    preferential attachment. More details in these papers, 
    Krapivsky, Redner 'Organization of Growing Random Networks', https://arxiv.org/pdf/cond-mat/0011094.pdf 
    Fotouhi, Rabbat 'Degree Correlation in Scale-Free Graphs', https://arxiv.org/pdf/1308.5169.pdf

    Parameters
    ----------

    n : int
        Network size.
    
    alpha : float
        Scale free exponent, k^{-alpha}. Must be > 2.

    avgk : int
        Average degree. Must be even and >= 2.
    
    Returns
    -------

    neighbours : list of lists
        Adjacency list for the network. First dimension is n. Then the lists within this
        list have length k, where k is the degree of the node.
    

    """

    assert alpha > 2, "Error: Scale free exponent must be > 2."
    assert avgk % 2 == 0, "Error: Average degree must be even."
    assert avgk >= 2, "Error: Average degree must be >= 2."

    m = avgk//2
    m0 = m + 2

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
