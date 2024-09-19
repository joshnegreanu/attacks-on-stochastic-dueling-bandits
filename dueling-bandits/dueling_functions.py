import numpy as np
from scipy.stats import bernoulli as ber
import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

v_sigmoid = np.vectorize(sigmoid)

def mod_div(a, b):
    if b == 0:
        return 1
    else:
        return a / b

v_mod_div = np.vectorize(mod_div)

def mod_div_2(a, b):
    if b == 0:
        return 0.5
    else:
        return a / b

v_mod_div_2 = np.vectorize(mod_div_2)

def duel(i, j, P):
    return (ber.rvs(P[i][j], P[j][i], size = 1)[0], 0)

def corrupt_duel(i, j, P):
    cost = False

    pre_val = ber.rvs(P[i][j], P[j][i], size = 1)[0]

    if i < j:
        if pre_val == 0:
            pre_val = 1
            cost = True

    elif j > i:
        if pre_val == 1:
            pre_val = 0
            cost = True
    
    return (pre_val, cost)

def corrupt_duel(i, j, P):
    cost = 0
    corrupt_index = 0

    pre_val = ber.rvs(P[i][j], P[j][i], size = 1)[0]

    if i == corrupt_index and j != corrupt_index:
        if pre_val == 0:
            pre_val = 1
            cost = 1

    elif j == corrupt_index and i != corrupt_index:
        if pre_val == 1:
            pre_val = 0
            cost = 1
    
    return (pre_val, cost)