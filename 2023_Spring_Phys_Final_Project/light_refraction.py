from vpython import *
import numpy as np

c = 299792458E-10 # speed of light (reduced)
n_air = 1.0 # refraction index of air
n_water = 1.35
n_glass = 1.70
theta = -pi/4
t = 0
height = 30
width = 20
height_piece = 60
width_piece = 40

scene = canvas(title = "Light Refraction", background = vec(0.5, 0.5, 0.5), width = 500, height = 500, center = vec(0, 0, 0))
ball = sphere(radius = 0.1, color = color.red, pos = vec(-20, 20, 0), make_trail = True)
ball.v = c * vector(cos(theta), sin(theta), 0)
layer1 = box(pos = vec(0, 0, 0), length = 30, height = 0.1, width = 10, color = color.blue)
layer2 = box(pos = vec(0, -10, 0), length = 30, height = 0.1, width = 10, color = color.green)
layer3 = box(pos = vec(10, -10, 0), length = 0.1, height = 30, width = 10, color = color.yellow)
refracted1 = False
refracted2 = False
refracted3 = False
print(180*theta/pi)

while(True):
    dt = 0.01
    ball.pos = ball.pos + ball.v * dt
    if ball.pos.y < layer1.pos.y and refracted1 == False:
        angle_in = acos(abs((vector.dot(ball.v, vector(0, 1, 0))/mag(ball.v))))
        angle_out = asin((n_air * sin(angle_in)/n_water))
        theta = -pi/2 + angle_out
        ball.v = c * vector(cos(theta),sin(theta),0)
        print(180*theta/pi)
        refracted1 = True
    if ball.pos.y < layer2.pos.y and refracted2 == False:
        angle_in = acos(abs((vector.dot(ball.v, vector(0, 1, 0))/mag(ball.v))))
        angle_out = asin((n_water * sin(angle_in)/n_glass))
        theta = -pi/2 + angle_out
        ball.v = c * vector(cos(theta),sin(theta),0)
        print(180*theta/pi)
        refracted2 = True
    if ball.pos.x > layer3.pos.x and refracted3 == False:
        angle_in = acos(abs((vector.dot(ball.v, vector(-1, 0, 0))/mag(ball.v))))
        angle_out = asin((n_air * sin(angle_in)/n_water))
        theta = -angle_out
        ball.v = c * vector(cos(theta),sin(theta),0)
        print(180*theta/pi)
        refracted3 = True
    t += dt

#suppose ray = [[r], [r']], r = (0, 0) is the position of source, 
#and r'=(\cos(1.5pi+\theta), \sin(1.5pi+\theta) is the direction of light
#r_new = r_old + r' * dt
#detect whether r_new.y <= liquid[i].y 
#the normal vector of the liquid surface is (0, -1)
#Calculate r' \cdot (0, -1) and divide by mag(r), you get cos(\theta)
#n1 * sin(\theta) = n2 * \sin(\phi), find \sin(\phi)
#r'_new = cos(1.5pi + \phi), sin(1.5pi + \phi)
#Repeat the steps until i = 200