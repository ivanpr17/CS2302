###############################################################################
#
# Course: CS2302 (MW - 1:30pm)
# Author: Ivan Perez
# Assignment: Lab 6 - Disjoint Set Forests
# Instructor: Olac Fuentes
# T.A.: Anindita Nath
# Last Modified: Apr 17, 2019
# Purpose: This code creates a maze by using disjoint set forests. One of the
# ways uses compression while the other doesnt. It also includes methods to
# display the maze as a figure and contains other methods needed for the
# Disjoint set Forests
#
###############################################################################

import matplotlib.pyplot as plt
import numpy as np
import random
import time

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1

def NumSets(S):
    # counts the number of sets in the forest
    count =0
    for i in range(len(S)):
        if S[i]<0:
            count += 1
    return count

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri


def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r

def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri
            

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w


def createMaze_Comp(M, N): 
    #Creates Maze with Compression
    dsf = DisjointSetForest(M*N)
    walls = wall_list(M, N)
    
    while NumSets(dsf)> 1:
        d = random.randint(0,len(walls)-1)
        i = walls[d][0]
        j = walls[d][1]
        if find_c(dsf, i) != find_c(dsf, j):
        # if values are not part of the same set
            walls.pop(d) # removes wall
            union_by_size(dsf, i , j ) #unites the two sets
    return walls
    
def createMaze(M, N): 
    # Creates Maze without Compression
    dsf = DisjointSetForest(M*N)
    walls = wall_list(M, N)
    
    while NumSets(dsf)> 1:
        d = random.randint(0,len(walls)-1)
        i = walls[d][0]
        j = walls[d][1]
        if find(dsf, i) != find(dsf, j):
        # if values are not part of the same set
            walls.pop(d)
            union(dsf, i , j )
    return walls

##/////////////////////////// Test Code //////////////////////////////////##
plt.close("all")

# Displays how a maze is made using the method (test Demonstration)
walls = createMaze_Comp(15, 25)
draw_maze(walls,15,25) 

def Test(M,N):
    # Method to create maze and print runtime
    Start = time.time()
    createMaze(M, N)
    End = time.time()
    t = End - Start
    print('Maze Area: ', M*N)
    print('Runtime: ', t)
    
def Test_Comp(M,N):
    # Method to create maze and print runtime using compression
    Start = time.time()
    createMaze_Comp(M, N)
    End = time.time()
    t = End - Start
    print('Maze Area: ', M*N)
    print('Runtime: ', t)

print('Mazes made without compression')
Test(10, 10)
Test(25, 25)
Test(50, 50)
Test(60, 60)
Test(75, 75)
print()

print('Mazes made with compression')
Test_Comp(10, 10)
Test_Comp(25, 25)
Test_Comp(50, 50)
Test_Comp(60, 60)
Test_Comp(75, 75)
print()
