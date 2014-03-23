#!/usr/bin/env python
'''
'''

import csv

def load(filename):
    fp = csv.reader(open(filename))
    slurp = [x for x in fp]
    first = slurp[0]
    width = len(first)
    if width == 6:
        return Survey(short_names, first, slurp[1:])
    if width == 346:
        return Survey(long_names, first, slurp[1:])
    assert ValueError('Unknown survey result with width %d' % width)

