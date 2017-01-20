import time
import curses
import curses.textpad, curses.panel
from helpers import *
from sprites import *
import threading
import sys
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=100))

def pbar(window):
    allsprites = []
    screen = curses.initscr()
    refreshrate = threading.Thread(target=refresh, args=(window,0.05))
    refreshrate.daemon = True
    refreshrate.start()
    worldmap = curses.newpad(1000,1000)

    Hubert = Sprite(5,14,3,0,[Hubert0,Hubert1],window,allsprites)
    while True:
        move = window.getch()
        Speak(Hubert,str(dir(worldmap).keys()[0]),offset=-2)
        screen.refresh()
        time.sleep(0.5)
    time.sleep(3)

curses.wrapper(pbar)