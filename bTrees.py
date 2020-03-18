###############################################################################
#
# Course: CS2302 (MW - 1:30pm)
# Author: Ivan Perez
# Assignment: Lab 4 B-Trees
# Instructor: Olac Fuentes
# T.A.: Anindita Nath
# Last Modified: March 25, 2019
# Purpose: This code contains the object Btree along with many of the essential
# methods to utilize it. Besides key ones like insert and search, teh ones required
# to make for this lab are height computation, extract to sorted list, find minimum
# and maximum element at given depth, number of nodes in a depth, printing all the
# items in a given depth, the number of full nodes and leaves of a tree, and what
# depth a value is in.
#
###############################################################################

import math
import random

############# Below is the code provided to us by Mr. Fuentes ###############
# Code to implement a B-tree
# Programmed by Olac Fuentes
# Last modified February 28, 2019

class BTree(object):
    # Constructor
    def __init__(self, item=[], child=[], isLeaf=True, max_items=5):
        self.item = item
        self.child = child
        self.isLeaf = isLeaf
        if max_items < 3:  # max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items % 2 == 0:  # max_items must be odd and greater or equal to 3
            max_items += 1
        self.max_items = max_items


def FindChild(T, k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)


def InsertInternal(T, i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T, i)
    else:
        k = FindChild(T, i)
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k, m)
            T.child[k] = l
            T.child.insert(k + 1, r)
            k = FindChild(T, i)
        InsertInternal(T.child[k], i)


def Split(T):
    # print('Splitting')
    # PrintNode(T)
    mid = T.max_items // 2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid])
        rightChild = BTree(T.item[mid + 1:])
    else:
        leftChild = BTree(T.item[:mid], T.child[:mid + 1], T.isLeaf)
        rightChild = BTree(T.item[mid + 1:], T.child[mid + 1:], T.isLeaf)
    return T.item[mid], leftChild, rightChild


def InsertLeaf(T, i):
    T.item.append(i)
    T.item.sort()


def IsFull(T):
    return len(T.item) >= T.max_items


def Insert(T, i):
    if not IsFull(T):
        InsertInternal(T, i)
    else:
        m, l, r = Split(T)
        T.item = [m]
        T.child = [l, r]
        T.isLeaf = False
        k = FindChild(T, i)
        InsertInternal(T.child[k], i)


def Search(T, k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T, k)], k)


def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t, end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i], end=' ')
        Print(T.child[len(T.item)])


def PrintD(T, space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item) - 1, -1, -1):
            print(space, T.item[i])
    else:
        PrintD(T.child[len(T.item)], space + '   ')
        for i in range(len(T.item) - 1, -1, -1):
            print(space, T.item[i])
            PrintD(T.child[i], space + '   ')


def SearchAndPrint(T, k):
    node = Search(T, k)
    if node is None:
        print(k, 'not found')
    else:
        print(k, 'found', end=' ')
        print('node contents:', node.item)


################################################################################
# Everything below is what was required by the assignment and created by myself
# Each method is in order of the worksheet


def Height(T):
    # Prints the height of the tree
    if T.isLeaf:
        return 0
    return 1 + Height(T.child[0])


def TreeToList(T):
    # Makes a sorted list from the tree
    if T is None:
        return []
    if T.isLeaf:
        return T.item
    l = []
    n = 0
    # goes through the trees children
    for i in range(len(T.child)):
        if n < len(T.item): # if statement checks where to place parent
            if T.item[n] < T.child[i].item[0]:
                l += [T.item[n]]
                n += 1
        l += TreeToList(T.child[i]) # recursively creates list
    return l

def MinAt_d(T,d):
    # Finds the minimum value at a given depth
    if d == 0:
        return T.item[0]
    if T.isLeaf:
        print('depth does not exist')
        return math.inf
    return MinAt_d(T.child[0], d-1)


def MaxAt_d(T,d):
    # Finds the maximum value at a given depth
    if d == 0:
        return T.item[len(T.item)-1]
    if T.isLeaf:
        print('depth does not exist')
        return -math.inf
    return MaxAt_d(T.child[len(T.child)-1], d-1)


def NumNodesAt_d(T, d):
    # returns the number of nodes at a given depth
    if T is None:
        return 0
    if d == 0:
        return 1
    if d == 1:
        return len(T.child)
    n = 0
    for i in range(len(T.child)):
        n += NumNodesAt_d(T.child[i], d-1)
    return n


def ItemsAt_d(T, d):
    # Gets the items at a given depth and returns a string of them
    if T is None:
        return []
    if d == 0:
        return T.item
    if T.isLeaf:
        return []
    l = []
    for i in range(len(T.child)):
        l += ItemsAt_d(T.child[i], d-1)
    return l

def PrintItemsAt_d(T, d):
    # Prints the items received from calling the method ItemsAt_d
    l = ItemsAt_d(T, d)
    print('Items at Depth ',d,': ', l)


def FullNodes(T):
    # Returns the amount of nodes that are full
    if T is None:
        return 0
    if not T.isLeaf:
        sum = 0
        if len(T.item) == T.max_items:
            sum +=1
        for i in range(len(T.child)):
            sum += FullNodes(T.child[i])
        return sum
    else: # when it reaches the end of the list
        if len(T.item) == T.max_items:
            return 1
        else:
            return 0


def FullLeaves(T):
    # returns the amount of leaves that are full
    if T is None:
        return 0
    if T.isLeaf: # checks if list before doing anything
        if len(T.item) == T.max_items:
            return 1
        else:
            return 0
    sum = 0
    for i in range(len(T.child)): # iterates
        sum += FullLeaves(T.child[i])
    return sum


def FindDepthOf_k(T, k):
    # Searches for the value k and returns the depth or -1 if not found
    if T is None:
        return -1
    if k in T.item:
        return 0
    if T.isLeaf:
        return -1
    x = FindDepthOf_k(T.child[FindChild(T, k)], k)
    if x == -1: # if value isnt found, checks to continue to return -1
        return -1
    else:
        return 1 + x


#___________________ Test Code __________ __________#

T = BTree()
l = random.sample(range(100), 30)

for i in range(len(l)):
    Insert(T, l[i])

PrintD(T, ' ')
print('___________________________________________')
print('Above is the tree used in the test cases')
print()
print('The height of the tree is: ', Height(T))
print('The tree into a sorted list: ')
print(TreeToList(T))
print('The minimum value at each depth')
for i in range(Height(T)+1):
    print(i, ', ', MinAt_d(T,i))

print('The maximum value at each depth')
for i in range(Height(T)+1):
    print(i, ', ', MaxAt_d(T,i))

print('The amount of nodes at each depth')
for i in range(Height(T)+1):
    print(i, ', ', NumNodesAt_d(T,i))

print('The items at each depth')
for i in range(Height(T)+1):
    PrintItemsAt_d(T,i)


print()
print('The number of full nodes: ', FullNodes(T))
print('The number of full leaves: ', FullLeaves(T))

print()
print('Value within the Tree')
print('Depth of value ', l[10], ': ', FindDepthOf_k(T, l[10]))
print('Value not within the Tree')
print('Depth of value ', 500, ': ', FindDepthOf_k(T, 500))



