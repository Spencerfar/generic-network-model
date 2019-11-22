import numpy as np
from gnm.model import Model


# example with adjacency list
network = [[2,3],[0],[1,3],[0]]

model = Model(network, 7.5, 6.5, 1.0)
t, x = model.simulate(100)
print(t)


# example with adjacency matrix
network = np.random.rand(10,10)

model = Model(network, 7.5, 6.5, 1.0)
t, x = model.simulate(100)
print(t)
