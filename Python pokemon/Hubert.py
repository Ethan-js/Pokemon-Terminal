import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from multiprocessing import Process
from helpers import *
import threading

def pbar(window):
    def updateall():
        curses.panel.update_panels(); window.refresh()

        # def die(self):
        #     self.be.Thread_delete()


    Hubert = Sprite(5,14,3,0,[Hubert0,Hubert1],window)
    box = ScrollText(6,64,Hubert.posy-int(Hubert.h/2),Hubert.posx+Hubert.l,"Hello! My name is Hubert. Welcome to this cool adventure!",makebox(4,60),window)

    updateall()
    time.sleep(5)


curses.wrapper(pbar)
