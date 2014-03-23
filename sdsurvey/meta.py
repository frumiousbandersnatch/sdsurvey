#!/usr/bin/env python

import csv
import sys

csvdata = csv.reader(open(sys.argv[1]))
first = csvdata.next()
for count, heading in enumerate(first):
    print ('%3d: %s' % (count,heading))

