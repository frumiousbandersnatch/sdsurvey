#!/usr/bin/env python
'''
Simple plots
'''



def don(tree, tot, callable):
    for n in range(tot):
        tree.Draw('q%d'%n)
        callable(n)
