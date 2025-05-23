from vpython import *

scene = canvas(background=vec(0.8, 0.8, 0.8), width=1200, height=300, center = vec(3,0,10), fov = 0.004)

# lens_surface1 = shapes.arc(radius=0.15, angle1=0, angle2=pi)
# circle1 = paths.arc(pos=vec(0, 0, 0), radius=0.0000001, angle2=2*pi, up = vec(1,0,0))
# lens_surface2 = shapes.arc(radius=0.15, angle1=-pi, angle2=0)
# circle2 = paths.arc(pos=vec(0, 0, 0), radius=0.0000001, angle2=2*pi, up = vec(1,0,0))
# extrusion(path=circle1, shape=lens_surface1, color=color.yellow, opacity = 0.6)
# extrusion(path=circle2, shape=lens_surface2, color=color.yellow, opacity = 0.6)
lens_surface = shapes.ellipse(width = 0.15, height = 0.85, angle1=0, angle2=pi)
circle = paths.arc(pos = vec(0, 0, 0), radius = 0.0000001, angle2=2*pi, up = vec(1, 0, 0))
extrusion(path = circle, shape = lens_surface, color = color.yellow, opacity = 0.6)
curve(pos=[vec(-7,0,0),vec(13,0,0)], color=color.red, radius = 0.02)

arrow(pos=vec(-6,0,0), axis=vec(0,0.5,0), shaftwidth=0.1)
arrow(pos=vec(12, 0, 0), axis=vec(0, -1, 0), shaftwidth = 0.1)

def refraction_vector(n1, n2, v_in, normal_v):
    v_in = v_in / mag(v_in)
    normal_v = normal_v / mag(normal_v)
    vin_angle = acos(v_in.x)
    if v_in.y < 0:
        vin_angle = -vin_angle 
    normal_angle = acos(normal_v.x)
    if normal_v.y < 0:
        normal_angle = -normal_angle 
    angle_in = acos(abs(vector.dot(v_in, normal_v)))
    angle_out = asin(n1*sin(angle_in)/n2)
    if vin_angle - normal_angle >= 0:
        v_out = vector(cos(normal_angle + angle_out), sin(normal_angle + angle_out), 0)
    else:
        v_out = vector(cos(normal_angle - angle_out), sin(normal_angle - angle_out), 0)
    return v_out

R = 4.0
thickness = 0.3
g1center = vec(-R + thickness/2, 0, 0)
g2center = vec(R - thickness/2, 0, 0)
nair = 1
nglass = 1.5

for angle in range(-7, 2):
    ray = sphere (pos=vec(-6, 0.5, 0), color = color.blue, radius = 0.01, make_trail=True)
    ray.v = vector (cos(angle/40.0), sin(angle/40.0), 0)
    dt = 0.002
    air_to_glass = False
    glass_to_air = False
    while True:
        rate(1000)
        ray.pos = ray.pos + ray.v*dt
        inlens_x = (ray.pos.x >= -0.15 and ray.pos.x < 0.15)
        inlens_y = (ray.pos.y >= -0.85 and ray.pos.y < 0.85)
        if inlens_x and inlens_y and air_to_glass == False:
            normal = vector(g2center.x - ray.pos.x, -ray.pos.y, 0)
            normal = normal / mag(normal)
            ray.v = refraction_vector(nair, nglass, ray.v, normal)
            air_to_glass = True
        if air_to_glass == True and ray.pos.x >= 0.15 and glass_to_air == False:
            normal = vector(ray.pos.x - g1center.x, ray.pos.y, 0)
            normal = normal / mag(normal)
            ray.v = refraction_vector(nglass, nair, ray.v, normal)
            glass_to_air = True
        if ray.pos.x >= 12:
            print(ray.pos.y)
            break