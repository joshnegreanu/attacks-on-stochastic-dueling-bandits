import numpy as np


class Arena:
    def __init__(self, P, Q):
        # real environment
        self.P = P
        self.P_condorcet = np.argmax(np.sum(np.where(self.P > 0.5, 1, 0), axis=1))

        # false environment
        self.Q = Q
        self.Q_condorcet = np.argmax(np.sum(np.where(self.Q > 0.5, 1, 0), axis=1))

        K = P.shape[0]
        self.W = np.ones((K, K))

        self.cost = 0
        self.P_regret = 0
        self.Q_regret = 0

        self.t = 0

    def duel(self, i, j):
        # compute strong regret
        self.P_regret += np.minimum(self.P[self.P_condorcet][i] - 0.5, self.P[self.P_condorcet][j] - 0.5)
        self.Q_regret += np.minimum(self.Q[self.Q_condorcet][i] - 0.5, self.Q[self.Q_condorcet][j] - 0.5)

        return np.random.choice([0, 1], p=[1 - self.P[i][j], self.P[i][j]])
    
    def CD_S(self, i, j):
        # duel
        x = self.duel(i, j)
        self.t += 1

        # skip same arm duels
        if i == j:
            return x

        # simulate false environment
        y = np.random.choice([0, 1], p=[1 - self.Q[i][j], self.Q[i][j]])

        self.cost += (y != x)
        return y
    
    def CD_CO(self, i, j):
        # duel
        x = self.duel(i, j)
        self.t += 1

        # skip same arm duels
        if i == j:
            return x
        
        # simulate false environment
        if self.Q[i][j] >= self.P[i][j]:
            y = 1 if x == 1 else np.random.choice([0, 1], p=[1 - (self.Q[i][j]-self.P[i][j])/(1-self.P[i][j]), (self.Q[i][j]-self.P[i][j])/(1-self.P[i][j])])
        else:
            y = 0 if x == 0 else np.random.choice([0, 1], p=[1 - self.Q[i][j]/self.P[i][j], self.Q[i][j]/self.P[i][j]])
        
        self.cost += (y != x)
        return y
    
    def CD_CL(self, i, j):
        # duel
        x = self.duel(i, j)
        self.t += 1

        # skip same arm duels
        if i == j:
            return x
        
        # update estimate
        self.W[i][j] += x
        self.W[j][i] += (1 - x)
        
        # Beta prior preference estimate
        p_ij = self.W[i][j] / (self.W[i][j] + self.W[j][i])
        
        # simulate false environment
        if self.Q[i][j] >= p_ij:
            y = 1 if x == 1 else np.random.choice([0, 1], p=[1 - (self.Q[i][j]-p_ij)/(1-p_ij), (self.Q[i][j]-p_ij)/(1-p_ij)])
        else:
            y = 0 if x == 0 else np.random.choice([0, 1], p=[1 - self.Q[i][j]/p_ij, self.Q[i][j]/p_ij])
        
        self.cost += (y != x)
        return y