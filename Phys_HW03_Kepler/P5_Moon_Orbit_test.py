from vpython import *

# Part 1 : Constants and Data
G = 6.637E-11
mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun': 1.99E30}
radius = {'earth': 6.371E6 * 10, 'moon': 1.317E6 * 10, 'sun': 6.95E8 * 10}
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4}
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}
theta = 5.145 * pi / 180.0

# Part 2 : Adjust of the initial speed of earth (COM)
earth_speed_z = mass['moon'] * moon_orbit['v'] / mass['earth']

# Part 3 : Set up the environment
scene = canvas(title = "The Precession of Moon's Orbit", width = 800, height = 800, background = vector(0.5, 0.5, 0))
scene.lights = []

sun = sphere(radius = radius['sun'], m = mass['sun'], pos = vec(0, 0, 0), color = color.orange, emissive = True)
local_light(pos = vec(0, 0, 0))

earth = sphere(radius = radius['earth'], m = mass['earth'], pos = vec(earth_orbit['r'], 0, 0) + vec(0, 0, 0), texture = {'file': textures.earth}, make_trail = False)
earth.v = vec(0, 0, -earth_orbit['v'] + earth_speed_z)
moon = sphere(radius = radius['moon'], m = mass['moon'], pos = vec(earth_orbit['r'], 0, 0) + vec(moon_orbit['r'] * cos(theta), moon_orbit['r'] * sin(-theta), 0), color = color.white, make_trail = False)
moon.v = vec(0, 0, -earth_orbit['v'] - moon_orbit['v'])

# Part 4 : The Initial angular momentum of the moon (mass is not considered)
moon_v_wrt_earth = moon.v - earth.v
moon_r_wrt_earth = moon.pos - earth.pos
L0 = 0.0005 * cross(moon_r_wrt_earth, moon_v_wrt_earth)
print(L0)

# Part 5 : Angular momentum vector visualization
Angular_Momentum = arrow(color = color.white, round = True)

# Part 6 : Initial Conditions
find_quar = False
find_half = False
find_period = False
show_answer = False

dt = 300.0
t = 0.0
scene.camera.follow(earth)

wtext(text = "\nThis program simulates the precession of moon's orbit.\n")
wtext(text = "\nScroll the mouse to see the earth and the moon.\n")
wtext(text = "\nThe white arrow represents the angular momentum of the moon.\n")
wtext(text = "\nWait a bit longer to see the period of precession shown below.\n")

# Part 7 : Main Program
while True:
    rate(20000)
    t = t + dt

    moon.a = (-G * earth.m / mag2(moon.pos - earth.pos) * norm(moon.pos - earth.pos)) + (-G * sun.m / mag2(moon.pos) * norm(moon.pos))
    moon.v += moon.a * dt
    moon.pos = moon.pos + moon.v * dt

    earth.a = (-G * moon.m / mag2(moon.pos - earth.pos) * norm(-moon.pos + earth.pos)) + (-G * sun.m / mag2(earth.pos) * norm(earth.pos))
    earth.v += earth.a * dt
    earth.pos = earth.pos + earth.v * dt

    moon_v_wrt_earth = moon.v - earth.v
    moon_r_wrt_earth = moon.pos - earth.pos

    L = 0.0005 * cross(moon_r_wrt_earth, moon_v_wrt_earth)

    Angular_Momentum.pos = earth.pos
    Angular_Momentum.axis = L

    if L.x <= 0 and find_quar == False:
        period_quarter = t / 86400.0
        print("A Quarter of the Period = %.2f days" % period_quarter)
        find_quar = True

    if L.z <= 0 and find_half == False:
        period_half = t / 86400.0
        print("Half of the Period = %.2f days" % period_half)
        find_half = True

    if find_half == True and L.z >= 0 and L.x >= 0 and find_period == False:
        period_precession = t / 86400.0
        print("Period = %.2f days" % period_precession)
        find_period = True
    

    if find_quar == True and find_half == True and find_period == True and show_answer == False:
        def result():
            answerline1.text = "\nThe Period of Precession of the Moon's Orbit is " + "{:.2f}" .format(period_precession) + " days." + "\n"
            answerline2.text = "It is equal to " + "{:.2f}" .format(period_precession / 365.2422) + " years." + "\n\n"

        answerline1 = wtext(text = "\nThe Period of Precession of the Moon's Orbit is " + "{:.2f}" .format(period_precession) + " days." + "\n", pos = scene.caption_anchor)
        answerline2 = wtext(text = "It is equal to " + "{:.2f}" .format(period_precession / 365.2422) + " years." + "\n\n", pos = scene.caption_anchor)

        show_answer = True

    #print('t = %.2f, Angular Momentum = <%e, %e, %e>' % (t / 86400.0, L.x, L.y, L.z))