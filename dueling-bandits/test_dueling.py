import numpy as np
import scipy.stats as stats
import random

from rucb_dueling import RUCB
from dts_dueling import DTS
from if1_dueling import IF1
from if2_dueling import IF2
from dueling_functions import v_sigmoid

K = 5
T = 10000

#cost_cap = T
#total_cost = 0
#costs = []

P = np.zeros((K, K))

def calculate_borda_score(i):
    borda_sum = 0

    for j in range(0, K):
        if i != j:
            borda_sum += P[i][j]
    
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
            if i != j and P[i][j] <= 0.5:
                condorcet_winner = False
        if condorcet_winner == True:
            return (True, i)
    
    return (False, -1)

'''
def find_copeland():
    max
    for i in range(0, K):
'''


#####################################################


# completely random preference matrix
'''
for i in range(0, K):
    P[i][i] = 0.5

    for j in range(i+1, K):
        rand_val = round(random.uniform(0, 1), 2)
        P[i][j] = rand_val
        P[j][i] = 1 - rand_val
'''

# condorcet winner guaranteed preference matrix
'''
condorcet_winner = random.randrange(K)

for i in range(0, K):
    P[i][i] = 0.5

    if i == condorcet_winner:
        for j in range(0, K):
            if i != j:
                rand_val = round(random.uniform(0.51, 1), 2)
                P[i][j] = rand_val
                P[j][i] = 1 - rand_val
    else:
        for j in range(i+1, K):
            if j != condorcet_winner:
                rand_val = round(random.uniform(0, 1), 2)
                P[i][j] = rand_val
                P[j][i] = 1 - rand_val
'''

# bradley-terry model

#outcomes = np.power(np.flip(v_sigmoid(np.arange(0, K))), 5)
#outcomes =  np.flip(np.arange(0, K) + 1)

outcomes = []


'''
this auto accounts for strong stochastic transitivity and the stochastic triangle inequality
we're basically carrying over the assumptions of the classic MAB problem, where each arm has a value in [0,1]
and that pairwise comparison is our way of distinguishing these values

this means that there is always a condorcet winner, which is basically the optimal arm in the MAB setting
and this arm is also the copeland winner (not always borda score winner...)
'''
for i in range(0, K):
    outcomes.append(random.uniform(0, 1))

#outcomes.sort(reverse=True)

print(outcomes)

for i in range(0, K):
    for j in range(0, K):
        P[i][j] = outcomes[i] / (outcomes[i] + outcomes[j])
        P[j][i] = 1 - P[i][j]

#P = np.array([[0.5, 0.9, 0.95], [0.1, 0.5, 0.9], [0.05, 0.1, 0.5]])

print(P)
#print(P-0.5)

(borda_winner, borda_score) = max_borda_score()

(cond_exist, condorcet_winner) = find_condorcet()
if cond_exist:
    print("condorcet winner exists")
    print("\tcondorcet winner:", condorcet_winner)

#print("borda winner:", borda_winner)

print("IF1 winner:", IF1(K, T, P, condorcet_winner))
#print("IF2 winner:", IF2(K, T, P))
print("RUCB winner:", RUCB(K, T, P, 0.75, condorcet_winner))
#print("DTS winner", DTS(K, T, P, 0.75))

#plt.plot(np.arange(T), costs, '-')
#plt.show()