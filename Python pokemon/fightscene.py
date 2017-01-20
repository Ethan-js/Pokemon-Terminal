import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *
import threading
from worldmap import *
from pokefunctions import *
import re
from bag import *
import random
import copy

def fightscene(poke1,poke2,player):
    def scene(window):
        window.clear()
        screensize = window.getmaxyx()
        allpanels = []
        allsprites = []
        # curses.echo()
        # curses.cbreak()
        # window.keypad(1)

        refreshrate = spin(refreshonce,(window,0.05))

        Poke1 = Pokemon(int(3*screensize[0]/5),int(3*screensize[1]/5),poke1,window,allsprites,allpanels)
        Poke2 = Pokemon(int(screensize[0]/5),int(1*screensize[1]/4),poke2,window,allsprites,allpanels)
        Poke1.hp_bar()
        Poke2.hp_bar()

        exec(poke1.name + "= Poke1")
        exec(poke2.name + "= Poke2")

        caught = False
        flee = False
        player_poke = None
        while Poke1.poke.hp > 0 and Poke2.poke.hp > 0 and caught == False and player_poke == None and flee == False:
            move = my_raw_input(20,20,"What should " + Poke1.poke.name + " do?          ",window)
            while move == "":
                move = my_raw_input(20,20,"What should " + Poke1.poke.name + " do?          ",window)
            if move == "bag()":
                for panel in allpanels:
                    panel.hide()
                window.erase()
                refreshrate.alive = False
                window.touchwin()
                window.refresh()
                bagmenu = menu(player.bag,window) 
                if bagmenu.returnval == "pokeball":
                    player.pokemon.append(copy.deepcopy(poke2))
                    window.addstr(20,20,"You caught a " + poke2.name + "!")
                    caught = True
                refreshrate = spin(refreshonce,(window,0.05))
            elif move == "flee()":
                flee = True
            else:
                try:
                    fcn = re.match("[a-z]*",move).group()
                    move1 = fcn + ".act(Poke1," + re.search("\((.*?)\)",move).group()[1:-1] + ",allsprites)"
                    if fcn in Poke1.poke.functions:
                        window.erase()
                        window.addstr(20,20,poke1.name + " used " + fcn + "!")
                        exec(move1)
                        window.erase()
                    elif fcn == "switch":
                        choice = re.search("\((.*?)\)",move).group()[1:-1]
                        for member in player.pokemon:
                            if member.name == choice and member.hp > 0:
                                player_poke = member
                                break
                    else:
                        window.erase()
                        window.addstr(20,20,poke1.name + " doesn't know this move!")
                        time.sleep(1)
                        window.erase()
                except:
                    window.erase()
                    window.addstr(20,20,poke1.name + " doesn't know this move!")
                    time.sleep(1)
                    window.erase()  


            time.sleep(1)

            if Poke1.poke.hp > 0 and Poke2.poke.hp > 0 and move != "bag()":
                poke2move = random.choice(poke2.functions)
                window.addstr(20,20,poke2.name + " used " + poke2move + "!             ")
                exec(poke2move + ".act(Poke2,Poke1,allsprites)")


        if Poke2.poke.hp <= 0 or caught == True:
            window.addstr(20,20,poke1.name + " earned 100xp!")
            time.sleep(1)
            poke1.xp += 100
            if poke1.set_level() > 0:
                window.erase()
                window.addstr(20,20,poke1.name + " leveled up!")
                poke1.hp = poke1.hpmax
                time.sleep(1)

        if Poke1.poke.hp <= 0:
            for teammember in player.pokemon:
                if teammember.hp > 0:
                    player_poke = teammember
                    break

        time.sleep(1)

        refreshrate.alive = False
        allsprites.clear()
        window.erase()
        return player_poke

    player_poke = curses.wrapper(scene) 
    if player_poke != None:
        fightscene(player_poke,poke2,player)

# fightscene(pokemon((7,13),[hlowrld],100,[]),
#     pokemon((5,14),[tor],100,[]))

# fightscene(pokemon((5,14),[Hubert0,Hubert1],100,[]),
#     pokemon((5,14),[tor],100,[]))