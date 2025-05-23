from vpython import *

# Part 1 : Define constants
g = 9.8
theta = pi/4
ball_size = 0.25
C_drag = 0.9
times = 1
t = 0
dt = 0.001
height_max = 0
distance = 0

# Part 2 : Create the scene
scene = canvas(title = "Projectile Motion", width = 600, height = 600, align = 'left', background = vec(0.5,0.5,0))
floor = box(length = 30, height = 0.01, width = 10, color = color.blue)
ball = sphere(radius = ball_size, color = color.red, make_trail = True)

# Part 3 : The Basic Properties of the ball
ball.pos = vec(-15,ball_size,0)
ball.v = vec(20 * cos(theta), 20 * sin(theta),0)
ball_arrow = arrow(color = color.yellow, shaftwidth = 0.05)

# Part 4 : Run and Pause Button
running = True
def run(b):
    global running
    running = not running
    if running:
        b.text = "Pause"
    else:
        b.text = "Run"

button(text = "Pause", pos = scene.title_anchor, bind = run)

# Part 5 : Reset Button
reset = False
def reset():
    global reset, times, t, C_drag, height_max, distance, end, running
    reset = not reset
    if not reset:
        ball.clear_trail()
        show_speed.delete()
        #show_displacement.delete()
        #show_height.delete()
        ball.pos = vec(-15,y.value,0)
        ball.v = vec(v.value * cos(theta), v.value * sin(theta),0)
        end = False
        t = 0
        times = 1
        height_max = 0
        distance = 0
        reset = not reset

button(text = "Reset", pos = scene.title_anchor, bind = reset)

# Part 6 : Initial Height Silder
def height(y):
    global height
    height = y.value
    ball.pos.y = y.value
    y_caption.text = "Height (y) = " + "{:1.2f}" .format(y.value) + " m" + "\n\n"

y = slider(bind = height, min = 0.25, max = 20.25, value = 0.25, step = 0.25, left = 20)
y_caption = wtext(text = "Height (y) = " + "{:1.2f}" .format(y.value) + " m" + "\n\n")

# Part 7 : Initial Speed Slider
def initial_speed(v):
    global speed
    speed = v.value
    ball.v = vec(v.value * cos(theta), v.value * sin(theta),0)
    speed_caption.text = "Speed = " + "{:1.2f}" .format(v.value) + " m/s" + "\n\n"

v = slider(bind = initial_speed, min = 0, max = 50, value = 20, step = 0.05, left = 20)
speed_caption = wtext(text = "Speed = " + "{:1.2f}" .format(v.value) + " m/s" "\n\n")

# Part 8 : Initial Angle Slider
def angle(w):
    global theta
    theta = w.value * pi / 180
    angle_caption.text = "angle = " + "{:1.2f}" .format(w.value) + " Degrees" + "\n\n"

w = slider(bind = angle, min = 0, max = 90, value = 45, step = 0.5, left = 20)
angle_caption = wtext(text = "angle = " + "{:1.2f}" .format(w.value) + " Degrees" + "\n\n")

# Part 9 : Drag Coefficient Slider
def cdrag(c):
    global C_drag
    C_drag = c.value
    drag_caption.text = "Drag = " + "{:1.2f}" .format(c.value) + "\n\n"

c = slider(bind = cdrag, min = 0, max = 3, value = 0.9, step = 0.05, left = 20)
drag_caption = wtext(text = "Drag = " + "{:1.2f}" .format(c.value) + "\n\n")

# Part 10 : Graph Settings
ball_speed = graph(title = "Speed-time Plot", xtitle = "t (s)", ytitle = "Speed (m/s)", width = 400, align = 'right')
show_speed = gcurve(graph = ball_speed, color = color.blue, width = 4)
#ball_displacement = graph(title = "Displacement", xtitle = "t (s)", ytitle = "x (m)", width = 400, align = 'left')
#show_displacement = gcurve(graph = ball_displacement, color = color.red, width = 4)
#ball_height = graph(title = "Height", xtitle = "t (s)", ytitle = "y (m)", width = 400, align = 'right')
#show_height = gcurve(graph = ball_height, color = color.green, width = 4)
    
#Part 11 : Messages
def readme():
    intro_line1.text = "    The ball will bounce for three times.\n"
    intro_line2.text = "    You can pause and reset before the ball bounces three times.\n"
    intro_line3.text = "    Initial height, initial speed, angle and drag coefficient can be modified.\n"
    intro_line4.text = "    If you want to adjust the values, press pause, move the slider, and press reset.\n\n\n"

intro_line1 = wtext(text = "    The ball will bounce for three times.\n")
intro_line2 = wtext(text = "    You can pause and reset before the ball bounces three times.\n")
intro_line3 = wtext(text = "    Initial height, initial speed, angle and drag coefficient can be modified.\n")
intro_line4 = wtext(text = "    If you want to adjust the values, press pause, move the slider, and press reset.\n\n\n")
sleep(0.5)

# Part 12 : Main Program
end = False
while end == False:
    while times <= 3:
        if running:
            rate(1.0/dt)
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
    
    def result():
        time_elapsed.text = "   t = " + "{:1.4f}" .format(t) + "s." + "\n\n"
        displacement_caption.text = "   Displacement = " + "{:1.4f}" .format(ball.pos.x + 15) + " m." + "\n\n"
        distance_caption.text = "   Distance = " + "{:1.4f}" .format(distance) + " m." + "\n\n"
        M_height_caption.text = "   Maximum Height = " + "{:1.4f}" .format(height_max) + " m." + "\n\n"
    
    time_elapsed = wtext(text = "   t = " + "{:1.4f}" .format(t) + "s." + "\n\n")
    displacement_caption = wtext(text = "   Displacement = " + "{:1.4f}" .format(ball.pos.x + 15) + " m." + "\n\n", pos = scene.caption_anchor)
    distance_caption = wtext(text = "   Distance = " + "{:1.4f}" .format(distance) + " m." + "\n\n", pos = scene.caption_anchor)
    M_height_caption = wtext(text = "   Maximum Height = " + "{:1.4f}" .format(height_max) + " m." + "\n\n", pos = scene.caption_anchor)

    end = True