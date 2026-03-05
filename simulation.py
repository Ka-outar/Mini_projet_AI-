import random


def simulate(start,goal,policy,epsilon,steps=100):

    state=start

    for t in range(steps):

        if state==goal:
            return True,t

        if state not in policy:
            return False,t

        r=random.random()

        if r < 1-epsilon:
            state=policy[state]

        elif r < 1-epsilon + epsilon/2:
            state=(state[0]+1,state[1])

        else:
            state=(state[0]-1,state[1])

    return False,steps


def monte_carlo(start,goal,policy,epsilon,N=1000):

    success=0
    times=[]

    for _ in range(N):

        ok,t=simulate(start,goal,policy,epsilon)

        if ok:
            success+=1
            times.append(t)

    prob=success/N

    avg_time=sum(times)/len(times) if times else None

    return prob,avg_time