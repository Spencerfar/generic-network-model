import numpy as np
from gnw.model import Model


network = np.random.rand(100,100)



model = Model(network, 7.5, 6.5, 1.0)
t, x = model.simulate(100)
print(t)
