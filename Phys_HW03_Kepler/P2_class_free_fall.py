from vpython import *
g = 9.8
size = 0.25
height = 15.0

class any_ball(sphere):
    m = 1.0
    v = vector(0, 0, 0)
    def kinetic_energy(self):

        return 0.5 * self.m * mag(self.v) ** 2

scene = canvas(width = 800, height = 800, center = vec(0, height / 2, 0), background = vec(0.5, 0.5, 0))
floor = box(length = 30, height = 0.01, width = 10, color = color.blue)

ball = any_ball(radius = size, color = color.red)

print(ball.m, ball.v, ball.kinetic_energy())

ball.pos = vector(0, height, 0)
ball.v = vector(0, 0, 0)
ball.m = 3.0
dt = 0.001

while ball.pos.y >= size:
    rate(1000)
    ball.pos += ball.v * dt
    ball.v.y += -g * dt

print(ball.m, ball.v, ball.kinetic_energy())