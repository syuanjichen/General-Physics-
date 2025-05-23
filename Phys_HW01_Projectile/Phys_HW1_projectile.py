from vpython import *

# Part 1 : Define constants
g = 9.8
theta = pi/4
ball_size = 0.25
C_drag = 0.9

# Part 2 : Create the scene
scene = canvas(title = "Projectile Motion", width = 600, height = 600, align = 'left', background = vec(0.5,0.5,0))
floor = box(length = 30, height = 0.01, width = 10, color = color.blue)
ball = sphere(radius = ball_size, color = color.red, make_trail = True)

ball.pos = vec(-15,ball_size,0)
ball.v = vec(20 * cos(theta), 20 * sin(theta),0)
ball_arrow = arrow(color = color.yellow, shaftwidth = 0.05)

ball_speed = graph(title = "Speed-time Plot", xtitle = "t (s)", ytitle = "Speed (m/s)", width = 400, align = 'right')
show_speed = gcurve(graph = ball_speed, color = color.blue, width = 4)

ball_displacement = graph(title = "Displacement", xtitle = "t (s)", ytitle = "x (m)", width = 400, align = 'left')
show_displacement = gcurve(graph = ball_displacement, color = color.red, width = 4)

ball_height = graph(title = "Height", xtitle = "t (s)", ytitle = "y (m)", width = 400, align = 'right')
show_height = gcurve(graph = ball_height, color = color.green, width = 4)
    
times = 1
t = 0
dt = 0.001
height_max = 0
distance = 0

while times <= 3:
    rate(1/dt)
    t = t + dt
    ball.v += vec(0,-g,0) * dt - (C_drag * ball.v * dt)
    ball.pos += ball.v * dt
    distance += ball.v.mag * dt
    
    ball_arrow.pos = ball.pos - vec(0,ball_size/2,0)
    ball_arrow.axis = ball.v

    show_speed.plot(pos = (t, ball.v.mag))
    #show_displacement.plot(pos = (t, ball.pos.x))
    #show_height.plot(pos = (t, ball.pos.y))

    if ball.pos.y >= height_max:
        height_max = ball.pos.y

    if ball.v.y <= 0 and ball.pos.y < ball_size:
        ball.v.y = -(ball.v.y)
        times = times + 1

msg = text(text = "Displacement = " + str(ball.pos.x + 15) + " m.", pos = vec(-15,-10,0))
msg = text(text = "Distance = " + str(distance) + " m.", pos = vec(-15,-12,0))
msg = text(text = "Maximum Height = " + str(height_max) + " m.", pos = vec(-15,-14,0))