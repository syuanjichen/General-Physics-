from vpython import *
from numpy import *

N = 100
R, lamda = 1.0, 500E-9
d = 100E-6
k = 2*pi/lamda

dx, dy = d/N, d/N #Screen Coordinate
dX, dY = d/N, d/N #Hole Coordinate

scene1 = canvas(align = 'left', height=600, width=600, center = vector(N*dx/2, N*dy/2, 0))
scene2 = canvas(align = 'right', x=600, height=600, width=600, center = vector(N*dx/2, N*dy/2, 0))
scene1.lights, scene2.lights = [], []
scene1.ambient, scene2.ambient = color.gray(0.99), color.gray(0.99)

screen_side = linspace(-0.01*pi, 0.01*pi, N)
x,y = meshgrid(screen_side, screen_side)

hole_side = linspace(-d/2, d/2, N)
X, Y = meshgrid(hole_side, hole_side)
Inside_X_Y = zeros((N, N))
for i in range(N):
    for j in range(N):
        if X[i][j]**2 + Y[i][j]**2 <= (d/2)**2:
            Inside_X_Y[i, j] = True
    
E_field = zeros((N, N))

for i in range(N):
    for j in range(N):
        E_field[i, j] = sum(cos(k*x[i][j]*X + k*y[i][j]*Y) * dX * dY * Inside_X_Y)
            
Intensity = abs(E_field) ** 2
maxI = amax(Intensity)
for i in range(N):
    for j in range(N):
        box(canvas = scene1, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,
            color=vector(Intensity[i,j]/maxI, Intensity[i,j]/maxI, Intensity[i,j]/maxI))

brightest_pos_x = 0
brightest_pos_y = 0   
for i in range(N):
    for j in range(N):
        if Intensity[i, j] == maxI:
            brightest_pos_x = i
            brightest_pos_y = j
            break

first_dark_pos_x = brightest_pos_x
first_dark = Intensity[first_dark_pos_x, brightest_pos_y]

for i in range(brightest_pos_x, N):
    if Intensity[i, brightest_pos_y] <= first_dark:
        first_dark_pos_x = i
        first_dark = Intensity[first_dark_pos_x, brightest_pos_y]
    else:
        break

theta_real = (first_dark_pos_x - brightest_pos_x + 0.5) * 0.02 * pi / (N - 1)
theta_theo = 1.22 * lamda / d
print("Simulated Rayleigh Criterion: " + str(theta_real))
print("Theoretical Rayleigh Criterion: " + str(theta_theo))

Intensity = abs(E_field)
maxI = amax(Intensity)
for i in range(N):
    for j in range(N):
        box(canvas = scene2, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,
            color=vector(Intensity[i,j]/maxI, Intensity[i,j]/maxI, Intensity[i,j]/maxI))