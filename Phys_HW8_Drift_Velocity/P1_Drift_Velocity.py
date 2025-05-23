from vpython import *
import numpy as np

#Part 1 : Parameters
prob = 0.005
N, L = 400, 7E-9/2.0
E = 1000000
q, m, size = 1.6E-19, 1E-6/6E23, 0.1E-9 #artificial charge particle
t, dt, vrms = 0, 1E-16, 10000.0
atoms, atoms_v = [],[]

#Part 2 : Initialization
scene = canvas(width=600, height=600,align = 'left', background=vector(0.2,0.2,0))
scenev = canvas(width=600, height=600, align = 'left', range = 4E4, background=vector(0.2, 0.2,0))
container = box(canvas=scene, length = 2*L, height = 2*L, width = 2*L, opacity=0.2, color = color.yellow )
pos_array = -L + 2*L*np.random.rand(N,3)
X, Y, Z = np.random.normal(0, vrms, N), np.random.normal(0, vrms, N), np.random.normal(0, vrms, N)
v_array = np.transpose([X, Y, Z])
def a_to_v(a): # array to vector
    return vector(a[0], a[1], a[2])

for i in range(N):
    atom = sphere(canvas=scene, pos=a_to_v(pos_array[i]), radius = size, color=a_to_v(np.random.rand(3,1)))
    atoms.append(atom)
    atoms_v.append(sphere(canvas=scenev,pos=a_to_v(v_array[i]), radius = vrms/30, color=a_to_v(np.random.rand(3,1))))

vd_graph = graph(title = "Theoretical and Real Drift Velocity", xtitle = "Time (s)", ytitle = "Drift Velocity (m/s)", width = 600, align = 'left', ymin = 0, ymax = 2500, fast = False)
show_theo = gcurve(graph = vd_graph, color = color.red, width = 4, label = "Theoretical")
show_real = gcurve(graph = vd_graph, color = color.blue, width = 4, label = "Real")

#Part 3 : the average velocity and two axes in velocity space
vd_ball = sphere(canvas=scenev,pos=vec(0,0,0),radius = vrms/15, color=color.red)
x_axis = curve(canvas=scenev, pos=[vector(-2*vrms,0,0), vector(2*vrms,0,0)], radius=vrms/100)
y_axis = curve(canvas=scenev, pos=[vector(0,-2*vrms,0), vector(0,2*vrms,0)], radius=vrms/100)
vv = vector(0, 0, 0) # for calculating the average velocity
total_c = 0 # the total number of collisions

#Part 4 : Main Program
while True:
    t += dt
    rate(10000)
    v_array[:,0] += q*E/m*dt
    pos_array += v_array*dt # calculate new positions for all atoms
    outside = abs(pos_array) >= L
    pos_array[outside] = - pos_array[outside]

# handle collision here
    for i in range (N):
        if(int((1/prob) * np.random.rand()) % (1/prob) == 0):
            total_c += 1
            v_array[i][0] = np.random.normal(0, vrms)
            v_array[i][1] = np.random.normal(0, vrms)
            v_array[i][2] = np.random.normal(0, vrms)
    
    vv += a_to_v(np.sum(v_array,axis = 0)/N)
    if int(t/dt)%2000 == 0:
        tau = t * N / total_c
    print("Collision time = " + str(tau) + " s.")
    print("Real Drift Velocity = " + str(vv.mag/(t/dt)) + " m/s.")
    print("Theoretical Drift Velosity = " + str(q*E*tau/m) + " m/s.\n")
    vd_ball.pos = vv/(t/dt)
    show_theo.plot(pos = (t, q*E*tau/m))
    show_real.plot(pos = (t, vv.mag/(t/dt)))


    for i in range(N):
        atoms_v[i].pos, atoms[i].pos = a_to_v(v_array[i]), a_to_v(pos_array[i])

    #wtext(text = "\tCollision time tau = " + "{:.4e}" .format(tau) + " s.\n\n")
    #wtext(text = "\tReal Drift Velocity = " + "{:.4f}" .format(vv.mag/(t/dt)) + " m/s.\n\n")
    #wtext(text = "\tTheoretical Drift Velocity = " + ":{:.4f}" .format(q*E*tau/m) + " m/s.\n\n")