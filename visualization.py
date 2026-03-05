import matplotlib.pyplot as plt


def plot_grid(grid,path=None):

    rows=len(grid)
    cols=len(grid[0])

    fig,ax=plt.subplots()

    for i in range(rows):
        for j in range(cols):

            if grid[i][j]=="#":
                ax.add_patch(plt.Rectangle((j,i),1,1,color="black"))

            else:
                ax.add_patch(plt.Rectangle((j,i),1,1,fill=False))

    if path:

        xs=[p[1]+0.5 for p in path]
        ys=[p[0]+0.5 for p in path]

        ax.plot(xs,ys,"r")

    ax.set_xlim(0,cols)
    ax.set_ylim(0,rows)
    ax.invert_yaxis()

    plt.show()