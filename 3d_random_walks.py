import random as rd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

num_paths = 100
num_iters = 1000


def rwalk_3d(num_paths, num_iters, int_steps=True):

    paths = []

    for path in range(num_paths):

        # iterate over paths
        x, y, z = 0, 0, 0
        x_list = [x]
        y_list = [y]
        z_list = [z]

        for iteration in range(num_iters):

            # integer steps
            if int_steps:
                x += rd.choice([-1, 1])
                y += rd.choice([-1, 1])
                z += rd.choice([-1, 1])

            # random decimal steps
            else:
                x += rd.uniform(-1, 1)
                y += rd.uniform(-1, 1)
                z += rd.uniform(-1, 1)

            x_list.append(x)
            y_list.append(y)
            z_list.append(z)

        paths.append([x_list, y_list, z_list])

    print('plotting results')
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for path in paths:
        ax.plot(*path, c=(rd.random(), rd.random(), rd.random(), 0.8))

    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)
    ax.set_axis_off()
    ax.view_init(elev=5, azim=-135)

    print('saving figure')
    return fig


for i in range(10):
    print(i+1)
    fig = rwalk_3d(num_paths, num_iters)
    plt.savefig('random_walk_3d_%i.png' % i, dpi=2000, bbox_inches='tight', pad_inches=0)
