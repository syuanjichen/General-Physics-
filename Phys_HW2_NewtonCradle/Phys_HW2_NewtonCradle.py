from vpython import *

# Part 1 : Define Constants
g = 9.8 # m / s^2
ball_radius = 0.2 # m
L = 2 # m
m = 1 # kg
n = 2
ball_number = 5
height = 0.05 # m
k = 150000 # N / m
dt = 0.0001 # s
t = 0 # s
sum_K = 0 # J
sum_U = 0 # J

# Part 2 : Background
scene = canvas(title = "Newton Cradle", width = 500, height = 500, center = vec(0.8, 0.4, 0), background = vec(0.5, 0.5, 0), align = 'left')
ceiling = box(length = 2.0, height = 0.005, width = 0.8, pos = vec(0.8, 2, 0), color = color.blue)

# Part 3 : Balls
balls = []
for i in range(ball_number):
    ball = sphere(pos = vec(2 * ball_radius * i, 0, 0), radius = ball_radius, color = color.white)
    ball.v = vec(0, 0, 0)
    balls.append(ball)

# Part 4 : Strings
springs = []
for i in range(ball_number):
    spring = cylinder(pos = vec(2 * ball_radius * i, L, 0), radius = 0.01)
    spring.axis = balls[i].pos - spring.pos
    spring.k = k
    springs.append(spring)

# Part 5 : Run / Pause Button
running = True
def run(b):
    global running
    running = not running
    if running:
        b.text = "Pause"
    else:
        b.text = "Run"

button(text = "Pause", pos = scene.title_anchor, bind = run)

# Part 6 : Reset Button
reset = False
def reset():
    global reset, t, end, running, i
    reset = not reset
    if not reset:
        show_K.delete()
        show_U.delete()
        show_avg_K.delete()
        show_avg_U.delete()

        for i in range(ball_number):
            balls[i].pos = vec(2 * ball_radius * i , 0, 0)
            balls[i].v = vec(0, 0, 0)
            springs[i].pos = vec(2 * ball_radius * i, L, 0)
            springs[i].axis = balls[i].pos - springs[i].pos

        for i in range(n.value):
            balls[i].pos += vec(-sqrt(L * L - (L - y.value) * (L - y.value)), y.value, 0)
            springs[i].axis = balls[i].pos - springs[i].pos
        
        end = False
        t = 0
        reset = not reset

button(text = "Reset", pos = scene.title_anchor, bind = reset)

# Part 7 : Collision Velocity Function
def af_col_v(v1, v2, m1, m2, x1, x2):
    v1_prime = v1 + 2 * (m2 / (m1 + m2)) * (x1 - x2) * dot(v2 - v1, x1 - x2) / dot(x1 - x2, x1 - x2)
    v2_prime = v2 + 2 * (m1 / (m1 + m2)) * (x2 - x1) * dot(v1 - v2, x2 - x1) / dot(x2 - x1, x2 - x1)
    return (v1_prime, v2_prime)

# Part 8 : Graph Settings
sum_ball_E = graph(title = "Sum of the Energy of all balls", xtitle = "t (s)", ytitle = "Energy (J)", width = 400, align = 'right')
show_K = gcurve(graph = sum_ball_E, color = color.blue, width = 4, label = "Kinetic Energy")
show_U = gcurve(graph = sum_ball_E, color = color.red, width = 4, label = "Potential Energy")

avg_ball_E = graph(title = "Avg of the Energy of all balls", xtitle = "t (s)", ytitle = "Energy (J)", width = 400, align = 'right')
show_avg_K = gcurve(graph = avg_ball_E, color = color.blue, width = 4, label = "Kinetic Energy")
show_avg_U = gcurve(graph = avg_ball_E, color = color.red, width = 4, label = "Potential Energy")

# Part 9 : Initialize the Velocity of balls
for i in range(n):
    #balls[i].v = vec(-(sqrt(2 * g * height)), 0, 0)
    balls[i].pos += vec(-sqrt(L * L - (L - height) * (L - height)), height, 0)
    springs[i].axis = balls[i].pos - springs[i].pos

# Part 10 : Slider for the balls to possess initial velocity
def move_balls(n):
    global move_balls, i
    move_balls = n.value
    n_caption.text = "{:1d}" .format(n.value) + " balls are moving." + "\n\n"

n = slider(bind = move_balls, min = 1, max = ball_number - 1, value = 2, step = 1, left = 20)
n_caption = wtext(text = "{:1d}" .format(n.value) + " balls are moving." + "\n\n")

# Part 11 : Slider for the initial height of the balls
def height_i(y):
    global height_i, i
    height_i = y.value
    y_caption.text = "Initial height = " + "{:.2f}" .format(y.value) + " m " + "\n\n"

y = slider(bind = height_i, min = 0.00, max = 2.00, value = 0.05, step = 0.05, left = 20)
y_caption = wtext(text = "Initial height = " + "{:.2f}" .format(y.value) + " m " + "\n\n")

# Part 12 : Main Program
while True:
    if running:
        rate(5000)
        t = t + dt

        for i in range(ball_number):
            springs[i].axis = balls[i].pos - springs[i].pos
            springs[i].force = -k * (mag(springs[i].axis) - L) * springs[i].axis.norm()
            balls[i].a = vec(0, -g, 0) + springs[i].force / m
            balls[i].v += balls[i].a * dt
            balls[i].pos += balls[i].v * dt

        for i in range(ball_number - 1):
            if((mag(balls[i].pos - balls[i + 1].pos) <= 2 * ball_radius) and dot(balls[i].pos - balls[i + 1].pos, balls[i].v - balls[i + 1].v) <= 0):
                (balls[i].v, balls[i + 1].v) = af_col_v(balls[i].v, balls[i + 1].v, m, m, balls[i].pos, balls[i + 1].pos)

        sum_K = 0.5 * m * ((balls[0].v.mag) * (balls[0].v.mag) + (balls[1].v.mag) * (balls[1].v.mag) + (balls[2].v.mag) * (balls[2].v.mag) + (balls[3].v.mag) * (balls[3].v.mag) + (balls[4].v.mag) * (balls[4].v.mag))
        sum_U = m * g * (balls[0].pos.y + balls[1].pos.y + balls[2].pos.y + balls[3].pos.y + balls[4].pos.y)

        show_K.plot(pos = (t, sum_K))
        show_U.plot(pos = (t, sum_U))
        show_avg_K.plot(pos = (t, sum_K / 5))
        show_avg_U.plot(pos = (t, sum_U / 5))