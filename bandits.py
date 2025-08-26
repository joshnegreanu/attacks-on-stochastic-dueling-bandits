import numpy as np


# random generator
rng = np.random.default_rng()


# safe division
def div_safe_element(a, b):
    if b == 0:
        return 1
    else:
        return a / b

div_safe = np.vectorize(div_safe_element)


class RUCB:
    def __init__(self, K, alpha):
        self.alpha = alpha
        self.K = K
        self.t = 1

        self.W = np.zeros((K, K))
        self.U = np.zeros((K, K))
    
    def choose_arm(self):
        # compute upper confidence bound
        self.U = div_safe(self.W,(self.W + self.W.T)) + np.sqrt(div_safe(self.alpha * np.log(self.t),(self.W + self.W.T)))
        np.fill_diagonal(self.U, 0.5)

        # choose potential condorcet winner
        c_pool = np.where((self.U >= 0.5).all(axis=1))[0]
        c = rng.choice(c_pool) if len(c_pool) > 0 else rng.integers(0, self.K)

        # choose opponent
        d = np.argmax(self.U[:,c])

        return c, d
    
    def update(self, i, j, outcome):
        self.W[i][j] += outcome
        self.W[j][i] += (1 - outcome)

        self.t += 1


class DTS:
    def __init__(self, K, alpha):
        self.alpha = alpha
        self.K = K
        self.t = 1

        self.B = np.zeros((K, K))
        self.U = np.zeros((K, K))
        self.L = np.zeros((K, K))
    
    def choose_arm(self):
        # compute upper and lower confidence bounds
        self.U = div_safe(self.B,(self.B + self.B.T)) + np.sqrt(div_safe(self.alpha * np.log(self.t),(self.B + self.B.T)))
        self.L = div_safe(self.B,(self.B + self.B.T)) - np.sqrt(div_safe(self.alpha * np.log(self.t),(self.B + self.B.T)))

        np.fill_diagonal(self.U, 0.5)
        np.fill_diagonal(self.L, 0.5)

        # compute copeland score
        copeland = np.sum(np.where(self.U > 0.5, 1, 0), axis=0) / (self.K-1)
        copeland_max = np.max(copeland)
        c_pool = np.where(copeland == copeland_max)[0]

        # sample beta distribution
        theta_1 = rng.beta(self.B + 1, self.B.T + 1)
        theta_1 = np.tril(1-theta_1, -1).T + np.tril(theta_1, -1)
        
        theta_pool = np.sum(np.where(theta_1 > 0.5, 1, 0), axis=1)

        # choose potential copeland winner
        a_1 = rng.choice(np.flatnonzero(theta_pool == theta_pool.max()))
        
        theta_2 = rng.beta(self.B[:,a_1] + 1, self.B[a_1,:] + 1)
        theta_pool = np.where(self.L[:,a_1] <= 0.5, theta_2, 0)

        # choose opponent
        a_2 = rng.choice(np.flatnonzero(theta_pool == theta_pool.max()))

        return a_1, a_2

    
    def update(self, i, j, outcome):
        self.B[i][j] += outcome
        self.B[j][i] += (1 - outcome)

        self.t += 1


class WSW:
    def __init__(self, K):
        self.t = 1

        self.W = np.zeros((K, K))
        
        self.i_old = None
        self.j_old = None
        

    def choose_arm(self):
        C = self.W - self.W.T
        np.fill_diagonal(C, 0)
        C = np.sum(C, axis=1)

        C_max = np.max(C)
        i_pool = np.where(C == C_max)[0]

        if len(i_pool) == 1:
            i = i_pool[0]
        else:
            if self.t > 1 and self.i_old in i_pool:
                i = self.i_old
            elif self.t > 1 and self.j_old in i_pool:
                i = self.j_old
            else:
                i = rng.choice(i_pool)
        
        C[i] = -np.inf
        C_max = np.max(C)
        j_pool = np.where(C == C_max)[0]
        
        if len(j_pool) == 1:
            j = j_pool[0]
        else:
            if self.t > 1 and self.i_old in j_pool:
                j = self.i_old
            elif self.t > 1 and self.j_old in j_pool:
                j = self.j_old
            else:
                j = rng.choice(j_pool)

        self.i_old = i
        self.j_old = j
        self.t += 1

        return i, j


    def update(self, i, j, outcome):
        self.W[i][j] += outcome
        self.W[j][i] += (1 - outcome)

        self.t += 1