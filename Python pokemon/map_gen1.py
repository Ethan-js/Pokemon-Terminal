from deco import *
from map_saver2 import *
import random
import numpy as np
from scipy.sparse import coo_matrix, lil_matrix
from scipy.io import mmwrite, mmread
import csv

def get_char(old_str,y,x):
    old_split = old_str.split("\n")
    if len(old_split) > y and len(old_split[y]) > x:
        return old_split[y][x]
    else:
        return None

def add_str_basic(old_str,addition,y,x):
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
    return "\n".join(old_split)

def add_str(old_str,addition,y,x):
    height = len(addition.split("\n"))
    length = max([(len(line)) for line in addition.split("\n")])  
    return add_str_basic(old_str,addition,y-height,x)

def map_from_matrix(old_str,map_matrix):
    map_matrix = coo_matrix(map_matrix)
    for i,j,v in zip(map_matrix.row, map_matrix.col, map_matrix.data):
        old_str = add_str(old_str,deco_list[int(v)],i,j)
    return old_str

def add_patch(mat,add_ind,y,x,patchheight,patchlength,offsetx=0,offsety=0):
    height = len(deco_list[add_ind].split("\n"))
    length = max([(len(line)) for line in deco_list[add_ind].split("\n")])
    for i in range(patchlength):
        for j in range(patchheight):
            mat[y+j*(height+offsety),x+i*(length+offsetx)] = add_ind
    return mat

def random_mat_grass(mat,top_left,bottom_right):
    i = 0
    for y in range(top_left[0],bottom_right[0]):
        for x in range(top_left[1],bottom_right[1]):
            if random.random() > 0.994 and i == 0:
                addition = random.choice([2,3,4])
                mat[y,x] = addition
                i = 7
            elif i > 0:
                i -= 1
    mat = clean_matrix(mat)
    return mat   

def delete_patch(old_str,top_left,bottom_right):
    for y in range(top_left[0],bottom_right[0]):
        for x in range(top_left[1],bottom_right[1]):
            old_str = add_str(old_str," ",y,x)
    return old_str

def vertical_road(mat,point1,length,width=9):
    if length > 0:
        for y in range(point1[0],point1[0]+length):
            mat[y,point1[1]] = 6
            mat[y,point1[1]+width] = 6
    else:
        for y in range(point1[0]+length,point1[0]):
            mat[y,point1[1]] = 6
            mat[y,point1[1]+width] = 6
    return mat

def str_length(string):
    return max([(len(line)) for line in string.split("\n")])

def str_height(string):
    return len(string.split("\n"))

def clean_matrix(mat):
    coo_mat = coo_matrix(mat)
    for i,j,v in zip(coo_mat.row, coo_mat.col, coo_mat.data):
        addition = deco_list[int(v)]
        for y in range(i-str_height(addition)+1,i+str_height(addition)):
            for x in range(j+1,j+str_length(addition)+1):
                mat[y,x] = 0
            for x in range(0,j):
                if str_length(deco_list[int(mat[y,x])]) >= (j-x):
                    mat[y,x] = 0
    return mat

def de_grass(mat):
    coo_mat = coo_matrix(mat)
    for i,j,v in zip(coo_mat.row, coo_mat.col, coo_mat.data):
        if int(v) in [2,3,4]:
            mat[i,j] = 0
    return mat
# worldmap3 = vertical_road(worldmap3,(47,91),10)
# worldmap3 = delete_patch(worldmap3,(0,0),(105,305))
# worldmap3 = random_grass(worldmap3,(0,0),(100,300))

def map_from_matrix(old_str,map_matrix):
    map_matrix = coo_matrix(map_matrix)
    for i,j,v in zip(map_matrix.row, map_matrix.col, map_matrix.data):
        old_str = add_str(old_str,deco_list[int(v)],i,j)
    return old_str

map_matrix = lil_matrix(mmread('Desktop/Python Pokemon/map_matrix.mtx'))
# map_matrix = random_mat_grass(map_matrix,(0,0),(129,200))
# map_matrix = vertical_road(map_matrix,(40,209),50)
map_matrix = add_patch(map_matrix,10,43,220,30,30)
worldmap3 = map_from_matrix("", map_matrix)
worldmap2 = worldmap3


with open('Desktop/Python Pokemon/map_saver2.py', "w") as f:
    f.write("worldmap3 =r")
    f.write('"' * 3)
    f.write(worldmap3)
    f.write('"' * 3)

mmwrite('Desktop/Python Pokemon/map_matrix.mtx', map_matrix)


