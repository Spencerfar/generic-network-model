import numpy as np
import matplotlib.pyplot as plt
from gnm.model import Model
from gnm.networks import scale_free_network

gammap = 7.5 # gamma_+
gamman = 6.5 # gamma_-
R = 1.0 # Gamma_+/Gamma_-

# scale free network function returns an adjacency list for a scale free network
network = scale_free_network(100, 2.27, 4)

# create model with chosen network and parameters
model = Model(network, gammap, gamman, R)

# simulate for num_individuals
num_individuals = 1000
t, x = model.simulate(num_individuals)

# Set Gamma_0 to scale simulated mean to population mean ~85 years
t *= (85/t.mean()) 

# create surival curve
t_sorted = np.sort(t)
survival = 1 - np.arange(1, len(t_sorted) + 1)/len(t_sorted)

# plot
plt.plot(t_sorted, survival)
plt.show()


# alternatively, create you own networks in two different ways:

"""

# example with network as adjacency list
network = [[2,3],[0],[1,3],[0]]

model = Model(network, gammap, gamman, R)
t, x = model.simulate(10)


# example with network as adjacency matrix
network = np.random.randint(2, size=(10,10))
np.fill_diagonal(network, 0)

model = Model(network, gammap, gamman, R)
t, x = model.simulate(10)

"""
