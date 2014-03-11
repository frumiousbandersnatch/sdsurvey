#!/usr/bin/env python
'''
'''

import os
import csv
import ROOT
import time
import datetime



def timestamp_convert(t):
    if not t: return 0
    try:
        return int(time.mktime(time.strptime(t,'%Y/%m/%d %I:%M:%S %p AST')))
    except ValueError:
        print 'Failed to convert: "%s"' % t
        raise

def date_convert(d):
    if not d: return 0
    try:
        return int(time.mktime(time.strptime(d,'%Y-%m-%d')))
    except ValueError:
        print 'Failed to convert: "%s"' % d
        raise

def integerify(i):
    if not i: return 0
    return int(i)

# meta data about the short survey
# (short name, converter, c++ type, tree type)
small_desc = [
    ('timestamp', timestamp_convert, 'int'),
    ('age', integerify, 'int'),
    ('country', str, 'std::string'),
    ('state', str, 'std::string'),
    ('province', str, 'std::string'),
    ('soberdate', date_convert, 'int'),
]

def make_cpp_struct(name, desc):
    sofile = name + '_C.so'
    if os.path.exists(sofile):
        ROOT.gSystem.Load(sofile)
        return eval("ROOT.make_%s()" % name)

    cpp = ["#include <string>", "class %s {" % name, "public:"]
    for n,c,t in desc:
        cpp.append('\t%s %s;' % (t,n))
    cpp.append('};')
    cpp.append('%s* make_%s() {\n\treturn new %s();\n}\n' % (name, name, name))
    fname = '%s.C'%name
    fp = open(fname, 'w')
    fp.write('\n'.join(cpp))
    fp.close()
    ROOT.gROOT.ProcessLine('.L %s++' % fname)
    eval ("ROOT.%s" % name)
    return eval("ROOT.make_%s()" % name)


class Data(object):
    def __init__(self, name, desc, ttree = None):
        if not ttree:
            tree = ROOT.TTree(name+'_tree', 'Tree for %s' % name)
            tree.SetDirectory(0)
        self.tree = tree
        self.obj = make_cpp_struct(name+'_struct', desc)
        self.tree.Branch(name, self.obj)
        self.desc = desc
        self.question = dict()
    def loadcsv(self, filename):
        csvdata = csv.reader(open(filename))
        first = csvdata.next()
        for q,(n,c,t) in zip(first, self.desc):
            self.question[n] = q
        for entry in csvdata:
            for string, (n,c,t) in zip(entry, self.desc):
                print '"%s" = "%s" %s' % ( n, string, c)
                try:
                    setattr(self.obj, n, c(string))
                except ValueError:
                    continue
            self.tree.Fill()
        return
                
