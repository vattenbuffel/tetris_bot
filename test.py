import time
import numpy as np

player = np.array([[4, 0],
       [5, 0],
       [4, 1],
       [3, 1]])
dx = -1
dy = 0
time_ = 0

for i in range(10000):
    start_t = time.perf_counter_ns()
    new_player = player + np.array([dx, dy])
    time_ += (time.perf_counter_ns() - start_t)/1e6



print(time_)

