from vpython import *
g = 9.8 # g = 9.8 m/s^2
size = 1.0 # ball radius = 1.0 m
height = 50.0 # ball center initial height = 100.0 m

scene = canvas(width = 800, height = 800, center = vec(0,height/2,0), background = vec(0.5,0.5,0))
floor = box(length = 30, height = 0.01, width = 10, color = color.blue)
ball = sphere(radius = size, color = color.red, make_trail = True, trail_radius = 0.05)

msg = text(text = 'Free Fall', pos = vec(-10,10,0))

ball.pos = vec(0,height,0) # ball center initial position
ball.v = vec(0,0,0) # ball initial velocity

dt = 0.001

while ball.pos.y >= size:
    rate(1000)

    ball.pos = ball.pos + ball.v * dt
    ball.v.y = ball.v.y - (g * dt)

msg.visible = False
msg = text(text = str(ball.v.y), pos = vec(-10,10,0))
print(ball.v.y)
