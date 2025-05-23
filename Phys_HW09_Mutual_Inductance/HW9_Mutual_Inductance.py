import numpy as np
from vpython import *
from math import *

large_r = 0.12 
small_r = 0.06
large_height = 0.00
small_height = 0.10
mu0 = 4e-7 * pi
part = 500
small_phi = 0
large_phi = 0

small_y = np.array([i*small_r/part for i in range(0, part + 1)])
small_ring_area = np.array([pi*(small_y[i + 1]**2 - small_y[i]**2) for i in range(0, part)])

large_y = np.array([i*large_r/part for i in range(0, part + 1)])
large_ring_area = np.array([pi*(large_y[i + 1]**2 - large_y[i]**2) for i in range(0, part)])

def BiotSavart(source_loop_r, source_height, target_loop_y, target_height, target_loop_area):
    target_flux = 0
    for i in range(0, part):
        field = np.array([0, 0, 0])
        for j in range(0, part):
            theta = 2*pi*j/part
            theta_prime = 2*pi*(j+1)/part
            source_loop_pos = np.array([source_loop_r * cos(theta), source_loop_r * sin(theta), source_height])
            source_loop_ds = np.array([source_loop_r * cos(theta_prime), source_loop_r * sin(theta_prime), source_height]) - source_loop_pos
            r = np.array([0, target_loop_y[i], target_height]) - source_loop_pos
            field = mu0 * np.cross(source_loop_ds, r) / (4 * pi * (np.linalg.norm(r))**3)
            target_flux += np.dot(field, [0, 0, target_loop_area[i]])
    return target_flux

print("Wait for 1 minute for the final result.")

small_phi = BiotSavart(large_r, large_height, small_y, small_height, small_ring_area)
print("M_sl (M of small loop from large loop) = " + str(small_phi) + " H.")

large_phi = BiotSavart(small_r, small_height, large_y, large_height, large_ring_area)
print("M_ls (M of large loop from small loop) = " + str(large_phi) + " H.")