import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Gráfico de ejemplo estático en 3D del llenado del contenedor
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define el contenedor
container_dim = [10, 10, 10]  # Dimensiones del contenedor (largo, ancho, alto)
ax.bar3d(0, 0, 0, container_dim[0], container_dim[1],
         container_dim[2], color='lightgrey', alpha=0.3, edgecolor='k')

# Función para añadir una caja al gráfico


def add_box(ax, position, dimensions, color='blue'):
    x, y, z = position
    dx, dy, dz = dimensions
    ax.bar3d(x, y, z, dx, dy, dz, color=color, alpha=0.8, edgecolor='k')


# Añadir cajas de ejemplo
boxes = [
    ((0, 0, 0), (4, 5, 5)),
    ((5, 0, 0), (5, 5, 2)),
    ((0, 5, 0), (3, 3, 3)),
    ((0, 0, 5), (3, 3, 5)),
    ((5, 5, 0), (5, 5, 8)),
]

for position, dimensions in boxes:
    add_box(ax, position, dimensions, color=np.random.rand(3,))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim([0, container_dim[0]])
ax.set_ylim([0, container_dim[1]])
ax.set_zlim([0, container_dim[2]])

plt.title('Ejemplo de Gráfico Estático en 3D del Llenado del Contenedor')
plt.show()
