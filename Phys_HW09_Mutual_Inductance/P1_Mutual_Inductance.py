import numpy as np
from vpython import *
from math import *

large_r = 0.12 
small_r = 0.06
large_height = 0.00
small_height = 0.10
mu0 = 4e-7 * pi
part = 200
small_phi = 0
large_phi = 0

small_y = np.array([i*small_r/part for i in range(0, part + 1)])
small_ring_area = np.array([pi*(small_y[i + 1]**2 - small_y[i]**2) for i in range(0, part)])
large_pos = np.zeros(shape = (part, 3))
large_pos[:, 0] = large_r * np.array([cos(2*pi*i/part) for i in range(0, part)])
large_pos[:, 1] = large_r * np.array([sin(2*pi*i/part) for i in range(0, part)])
large_ds = np.zeros(shape = (part, 3))
large_ds[:, 0] = large_r * np.array([cos(2*pi*(i+1)/part)-cos(2*pi*i/part) for i in range(0, part)])
large_ds[:, 1] = large_r * np.array([sin(2*pi*(i+1)/part)-sin(2*pi*i/part) for i in range(0, part)])

large_y = np.array([i*large_r/part for i in range(0, part + 1)])
large_ring_area = np.array([pi*(large_y[i + 1]**2 - large_y[i]**2) for i in range(0, part)])
small_pos = np.zeros(shape = (part, 3))
small_pos[:, 0] = small_r * np.array([cos(2*pi*i/part) for i in range(0, part)])
small_pos[:, 1] = small_r * np.array([sin(2*pi*i/part) for i in range(0, part)])
for i in range(0, part):
    small_pos[i, 2] = small_height
small_ds = np.zeros(shape = (part, 3))
small_ds[:, 0] = small_r * np.array([cos(2*pi*(i+1)/part)-cos(2*pi*i/part) for i in range(0, part)])
small_ds[:, 1] = small_r * np.array([sin(2*pi*(i+1)/part)-sin(2*pi*i/part) for i in range(0, part)])
for i in range (0, part):
    small_ds[i, 2] = small_height

def BiotSavart(source_loop_pos, source_loop_ds, target_loop_y, target_loop_height, target_loop_area):
    target_flux = 0
    for i in range(0, part):
        field = np.array([0, 0, 0])
        for j in range(0, part):
            r = np.array([0, target_loop_y[i], target_loop_height]) - source_loop_pos[j]
            field = mu0 * np.cross(source_loop_ds[j], r) / (4 * pi * (np.linalg.norm(r))**3)
            target_flux += np.dot(field, [0, 0, target_loop_area[i]])
    return target_flux

small_phi = BiotSavart(large_pos, large_ds, small_y, small_height, small_ring_area)
print("M_sl (M of small loop from large loop) = " + str(small_phi) + " H.")

large_phi = BiotSavart(small_pos, small_ds, large_y, large_height, large_ring_area)
print("M_ls (M of large loop from small loop) = " + str(large_phi) + " H.")
