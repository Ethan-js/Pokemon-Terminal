import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *
import threading
from worldmap import *
from pokefunctions import *

def fightscene(poke1,poke2,bigwindow):
    screensize = bigwindow.getmaxyx() 
    window = curses.newwin(screensize[0],screensize[1],0,0)
    screensize = window.getmaxyx() 
    allsprites = []
    curses.echo()
    curses.cbreak()
    window.keypad(1)

    refreshrate = threading.Thread(target=refresh, args=(window,0.05))
    refreshrate.daemon = True
    refreshrate.start()

    Poke1 = Pokemon(poke1.size[0],poke1.size[1],int(3*screensize[0]/5),int(3*screensize[1]/5),poke1.texts,window,allsprites,100,[])
    Poke2 = Pokemon(poke2.size[0],poke2.size[1],int(screensize[0]/5),int(1*screensize[1]/4),poke2.texts,window,allsprites,100,[])
    Poke1.hp_bar()
    Poke2.hp_bar()

    while Poke1.hp > 0 and Poke2.hp > 0:

        fire.act(Poke1,Poke2,allsprites)

        if Poke2.hp > 0:
            charge.act(Poke2,Poke1,allsprites)

    for sprite in allsprites:
        # sprite.alive = 0
        # sprite.hide()
        # allsprites.remove(sprite)
        del sprite

    window.erase()

    # del window

    # curses.nocbreak(); window.keypad(0); curses.echo()
    # curses.endwin()


# fightscene(pokemon((7,13),[hlowrld],100,[]),
#     pokemon((5,14),[tor],100,[]))

# fightscene(pokemon((5,14),[Hubert0,Hubert1],100,[]),
#     pokemon((5,14),[tor],100,[]))