import win32gui
import win32api
dc = win32gui.GetDC(0)
Displayheight = win32api.GetSystemMetrics(1)
Displaywidth = win32api.GetSystemMetrics(0)
sizepx = 30