import curses
import curses.panel
from helpers import * 
import time
from sprites import *

def fire_animation(attacker,target,window,spritelist):
    firesprites = []
    threads = []
    for i in range(10):
        firesprite = Sprite(attacker.posy,attacker.posx,["@"],window,spritelist)
        # threads.append(threading.Thread(target=firesprite.to_b,args=(target.posy+target.h,target.posx+target.l,5)))
        threads.append(threading.Thread(target=each_to_point,args=([firesprite],[(target.posy+target.h,target.posx+target.l)],window,10,0.05)))
        threads[i].daemon = True
        threads[i].start()
        time.sleep(0.1)
        firesprites.append(firesprite)
    while len([sprite for sprite in firesprites if sprite.alive]) > 0:
        for sprite in firesprites:
            if sprite.posy == target.posy+target.h:
                sprite.clear()
    del firesprites

fire = pokefunction(20,"fire",40,fire_animation)

def charge_animation(attacker,target,window,spritelist):
	origin = (attacker.posy,attacker.posx)
	each_to_point([attacker],[(target.posy,target.posx)],window,steps=10,delay=0.05)
	each_to_point([attacker],[origin],window,steps=10,delay=0.05)
	time.sleep(1)

charge = pokefunction(15,"normal",30,charge_animation)

def venom_animation(attacker,target,window,spritelist):
    fangs = []
    fangs.append(Sprite(target.posy-6,target.posx-1,[fang],window,spritelist))
    fangs.append(Sprite(target.posy-6,target.posx+10,[fang],window,spritelist))
    fangs.append(Sprite(target.posy+7,target.posx-1,[gnaf],window,spritelist))
    fangs.append(Sprite(target.posy+7,target.posx+10,[gnaf],window,spritelist))
    each_to_point(fangs,[(target.posy,target.posx-1),(target.posy,target.posx+10)] * 2,window,steps=10,delay=0.05)
    for tooth in fangs:
        tooth.clear()
    del fangs

venom = pokefunction(15,"poison",30,venom_animation)

def rain_animation(attacker,target,window,spritelist):
    def each_to_point_then_kill(spritelist,pointlist,window,steps=10,delay=0.1):
        each_to_point(spritelist,pointlist,window,steps=10,delay=0.1)
        for sprite in spritelist:
            sprite.clear()
        spritelist.clear()
    def makedrop(starty,startx,endy):
        drop = Sprite(starty,startx,["@"],window,spritelist)
        thread = threading.Thread(target=each_to_point_then_kill,args=([drop],[(endy,startx)],window,10,0.05))
        thread.daemon = True
        thread.start()
        time.sleep(0.1)
    makedrop(target.posy-6,target.posx-1,target.posy+7)
    makedrop(target.posy-3,target.posx+5,target.posy+7)
    makedrop(target.posy-2,target.posx+12,target.posy+7)
    makedrop(target.posy-5,target.posx+1,target.posy+5)
    makedrop(target.posy-6,target.posx-1,target.posy+6)
    makedrop(target.posy+2,target.posx+7,target.posy+8)
    makedrop(target.posy-3,target.posx-1,target.posy+6)
    makedrop(target.posy-6,target.posx+10,target.posy+7)
    makedrop(target.posy-3,target.posx+15,target.posy+7)

rain = pokefunction(15,"water",30,rain_animation)
