from vpython import *

g = 9.8
size = 0.02
m = 0.5
L = 0.5
k = 15000

scene = canvas(width = 500, height = 500, center = vec(0, -0.2, 0), background = vec(0.5, 0.5, 0))
ceiling = box(length = 0.8, height = 0.005, width = 0.8, color = color.blue)
ball = sphere(radius = size, color = color.red)
spring = cylinder(radius = 0.005)
ball.v = vec(0.6, 0, 0)
ball.pos = vec(0, -L - (m * g / k), 0)

dt = 0.001
t = 0

while True:
    rate(1000)
    t = t + dt

    spring.axis = ball.pos - spring.pos
    spring_force = -k * (mag(spring.axis) - L) * spring.axis.norm()
    ball.a = vector(0, -g, 0) + spring_force / m

    ball.v = ball.v + ball.a * dt
    ball.pos = ball.pos + ball.v * dt