import numpy as np


def build_transition_matrix(states,policy,epsilon):

    n=len(states)

    index={s:i for i,s in enumerate(states)}

    P=np.zeros((n,n))

    for s in states:

        i=index[s]

        if s not in policy:
            P[i,i]=1
            continue

        intended=policy[s]

        transitions=[
            (intended,1-epsilon),
            ((s[0]+1,s[1]),epsilon/2),
            ((s[0]-1,s[1]),epsilon/2)
        ]

        for ns,p in transitions:

            if ns in index:
                j=index[ns]
                P[i,j]+=p
            else:
                P[i,i]+=p

    return P


def compute_Pn(P,n):
    return np.linalg.matrix_power(P,n)


def compute_pi_n(pi0,P,n):
    return pi0 @ compute_Pn(P,n)