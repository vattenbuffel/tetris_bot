import numpy as np
import colors

s0 = np.array([[0, 0], [1, 0], [0, 1], [-1, 1]])
s1 = np.array([[0,0], [0, -1], [1, 0], [1, 1]])

z0 = np.array([[0, 0], [1, 1], [0, 1], [-1, 0]])
z1 = np.array([[0, 0], [0, -1], [1, 0], [1, 1]])

lr0 = np.array([[0, 0], [-1, 0], [1, 0], [-1, 1]])
lr1 = np.array([[0, 0], [0, -1], [-1, -1], [0, 1]])
lr2 = np.array([[0, 0], [1, 0], [1, -1], [-1, 0]])
lr3 = np.array([[0, 0], [0, -1], [0, 1], [1, 1]])

ll0 = np.array([[0, 0], [-1, -1], [-1, 0], [1, 0]])# TODO: This spawns off screen
ll1 = np.array([[0, 0], [0, -1], [1, -1], [0, 1]])
ll2 = np.array([[0, 0], [-1, 0], [1, 0], [1, 1]])
ll3 = np.array([[0, 0], [0, -1], [0, 1], [-1, 1]])

p0 = np.array([[0, 0], [0, -1], [0, 1], [0, 2]])
p1 = np.array([[0, 0], [-1, 0], [1, 0], [2, 0]])

t0 = np.array([[0, 0], [-1, 0], [1, 0], [0, 1]])
t1 = np.array([[0, 0], [-1, 0], [0, -1], [0, 1]])
t2 = np.array([[0, 0], [-1, 0], [1, 0], [0, -1]])
t3 = np.array([[0, 0], [0, -1], [1, 0], [0, 1]])

b0 = np.array([[0,0], [0, 1], [1, 0], [1, 1]])
b1 = np.array([[0,0], [0, 1], [1, 0], [1, 1]])


starts = np.array([s0, z0, lr0, ll0, p0, t0, b0])
# starts = np.array([p0])
rotated = {
    tuple((tuple(pos) for pos in s0)) : s1,
    tuple((tuple(pos) for pos in s1)) : s0,

    tuple((tuple(pos) for pos in z0)) : z1,
    tuple((tuple(pos) for pos in z1)) : z0,

    tuple((tuple(pos) for pos in lr0)) : lr1,
    tuple((tuple(pos) for pos in lr1)) : lr2,
    tuple((tuple(pos) for pos in lr2)) : lr3,
    tuple((tuple(pos) for pos in lr3)) : lr0,

    tuple((tuple(pos) for pos in ll0)) : ll1,
    tuple((tuple(pos) for pos in ll1)) : ll2,
    tuple((tuple(pos) for pos in ll2)) : ll3,
    tuple((tuple(pos) for pos in ll3)) : ll0,

    tuple((tuple(pos) for pos in p0)) : p1,
    tuple((tuple(pos) for pos in p1)) : p0,

    tuple((tuple(pos) for pos in t0)) : t1,
    tuple((tuple(pos) for pos in t1)) : t2,
    tuple((tuple(pos) for pos in t2)) : t3,
    tuple((tuple(pos) for pos in t3)) : t0,

    tuple((tuple(pos) for pos in b0)) : b0,
}

def rotate(tetromino):
    return rotated[tuple((tuple(pos) for pos in tetromino))].copy()



colors = {
    tuple(p0.reshape(-1)): colors.cyan,
    tuple(ll0.reshape(-1)): colors.blue,
    tuple(lr0.reshape(-1)): colors.orange,
    tuple(t0.reshape(-1)): colors.purple,
    tuple(s0.reshape(-1)): colors.green,
    tuple(z0.reshape(-1)): colors.red,
    tuple(b0.reshape(-1)): colors.yellow,
}


def color_get(tetromino):
    tetromino_tuple = tuple(tetromino.reshape(-1))
    return colors[tetromino_tuple]