from numpy import*
from vpython import*

# Part 1 : Variables and constants
# ----------------------------------------
epsilon = 8.854E-12 #permittivity constant
delta = 1E-12       #Small error in solving PDE
execute_time = 0    #The number of execution in solving PDE
N = 101             #Number of grids on x and y axis (0 ~ 100)
h = 1E-2 / (N - 1)  #One unit grid distance
L = 4E-3            #Length of the capacitor plates
d = 1E-3            #Distance between two plates
flux_top = 0        #Electric Flux including top plate
V0 = 200            #Voltage difference between two plates
# ----------------------------------------

# Part 2 : Laplace Equation Solver
# ----------------------------------------
def solve_laplacian(u, u_cond):
    global execute_time
    run = True
    V = array(u)
    while (run):
        V_prev = array(V)
        V[u_cond] = u[u_cond]
        V[1:-1, 1:-1] = (V[:-2, 1:-1] + V[2:, 1:-1] + V[1:-1, :-2] + V[1:-1, 2:])/4
        execute_time += 1
        run = False
        for i in range (N):
            for j in range (N):
                if(abs(V[i, j] - V_prev[i, j]) > delta):
                    run = True
                    break
    print("Run " + str(execute_time) + " times to reach equilibrium.")
    return V
# ----------------------------------------

# Part 3 : Calculate Electric Field
# ----------------------------------------
def get_field(V, h):
    Ex, Ey = gradient(V)
    Ex, Ey = -Ex/h, -Ey/h
    return Ex, Ey
# ----------------------------------------

# Part 4 : Calculate Flux of the top plate
# ----------------------------------------
def get_flux(Ex, Ey, h):
    phi = 0
    for i in range (left_pos - 5, right_pos + 5):                        #x from 25 to 75
        for j in range (int((top_pos + bottom_pos)/2), top_pos + 5):     #y from 50 to 60
            phi += (Ex[i, j] - Ex[i - 1, j]) * h * 1
            phi += (Ey[i, j] - Ey[i, j - 1]) * h * 1
    return phi
# ----------------------------------------

# Part 5 : Define Grids and the range of the capacitor
# ----------------------------------------
u = zeros([N, N])
left_pos = int(N/2) - int(L/h/2.0)       #50 - 20 = 30
right_pos = int(N/2) + int(L/h/2.0)      #50 + 20 = 70
top_pos = int(N/2) + int(d/h/2.0)        #50 +  5 = 55
bottom_pos = int(N/2) - int(d/h/2.0)     #50 -  5 = 45
# ----------------------------------------

# Part 6 : Set Voltages of the plates and other grid points
# ----------------------------------------
u[left_pos : right_pos, top_pos] = V0/2
u[left_pos : right_pos, bottom_pos] = -V0/2
u_cond = not_equal(u, 0)
# ----------------------------------------

# Part 7 : Calculate Voltage and Electric Field
# ----------------------------------------
V = solve_laplacian(u, u_cond)
Ex, Ey = get_field(V, h)
# ----------------------------------------


# Part 8 : Calculate Flux, charge, and capacitance
# ----------------------------------------
flux_top = get_flux(Ex, Ey, h)
charge_top = epsilon * flux_top
C_nonideal = charge_top / V0
C_ideal = epsilon * L * 1.0 / d
# ----------------------------------------

# Part 9 : Print the result on the terminal
# ----------------------------------------
print("Charge_top = " + str(charge_top) + " C.")
print("C_nonideal = " + str(C_nonideal) + " farad.")
print("C_ideal = " + str(C_ideal) + " farad.")
print("C_nonideal / C_ideal = " + str(C_nonideal / C_ideal) + ".")
# ----------------------------------------

# Part 10 : Set up the window
# ----------------------------------------
scene = canvas(title = 'Non-ideal capacitor', height = 1000, width = 1000, center = vec(N * h/2, N * h/2, 0), align = 'left')
scene.lights = []
scene.ambient = color.gray(0.99)
box(pos = vec(N * h/2, N * h/2 - d/2 - h, 0), length = L, height = h/5, width = h)
box(pos = vec(N * h/2, N * h/2 + d/2 - h, 0), length = L, height = h/5, width = h)


for i in range (N):
    for j in range (N):
        point = box(pos = vec(i * h, j * h, 0), length = h, height = h, width = h / 10, color = vec((V[i, j] + 100)/200, (100 - V[i, j])/200, 0.0))

for i in range(0, N):
    for j in range(0, N):
        ar = arrow(pos = vec(i * h, j * h, h / 10), axis = vec(Ex[i, j]/ 2E9, Ey[i, j]/2E9, 0), shaftwidth = h / 6.0, color = color.black)
# ----------------------------------------

# Part 11 : Print the result on the window
# ----------------------------------------
wtext(text = "  Run " + str(execute_time) + " times to reach equilibrium.\n\n", pos = scene.caption_anchor)
wtext(text = "  Charge of top plate = " + str(charge_top) + " C.\n\n", pos = scene.caption_anchor)
wtext(text = "  Capacitance of nonideal capacitor = " + str(C_nonideal) + " F.\n\n", pos = scene.caption_anchor)
wtext(text = "  Capacitance of ideal capacitor = " + str(C_ideal) + " F.\n\n", pos = scene.caption_anchor)
wtext(text = "  C_nonideal / C_ideal = " + str(C_nonideal/C_ideal) + ".\n\n", pos = scene.caption_anchor)
# ----------------------------------------