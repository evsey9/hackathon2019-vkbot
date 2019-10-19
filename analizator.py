import commander
import speech2text
import config as cc
import sys
import signal
import os
import pyautogui
from subprocess import check_output

# def get_pid(name):
#     return map(int,check_output(["pidof",name]).split())
#
#

#
# def blacktheme():
#     os.rename('active.png','gw.png')
#     os.rename('gb.png','active.png')
# os.kill(get_pid('ImageToDesktop.exe'),signal.CTRL_C_EVENT)

#def move2dir(kl,n):
""" kx = cc.xc =
    ky =
    if kl == "вверх":
            pyautogui.moveTo(cc.xc, )
            cc.yc
    elif kl == "вниз":
            pyautogui.move(cc.xc, k)
    elif kl == "вправо":
            pyautogui.move(k, 0)
    elif kl == "влево":
            pyautogui.move(-k, 0)
"""

commander.move2cords(1,'a')
#os.system(r'C:\Users\1\Desktop\i2i\ImageToDesktop')
while True:
    out = (speech2text.S2T.main())
    print(out)
    out = out.lower()
    if 'клик' in out:
        if 'двойной' in  out:
            commander.doubleclick()
        else:
            commander.click()

    if 'клет' in out:
        n = 0
        for i in out.split():
            if i.isdigit():
                n = i
        kl = 0
        k = out.split()
        for i in k:
            if i in commander.dirs:
                kl = i
        print(kl, n)
    elif 'мышь' in out:
            d = out.split()
            xy = d[-1]
            x = str()
            y = str()
            for i in xy:
                if i.isdigit():
                    x+=i
                else:
                    y+=i
            x = int(x)
            commander.move2cords(x,y)
    elif 'листать' in out:
        n = 0
        for i in out.split():
            if i.isdigit:
                n = i
        kl = str()
        td = False
        for i in out.split():
            if i in commander.dirs[2:4]:
                kl = i
            else:
                break
        else:
            continue
        commander.scroll(n,kl)
    elif 'печат' in out:
        text = ''
        for i in out.split()[1:]:
            if not i.isdigit():
                text.join(i + ' ')
            else:
                text.join(str(i) + ' ')

        commander.write(text)
    elif 'нажать' in out:
        key = out.split()
        for i in key:
            if i in commander.keys:
                key = i
        commander.presskey(key)
    elif 'закрыть' in out:
        commander.closewindow()
    elif 'открыть' in out:
        wind = out.split()
        for i in wind:
            if i in commander.progs or i in commander.ruprogrs:
                wind = commander.prdict[i]
        commander.openwindow(wind)

