import heapq

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def reconstruct(came_from,start,goal):

    node=goal
    path=[]

    while node!=start:
        path.append(node)
        node=came_from[node]

    path.append(start)
    path.reverse()

    return path


def search(grid,start,goal,mode="astar",weight=1):

    open_list=[]
    heapq.heappush(open_list,(0,start))

    g={start:0}
    came_from={}

    explored=0

    while open_list:

        _,current=heapq.heappop(open_list)
        explored+=1

        if current==goal:
            return reconstruct(came_from,start,goal),explored

        for n in grid.neighbors(current):

            new_cost=g[current]+1

            if n not in g or new_cost<g[n]:

                g[n]=new_cost
                came_from[n]=current

                if mode=="ucs":
                    f=g[n]

                elif mode=="greedy":
                    f=manhattan(n,goal)

                elif mode=="weighted":
                    f=g[n]+weight*manhattan(n,goal)

                else:
                    f=g[n]+manhattan(n,goal)

                heapq.heappush(open_list,(f,n))

    return None,explored