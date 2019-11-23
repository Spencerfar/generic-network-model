import numpy as np
import matplotlib.pyplot as plt
from gnm.model import Model
from gnm.networks import scale_free_network



# example with network as adjacency list
network = [[2,3],[0],[1,3],[0]]

model = Model(network, 7.5, 6.5, 1.0)
t, x = model.simulate(10)


# example with network as adjacency matrix
network = np.random.randint(2, size=(10,10))
np.fill_diagonal(network, 0)

model = Model(network, 7.5, 6.5, 1.0)
t, x = model.simulate(10)


# scale free network function returns an adjacency list for a scale free network
network = scale_free_network(1000, 2.27, 4)

model = Model(network, 7.5, 6.5, 1.0)
t, x = model.simulate(100)

# plot some survival data
t *= (85/t.mean()) # scale mean to population mean ~85 years

# create surival
t_sorted = np.sort(t)
survival = 1 - np.arange(1, len(t_sorted) + 1)/len(t_sorted)

plt.plot(t_sorted, survival)
plt.show()
