class Grid:

    def __init__(self, grid, start, goal):

        self.grid = grid
        self.start = start
        self.goal = goal

        self.rows = len(grid)
        self.cols = len(grid[0])

    def in_bounds(self,node):

        x,y=node
        return 0<=x<self.rows and 0<=y<self.cols

    def passable(self,node):

        x,y=node
        return self.grid[x][y] != "#"

    def neighbors(self,node):

        x,y=node

        candidates = [
            (x+1,y),
            (x-1,y),
            (x,y+1),
            (x,y-1)
        ]

        result=[]

        for n in candidates:
            if self.in_bounds(n) and self.passable(n):
                result.append(n)

        return result