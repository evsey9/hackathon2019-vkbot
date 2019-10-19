import pyautogui
import config as cc
keys = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
progs = ['chrome','notepad']
ruprogrs = ['хром', 'блокнот']
prdict ={'хром':'chrome','блокнот':'notepad','chrome':'chrome','notepad':'notepad'}
alphcor = (chr(z) for z in range(ord('a'),(ord('z') + 1)))
alphabet = {chr(x): y for x, y in zip(range(ord('a'),(ord('z') + 1)), range(1,28))}
dirs = ('влево','вправо','вверх','вниз')
exept = {'а':'a', 'б':"b",'ц':'c','д':'d','и':'e','ф':'f','м':'m','н':'n','р':'r','с':'s','з':'z','о':'o'}
rusalphabet = [chr(x) for x in range(ord('а'),(ord('я')+1))]
def y2num(y):
    if y in rusalphabet:
        y = exept[y]
    k = 0
    k1 = 0
    for i in reversed(y):
        k += alphabet[i] * 27 ** k1
        k1 += 1
    return k


    #speechcomand == 'Мышь на x,y'
def move2cords(x:int, y):
    y1 = y2num(y)
    cc.y = ((y1-1) * cc.sizepx) + (cc.sizepx // 2)
    cc.x = ((x-1) * cc.sizepx) + (cc.sizepx // 2)
    cc.xc = x
    cc.yc = y
    pyautogui.moveTo(cc.x, cc.y)


    # speechcomand == 'Мышь на n клеток dir'
def move2dir(n:int, kl):
    if kl == "вверх":
            pyautogui.move(None, -15 * n)
    elif kl == "вниз":
            pyautogui.move(None, 15 * n)
    elif kl == "вправо":
            pyautogui.move(15*n , None)
    elif kl == "влево":
            pyautogui.move(-15*n , None)


    # speechcomand == 'Клик'
def click():
    pyautogui.click()
    #def rightclick():


    # speechcomand == 'ДвойнойКлик'
def doubleclick():
    pyautogui.doubleClick()


    # speechcomand == 'Листать dir на n'
def scroll(n:int,kl):
    if kl == 'вниз':
        pyautogui.scroll(-n)
    elif kl == 'вверх':
        pyautogui.scroll(n)


    # speechcomand == 'Печатать text'
def write(text):
    pyautogui.typewrite(text, interval=0.25)


    # speechcomand == 'Нажать key'
def presskey(key):
    pyautogui.press(key)


    # speechcomand == 'Нажать клавиши *keys'
def pressHotKey(*keys):
    pyautogui.hotkey(*keys)


    # speechcomand == 'Закрыть окно'
def closewindow():
    pyautogui.hotkey('alt','f4')


    # speechcomand =='Открыть wind'
def openwindow(wind):
    pyautogui.hotkey('win', 'r')
    pyautogui.typewrite(wind)
    pyautogui.press('enter')

write('привет')
move2dir(5,'вправо')