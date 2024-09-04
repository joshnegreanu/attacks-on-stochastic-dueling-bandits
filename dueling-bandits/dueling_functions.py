import numpy as np
from scipy.stats import bernoulli as ber

def mod_div(a, b):
    if b == 0:
        return 1
    else:
        return a / b

v_mod_div = np.vectorize(mod_div)

def duel(i, j, P):
    return ber.rvs(P[i][j], P[j][i], size = 1)[0]

def corrupt_duel(i, j, c, P):
    global total_cost

    pre_val = ber.rvs(P[i][j], P[j][i], size = 1)[0]

    if total_cost <= cost_cap:
        if i == c and j != c:
            total_cost += 1
            if pre_val == 0:
                pre_val = 1
        
        if j == c and i != c:
            total_cost += 1
            if pre_val == 1:
                pre_val = 0
    
    return pre_val