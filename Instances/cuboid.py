# %%
import numpy
import mayavi.mlab


#             pt1_ _ _ _ _ _ _ _ _pt2
#              /|                 /|
#             / |                / |
#         pt3/_ | _ _ _ _ _ _pt4/  |
#           |   |              |   |
#           |   |              |   |
#           |  pt5_ _ _ _ _ _ _|_ _|pt6
#           |  /               |  /
#           | /                | /
#        pt7|/_ _ _ _ _ _ _ _ _|/pt8

# Where :
x1, y1, z1 = (0, 1, 1)  # | => pt1
x2, y2, z2 = (1, 1, 1)  # | => pt2
x3, y3, z3 = (0, 0, 1)  # | => pt3
x4, y4, z4 = (1, 0, 1)  # | => pt4
x5, y5, z5 = (0, 1, 0)  # | => pt5
x6, y6, z6 = (1, 1, 0)  # | => pt6
x7, y7, z7 = (0, 0, 0)  # | => pt7
x8, y8, z8 = (1, 0, 0)  # | => pt8


box_points = numpy.array([[x1, y1, z1], [x2, y2, z2], [x3, y3, z3],
                          [x4, y4, z4], [x5, y5, z5], [x6, y6, z6],
                          [x7, y7, z7], [x8, y8, z8]])

mayavi.mlab.points3d(box_points[:, 0], box_points[:, 1], box_points[:, 2],
                     mode="axes", color=(1, 0, 0))


mayavi.mlab.mesh([[x1, x2],
                  [x3, x4]],  # | => x coordinate

                 [[y1, y2],
                  [y3, y4]],  # | => y coordinate

                 [[z1, z2],
                  [z3, z4]],  # | => z coordinate

                 color=(0, 0, 0))  # black

# Where each point will be connected with this neighbors :
# (link = -)
#
# x1 - x2     y1 - y2     z1 - z2 | =>  pt1 - pt2
# -    -  and  -   -  and -    -  | =>   -     -
# x3 - x4     y3 - y4     z3 - z4 | =>  pt3 - pt4


mayavi.mlab.mesh([[x5, x6], [x7, x8]],
                 [[y5, y6], [y7, y8]],
                 [[z5, z6], [z7, z8]],
                 color=(1, 0, 0))  # red

mayavi.mlab.mesh([[x1, x3], [x5, x7]],
                 [[y1, y3], [y5, y7]],
                 [[z1, z3], [z5, z7]],
                 color=(0, 0, 1))  # blue

mayavi.mlab.mesh([[x1, x2], [x5, x6]],
                 [[y1, y2], [y5, y6]],
                 [[z1, z2], [z5, z6]],
                 color=(1, 1, 0))  # yellow

mayavi.mlab.mesh([[x2, x4], [x6, x8]],
                 [[y2, y4], [y6, y8]],
                 [[z2, z4], [z6, z8]],
                 color=(1, 1, 1))  # white

mayavi.mlab.mesh([[x3, x4], [x7, x8]],
                 [[y3, y4], [y7, y8]],
                 [[z3, z4], [z7, z8]],
                 color=(1, 0, 1))  # pink

mayavi.mlab.show()

# %%
