import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools as it
import random as rd
import time
start = time.time()

'''plot the roots of polynomials with integer coefficients'''

def get_roots(highest_degree, possible_coefficients=[-1,1]):
    # highest_degree = 12
    # possible_coefficients = list(range(-3, 4))
    # possible_coefficients = [-7, -5, -3, -2, 2, 3, 5, 7]
    # possible_coefficients = [-1, 1]
    lol = [possible_coefficients]*(highest_degree+1)

    roots = []
    degs = []
    for cs in it.product(*lol):
        root = np.roots(cs)
        root = [[r.real, r.imag] for r in root]
        roots.extend(root)
        first_nonzero = next((i for i, x in enumerate(cs) if x != 0), highest_degree + 1)
        deg = highest_degree - first_nonzero
        degs.extend([deg]*len(root))

    # transpose
    roots = list(map(list, zip(*roots)))

    return roots[0], roots[1], degs


# coefs_lol = [rd.sample(range(1,10), 3) for x in range(20)]
coefs_lol = [map(lambda x: x + y, [1,2,3]) for y in range(20)]
coefs_lol = [sorted(coefs+map(lambda x: -x, coefs)) for coefs in coefs_lol]


def make_plot(coefs):
    fig = plt.figure()
    # plt.scatter(*roots, s=0.05, marker='.', edgecolors='none') # c=degs, cmap='gist_rainbow')
    x_roots = []
    y_roots = []
    all_degs = []
    max_deg = 7
    for i in reversed(range(1, max_deg+1)):
        print(i)
        x, y, degs = get_roots(i, possible_coefficients=coefs)
        x_roots.extend(x)
        y_roots.extend(y)
        all_degs.extend(degs)
    print('making plot...')
    cmap = mpl.colors.ListedColormap(['#e83515','#ff71ce','#fffb96','#48d1cc','#05ffa1','#f18200','#cdbaa2'])
    # cmap = plt.cm.gist_rainbow
    bounds = range(1, max_deg+1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    plt.scatter(x_roots, y_roots, s=list(map(lambda deg: 0.01*(max_deg - deg)**2, all_degs)), marker='.', edgecolors='none', c=all_degs, cmap=cmap, norm=norm)
    ax = plt.gca()
    ax.set_axis_bgcolor('black')
    # ax.set_axis_bgcolor('#ff8c00')
    plt.colorbar(cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
    plt.title(str(coefs))
    plt.axis('equal')
    plt.xlim(-1.5,1.5)
    plt.ylim(-1.5,1.5)
    return fig

i = 0
for coefs in coefs_lol:
    fig = make_plot(coefs)
    print('saving fig %i...' % i)
    plt.savefig('roots_rd_hr7_%i.png' % i, figure=fig, dpi=2000, bbox_inches='tight')
    i += 1