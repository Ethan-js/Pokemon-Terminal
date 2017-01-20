import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *
import threading
from worldmap import *
from pokefunctions import *
from mapfunctions2 import *
from world2 import *

def intro(window):
    allsprites = []
    # curses.echo()
    # curses.cbreak()
    # window.keypad(1)
    refreshrate = spin(refreshonce,(window,0.05))
        
    Hubert = Sprite(3,0,[Hubert0,Hubert1],window,allsprites)
    Speak(Hubert,"Hello! My name is Hubert. Welcome to this cool adventure!",offset=-2)
    Speak(Hubert,"This is a game of wit and skill.",offset=-2)
    Hubert.alive = 0
    allsprites.remove(Hubert)
    del Hubert
    Ghostsprite = Sprite(3,0,[ghost],window,allsprites)
    Speak(Ghostsprite,"Boo! I am a scary ghost.",offset=-2)
    Hubert = Sprite(3,14,[SadHubert0,SadHubert1],window,allsprites)
    Speak(Hubert,"Oh no! I am being kidnapped by the scary ghost!",offset=-2)
    Speak(Hubert,"Here, take this POKEMON and fight the ghost!",offset=-2)
    hwsprite = Sprite(3,17,[hlowrld],window,allsprites)
    hwsprite.to_b(16,60)
    ScrollText(30,30,"You have received your first POKEMON!",JustText,window)
    Speak(Hubert,"This is HloWrld, my favourite POKEMON! It knows one FUNCTION, fire([target]).",offset=-2)
    Speak(Hubert,"Duel the ghost, and use fire()!",offset=-2)

    for sprite in allsprites:
        sprite.clear()
    allsprites.clear()
    refreshrate.alive = False
    curses.endwin()


Player1 = playerclass([pokemon([hlowrld],45,45,["fire","charge"],"Hlowrld",1,"fire")],{"Items":{"Pokeballs":{},"Potions":{},"Clothes":{}},"Exit":{}})  

# curses.wrapper(intro)
# fightscene(pokemon([hlowrld],100,100,["fire"],"Hlowrld",1,"fire"),
#      pokemon([ghost],120,120,["charge"],"Ghost",10,"ghost"),Player1)  

while True:
    a,b,y,x,fight,pokes = curses.wrapper(makemap,a,b,y,x,Player1)
    if fight == 1:
        fightscene(pokes[0],pokes[1],Player1)


