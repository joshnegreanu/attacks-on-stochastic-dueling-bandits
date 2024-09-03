import numpy as np
from scipy.stats import bernoulli as ber
import scipy.stats as stats
import random
import math

K = 3
T = 100

pref_matrix = np.zeros((K, K))

def mod_div(a, b):
    if b == 0:
        return 1
    else:
        return a / b

v_mod_div = np.vectorize(mod_div)

def calculate_borda_score(i):
    borda_sum = 0

    for j in range(0, K):
        if i != j:
            borda_sum += pref_matrix[i][j]
    
    return round(borda_sum / (K-1), 2)

def max_borda_score():
    max_borda = calculate_borda_score(0)
    max_i = 0

    for i in range(1, K):
        i_borda = calculate_borda_score(i)
        if i_borda > max_borda:
            max_borda = i_borda
            max_i = i
    
    return (max_i, max_borda)

def find_condorcet():
    for i in range(0, K):
        condorcet_winner = True
        for j in range(0, K):
            if i != j and pref_matrix[i][j] <= 0.5:
                condorcet_winner = False
        if condorcet_winner == True:
            return (True, i)
    
    return (False, -1)

'''
def find_copeland():
    max
    for i in range(0, K):
'''

def duel(i, j):
    return ber.rvs(pref_matrix[i][j], pref_matrix[j][i], size = 1)[0]

def RUCB(a):
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
        
        if duel(c, d) == 1:
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


#####################################################


# completely random preference matrix

for i in range(0, K):
    pref_matrix[i][i] = 0.5

    for j in range(i+1, K):
        rand_val = round(random.uniform(0, 1), 2)
        pref_matrix[i][j] = rand_val
        pref_matrix[j][i] = 1 - rand_val


# condorcet winner guaranteed preference matrix
'''
condorcet_winner = random.randrange(K)

for i in range(0, K):
    pref_matrix[i][i] = 0.5

    if i == condorcet_winner:
        for j in range(0, K):
            if i != j:
                rand_val = round(random.uniform(0.51, 1), 2)
                pref_matrix[i][j] = rand_val
                pref_matrix[j][i] = 1 - rand_val
    else:
        for j in range(i+1, K):
            if j != condorcet_winner:
                rand_val = round(random.uniform(0, 1), 2)
                pref_matrix[i][j] = rand_val
                pref_matrix[j][i] = 1 - rand_val
'''

print(pref_matrix)

(borda_winner, borda_score) = max_borda_score()

(cond_exist, condorcet_winner) = find_condorcet()
if cond_exist:
    print("condorcet winner exists")
    print("\tcondorcet winner:", condorcet_winner)

print("borda winner:", borda_winner)

print("RUCB winner:", RUCB(0.51))