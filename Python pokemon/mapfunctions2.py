import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *
import threading
# from worldmap2 import *
from fightscene import *
import random
from math import ceil, floor
import copy
from map_gen1 import *
no_walk = [tree]
wild_poke = [pokemon([tor],45,45,["charge"],"Tor",1,"normal"), pokemon([sn8k],35,35,["venom"],"Sn8k",1,"poison"), pokemon([raindeer],50,50,["charge","rain"],"Raindeer",1,"water")]
scene_panels = []


def can_move_down(y,x,a,b,window,mat):
    screensize = window.getmaxyx()
    if deco_list[int(mat[y+a+ceil(screensize[0]/2)+5,x+b+ceil(screensize[1]/2)-1])] in no_walk:
        return False
    else:
        return True
def can_move_up(y,x,a,b,window,mat):
    screensize = window.getmaxyx() 
    try:
        if worldmap2.split("\n")[y+a+ceil(screensize[0]/2)-2][x+b+ceil(screensize[1]/2)] in no_walk:
            return False
        elif worldmap2.split("\n")[y+a+ceil(screensize[0]/2)-2][x+b+ceil(screensize[1]/2)-1] in no_walk:
            return False
        elif worldmap2.split("\n")[y+a+ceil(screensize[0]/2)-2][x+b+ceil(screensize[1]/2)+1] in no_walk:
            return False
        elif worldmap2.split("\n")[y+a+ceil(screensize[0]/2)-2][x+b+ceil(screensize[1]/2)+2] in no_walk:
            return False
        else:
            return True
    except:
        return True
def can_move_left(y,x,a,b,window,mat):
    screensize = window.getmaxyx() 
    try:
        if worldmap2.split("\n")[y+a+ceil(screensize[0]/2)-1][x+b+ceil(screensize[1]/2)-2] in no_walk:
            return False
        elif worldmap2.split("\n")[y+a+ceil(screensize[0]/2)][x+b+ceil(screensize[1]/2)-2] in no_walk:
            return False
        else:
            return True
    except:
        return True
def can_move_right(y,x,a,b,window,mat):
    screensize = window.getmaxyx() 
    if deco_list[int(mat[y+a+ceil(screensize[0]/2)+4,x+b+ceil(screensize[1]/2)])] in no_walk:
        return False
    else:
        return True

def get_move(pad,y,x,a,b,Hubert,window,Player1):
    prob = 0.035
    # prob = 0
    # prob = 0.5
    screensize = window.getmaxyx() 
    move_sprites(Hubert,window,a,b)
    refreshpad(pad,y,x,window)
    move_sprites(Hubert,window,a,b)
    curses.doupdate()
    while True:
        move = window.getch()
        if move == curses.KEY_DOWN or move == curses.KEY_UP or move == curses.KEY_LEFT or move == curses.KEY_RIGHT:
            special_move(y,x,a,b,window,Player1)
            try:
                if random.random() > (1-prob) and worldmap2.split("\n")[y+a+int(screensize[0]/2)+3][x+b+int(screensize[1]/2)+6]=="*":
                    player_poke = None
                    for teammember in Player1.pokemon:
                        if teammember.hp > 0:
                            player_poke = teammember
                            break
                    enemy_poke = copy.deepcopy(random.choice(wild_poke))
                    if player_poke:
                        while enemy_poke.name in [teammember.name for teammember in Player1.pokemon]:
                            for team_poke in Player1.pokemon:
                                if team_poke.name == enemy_poke.name:
                                    enemy_poke.name = "wild_" + enemy_poke.name
                        scene_panels.clear()
                        return a,b,y,x,1,[player_poke,enemy_poke]
            except:
                pass
        if move == curses.KEY_DOWN:
            if can_move_down(y,x,a,b,window,map_matrix):
                if a < 0:
                    a += 1
                else:
                    y += 1
                    a = 0
                if Hubert.texts == [playersprite6]:
                    Hubert.change_panels([playersprite7])
                else:
                    Hubert.change_panels([playersprite6])
                move_sprites(Hubert,window,a,b)
                scene_panels = map_panels_below(window,map_matrix,y,x,a,b)
                refreshpad(pad,y,x,window)
                move_sprites(Hubert,window,a,b)
                # for panel in [pair[1] for pair in scene_panels]:
                #     panel.top()
        if move == curses.KEY_UP:
            if can_move_up(y,x,a,b,window,map_matrix):
                if y > 0:
                    y -= 1
                    a = 0
                else:
                    a -= 1
                if Hubert.texts == [playersprite4]:
                    Hubert.change_panels([playersprite5])
                else:
                    Hubert.change_panels([playersprite4])
                move_sprites(Hubert,window,a,b)
                scene_panels = map_panels_below(window,map_matrix,y,x,a,b)
                refreshpad(pad,y,x,window)
                move_sprites(Hubert,window,a,b)
                # for panel in [pair[1] for pair in scene_panels]:
                #     panel.top()
        if move == curses.KEY_LEFT:
            if can_move_left(y,x,a,b,window,map_matrix):
                if x > 0:
                    x -= 1
                    b = 0
                else:
                    b -= 1
                if Hubert.texts == [playersprite2]:
                    Hubert.change_panels([playersprite3])
                else:
                    Hubert.change_panels([playersprite2])
                move_sprites(Hubert,window,a,b)
                scene_panels = map_panels_below(window,map_matrix,y,x,a,b)
                refreshpad(pad,y,x,window)
                move_sprites(Hubert,window,a,b)
        if move == curses.KEY_RIGHT:
            if can_move_right(y,x,a,b,window,map_matrix):
                if b < 0:
                    b += 1
                else:
                    x += 1
                    b = 0
                if Hubert.texts == [playersprite]:
                    Hubert.change_panels([playersprite1])
                else:
                    Hubert.change_panels([playersprite])
                move_sprites(Hubert,window,a,b)
                scene_panels = map_panels_below(window,map_matrix,y,x,a,b)
                refreshpad(pad,y,x,window)
                move_sprites(Hubert,window,a,b)
        if move == curses.KEY_RESIZE:
            refreshpad(pad,y,x,window)
            move_sprites(Hubert,window,a,b)
        curses.panel.update_panels()
        curses.doupdate()

def move_sprites(sprite,window,a=0,b=0):
    screensize = window.getmaxyx()
    for panel in sprite.panels:
        panel.move(int((screensize[0]-1)/2)+a,int((screensize[1]-1)/2)+b)
    window.noutrefresh()
    curses.panel.update_panels()

def map_panels_below(window,mat,y,x,a,b):
    scene_panels.clear()
    screensize = window.getmaxyx()
    for i in range(y+a+ceil(screensize[0]/2)+4, y+a+int(screensize[0])):
        for j in range(x+b+5,x+b+ int(screensize[1])):
            if mat[i,j]:
                addition = deco_list[int(mat[i,j])]
                if addition in panels_list:
                    height = len(addition.split("\n"))
                    split_add = addition.split("\n")
                    for line_num in range(len(split_add)):
                        for ch_num in range(len(split_add[line_num])):
                            if split_add[line_num][ch_num] != " ":
                                if i-y-height+line_num-a < screensize[0]/2+4 and i-y-height+line_num-a >= floor(screensize[0]/2)-1 and screensize[1]/2-2 < j-x + ch_num-b and j-x+ch_num-b < screensize[1]/2+6:
                                    if split_add[line_num][ch_num] != "&":
                                        scene_panels.append(make_panel(i-y-height+line_num,j-x+ch_num,split_add[line_num][ch_num])[:2])
                                        # scene_panels[-1][0].addstr(0,0,"W")
                                    else:
                                        scene_panels.append(make_panel(i-y-height+line_num,j-x+ch_num," ")[:2])
    window.noutrefresh()
    curses.panel.update_panels()
    return scene_panels

def special_move(y,x,a,b,window,player):
    screensize = window.getmaxyx() 
    if (y+a+int(screensize[0]/2),x+b+int(screensize[1]/2)) in pokecenters:
        for poke in player.pokemon:
            poke.hp = poke.hpmax
        window.addstr(20,20,"Health restored!")
        window.refresh()
        time.sleep(1)   
    