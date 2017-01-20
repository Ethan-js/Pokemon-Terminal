import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *
import threading
from worldmap import *
from fightscene import *
from mapfunctions import *

# def pbar(stdscr):

y = 0
x = 0
a = 0
b = 0

def makemap(stdscr):


while True:

    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    curses.echo()
    allsprites = []

    screensize = stdscr.getmaxyx()
    worldmap = curses.newpad(1000,1000)
    for y1 in range(len(world)):
        for x1 in range(len(world[y1])):
            worldmap.addch(y1,x1,world[y1][x1])

    Hubert = Sprite(2,4,int((screensize[0]-1)/2),int((screensize[1]-1)/2),[Player],stdscr,allsprites)
    a,b,y,x,fight,pokes = get_move(worldmap,y,x,a,b,Hubert,stdscr)
    worldmap.refresh(0,0,0,0, 1,1)
    time.sleep(2)
    for sprite in allsprites:
        sprite.clear()
    allsprites = []
    stdscr.addstr(0,0,"")
    curses.endwin()
    # time.sleep(3)
    if fight == 1:
        fightscene(pokes[0],pokes[1])

# move = threading.Thread(target=get_move, args=(worldmap,y,x,Hubert,stdscr))
# move.daemon = True
# move.start()
