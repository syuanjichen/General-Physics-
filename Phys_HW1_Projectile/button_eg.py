from vpython import *

"""
 1. 參數設定, 設定變數及初始值
"""
size = 10         # 木塊邊長
L = 200           # 地板長度
t = 0             # 時間
dt = 0.01         # 時間間隔
re = False        # 重置狀態
running = False   # 物體運動狀態
end = False       # 程式是否結束

"""
 2. 畫面及函式設定
"""
# 初始畫面設定
scene = canvas(title="1D Motion\n\n", width=800, height=400, x=0, y=0,
               center=vec(0, 5, 0), background=vec(0, 0.6, 0.6))
scene.caption = "\n"
floor = box(pos=vec(0, 0, 0), size=vec(L, 0.1*size, 0.5*L), color=color.blue)
cube = box(pos=vec(0, 0.55*size, 0), size=vec(size, size, size), v=vec(0, 0, 0), color=color.red)

gd = graph(title="<i>x</i>-<i>t</i> plot", width=600, height=450, x=0, y=400,
           xtitle="<i>t</i> (s)", ytitle="<i>x</i> (cm)", fast=False)
gd2 = graph(title="<i>v</i>-<i>t</i> plot", width=600, height=450, x=0, y=850,
            xtitle="<i>t</i> (s)", ytitle="<i>v</i> (c  m/s)", ymin=-6.0, ymax=6.0, fast=False)
xt = gcurve(graph=gd, color=color.red)
vt = gcurve(graph=gd2, color=color.red)

# 執行按鈕
def run(b1):
    global running
    running = not running
    if running: b1.text = "Pause"
    else: b1.text = "Run"
    
b1 = button(text="Run", pos=scene.title_anchor, bind=run)

# 重置按鈕
def reset(b2):
    global re
    re = not re
    
b2 = button(text="Reset", pos=scene.title_anchor, bind=reset)

# 重置用, 初始化
def init():
    global re, running
    cube.pos = vec(0, size*0.55, 0)
    cube.v.x = vslider.value   
    t = 0
    xt.delete()
    vt.delete()
    re = False
    running = False
    b1.text = "Run"

# 停止按鈕
def stop(b3):
    global end
    end = not end
    
b3 = button(text="Stop Program", pos=scene.title_anchor, bind=stop)

# 設定速度滑桿
def setv(vslider):
    cube.v.x = vslider.value
    vtext.text = '{:1.1f} cm/s'.format(vslider.value)
    
vslider = slider(min=-5.0, max=5.0, value=1.0, length=200, bind=setv, right=15,
                 pos=scene.title_anchor)
vtext = wtext(text='{:1.1f} cm/s'.format(vslider.value), pos=scene.title_anchor)
cube.v.x = vslider.value

# 更新狀態
def update():
    global t
    rate(1000)
    cube.pos += cube.v*dt
    xt.plot(pos=(t, cube.pos.x))
    vt.plot(pos=(t, cube.v.x))
    t += dt

"""
 3. 主程式
"""
while not end:
    if (cube.pos.x <= -L*0.5+size*0.5 and cube.v.x < 0) or (cube.pos.x >= L*0.5-size*0.5 and cube.v.x > 0): cube.v.x = 0
    if running: update()
    if re: print("Reset"); init()

print("Stop Program")