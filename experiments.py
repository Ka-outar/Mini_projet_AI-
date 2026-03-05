from grid import Grid
from search_algorithms import search
from markov_chain import *
from simulation import *
from visualization import plot_grid

import numpy as np
import matplotlib.pyplot as plt


grid_map=[

["S",".",".","."],
[".","#","#","."],
[".",".",".","."],
[".","#",".","G"]

]

start=(0,0)
goal=(3,3)

grid=Grid(grid_map,start,goal)

print("=== SEARCH COMPARISON ===")

algorithms=["ucs","greedy","astar","weighted"]

for algo in algorithms:

    path,explored=search(grid,start,goal,algo,weight=2)

    print(algo)
    print("path:",path)
    print("nodes:",explored)

plot_grid(grid_map,path)

policy={}

for i in range(len(path)-1):
    policy[path[i]]=path[i+1]

states=[]

for i in range(grid.rows):
    for j in range(grid.cols):

        if grid_map[i][j]!="#":
            states.append((i,j))

epsilons=[0,0.1,0.2,0.3]

results=[]

for eps in epsilons:

    prob,avg=monte_carlo(start,goal,policy,eps,1000)

    results.append(prob)

    print("\nEPSILON",eps)
    print("Success probability:",prob)
    print("Average time:",avg)

plt.plot(epsilons,results)
plt.xlabel("epsilon")
plt.ylabel("P(success)")
plt.title("Impact of uncertainty")
plt.show()