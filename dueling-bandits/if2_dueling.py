import numpy as np
import scipy.stats as stats
import math
import random
import matplotlib.pyplot as plt

from dueling_functions import duel, corrupt_duel, v_mod_div_2

def IF2(K, T, P):
    total_duels = 0

    delta = 1/(T * math.pow(K, 2))

    b = random.randrange(0, K)

    W = list(set(np.arange(K))-set([b]))

    U = np.ones((K, K))

    while len(W) != 0:
        for w in W:
            # back out after T duels
            '''
            if total_duels > T:
                return b
            '''
            
            (duel_res, cost) = duel(b, w, P)
            total_duels += 1

            if duel_res == 1:
                U[b][w] += 1
            else:
                U[w][b] += 1
        
            P_ = U / (U + U.T)
    
        for w in W:
            conf = math.sqrt(np.log(1/delta)/(U[b][w]+U[w][b]))

            if (P_[b][w] - conf) > 0.5:
                W.remove(w)
        
        for w in W:
            conf = math.sqrt(np.log(1/delta)/(U[b][w]+U[w][b]))

            if (P_[b][w] + conf) < 0.5:
                # pruning, only difference between IF1 and IF2
                for i in W:
                    if P_[b][i] > 0.5:
                        W.remove(i)

                b = w
                W.remove(w)

                for i in W:
                    U[b][i] = 1
                    U[i][b] = 1
                    P_ = U / (U + U.T)
                    U_ = P_ + conf
                    L_ = P_ - conf
                
                break

    return (b, total_duels)