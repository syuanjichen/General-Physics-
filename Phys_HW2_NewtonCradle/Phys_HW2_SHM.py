from vpython import *

g = 9.8
size = 0.1
m = 1.0
L = 0.5
k = 20.0

scene = canvas(width = 500, height = 500, center = vec(0, -0.2, 0), background = vec(0.5, 0.5, 0))
ceiling = box(length = 2.0, height = 0.005, width = 2.0, color = color.blue)
ball = sphere(radius = size, color = color.red)
spring = helix(radius = 0.01, thickness = 0.01)
ball.v = vec(0, 0, 0)
ball.pos = vec(0, -L, 0)

dt = 0.001

while True:
    rate(1000)
    spring.axis = ball.pos - spring.pos

    spring.force = -k * (mag(spring.axis) - L) * spring.axis.norm()
    ball.a = vector(0, -g, 0) + spring.force / m

    ball.v += ball.a * dt
    ball.pos += ball.v * dt
