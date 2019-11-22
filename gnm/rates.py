import numpy as np

def damage_rate(f, params):
    return np.exp(params[0]*f)

def repair_rate(f, params):
    return np.exp(-params[1]*f)/params[2]
