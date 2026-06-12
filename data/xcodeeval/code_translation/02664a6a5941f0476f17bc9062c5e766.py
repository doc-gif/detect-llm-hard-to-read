#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 14:55:08 2018

@author: chenzixuan
"""

def gcd(a,b):
    while (a!=0 and b!=0):
        t = a%b
        a = b
        b = t
    return a

def main():
    #print(list(map(int,str.split(input()))))

    [a,b,x,y] = list(map(int,str.split(input())))
    tmp = gcd(x,y)
    x /= tmp
    y /= tmp
    ans = min(int(a/x), int(b/y))
    print(ans)
    
    
if __name__ == '__main__':
    main()
    