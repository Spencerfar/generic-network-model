import numpy as np

def damage_rate(f, params):
    """
    Default unscaled damage rate (no Gamma0). 
    Uses gammap = params[0]
    """
    return np.exp(params[0]*f)

def repair_rate(f, params):
    """
    Default unscaled repair rate (no Gamma0). 
    Uses gamman = params[1], R = params[2]
    """
    return np.exp(-params[1]*f)/params[2]
