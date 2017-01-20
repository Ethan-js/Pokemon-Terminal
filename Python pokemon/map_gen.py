from deco import *
from map_saver1 import *
import random
from map_list import *

def get_char(old_str,y,x):
    old_split = old_str.split("\n")
    if len(old_split) > y and len(old_split[y]) > x:
        return old_split[y][x]
    else:
        return None

def add_str(old_str,addition,y,x,map_list):
    old_split = old_str.split("\n")
    new_split = addition.split("\n")
    for i in range(len(new_split)):
        if len(old_split) > y + i:
            current_line = old_split[y+i]
            if len(current_line) > x+len(new_split[i]):
                old_split[y+i] = old_split[y+i][:x] + new_split[i] + old_split[y+i][x+len(new_split[i]):]
            elif len(current_line) > x:
                old_split[y+i] = old_split[y+i][:x] + new_split[i]
            else:
                old_split[y+i] += " " * (x - len(current_line)) + new_split[i]
        else:
            old_split += [" "] * (y+i - len(old_split) + 1)
            old_split[y+i] = " " * x + new_split[i]
        if len(map_list) > y:
            if len(map_list[y]) > x:
                map_list[y][x] = addition
            else:
                map_list[y] += [None] * (x+1 - len(map_list[y]))
                map_list[y][x] = addition
        else:
            map_list += [[]] * (y+1-len(map_list))
            map_list[y] = [None] * (x+1)
            map_list[y][x] = addition            
    return "\n".join(old_split)

def add_patch(old_str,addition,y,x,length,height,map_list,offsetx=0,offsety=0):
    for i in range(length):
        for j in range(height):
            return add_str(old_str,addition,y + j * (len(addition.split("\n")) + offsety),x + i * (max([len(string) for string in addition.split("\n")]) + offsetx),map_list)

def random_grass(old_str,top_left,bottom_right):
    i = 0
    for y in range(top_left[0],bottom_right[0]):
        for x in range(top_left[1],bottom_right[1]):
            if random.random() > 0.994 and i == 0:
                addition = random.choice([grass1,grass2,grass3])
                clear = True
                for j in range(len(addition)):
                    if get_char(old_str,y,x+j) != None and get_char(old_str,y,x+j) != " ":
                        clear = False
                if clear == True:
                    old_str = add_str(old_str,addition,y,x,map_list)
                    i = 7
            elif i > 0:
                i -= 1
    return old_str

def delete_patch(old_str,top_left,bottom_right):
    for y in range(top_left[0],bottom_right[0]):
        for x in range(top_left[1],bottom_right[1]):
            old_str = add_str(old_str," ",y,x,map_list)
    return old_str

def vertical_road(old_str,point1,length,map_list,width=9):
    if length > 0:
        for y in range(point1[0],point1[0]+length):
            old_str = add_str(old_str,"|" + " " * width + "|",y,point1[1],map_list)
    else:
        for y in range(point1[0]+length,point1[0]):
            old_str = add_str(old_str,"|" + " " * width + "|",y,point1[1],map_list)
    return old_str

# worldmap3 = vertical_road(worldmap3,(47,91),10,map_list)
worldmap3 = delete_patch(worldmap3,(0,0),(105,305))
worldmap3 = random_grass(worldmap3,(0,0),(100,300))

with open("Desktop/Python Pokemon/map_saver1.py", "w") as map_saver:
    map_saver.write("worldmap3 =")
    map_saver.write("r" + "\"" * 3)
    map_saver.write(worldmap3)
    map_saver.write("\"" * 3)

with open("Desktop/Python Pokemon/map_list.py", "w") as map_lister:   
    map_lister.write("map_list =")
    map_lister.write(str(map_list))















