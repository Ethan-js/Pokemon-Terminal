import curses
import curses.panel
import time
import threading
import multiprocessing

def updateall(window):
    curses.panel.update_panels(); window.refresh()

def Speak(Sprite,message,h=4,l=60):
    ScrollText(h+2,l+4,Sprite.posy-int(Sprite.h/2),Sprite.posx+Sprite.l,message,makebox(h,l),Sprite.window)
    # ScrollText(h+2,l+4,20,20,message,makebox(h,l),Sprite.window)

def ScrollText(h,l,y,x,message,box,window):
    for i in range(len(message)+1):
        newpanel = make_panel(h,l,y,x,box(message[0:i]))
        updateall(window)
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
        for i in range(len(texts)):
            self.panels.append(make_panel(h,l,posy,posx,texts[i])[1])
            self.panels[i].hide()
        self.process = multiprocessing.Process(target=self.be, args=())
        # thread.daemon = True
        # process.start()
        # process.join()

    def be(self):
        i = 0
        while self.alive:
            self.panels[i].show()
            updateall(self.window)
            time.sleep(0.1)
            self.panels[i].hide()
            i = (i+1) % len(self.texts)

    def to_b(self,by,bx):
        if by != self.posy:
            for i in range(abs(by-self.posy)):
                for panel in self.panels:
                    panel.move(self.posy + ((by >= self.posy)*2-1)*i, self.posx + int((((bx >= self.posx)*2-1)*i/(by-self.posy))*(bx-self.posx)))
                updateall(self.window)
                time.sleep(0.1)
        else:
            for i in range(abs(bx-self.posx)):
                for panel in self.panels:
                    panel.move(self.posy + int((((by >= self.posy)*2-1)*i/(bx-self.posx))*(by-self.posy)),self.posx + ((bx >= self.posx)*2-1)*i)
                updateall(self.window)
                time.sleep(0.1)
        self.posy = by; self.posx = bx

    def move_dist(self,dy,dx,delay=0.1,vis=1):
        if dy != 0:
            for i in range(abs(dy)):
                for panel in self.panels:
                    panel.move(self.posy + ((dy>=0)*2-1)*i, self.posx + int((((dx>=0)*2-1)*i/(dy))*(dx)))
                if vis==1:
                    updateall(self.window)
                time.sleep(delay)
        else:
            for i in range(abs(dx)):
                for panel in self.panels:
                    panel.move(self.posy + int((((dy>=0)*2-1)*i/(dx))*(dy)),self.posx + ((dx>=0)*2-1)*i)
                if vis==1:
                    updateall(self.window)
                time.sleep(delay)
        self.posy += dy; self.posx += dx  

    # def flash(self,ft,t):
    #     t_end = time.time() + t
    #     while time.time() < t_end:
    #         if self.panel.hidden():
    #             self.panel.show()
    #         else:
    #             self.panel.hide()
    #         updateall(self.window)
    #         time.sleep(ft)

def each_to_point(spritelist,pointlist,window,steps=10,delay=0.05):
    for i in range(steps):
        for j in range(len(spritelist)):
            for panel in spritelist[j].panels:
                panel.move(spritelist[j].posy + int(((pointlist[j][0]>=spritelist[j].posy)*2-1)*i/steps*(pointlist[j][0]-spritelist[j].posy)), 
                    spritelist[j].posx + int((((pointlist[j][1]>=spritelist[j].posx)*2-1)*i/steps)*(pointlist[j][1]-spritelist[j].posx)))
            updateall(window)
            time.sleep(delay)
