import curses
import curses.panel
import time
import threading
from sprites import *
from math import ceil, floor
import random
import copy

type_chart = {"normal" : {"normal":1,"fire":1,"water":1,"electric":1,"grass":1,"ice":1,"fighting":1,"poison":1,"ground":1,"flying":1,"psychic":1,"bug":1,"rock":0.5,"ghost":0,"dragon":1,"dark":1,"steel":0.5,"fairy":1},
"fire" : {"normal":1,"fire":0.5,"water":0.5,"electric":1,"grass":2,"ice":2,"fighting":1,"poison":1,"ground":1,"flying":1,"psychic":1,"bug":2,"rock":0.5,"ghost":1,"dragon":0.5,"dark":1,"steel":2,"fairy":1},
"water" : {"normal":1,"fire":2,"water":0.5,"electric":1,"grass":0.5,"ice":1,"fighting":1,"poison":1,"ground":2,"flying":1,"psychic":1,"bug":1,"rock":2,"ghost":1,"dragon":0.5,"dark":1,"steel":1,"fairy":1},
"electric" : {"normal":1,"fire":1,"water":2,"electric":0.5,"grass":0.5,"ice":1,"fighting":1,"poison":1,"ground":0,"flying":2,"psychic":1,"bug":1,"rock":1,"ghost":1,"dragon":0.5,"dark":1,"steel":1,"fairy":1},
"grass" : {"normal":1,"fire":0.5,"water":2,"electric":1,"grass":0.5,"ice":1,"fighting":1,"poison":0.5,"ground":2,"flying":0.5,"psychic":1,"bug":0.5,"rock":2,"ghost":1,"dragon":0.5,"dark":1,"steel":0.5,"fairy":1},
"ice" : {"normal":1,"fire":0.5,"water":0.5,"electric":1,"grass":2,"ice":0.5,"fighting":1,"poison":1,"ground":2,"flying":2,"psychic":1,"bug":1,"rock":1,"ghost":1,"dragon":2,"dark":1,"steel":0.5,"fairy":1},
"fighting" : {"normal":2,"fire":1,"water":1,"electric":1,"grass":1,"ice":2,"fighting":1,"poison":0.5,"ground":1,"flying":0.5,"psychic":0.5,"bug":0.5,"rock":2,"ghost":0,"dragon":1,"dark":2,"steel":2,"fairy":0.5},
"poison" : {"normal":1,"fire":1,"water":1,"electric":1,"grass":2,"ice":1,"fighting":1,"poison":0.5,"ground":0.5,"flying":1,"psychic":1,"bug":1,"rock":0.5,"ghost":0.5,"dragon":1,"dark":1,"steel":0,"fairy":2},
"ground" : {"normal":1,"fire":2,"water":1,"electric":2,"grass":0.5,"ice":1,"fighting":1,"poison":2,"ground":1,"flying":0,"psychic":1,"bug":0.5,"rock":2,"ghost":1,"dragon":1,"dark":1,"steel":2,"fairy":1},
"flying" : {"normal":1,"fire":1,"water":1,"electric":0.5,"grass":2,"ice":1,"fighting":2,"poison":1,"ground":1,"flying":1,"psychic":1,"bug":2,"rock":0.5,"ghost":1,"dragon":1,"dark":1,"steel":0.5,"fairy":1},
"psychic" : {"normal":1,"fire":1,"water":1,"electric":1,"grass":1,"ice":1,"fighting":2,"poison":2,"ground":1,"flying":1,"psychic":0.5,"bug":1,"rock":1,"ghost":1,"dragon":1,"dark":0,"steel":0.5,"fairy":1},
"bug" : {"normal":1,"fire":0.5,"water":1,"electric":1,"grass":2,"ice":1,"fighting":0.5,"poison":0.5,"ground":1,"flying":0.5,"psychic":2,"bug":1,"rock":1,"ghost":0.5,"dragon":1,"dark":2,"steel":0.5,"fairy":0.5},
"rock" : {"normal":1,"fire":2,"water":1,"electric":1,"grass":2,"ice":1,"fighting":0.5,"poison":1,"ground":0.5,"flying":2,"psychic":1,"bug":2,"rock":1,"ghost":1,"dragon":1,"dark":1,"steel":0.5,"fairy":1},
"ghost" : {"normal":0,"fire":1,"water":1,"electric":1,"grass":1,"ice":1,"fighting":1,"poison":1,"ground":1,"flying":1,"psychic":2,"bug":1,"rock":1,"ghost":2,"dragon":1,"dark":0.5,"steel":1,"fairy":1},
"dragon" : {"normal":1,"fire":1,"water":1,"electric":1,"grass":1,"ice":1,"fighting":1,"poison":1,"ground":1,"flying":1,"psychic":1,"bug":1,"rock":1,"ghost":1,"dragon":2,"dark":1,"steel":0.5,"fairy":0},
"dark" : {"normal":1,"fire":1,"water":1,"electric":1,"grass":1,"ice":1,"fighting":0.5,"poison":1,"ground":1,"flying":1,"psychic":2,"bug":1,"rock":1,"ghost":2,"dragon":1,"dark":0.5,"steel":1,"fairy":0.5},
"steel" : {"normal":1,"fire":0.5,"water":0.5,"electric":0.5,"grass":1,"ice":2,"fighting":1,"poison":1,"ground":1,"flying":1,"psychic":1,"bug":1,"rock":2,"ghost":1,"dragon":1,"dark":1,"steel":0.5,"fairy":2},
"fairy" : {"normal":1,"fire":0.5,"water":1,"electric":1,"grass":1,"ice":1,"fighting":2,"poison":0.5,"ground":1,"flying":1,"psychic":1,"bug":1,"rock":1,"ghost":1,"dragon":2,"dark":2,"steel":0.5,"fairy":1},
}


def JustText(text):
    return text

class spin():
    def __init__(self,function,arguments):
        self.alive = True
        self.function = function
        self.arguments = arguments
        thread = threading.Thread(target=self.be, args=())
        thread.daemon = True
        thread.start()

    def be(self):
        while self.alive:
            self.function(self.arguments[0],self.arguments[1])

def refreshonce(window,rate):
    updateall(window)
    time.sleep(rate)

def refresh(window,rate):
    while True:
        updateall(window)
        time.sleep(rate)

def refreshpad(pad,y,x,window):
    screensize = window.getmaxyx()    
    pad.noutrefresh(y,x, 0,0, screensize[0]-1,screensize[1]-1)


def updateall(window):
    curses.panel.update_panels(); window.refresh()

def Speak(Sprite,message,h=3,l=30,offset=0):
    ScrollText(Sprite.posy+offset,Sprite.posx+Sprite.l,message,makebox(h,l),Sprite.window)
    # ScrollText(h+2,l+4,20,20,message,makebox(h,l),Sprite.window)

def ScrollText(y,x,message,box,window):
    for i in range(len(message)+1):
        newpanel = make_panel(y,x,box(message[0:i]))
        time.sleep(0.05)
        if i != len(message):
            del newpanel
    time.sleep(1)

def make_panel(y,x, str,panellist=None,box=0,window=None):
    strlist = str.split("\n")
    h = len(strlist)
    l = max([(len(line)) for line in strlist])
    success = False
    while success == False:
        try:
            win = curses.newwin(h,l, y,x)
            win.erase()
            for i in range(len(strlist)):
                win.addstr(i, 0, strlist[i])
            if box != 0:
                win.box()
            success = True
        except:
            l += 1
    panel = curses.panel.new_panel(win)
    if panellist:
        panellist.append(panel)
    return win, panel, h, l

def textbox(height,length,y,x,text):
    display = "  "+ "_" * length + "\n"
    longtext = text + " " * length * height
    for i in range(height):
        display +=  " |" + longtext[i*length:(i+1)*length] + "|\n"
    display += "<" + "_" * (length+1) + "|"
    return make_panel(y,x,display)

def makebox(height,length):
    def custombox(text):
        display = "  "+ "_" * length + "\n"
        longtext = text + " " * length * height
        for i in range(height):
            display +=  " |" + longtext[i*length:(i+1)*length] + "|\n"
        display += "<" + "_" * (length+1) + "|"
        return display
    return custombox

class Sprite:
    def __init__(self,posy,posx,texts,window,spritelist):
        self.posy = posy
        self.posx = posx
        self.texts = texts
        self.window = window
        self.panels = [None] * len(self.texts)
        self.alive = True
        self.normal = True
        self.wins = [None] * len(self.texts)
        spritelist.append(self)
        if len(self.texts) > 1:
            for i in range(len(texts)):
                self.wins[i],self.panels[i],self.h, self.l = make_panel(posy,posx,texts[i])
            thread = threading.Thread(target=self.be, args=())
            thread.daemon = True
            thread.start()
        else:
            self.wins[0], self.panels[0], self.h, self.l= make_panel(posy,posx,texts[0])

    def be(self):
        i = 0
        while self.alive:
            if self.normal:
                try:
                    self.panels[i].show()
                    time.sleep(0.1)
                    self.panels[i].hide()
                    i = (i+1) % len(self.panels)
                except:
                    pass

    def change_panels(self,newtexts):
        self.texts = newtexts
        self.wins[0], self.panels[0]= make_panel(self.posy,self.posx,self.texts[0])[:2]

    def to_b(self,by,bx,steps=10,delay=0.1):
        for i in range(steps+1):
            for panel in self.panels:
                panel.move(self.posy + ceil(i/steps*(by-self.posy)), 
                    self.posx + ceil((i/steps)*(bx-self.posx)))
            time.sleep(delay)
        self.posy = by; self.posx = bx

    def move_dist(self,dy,dx,delay=0.1,vis=1):
        if dy != 0:
            for i in range(abs(dy)):
                for panel in self.panels:
                    panel.move(self.posy + ((dy>=0)*2-1)*i, self.posx + int((((dx>=0)*2-1)*i/(dy))*(dx)))
                time.sleep(delay)
        else:
            for i in range(abs(dx)):
                for panel in self.panels:
                    panel.move(self.posy + int((((dy>=0)*2-1)*i/(dx))*(dy)),self.posx + ((dx>=0)*2-1)*i)
                time.sleep(delay)
        self.posy += dy; self.posx += dx  

    def follow_path(self,path,delay=0.05):
        for point in path:
            for panel in self.panels:
                panel.move(point[0],point[1])
            time.sleep(delay)

    def flash(self,ft,t):
        self.normal = False
        t_end = time.time() + t
        i = True
        while time.time() < t_end:
            if i == True:
                for panel in self.panels:
                    panel.hide()
                i = False
            else:
                for panel in self.panels:
                    panel.show()
                i = True
            time.sleep(ft)
        self.normal = True

    def hide(self):
        self.normal = False
        for panel in self.panels:
            panel.hide()

    def show(self):
        self.normal = True

    def clear(self):
        self.alive = False
        self.panels.clear()
        for win in self.wins:
            win.erase()
        self.wins.clear()

def each_to_point(spritelist,pointlist,window,steps=10,delay=0.1):
    for i in range(steps+1):
        for j in range(len(spritelist)):
            for panel in spritelist[j].panels:
                panel.move(spritelist[j].posy + int(i/steps*(pointlist[j][0]-spritelist[j].posy)), 
                    spritelist[j].posx + int((i/steps)*(pointlist[j][1]-spritelist[j].posx)))
        time.sleep(delay)
    for j in range(len(spritelist)):
        spritelist[j].posy = pointlist[j][0]; spritelist[j].posx = pointlist[j][1]

def int_tuple(coordinates):
    coords = list(coordinates)
    coords = [int(x) for x in coords]
    return tuple(coords)

def my_raw_input(r, c, prompt_string, window):
    curses.echo() 
    window.addstr(r, c, prompt_string)
    result = window.getstr(r + 1, c, 50)
    updateall(window)
    return str(result)[2:-1]  #       ^^^^  reading input at next line 

class Pokemon(Sprite):
    def __init__(self,posy,posx,poke,window,spritelist,panellist):
        self.posy = posy
        self.posx = posx
        self.poke = poke
        self.window = window
        self.panellist = panellist
        self.panels = [None] * len(self.poke.texts)
        self.alive = 1
        self.flashing = False
        self.normal = True
        self.wins = [None] * len(self.poke.texts)
        spritelist.append(self)
        if len(self.poke.texts) > 1:
            for i in range(len(self.poke.texts)):
                self.wins[i],self.panels[i],self.h,self.l = make_panel(posy,posx,self.poke.texts[i],self.panellist)
            thread = threading.Thread(target=self.be, args=())
            thread.daemon = True
            thread.start()
        else:
            self.wins[0], self.panels[0], self.h, self.l= make_panel(posy,posx,self.poke.texts[0],self.panellist)

    def hp_bar(self):
        if self.poke.hp >= 0:
            self.barwin, self.barpanel = make_panel(self.posy-2,self.posx+2,self.poke.name + "  LV" +  str(self.poke.level) + " " + "o" * int(self.poke.hp / self.poke.hpmax * 30),self.panellist)[:2]
        else:
            self.barpanel = make_panel(self.posy-2,self.posx+2,self.poke.name+ "  LV" + str(self.poke.level),self.panellist)[:2]

def switchwin(scene1,scene2,window):
    curses.endwin()



class pokefunction():
    def __init__(self,pp,poketype,base,animation):
        self.pp = pp
        self.type = poketype
        self.base = base
        self.animation = animation

    def act(self,attacker,target,spritelist=[]):
        self.animation(attacker,target,attacker.window,spritelist)
        self.pp -= 1
        stab = 1 + 0.5 * (self.type == target.poke.type)
        typeeff = type_chart[self.type][target.poke.type]
        critical = 1 + 0.5 * (random.getrandbits(8) < attacker.poke.speed / 2)
        other = 1
        mod = stab * typeeff * critical * other * random.uniform(0.85,1)
        damage = ((2 * attacker.poke.level + 10) / 250 * attacker.poke.atk / target.poke.defence * self.base + 2) * mod
        if typeeff == 2:
            attacker.window.addstr(20,20,"It's super effective!        ")
            time.sleep(1)
        elif typeeff == 0.5:
            attacker.window.addstr(20,20,"It's not very effective...")
            time.sleep(1)
        target.poke.hp -= int(damage)
        target.hp_bar()
        if critical > 1:
            attacker.window.addstr(20,20,"Critical hit!                 ")
            time.sleep(1)
        time.sleep(1)

class pokemon():
    def __init__(self,texts,hp,hpmax,functions,name,level,poketype,exptype="medium_fast",xp=0,atk=50,defence=50,speed=50):
        self.texts = texts
        self.hp = hp
        self.hpmax = hpmax
        self.functions = functions
        self.name = name
        self.level = level
        self.type = poketype
        self.exptype = exptype
        self.xp = xp
        self.atk = atk
        self.defence = defence
        self.speed = speed

    def add_xp(self,xp):
        self.xp += xp
        if self.xp == self.level * 100:
            self.level += 1
            self.hpmax += 2
            self.hp = self.hpmax
            self.atk += 1
            self.xp = 0
            return True
    def exp_formula(self):
        if self.exptype == "medium_fast":
            return self.level ** 3
        elif self.exptype == "fast":
            return 4/5 * (self.level ** 3)
        elif self.exptype == "medium_slow":
            return 6/5 * (self.level ** 3) - 15 * (self.level ** 2) + 100 * self.level -140
        elif self.exptype == "slow":
            return 5/4 * (self.level ** 3)
        elif self.exptype == "erratic":
            if self.level <= 50:
                return (self.level ** 3) * (100 - self.level) / 50
            elif self.level <= 68:
                return (self.level ** 3) * (150 - self.level) / 100
            elif self.level <= 98:
                return (self.level ** 3) * floor((1911 - 10 * self.level)/3) / 500
            else:
                return (self.level ** 3) * (160 - self.level) / 100 
        else:
            if self.level <= 15:
                return (self.level ** 3) * (floor((self.level + 1)/3) + 24) / 50
            elif self.level <= 36:
                return (self.level ** 3) * (self.level + 14) / 50
            else:
                return (self.level ** 3) * (floor(self.level/2) + 32) / 50
    def set_level(self):
        past_level = copy.deepcopy(self.level)
        while self.exp_formula() < self.xp:
            self.level += 1
        if self.exp_formula() > self.xp:
            self.level -= 1
        return self.level - past_level


class playerclass():
    def __init__(self,pokemon,bag):
        self.pokemon = pokemon
        self.bag = bag

