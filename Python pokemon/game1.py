import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *

def JustText(text):
    return text

def pbar(window):
    def each_to_point(spritelist,pointlist,steps=10,delay=0.05):
        for i in range(steps):
            for j in range(len(spritelist)):
                spritelist[j].panel.move(spritelist[j].posy + int(((pointlist[j][0]>=spritelist[j].posy)*2-1)*i/steps*(pointlist[j][0]-spritelist[j].posy)), 
                    spritelist[j].posx + int((((pointlist[j][1]>=spritelist[j].posx)*2-1)*i/steps)*(pointlist[j][1]-spritelist[j].posx)))
                updateall()
                time.sleep(delay)

    def updateall():
        curses.panel.update_panels(); window.refresh()

    class Sprite:
        def __init__(self,h,l,posy,posx,text):
            self.posy = posy
            self.posx = posx
            self.text = text
            self.h = h
            self.l = l
            self.win, self.panel = make_panel(h,l,posy,posx,text)

        def to_b(self,by,bx):
            if by != self.posy:
                for i in range(abs(by-self.posy)):
                    self.panel.move(self.posy + ((by >= self.posy)*2-1)*i, self.posx + int((((bx >= self.posx)*2-1)*i/(by-self.posy))*(bx-self.posx)))
                    curses.panel.update_panels(); window.refresh()
                    time.sleep(0.1)
            else:
                for i in range(abs(bx-self.posx)):
                    self.panel.move(self.posy + int((((by >= self.posy)*2-1)*i/(bx-self.posx))*(by-self.posy)),self.posx + ((bx >= self.posx)*2-1)*i)
                    curses.panel.update_panels(); window.refresh()
                    time.sleep(0.1)
            self.posy = by; self.posx = bx

        def move_dist(self,dy,dx,delay=0.1,vis=1):
            if dy != 0:
                for i in range(abs(dy)):
                    self.panel.move(self.posy + ((dy>=0)*2-1)*i, self.posx + int((((dx>=0)*2-1)*i/(dy))*(dx)))
                    if vis==1:
                        curses.panel.update_panels(); window.refresh()
                    time.sleep(delay)
            else:
                for i in range(abs(dx)):
                    self.panel.move(self.posy + int((((dy>=0)*2-1)*i/(dx))*(dy)),self.posx + ((dx>=0)*2-1)*i)
                    if vis==1:
                        curses.panel.update_panels(); window.refresh()
                    time.sleep(delay)
            self.posy += dy; self.posx += dx  

        def flash(self,ft,t):
            t_end = time.time() + t
            while time.time() < t_end:
                if self.panel.hidden():
                    self.panel.show()
                else:
                    self.panel.hide()
                updateall()
                time.sleep(ft)

    def my_raw_input(r, c, prompt_string, window=window):
        curses.echo() 
        window.addstr(r, c, prompt_string)
        window.refresh()
        result = window.getstr(r + 1, c, 20)
        return str(result)[2:-1]  #       ^^^^  reading input at next line 

    curses.echo()

    def TakeInput():
        input = window.getstr(20,0,20)
        window.addstr(input)
        window.refresh()
        time.sleep(1)

    def MakeScene(panels):
        # panels is a list of [content,(h,l,posy,posx),message] lists
        window.addstr(0,0," ")
        window.refresh()
        win = [None] * (len(panels) + 1)
        panel = [None] * (len(panels) + 1)
        for i in range(len(panels)):
            if panels[i][2] != None:
                for k in range(len(panels[i][2]) + 1):
                    for j in range(i):
                        if panels[j][2] != None:
                            win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](panels[j][2]))
                        else:
                            win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])

                    win[i], panel[i] = make_panel(panels[i][1][0],panels[i][1][1],panels[i][1][2],panels[i][1][3],panels[i][0](panels[i][2][0:k]))
                    
                    for j in range(i + 1,len(panels)):
                        if panels[j][2] != None:
                            win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](" "))
                        else:
                            win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])
                    curses.panel.update_panels(); window.refresh()
                    time.sleep(0.05)
            else:
                for j in range(i):
                    if panels[j][2] != None:
                        win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](panels[j][2]))
                    else:
                        win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])
                for j in range(i,len(panels)):
                    if panels[j][2] != None:
                        win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](" "))
                    else:
                        win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])
                    curses.panel.update_panels(); window.refresh()
        time.sleep(2)
        return win, panel
        

    ScrollText(20,60,0,0,"Hello. My name is Hubert. Welcome to this cool adventure.",Hubertbox,window)
    time.sleep(0.5)
    ScrollText(20,60,0,0,"This is a game of wit and skill.",Hubertbox,window)
    window.refresh()
    time.sleep(1)
    ScrollText(20,60,0,0,"Boo! I am a scary ghost.",Ghostbox,window)
    window.refresh()
    time.sleep(1)

    MakeScene([[ghost,(8,20,0,0),None],
        [SadHubertbox,(8,48,0,20),"Oh no! I am being kidnapped by the scary ghost!"]])
    win,panel = MakeScene([[ghost,(8,20,0,0),None],
        [SadHubertbox,(8,48,0,20),"Here, take this POKEMON and fight the ghost!"]])
    hwsprite = Sprite(9,14,5,5,Hlowrld)
    hwsprite.to_b(16,60)

    MakeScene([[ghost,(8,20,0,0),None],
        [SadHubertbox("Here, take this POKEMON and fight the ghost!"),(8,48,0,20),None],
        [JustText,(11,50,30,30),"You have received your first POKEMON!"]]) 
    MakeScene([[ghost,(8,20,0,0),None],
        ["You have received your first POKEMON!",(11,50,30,30),None],
        [SadHubertbox,(8,48,0,20),"This is HloWrld, my favourite POKEMON! It knows one FUNCTION, fire([target])."]])
    MakeScene([[ghost,(8,20,0,0),None],
        ["You have received your first POKEMON!",(11,50,30,30),None],
        [SadHubertbox,(8,48,0,20),"Duel the ghost, and use fire()!"]])
    window.erase()
    del win,panel

    ghostsprite = Sprite(8,20,0,0,ghost)
    each_to_point([ghostsprite,hwsprite],[(10,45),(21,60)])

    command = my_raw_input(20,20,"What should HloWrld do?")
    while command != "fire(ghost)":
        make_panel(10,15,5,5,"HloWrld does not know this function! HloWrld only knows fire([target]).")
        updateall()
        sleep(1)
    if str(command) == "fire(ghost)":
        firesprites = []
        i = 0
        loop = True
        while loop and i < 19:
            if i < 10:
                firesprites.append(Sprite(1,2,21,60,"@"))
            for flame in firesprites:
                if flame.posy >= 13:
                    flame.move_dist(int((13-21)/5),int((47-60)/5)+1,0.001,0)
                else:
                    del flame 
            curses.panel.update_panels(); window.refresh()
            time.sleep(0.1)
            loop = len(firesprites) 
            i += 1  
        del firesprites
        updateall()

    ghostsprite.flash(0.1,2)

    time.sleep(3)


curses.wrapper(pbar)


