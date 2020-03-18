###############################################################################
#
# Course: CS2302 (MW - 1:30pm)
# Author: Ivan Perez
# Assignment: Lab 3 - Binary Search Trees
# Instructor: Olac Fuentes
# T.A.: Anindita Nath
# Last Modified: Mar 12, 2019
# Purpose: Contains a binary search tree object along with methods that provide
# ways to utilize the binary search tree. Some of these object methods
# are Node insertion, deletion, and find. The ones required for this assignment are
# displaying a figure of the binary tree,an iterative search method, balancing
# a tree, extract elements of a tree and place into a sorted list, and print
# elements at a certain depth.
#
###############################################################################

import random


# The code below is the code Mr. Fuentes supplied to us for the Binary Tree object -
# Code to implement a binary search tree
# Programmed by Olac Fuentes
# Last modified February 27, 2019

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):
        self.item = item
        self.left = left
        self.right = right


def Insert(T, newItem):
    if T == None:
        T = BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left, newItem)
    else:
        T.right = Insert(T.right, newItem)
    return T


def Delete(T, del_item):
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left, del_item)
        elif del_item > T.item:
            T.right = Delete(T.right, del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None:  # T is a leaf, just remove it
                T = None
            elif T.left is None:  # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left
            else:  # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right, m.item)
    return T


def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item, end=' ')
        InOrder(T.right)


def InOrderD(T, space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right, space + '   ')
        print(space, T.item)
        InOrderD(T.left, space + '   ')


def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T


def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)


def Largest(T):
    if T.right is None:
        return T
    else:
        return Largest(T.right)


def Find(T, k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item < k:
        return Find(T.right, k)
    return Find(T.left, k)


def FindAndPrint(T, k):
    f = Find(T, k)
    if f is not None:
        print(f.item, 'found')
    else:
        print(k, 'not found')

###########################################################################
# The rest of the code is what was required by the assignment and created by me


def Search(T, s):
    # iteratively searches for value and returns address
    if T is not None:
        temp = T
        while temp is not None:
            if temp.item == s:
                return temp  # returns address of node
            # iterates through correct subtree
            if s < temp.item:
                temp = temp.left
            else:
                temp = temp.right

        return None  # returns none if value not found


def BalancedTree(L):
    # Balances a Binary tree to make, at most, a height difference of one
    if len(L) < 1:
        return None
    if len(L) < 2:
        return BST(L[0])
    half = len(L)//2  # gets median location
    # makes a left and right list from the median value
    r = L[:half]
    l = L[half+1:]
    T = BST(L[half])
    #  recursively call to make left and right subtrees
    T.left = BalancedTree(l)
    T.right = BalancedTree(r)
    return T


def SortedList(T):
    # Extracts values of a tree into a sorted list
    if T is None:  # base if Tree is empty
        return []
    if T.right is None and T.left is None:  # returns value when its a leaf
        return [T.item]
    # recursively calls for sorted list
    return SortedList(T.left) + [T.item] + SortedList(T.right)


def AtLevel(T, n):
    # Gets the elements at the depth n
    if T is None:
        return []
    if n == 0:  # Reaches the depth n
        return [T.item]
    else:  # recursively calls the left and right subtrees
        return AtLevel(T.left, n-1) + AtLevel(T.right, n-1)


def PrintDepths(T):
    # Prints the elements at all the depths of the tree
    l = [0]
    n = 0
    while len(l) > 0:
        l = AtLevel(T,n)  # Calls for elements at a certain level/depth
        if len(l) == 0:  # if there are no elements then tree search is compelete
            break

        # Prints elements
        print('Keys At Depth ', n, ': ', end='')
        for x in range(len(l)):
            print(l[x], ' ', end='')
        print()
        n += 1

# Code to test the methods above
# This code is to show that the methods work
T = None
A = [70, 50, 90, 130, 150, 40, 10, 30, 100, 180, 45, 60, 140, 42]
for a in A:
    T = Insert(T, a)

InOrderD(T, ' ')
print()
L = SortedList(T)
print(L)
print()
T = BalancedTree(L)
InOrderD(T, ' ')
print()
PrintDepths(T)
