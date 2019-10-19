import win32api
Displayheight = win32api.GetSystemMetrics(1)
Displaywidth = win32api.GetSystemMetrics(0)
sizepx = int(30)
# print(Displayheight,Displaywidth)
wmax = Displaywidth // sizepx
hmax = Displayheight // sizepx

xc = int(1)
yc = 'a'

x = 15
y = 15