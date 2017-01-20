import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *
import threading
from worldmap2 import *
from fightscene import *
from mapfunctions2 import *

# def pbar(stdscr):

y = 0
x = 0
a = 0
b = 0

def makemap(stdscr,a,b,y,x,Player1):
    allsprites = []
    screensize = stdscr.getmaxyx()
    worldmap = curses.newpad(1000,1000)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    # for y1 in range(len(worldmap2.split("\n"))):
    #     for x1 in range(len(worldmap2.split("\n")[y1])):
    #         if x1 + 1 < len(worldmap2.split("\n")[y1]) and worldmap2.split("\n")[y1][x1] == "\ "[:-1] and (worldmap2.split("\n")[y1][x1+1] == "|" or worldmap2.split("\n")[y1][x1+1] == "*"):
    #             worldmap.addch(y1,x1,worldmap2.split("\n")[y1][x1],curses.color_pair(47))
    #         elif worldmap2.split("\n")[y1][x1] == "*":
    #             worldmap.addch(y1,x1,worldmap2.split("\n")[y1][x1],curses.color_pair(47))
    #         elif x1 > 0 and worldmap2.split("\n")[y1][x1] == "/ "[:-1] and (worldmap2.split("\n")[y1][x1-1] == "|" or worldmap2.split("\n")[y1][x1-1] == "*"):
    #             worldmap.addch(y1,x1,worldmap2.split("\n")[y1][x1],curses.color_pair(47))
    #         else:
    #             worldmap.addch(y1,x1,worldmap2.split("\n")[y1][x1],curses.color_pair(5))
    worldmap.addstr(0,0,worldmap2)
    Hubert = Sprite(int((screensize[0]-1)/2),int((screensize[1]-1)/2),[playersprite],stdscr,allsprites)
    # refreshpad(worldmap,y,x,stdscr)
    # move_sprites(Hubert,stdscr,a,b)
    a,b,y,x,fight,pokes = get_move(worldmap,y,x,a,b,Hubert,stdscr,Player1)
    for sprite in allsprites:
        sprite.clear()
    allsprites.clear()
    del worldmap
    curses.panel.update_panels()
    curses.doupdate()
    stdscr.refresh()
    curses.endwin()
    return a,b,y,x,fight,pokes


# while True:
#     a,b,y,x,fight,pokes = curses.wrapper(makemap,a,b,y,x)
#     if fight == 1:
#         fightscene(pokes[0],pokes[1])

# move = threading.Thread(target=get_move, args=(worldmap,y,x,Hubert,stdscr))
# move.daemon = True
# move.start()