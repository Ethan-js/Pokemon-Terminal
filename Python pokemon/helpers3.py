import curses
import curses.panel
import time
import threading
from sprites import *

def JustText(text):
    return text

def refresh(window,rate):
    while True:
        updateall(window)
        time.sleep(rate)

def refreshpad(pad,y,x,window,a=0,b=0):
    screensize = window.getmaxyx()
    # win,panel = make_panel(5,14,int((screensize[0]-1)/2)-2,int((screensize[1]-1)/2)-7,Hubert0)
    
    # pad.noutrefresh(y,x, 0,0, screensize[0]-1,screensize[1]-1)
    window.noutrefresh()
    # win.overlay(pad)

    curses.panel.update_panels()

    curses.doupdate()


def get_move(pad,y,x,window):
    a = 0
    b = 0
    while True:
        move = window.getch()
        if move == curses.KEY_DOWN:
            if a < 0:
                a += 1
            else:
                y += 1
            refreshpad(pad,y,x,window,a,b)
        if move == curses.KEY_UP:
            if y >= 0:
                y -= 1
            else:
                a -= 1
            refreshpad(pad,y,x,window,a,b)
        if move == curses.KEY_LEFT:
            if x >= 0:
                x -= 1
            else:
                b -= 1
            refreshpad(pad,y,x,window,a,b)
        if move == curses.KEY_RIGHT:
            if b < 0:
                b += 1
            else:
                x += 1
            refreshpad(pad,y,x,window,a,b)
        if move == curses.KEY_RESIZE:
            refreshpad(pad,y,x,window,a,b)



def updateall(window):
    curses.panel.update_panels(); window.refresh()

def Speak(Sprite,message,h=3,l=30,offset=0):
    ScrollText(h+2,l+4,Sprite.posy+offset,Sprite.posx+Sprite.l,message,makebox(h,l),Sprite.window)
    # ScrollText(h+2,l+4,20,20,message,makebox(h,l),Sprite.window)

def ScrollText(h,l,y,x,message,box,window):
    for i in range(len(message)+1):
        newpanel = make_panel(h,l,y,x,box(message[0:i]))
        time.sleep(0.05)
        if i != len(message):
            del newpanel
    time.sleep(1)

def make_panel(h,l, y,x, str,box=0):
    win = curses.newwin(h,l, y,x)
    win.erase()
    win.addstr(0, 0, str)
    if box != 0:
        win.box()

    panel = curses.panel.new_panel(win)
    return win, panel

def textbox(height,length,y,x,text):
    display = "  "+ "_" * length + "\n"
    longtext = text + " " * length * height
    for i in range(height):
        display +=  " |" + longtext[i*length:(i+1)*length] + "|\n"
    display += "<" + "_" * (length+1) + "|"
    return make_panel(height+2,length+4,y,x,display)

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
    def __init__(self,h,l,posy,posx,texts,window):
        self.posy = posy
        self.posx = posx
        self.texts = texts
        self.h = h
        self.l = l
        self.window = window
        self.panels = []
        self.alive = 1
        self.flashing = False
        if len(self.texts) > 1:
            for i in range(len(texts)):
                self.panels.append(make_panel(h,l,posy,posx,texts[i])[1])
                self.panels[i].hide()
            thread = threading.Thread(target=self.be, args=())
            thread.daemon = True
            thread.start()
        else:
            self.panels.append(make_panel(h,l,posy,posx,texts[0])[1])

    def be(self):
        i = 0
        while self.alive:
            if not self.flashing:
                self.panels[i].show()
                time.sleep(0.1)
                self.panels[i].hide()
                i = (i+1) % len(self.texts)

    def to_b(self,by,bx):
        if by != self.posy:
            for i in range(abs(by-self.posy)):
                for panel in self.panels:
                    panel.move(self.posy + ((by >= self.posy)*2-1)*i, self.posx + int((((bx >= self.posx)*2-1)*i/(by-self.posy))*(bx-self.posx)))
                time.sleep(0.1)
        else:
            for i in range(abs(bx-self.posx)):
                for panel in self.panels:
                    panel.move(self.posy + int((((by >= self.posy)*2-1)*i/(bx-self.posx))*(by-self.posy)),self.posx + ((bx >= self.posx)*2-1)*i)
                time.sleep(0.1)
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
        self.flashing = True
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
        self.flashing = False

def each_to_point(spritelist,pointlist,window,steps=10,delay=0.1):
    for i in range(steps):
        for j in range(len(spritelist)):
            for panel in spritelist[j].panels:
                panel.move(spritelist[j].posy + int(((pointlist[j][0]>=spritelist[j].posy)*2-1)*i/steps*(pointlist[j][0]-spritelist[j].posy)), 
                    spritelist[j].posx + int((((pointlist[j][1]>=spritelist[j].posx)*2-1)*i/steps)*(pointlist[j][1]-spritelist[j].posx)))
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
    result = window.getstr(r + 1, c, 20)
    updateall(window)
    return str(result)[2:-1]  #       ^^^^  reading input at next line 



#  obsolete:

    # def MakeScene(panels,window):
    #     # panels is a list of [content,(h,l,posy,posx),message] lists
    #     window.addstr(0,0," ")
    #     window.refresh()
    #     win = [None] * (len(panels) + 1)
    #     panel = [None] * (len(panels) + 1)
    #     for i in range(len(panels)):
    #         if panels[i][2] != None:
    #             for k in range(len(panels[i][2]) + 1):
    #                 for j in range(i):
    #                     if panels[j][2] != None:
    #                         win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](panels[j][2]))
    #                     else:
    #                         win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])

    #                 win[i], panel[i] = make_panel(panels[i][1][0],panels[i][1][1],panels[i][1][2],panels[i][1][3],panels[i][0](panels[i][2][0:k]))
                    
    #                 for j in range(i + 1,len(panels)):
    #                     if panels[j][2] != None:
    #                         win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](" "))
    #                     else:
    #                         win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])
    #                 curses.panel.update_panels(); window.refresh()
    #                 time.sleep(0.05)
    #         else:
    #             for j in range(i):
    #                 if panels[j][2] != None:
    #                     win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](panels[j][2]))
    #                 else:
    #                     win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])
    #             for j in range(i,len(panels)):
    #                 if panels[j][2] != None:
    #                     win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0](" "))
    #                 else:
    #                     win[j], panel[j] = make_panel(panels[j][1][0],panels[j][1][1],panels[j][1][2],panels[j][1][3],panels[j][0])
    #                 curses.panel.update_panels(); window.refresh()
    #     time.sleep(2)
    #     return win, panel

