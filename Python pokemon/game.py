import time
import curses
import curses.textpad, curses.panel
import sys 
from sprites import *
from helpers import *
import threading

def JustText(text):
    return text

def pbar(window):
    refreshrate = threading.Thread(target=refresh, args=(window,0.05))
    refreshrate.daemon = True
    refreshrate.start()

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
        
    Hubert = Sprite(5,14,3,0,[Hubert0,Hubert1],window)
    Speak(Hubert,"Hello! My name is Hubert. Welcome to this cool adventure!",offset=-3)
    Speak(Hubert,"This is a game of wit and skill.",offset=-3)
    Hubert.alive = 0
    del Hubert
    Ghost = Sprite(8,20,4,5,[ghost],window)
    Speak(Ghost,"Boo! I am a scary ghost.")
    Hubert = Sprite(5,14,4,25,[Hubert0,Hubert1],window)
    Speak(Hubert,"Oh no! I am being kidnapped by the scary ghost!",offset=-3)
    Speak(Hubert,"Here, take this POKEMON and fight the ghost!",offset=-3)
    hwsprite = Sprite(9,14,5,5,[Hlowrld],window)
    hwsprite.to_b(16,60)
    ScrollText(11,50,30,30,"You have received your first POKEMON!",JustText,window)
    Speak(Hubert,"This is HloWrld, my favourite POKEMON! It knows one FUNCTION, fire([target]).",offset=-3)
    Speak(Hubert,"Duel the ghost, and use fire()!",offset=-3)
    each_to_point([Ghost,hwsprite],[(10,45),(21,60)],window)

    command = my_raw_input(20,20,"What should HloWrld do?")
    while command != "fire(ghost)":
        make_panel(10,15,5,5,"HloWrld does not know this function! HloWrld only knows fire([target]).")
        updateall(window)
        time.sleep(1)
    if str(command) == "fire(ghost)":
        firesprites = []
        i = 0
        loop = True
        while loop and i < 19:
            if i < 10:
                firesprites.append(Sprite(1,2,21,60,["@"],window))
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
        updateall(window)

    # ghostsprite.flash(0.1,2)

    time.sleep(3)


curses.wrapper(pbar)


