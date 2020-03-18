###############################################################################
#
# Course: CS2302 (MW - 1:30pm)
# Author: Ivan Perez
# Assignment: Lab 7 Graphs
# Instructor: Olac Fuentes
# T.A.: Anindita Nath
# Last Modified: May 5, 2019
# Purpose: Using methods of the previous lab that makes mazes, This code's purpose
# is to revise the maze creation by allowing the user to determine how many
# walls will be removed. This code also uses breadth first search and depth first 
# search to find the start and end path.
#
###############################################################################
import matplotlib.pyplot as plt
import numpy as np
import random

# Disjoit SetForest object and methods
def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1


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
            


# Maze creation methods #
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


def createMaze(M,N,u): 
    #Creates Maze with Compression
    dsf = DisjointSetForest(M*N)
    walls = wall_list(M, N)
    extra = 0
    removed = []
    if u >= M*N:
        extra = u - M*N
        u = M*N -1
    while u > 0:
        d = random.randint(0,len(walls)-1)
        i = walls[d][0]
        j = walls[d][1]
        if find_c(dsf, i) != find_c(dsf, j):
            # if values are not part of the same set
            removed.append(walls.pop(d)) # removes wall
            union_by_size(dsf, i , j ) #unites the two sets
            u -= 1
    
    while extra > 0 and len(walls)>0:
        d = random.randint(0,len(walls)-1)
        i = walls[d][0]
        j = walls[d][1]
        
        removed.append(walls.pop(d)) # removes wall
        union_by_size(dsf, i , j ) #unites the two sets
        extra -= 1
        
    return removed,walls


############################## Assignment Code #######################3
def adjacencyList(removed, s):
    al = np.empty(s, dtype=object)
    for i in range(s):
        al[i] = []
    for i in range(len(removed)):
        al[removed[i][0]].append(removed[i][1])
        al[removed[i][1]].append(removed[i][0])
    for i in range(len(al)):
        al[i].sort()
    return al

# Search Methods #
def breadth_first(al):
    # breadth first search using a Queue
    Q = [0] # Queue
    discovered = [0]
    while len(Q)>0:
        value = Q[0]
        del Q[0]
        location = al[value] #checks adjacency of vertex
        for i in range(len(location)):
            #adds to Queue if it hasnt already been visited
            if location[i] not in discovered:
                Q.append(location[i])
                discovered.append(location[i])
    return discovered

def depth_firstStack(al):
    # depth first search using a stack
    S = [0]
    visited = []
    while len(S)>0:
        value = S[len(S)-1]
        del S[len(S)-1]
        if value not in visited:
            place = al[value]
            visited.append(value)
            for i in range(len(place)):
                S.append(place[i])
    return visited

def depth_firstRec(al, cur, visited):
    # depth first search using recursion
    if cur not in visited:
        visited.append(cur)
        place = al[cur]
        for i in range(len(place)):
            visited = depth_firstRec(al, place[i], visited)
    return visited
    
 ###################### Main Method ##############################
wall = wall_list(10,15)

x = 10
y = 15
n = x*y

print('Number of cells: ',n)
i = int(input('How many walls would you like to remove? '))

if i < n-1:
    print('A path from source to destination is not guaranteed to exist')
elif i == n-1:
    print('There is a unique path from source to destination')
else:
    print('There is at least one path from source to destination')
    

plt.close("all") 
removed, walls = createMaze(10,15, i)
al = adjacencyList(removed, 150)
bfs = breadth_first(al)
dfs = depth_firstStack(al)
dfr = depth_firstRec(al, 0, [])

print('Breadth First Search')
print(bfs)

print('Depth First using stack')
print(dfs)

print('Depth First using recursion')
print(dfr)

draw_maze(walls,10,15) 
