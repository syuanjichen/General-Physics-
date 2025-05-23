from vpython import *

G = 6.637E-11

mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun': 1.99E30}
radius = {'earth': 6.371E6 * 10, 'moon': 1.317E6 * 10, 'sun': 6.95E8 * 10}
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4}
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}
theta = 5.145 * pi / 180.0

earth_pos_x = -mass['moon'] * radius['moon'] / (mass['earth'] + mass['moon'])
moon_pos_x = radius['moon'] + earth_pos_x
earth_speed_z = mass['moon'] * moon_orbit['v'] / mass['earth']

scene = canvas(width = 800, height = 800, background = vector(0.5, 0.5, 0), align = 'left')

sun = sphere(radius = radius['sun'], m = mass['sun'], pos = vec(0, 0, 0), color = color.orange)
earth = sphere(radius = radius['earth'], m = mass['earth'], pos = vec(earth_orbit['r'], 0, 0) + vec(0, 0, 0), texture = {'file': textures.earth}, make_trail = False)
earth.v = vec(0, 0, -earth_orbit['v'] + earth_speed_z)
moon = sphere(radius = radius['moon'], m = mass['moon'], pos = vec(earth_orbit['r'], 0, 0) + vec(moon_orbit['r'] * cos(theta), moon_orbit['r'] * sin(-theta), 0), color = color.red, make_trail = True)
moon.v = vec(0, 0, -earth_orbit['v'] - moon_orbit['v'])

dt = 60 * 60 * 24
t = 0
scene.center = earth.pos
#scene.camera.follow(earth)

while True:
    rate(100)
    t = t + dt
    moon.a = (-G * earth.m / mag2(moon.pos - earth.pos) * norm(moon.pos - earth.pos)) + (-G * sun.m / mag2(moon.pos) * norm(moon.pos))
    moon.v += moon.a * dt
    moon.pos = moon.pos + moon.v * dt

    earth.a = (-G * moon.m / mag2(moon.pos - earth.pos) * norm(-moon.pos + earth.pos)) + (-G * sun.m / mag2(earth.pos) * norm(earth.pos))
    earth.v += earth.a * dt
    earth.pos = earth.pos + earth.v * dt