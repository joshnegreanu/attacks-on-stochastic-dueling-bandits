import numpy as np
import scipy.stats as stats
import math
import random
import matplotlib.pyplot as plt

from dueling_functions import duel, corrupt_duel, v_mod_div_2

total_cost = 0
total_duels = 0
costs = []
pulls = []
total_pulls = 0
total_regret = 0
regrets = []

def IF1(K, T, P, c):
    global total_duels, total_cost, costs, pulls, total_pulls, total_regret, regrets

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
            total_cost += cost
            costs.append(total_cost)

            if b == 0 or w == 0:
                total_pulls += 1
            
            total_regret += ((P[c][b] - 0.5 + P[c][w] - 0.5) / 2)
            regrets.append(total_regret)
            
            pulls.append(total_pulls)

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
                b = w
                W.remove(w)

                for i in W:
                    U[b][i] = 1
                    U[i][b] = 1
                    P_ = U / (U + U.T)
                    U_ = P_ + conf
                    L_ = P_ - conf
                
                break

    plt.plot(np.arange(total_duels), costs, regrets, '-')
    plt.show()
    #print(P_)
    return (b, total_duels)