import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from lcp.src.container import Box, Container
# %matplotlib qt

# %matplotlib inline
# import matplotlib_inline
# matplotlib_inline.backend_inline.set_matplotlib_formats('svg')

# %config InlineBackend.figure_format = 'retina'
plt.style.use('ggplot')
# plt.style.use('fast')
# from pylab import rcParams
# rcParams['figure.figsize'] = 8, 5


# pallete = sns.color_palette(
#    "Paired", 10) + sns.color_palette("Accent", 10) + sns.color_palette("bright", 10)

# Obtén una paleta de colores 'tab20' con 20 colores distintos
colors_tab20 = cm.get_cmap('tab20', 20)
# Obtén una paleta de colores 'Set3' con 10 colores distintos
colors_set3 = cm.get_cmap('Set3', 10)

pallete = []

for i in range(30):
    if i < 20:
        pallete.append(colors_tab20(i))
    else:
        pallete.append(colors_set3(i - 20))


def cuboid_data(o, size=(1, 1, 1)):
    # suppose axis direction: x: to left; y: to inside; z: to upper
    # get the length, width, and height
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1], o[1], o[1]],
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]
    z = [[o[2], o[2], o[2], o[2], o[2]],
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]
    return np.array(x), np.array(y), np.array(z)


def plotcuboid(pos=(0, 0, 0), size=(1, 1, 1), ax=None, **kwargs):
    # Plotting a cube element at position pos
    if ax is not None:
        X, Y, Z = cuboid_data(pos, size)
        # print(X)
        # print(Y)
        # print(Z)
        ax.plot_surface(X, Y, Z, **kwargs)


def draw(pieces: list[Box], title="", container_dimension: Container = None):
    positions = []
    sizes = []
    colors = []
    for each in pieces:
        positions.append(list(each.position))
        sizes.append(list(each.size))
        colors.append(each.type)
    cuboids = zip(positions, sizes, colors)

    fig = plt.figure(dpi=300)
    # fig.canvas.layout.width = '100%'
    # fig.canvas.layout.height = '900px'
    ax = fig.add_subplot(111, projection='3d')
    for p, s, c in cuboids:
        color = pallete[c]
        plotcuboid(pos=p, size=s, ax=ax,
                   alpha=0.8,
                   color=color, antialiased=1,
                   # ligther border color
                   edgecolor=[min(1., c + 0.1) for c in color]
                   )
    if title:
        plt.title(title)
    if container_dimension != None:
        ax.set_xlim([0, container_dimension.length])
        ax.set_ylim([0, container_dimension.width])
        ax.set_zlim([0, container_dimension.height])
        # draw container boundaries
        x, y, z = cuboid_data([0, 0, 0], container_dimension)
        ax.plot_surface(x, y, z, color='b', alpha=0.01,
                        rstride=1, cstride=1, edgecolor='black')

    plt.axis('off')
    ax.set_aspect('equal')
    plt.savefig('lcp/document/Figures/ejemplo_solucion.svg', format='svg')
    plt.draw()  # show()
