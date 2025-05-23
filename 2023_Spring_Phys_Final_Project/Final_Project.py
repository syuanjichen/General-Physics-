from vpython import *
import numpy as pd

#基本數據
t, dt = 0, 1E-3             # 時間間距 0.001s
frameCount = 0              # 記錄幀數

#液體、氣體、熱源基本內容
height, width = 60, 40      # 液體高度和寬度分別切為 300 和 200 等分
heightN, widthN = 30, 20    # 液體總高度和寬度
C_liquid, C_air = 1.00, 3.1E-7             # 水的比熱(非必要)
Temp_Liq, Temp_Air, Temp_Heat = 25, 25, 100  # 液體、空氣、水的起始溫度
liquid_Array = pd.zeros((height,width))     # 液體
liquid_Array[0:, 0:] = Temp_Liq             # 液體溫度

#光學部分
n_air = 1.000293        # 空氣折射率
delta_n = -2.75E-4      # 折射率變化率(C^-1)
c = 0.02                # 光速
phi = -pi/4             # 入射角
light_pos = pd.array([-1, -1])    # 記錄光線前一刻在液體中的位置

# 畫面設置
scene = canvas(width=600, height=600,align = 'left', background=vector(245/255, 231/255, 193/255))
scene.background = vector(245/255, 231/255, 193/255)
Heater = box(pos = vec(0, -16, 0), axis = vec(0, 0, 1), size = vec(50, 2, 50), color = vec(222/255, 222/255, 222/255))
Left_wall = box(pos = vec(-10, 0, 0), axis = vec(0, 0, 1), size = vec(0.2, 30, 0.2), color = vec(0.9, 0.9, 0.9), opacity=0.8)
Right_wall = box(pos = vec(10, 0, 0), axis = vec(0, 0, 1), size = vec(0.2, 30, 0.2), color = vec(0.9, 0.9, 0.9), opacity=0.8)
Screen = box(pos = vec(20, 0, 0), axis = vec(0, 0, 1), size = vec(10, 30, 0.1), color = color.white)

def refrectionRate(x, y):
    # print(x, y)
    rate = 1.337+delta_n*liquid_Array[y][x]
    # print(rate)
    return rate
def generateLight(light_pos, theta):
    n_now = 1.000293        # 目前光線所在位置的折射率
    alpha = theta
    light = sphere(pos = vec(-20, 20, 0), size = vec(0.5, 0.5, 0.5), color = color.red, make_trail = True, \
                   trail_radius = 0.05, trail_color = color.black)
    while(True):
        light_pos_t = pd.array([(light.pos.x + 10) // (widthN / width), (light.pos.y + 15) // (heightN / height)])
        # print(int(light_pos_t[0]), int(light_pos_t[1]))
        light.v = c * vec(cos(theta), sin(theta), 0)
        light.pos += light.v * dt
        if light.pos.y <= -15:
            return
        if -10 <= light.pos.x <= 10:
            if light_pos_t.all() != light_pos.all():
                light_pos = light_pos_t.copy()
                theta = asin(n_now * sin(theta) / refrectionRate(int(light_pos_t[0]), int(light_pos_t[1])))
                n_now = refrectionRate(int(light_pos_t[0]), int(light_pos_t[1]))
                # print(theta)
        elif light.pos.x >10:
            light.v = c * vec(cos(alpha), sin(alpha), 0)
            while light.pos.x <= 20:
                light.pos += light.v * dt
            print(light.pos.y)
            return
        # if(light.pos.y < 15):
        #     angle_in = acos(abs(vector.dot(light.v, vector(0, 1, 0))/c))
        #     angle_out = asin(1.0 * sin(angle_in) / 1.35)
        #     theta = -pi/2 + angle_out
        #     light.v = c * vector(cos(theta), sin(theta), 0)

# 用小方塊表示液體
particles = []
for i in range(width):
    row = []
    for j in range(height):
        particle = box(pos=vector(-10 + 0.5 * widthN / width + i * widthN / width, -15 + j * heightN / height, 0), \
                       size=vec(heightN / height, widthN / width, 0.2), color = vec(j / height, j / height, j / height), \
                       opacity = 0.2)
        row.append(particle)
    particles.append(row)

# 溫度用灰階呈現，介於空氣與熱源之間
def showParticle():
    rc, gc, bc, crange= Temp_Heat, (Temp_Heat + Temp_Air) / 2, Temp_Air, (Temp_Heat - Temp_Air) / 2
    for i in range(width):
        for j in range(height):
            particles[i][j].color = vector(1, 1, 1) - vector(min(1, abs(liquid_Array[j][i] - rc) / crange),
                                                              min(1, abs(liquid_Array[j][i] - gc) / crange),
                                                                min(1, abs(liquid_Array[j][i] - bc) / crange))

# 液體進行熱平衡
# 平衡方式：周遭與本身的平均
def TherEqui():
    # 先處理邊界
    # 特例：左上角和右上角
    liquid_Array[height - 1][0] = (liquid_Array[height - 1][0] + liquid_Array[height - 1][1] + \
                                  liquid_Array[height - 2][0] + Temp_Air * C_air * 2) / (C_liquid * 3 + C_air * 2)
    liquid_Array[height - 1][width - 1] = (liquid_Array[height - 1][width - 1] + liquid_Array[height - 1][width - 2] + \
                                  liquid_Array[height - 2][width - 1] + Temp_Air * C_air * 2) / (C_liquid * 3 + C_air * 2)
    # 邊上的質點
    # 液體上部表面
    for i in range(1, width - 1):
        liquid_Array[0][i] = Temp_Heat
        liquid_Array[height - 1][i] = (liquid_Array[height - 1][i] + liquid_Array[height - 1][i - 1] + \
                                  liquid_Array[height - 1][i + 1] + liquid_Array[height - 2][i] + \
                                  Temp_Air * C_air) / (C_liquid * 4 + C_air)
    # 液體左右表面
    for i in range(1, height - 1):
        liquid_Array[i][0] = (liquid_Array[i][0] + liquid_Array[i - 1][0] + \
                                  liquid_Array[i + 1][0] + liquid_Array[i][1] + \
                                  Temp_Air * C_air) / (C_liquid * 4 + C_air)
        liquid_Array[i][width - 1] = (liquid_Array[i][width - 1] + liquid_Array[i - 1][width - 1] + \
                                  liquid_Array[i + 1][width - 1] + liquid_Array[i][width - 2] + \
                                  Temp_Air * C_air) / (C_liquid * 4 + C_air)
    # 處理液體內部
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            liquid_Array[i][j] = (liquid_Array[i][j] + liquid_Array[i][j - 1] + \
                                  liquid_Array[i][j + 1] + liquid_Array[i - 1][j] + \
                                  liquid_Array[i + 1][j]) / 5
generateLight(light_pos, phi)
while True:
    t += dt             #時間進行
    frameCount += 1     # 數幀數
    TherEqui()          # 進行熱平衡
    # print(liquid_Array[30][20]) # 液體正中央溫度
    if frameCount % 200 == 0:   # 每0.2秒(200幀)更新一次液體顯示
        showParticle()
    if frameCount % 1000 == 0:  # 每一秒(1000幀)發出一道光線
        generateLight(light_pos, phi)