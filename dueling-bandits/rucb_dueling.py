import numpy as np
import scipy.stats as stats
import math
import random

from dueling_functions import duel, v_mod_div

def RUCB(K, T, P, a):
    W = np.zeros((K, K))
    B = []
    for t in range(1, T+1):
        U = v_mod_div(W, W + W.T) + np.sqrt(v_mod_div(a * np.log(t), W + W.T))
        
        for i in range(0, K):
            U[i][i] = 0.5

        C = []

        for i in range(0, K):
            can_beat = True
            for j in range(0, K):
                if U[i][j] < 0.5:
                    can_beat = False
            if can_beat:
                C.append(i)
        
        c = 0

        if C == []:
            c = random.randrange(0, K)
        
        B = [x for x in B if x in C]

        if len(C) == 1:
            B = C
            c = C[0]
        elif len(C) > 1:
            probs = ()
            for i in range(0, K):
                if i in B:
                    probs += (0.5,)
                else:
                    probs += (1/(math.pow(2, len(B)) * len(list(set(C)-set(B)))),)
            
            probs = tuple(x/sum(probs) for x in probs)
            
            custom_dist = stats.rv_discrete(values=(np.arange(K), probs))

            c = custom_dist.rvs(size=1)[0]

        d = 0
        d_u_max = U[0][c]

        for i in range(1, K):
            if U[i][c] > d_u_max:
                d = i
                d_u_max = U[i][c]
        
        if duel(c, d, P) == 1:
            W[c][d] += 1
        else:
            W[d][c] += 1

    arm_counts = []
    for i in range(0, K):
        count = 0
        for j in range(0, K):
            if W[i][j] == 0 and W[j][i] == 0:
                continue
            elif W[i][j]/(W[i][j]+W[j][i]) > 0.5:
                count += 1
        arm_counts.append(count)
    
    return np.argmax(arm_counts)