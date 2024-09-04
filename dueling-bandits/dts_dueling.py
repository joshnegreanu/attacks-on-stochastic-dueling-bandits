import numpy as np
import scipy.stats as stats

from dueling_functions import duel, v_mod_div

def DTS(K, T, P, a):
    B = np.zeros((K, K))
    for t in range(1, T+1):
        U = v_mod_div(B, B + B.T) + np.sqrt(v_mod_div(a * np.log(t), B + B.T))
        L = v_mod_div(B, B + B.T) - np.sqrt(v_mod_div(a * np.log(t), B + B.T))
    
        for i in range(0, K):
            U[i][i] = 0.5
            L[i][i] = 0.5
        
        upper_cop_scores = []
        for i in range(0, K):
            cop_count = 0
            for j in range(0, K):
                if i != j:
                    if U[i][j] > 0.5:
                        cop_count += 1
            upper_cop_scores.append(cop_count/(K-1))
        
        max_cop = max(upper_cop_scores)
        C = []
        T1 = np.zeros((K, K))
        T2 = np.zeros((K, K))

        for i in range(0, K):
            if upper_cop_scores[i] == max_cop:
                C.append(i)
        
        for i in range(0, K):
            for j in range(0, K):
                if i < j:
                    beta_dist = stats.beta(B[i][j]+1, B[j][i]+1)
                    T1[i][j] = beta_dist.rvs(size=1)[0]
                    T1[j][i] = 1 - T1[i][j]

        win_scores = []

        for i in C:
            count = 0
            for j in range(0, K):
                if i != j and T1[i][j] > 0.5:
                    count += 1
            win_scores.append(count)
        
        a_1 = C[np.argmax(win_scores)]
        
        for i in range(0, K):
            if i != a_1:
                beta_dist = stats.beta(B[i][a_1]+1, B[a_1][i]+1)
                T2[i][a_1] = beta_dist.rvs(size=1)[0]
            else:
                T2[i][i] = 0.5
        
        uncertain_arms = []
        uncertain_arm_t2 = []
        for i in range(0, K):
            if L[i][a_1] <= 0.5:
                uncertain_arms.append(i)
                uncertain_arm_t2.append(T2[i][a_1])
        
        a_2 = uncertain_arms[np.argmax(uncertain_arm_t2)]

        if duel(a_1, a_2, P) == 1:
            B[a_1][a_2] += 1
        else:
            B[a_2][a_1] += 1
    
    arm_counts = []
    for i in range(0, K):
        count = 0
        for j in range(0, K):
            if B[i][j] == 0 and B[j][i] == 0:
                continue
            elif B[i][j]/(B[i][j]+B[j][i]) > 0.5:
                count += 1
        arm_counts.append(count)
    
    return np.argmax(arm_counts)