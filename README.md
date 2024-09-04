# attacks-on-stochastic-dueling-bandits
 
\documentclass{article}
\usepackage{graphicx} % Required for inserting images

\usepackage{amsmath}

\DeclareMathOperator*{\argmax}{arg\,max} % Jan Hlavacek

\usepackage{geometry}
 \geometry{
 left=1in,
 right=1in,
 top=1in,
 bottom=1in,
 }

\title{Attacks on Stochastic Dueling Bandits}
\author{Joshua Negreanu}

\begin{document}

\maketitle

\section{Introduction}

\section{Problem Formulation}

\paragraph{Stochastic Dueling Bandits}

Dueling bandits is an online reinforcement learning problem that considers pairwise comparison between arms. It is a modified version of the well-known stochastic multi-armed bandit problem. An algorithm is tasked for \(T\) rounds with choosing between \(K\) arms from the set \([K]=\{a_1,a_2,...a_k\}\). Each round, the two chosen arms, say \(a_i\) and \(a_j\), are placed in a "duel", and the result is a binary value \(o_t\) essentially determining the winner; \(o_t=1\) means \(a_i\) won and \(o_t=0\) means \(a_j\) won.\\

Dueling bandits also references the existence of a preferential matrix \(P_{K \times K}\). All values within the matrix exist between 0 and 1, and any entry \(p_{ij}\) represents the probability of arm \(a_i\) beating arm \(a_j\) in a duel. As would follow: \[p_{ji}=1-p_{ij}\]
This is true \(\forall i,j \in \{1,2,...K\}\), meaning that for a single arm \(a_i\), \(p_{ii}=0.5\) always. The return value \(o_t\), therefore, is chosen using a Bernoulli Distribution with parameter \(p\) being the preferential matrix entry. This is to say that: \[o_t=Ber(p_{ij})\]

\paragraph{Winning Arms in Dueling Bandits}

There are different types of winner denominations in dueling bandits, all of which rely on the underlying preferential matrix \(P\). The most ideal is the Condorcet winner, that being the arm that is preferred to beat all other arms. This is to say that if arm \(a_c\) is the Condorcet winner, then \(\forall i \neq c \in K\), \(p_{ci}>0.5\). However, the Condorcet winner is not guaranteed to exist for all valid preferential matrices. In the absence of a Condorcet winner, another popular alternative is the Borda score winner. The Borda score of an arm \(a_i\) is defined as:
\[b(a_i)={\frac{1}{K-1} \sum_{j \neq i}^K p_{ij}}\]
The Borda score winner is the arm with the highest Borda score. A Borda score winner always exists for any preferential matrix. However, if a Condorcet winner exists, it is not guaranteed to be the Borda score winner. We will refer to the Borda score winner arm as \(a_b\), and it will be considered the optimal arm for the continuation of this paper. We define the Borda score winner as:\[a_b=\argmax_{a_i \in [K]} b(a_i)\]
The optimal strategy for all \(T\) rounds is to pair the optimal arm \(a_b\) against itself. Any other sub-optimal strategy incurs regret. Regret at a particular round \(t\) is defined as:\[r_t(a_i,a_j)=b(a_b)-\frac{1}{2}(b(a_i)+b(a_j))\]
Notice that only when \(a_i=a_j=a_b\) will regret equal 0.  The objective of a dueling bandits algorithm is to minimizes the cumulative regret over \(T\) rounds:\[R_T=\sum_t^T r_t\]I am realizing now that I may want to change to either Copeland winner or simply use Condorcet assumption.

\paragraph{Dueling Bandit Algorithms} To be written... Would like to analyze RUCB, MergeRUCB, RCS, and DTS (since it solves Copeland, and Condorcet winner is a Copeland winner).

\section{Attacks on Stochastic Dueling Bandits}

\paragraph{Threat Model 1 (Pre-Bernoulli)}

We consider an attacker in the dueling bandits setup as an intermediary between our choosing of two arms \(a_i\) and \(a_j\) at a round \(t\) and the returning of value \(o_t\). The attacker aims to have the algorithm determine a preferred arm \(a_x\) which is distinctly different from the true Borda score winner \(a_b\). The attacker intervenes in round \(t\) by adding to the value of \(p_{ij}\) a value \(c_t\) before drawing from the Bernoulli Distribution. \(c_t\) can either be positive, meaning the attacker prefers \(a_i\) to win, or negative, meaning they prefer \(a_j\) to win. We denote the modified Bernoulli parameter as:\[\tilde{p}_{ij}=p_{ij}+c_t\]
Therefore, the altered return value is:\[\tilde{o}_t=Ber(\tilde{p}_{ij})\]
An attacker accumulates cost through their actions. They are limited by a cost cap \(C\) such that:\[\sum_t^T ||c_t|| \leq C\]
It is in the attacker's best interest to keep intervention to a minimum and only when it benefits the algorithm's impressions of \(a_x\).

\paragraph{Threat Model 2 (Post-Bernoulli)} We consider an attacker in the dueling bandits setup as an intermediary between our choosing of two arms \(a_i\) and \(a_j\) at a round \(t\) and the returning of value \(o_t\). The attacker aims to have the algorithm determine a preferred arm \(a_x\) which is distinctly different from the true Borda score winner \(a_b\). The attacker intervenes in round \(t\) by switching the value of \(o_t\) to its complement. If \(a_i\) and \(a_j\) were to duel, and the result was \(o_t=1\), if the attacker had wanted \(a_j\) to win, they would return a modified \(\tilde{o}_t=0\). We denote switching by the addition of a value \(c_t \in \{-1,1\}\). Therefore:\[\tilde{o}_t=o_t+c_t\]
An attacker accumulates cost through their actions. Each switch of \(o_t\) accumulates 1 cost. The attacker is limited by a cost cap, essentially the number of switches they are allowed:\[\sum_t^T ||c_t|| \leq C\]
It is in the attacker's best interest to keep intervention to a minimum and only when it benefits the algorithm's impressions of \(a_x\).\\

These are the two main ways I thought attacks could happen in dueling bandits. Maybe there's a different, more subtle way! I believe that the attacker would want to make their arm appear to be the Condorcet winner, which would pretty much guarantee their selection in an Condorcet-assuming algorithm. 



\end{document}
