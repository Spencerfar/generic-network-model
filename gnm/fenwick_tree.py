import numpy as np



class FenwickTree:
    """
    Creates a partial sum tree for quicker evaluation of partial sums.
    """
    def __init__(self, n, initial_rate):

        self.n_total = 0
        self.offset = 0

        n_round = 1
        while n_round < n:
            n_round *= 2

        #where rates start as leaves
        self.offset = n_round - 1

        n_round = 2*n_round - 1
        self.n_total = n_round

        self.nodes = np.zeros(self.n_total)
        for i in range(self.offset, self.offset + n):
            self.nodes[i] = initial_rate

        self.sumTree()

    def sumTree(self):
        # sum full tree

        for parent in range(self.offset-1, -1, -1):
            child1 = 2*parent + 1
            child2 = 2*parent + 2
            self.nodes[parent] = self.nodes[child1] + self.nodes[child2]

        self.total_sum = self.nodes[0]

    def update(self, index, value):

        #set value of tree at index to value
        self.nodes[self.offset+index] = value

        i = index + self.offset

        while i > 0:

            if i % 2:
                sibling = i + 1
            else:
                sibling = i - 1

            parent = (i-1)//2
            ##print(i,sibling)
            self.nodes[parent] = self.nodes[i] + self.nodes[sibling]
            i = parent

        self.total_sum = self.nodes[0]

    def search(self, value):
        #search for value

        i = 0
        while i < self.offset:
            left_child = 2*i + 1
            if value <= self.nodes[left_child]:
                i = left_child
            else:
                value -= self.nodes[left_child]
                i = left_child + 1

        return i - self.offset

    def resetTree(self, initial_rate):

        #reset tree to zero
        for i in range(self.ntotal):
            self.nodes[i] = 0

        #set leaves
        for i in range(self.offset, offset + n):
            self.nodes[i] = initial_rate

        self.sumTree()
            
