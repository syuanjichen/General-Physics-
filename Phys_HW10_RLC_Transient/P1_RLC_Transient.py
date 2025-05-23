from vpython import*
fd = 120 # 120 Hz
R = 30 # 30 Ohms
L = 0.2 # 0.2 Henry
C = 2E-5 # 2E-5 Farad
t = 0
dt = 1.0/(fd * 5000) # 5000 simulation points per cycle
i_old = 0
i_new = 0
i_max_real = 0
i_phase_real = 0
i_max_t = 0
v_max_real = 0
v_max_t = 0
v_c = 0
E_0 = 0
step = 0

scene1 = graph(align = 'left', xtitle='t', ytitle='i (A) blue, v (100V) red,', background=vector(0.2, 0.6, 0.2))
scene2 = graph(align = 'left', xtitle='t', ytitle='Energy (J)', background=vector(0.2, 0.6, 0.2))
i_t = gcurve(color=color.blue, graph = scene1)
v_t = gcurve(color=color.red, graph = scene1)
E_t = gcurve(color=color.red, graph = scene2)

i_max_theo = 36.0/sqrt(R**2 + (2*pi*fd*L - 1.0/(2*pi*fd*C))**2)
i_phase_theo = -atan((2*pi*fd*L - 1.0/(2*pi*fd*C))/(R)) * 180 / pi
print("Theoretical Value: I = " + str(i_max_theo) +" A, phase = " + str(i_phase_theo) + " deg.")


def voltage(t):
    if t < 0:
        v = 0
        return v
    elif t >= 0 and t < 12/fd:
        v = 36 * sin(2*pi*fd*t)
        return v
    else:
        v = 0
        return v

while t <= 20.0/fd:
    t += dt
    v_c += i_old * dt / C
    i_old = i_new
    i_new = (voltage(t) + L*i_old/dt - v_c)/(R + dt/C + L/dt)
    E = 0.5 * (C * v_c ** 2 + L * i_new ** 2)
    i_t.plot(pos = (t, i_new))
    v_t.plot(pos = (t, voltage(t)/100))
    E_t.plot(pos = (t, E))

    if step == 0 and t >= 8.0 / fd and t <= 9.0 / fd:
        if i_new > i_max_real:
            i_max_real = i_new
            i_max_t = t
        if voltage(t) > v_max_real:
            v_max_real = voltage(t)
            v_max_t = t
        if t + dt > 9.0/fd:
            step = 1

    if step == 1: 
        i_phase_real = (v_max_t - i_max_t) * (180/pi) * (2*pi*fd)
        print("Real Value: I = " + str(i_max_real) + " A, phase = " + str(i_phase_real) + " deg.")
        step = 2

    if step == 2 and voltage(t) == 0 and voltage(t + dt) == 0:
        E_0 = E
        step = 3
    if step == 3 and t > 12.0/fd and E <= 0.1 * E_0:
        print("At t = " + str(t) + " s (" + str(t*fd) +"T), the total energy is 10 percent of the initial value E(t = 12T).")
        print("Decay time = " + str(t - 12.0/fd) + " s.")
        step = 4