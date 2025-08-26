import numpy as np
import matplotlib.pyplot as plt
import tqdm

from arena import Arena
from bandits import RUCB, DTS, WSW


# test config
config = {
    "K": 10,  # number of arms
    "T": 100000,  # number of rounds
    "trials": 100,  # number of trials
    "bandit": "WSW",  # bandit algorithm to use, options: RUCB, DTS, WSW
    "alpha": 0.75,  # hyperparameter for bandit, if needed
    "duel": "CD_CO",  # duel type, options: CD_S, CD_CO, CD_CL, None
}


if __name__ == "__main__":

    K = config["K"]
    T = config["T"]
    trials = config["trials"]

    # preference matrices
    P = np.ndarray((K, K))
    Q = np.ndarray((K, K))

    m = np.flip(np.arange(1, K+1))
    for i,j in np.ndindex((K,K)):
        P[i][j] = (m[i])/(m[i]+m[j])
    
    for attacker in ["CD_S", "CD_CO", "CD_CL", None]:

        config["duel"] = attacker

        strong_regret_graph = np.zeros((T, trials))
        cost_graph = np.zeros((T, trials))

        corrupt = config["duel"] is not None

        for trial in tqdm.tqdm(range(trials)):
            
            m = np.flip(m)
            # m[0], m[1] = m[1], m[0]
            # np.random.shuffle(m)
            for i,j in np.ndindex((K,K)):
                Q[i][j] = (m[i])/(m[i]+m[j])
            
            # delta = np.min(np.delete(P_forge[i_max,:], i_max)) - 0.5
            
            # initialize arena
            arena = Arena(P, Q)

            # initialize bandit
            bandit = None
            if config["bandit"] == "RUCB":
                bandit = RUCB(K, config["alpha"])
            elif config["bandit"] == "DTS":
                bandit = DTS(K, config["alpha"])
            elif config["bandit"] == "WSW":
                bandit = WSW(K)
            
            # set duel function based on config
            duel = None
            if config["duel"] == "CD_S":
                duel = arena.CD_S
            elif config["duel"] == "CD_CO":
                duel = arena.CD_CO
            elif config["duel"] == "CD_CL":
                duel = arena.CD_CL
            elif config["duel"] is None:
                duel = arena.duel

            # run bandit
            for round in range(T):

                i, j = bandit.choose_arm()
                x = duel(i, j)
            
                if corrupt:
                    cost_graph[round, trial] = arena.cost
                
                strong_regret_graph[round, trial] = arena.Q_regret if corrupt else arena.P_regret

                bandit.update(i, j, x)

        cost_mean = np.mean(cost_graph, axis=1)
        strong_regret_mean = np.mean(strong_regret_graph, axis=1)

        if corrupt:
            plt.plot(cost_mean, label=config["duel"] + " cost")
        else:
            plt.plot(strong_regret_mean, label=config["bandit"] + " weak regret")

    plt.legend()
    plt.show()