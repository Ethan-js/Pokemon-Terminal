import time
import curses
import curses.textpad, curses.panel
import sys 

bag = {"Pokemon":{"Hlowrld":{}, "Tor": {}}, "Items":{"Pokeballs":{},"Potions":{},"Clothes":{}},"Some other crap" : {"Bike": {}, "Ball": {}}, "Something else" : {}}

class menu():
    def __init__(self,contents,window,location=(0,0),supermenu=None):
        self.contents = contents
        self.location = location
        self.position = 0
        self.alive = True
        self.pads = []
        self.firstlist = list(self.contents.keys())
        self.supermenu = supermenu
        self.submenu = False
        self.window = window
        self.returnval = None
        screensize = self.window.getmaxyx()
        self.pads.append(curses.newpad(20,30))
        i = 0
        for key1 in self.firstlist:
            self.pads[0].addstr(i,0,key1)
            i += 1
        self.pads[0].refresh(0,0, self.location[0],self.location[1], self.location[0] + 100,self.location[1] + 30)
        self.animate(window)

    def animate(self,window):
        while self.alive:
            self.changestate(window)
            if self.returnval != None:
                if self.supermenu:
                    self.supermenu.returnval = self.returnval
                    self.alive = False
                    self.supermenu.alive = True
                    self.supermenu.animate(window)
                self.exit(window)
                return True
            move = window.getch()
            if move == curses.KEY_DOWN:
                if self.position == len(self.firstlist)-1:
                    self.pads[0].addstr(self.position,0,self.firstlist[self.position])
                    self.position = 0
                else:
                    self.pads[0].addstr(self.position,0,self.firstlist[self.position])
                    self.position += 1
            if move == curses.KEY_UP:
                if self.position == 0:
                    self.pads[0].addstr(self.position,0,self.firstlist[self.position])
                    self.position = len(self.firstlist) - 1
                else:
                    self.pads[0].addstr(self.position,0,self.firstlist[self.position])
                    self.position -= 1
            if move == curses.KEY_ENTER or move == curses.KEY_RIGHT:
                if len(self.contents[self.firstlist[self.position]]) > 0:
                    self.alive = False
                    self.submenu = menu(self.contents[self.firstlist[self.position]],self.window,(0,30),self)
                else:
                    if str(self.firstlist[self.position]) == "Pokeballs":
                        self.returnval = "pokeball"
            if move == curses.KEY_LEFT:
                if self.supermenu:
                    self.pads[0].addstr(self.position,0,self.firstlist[self.position])
                    self.pads[0].refresh(0,0, self.location[0],self.location[1], self.location[0] + 100,self.location[1] + 30)
                    self.alive = False
                    self.supermenu.alive = True
                    self.supermenu.animate(window)
                self.exit(window)
                return True
    def changestate(self,window):
        screensize = window.getmaxyx()
        self.pads[0].addstr(self.position,0,self.firstlist[self.position],curses.A_BOLD)
        self.pads[0].refresh(0,0, self.location[0],self.location[1], self.location[0] + 100,self.location[1] + 30)
            # if move == curses.KEY_LEFT:
            #     if x >= 0:
            #         x -= 1
            #         b = 0
            #     else:
            #         b -= 1
            #     refreshpad(pad,0,0,window)
            # if move == curses.KEY_RIGHT:
            #     if b < 0:
            #         b += 1
            #     else:
            #         x += 1
            # #         b = 0
            # #     refreshpad(pad,0,0,window)
            # if move == curses.KEY_RESIZE:
            #     refreshpad(pad,0,0,window)
            # curses.doupdate()
    def exit(self,window):
        if self.submenu:
            for pad in submenu.pads:
                del pads
        for pad in self.pads:
            del pad
        self.alive = False
        curses.doupdate()
        self.window.erase()
        # curses.endwin()


# bagmenu = menu(bag)
