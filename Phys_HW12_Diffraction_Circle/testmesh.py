from numpy import *

side_x = linspace(0, 1, 5)
side_y = linspace(0, 1, 6)
X = meshgrid(side_x)
Y = meshgrid(side_y)

print(X)
print(Y)