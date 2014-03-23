#!/usr/bin/env python
'''
'''

import os
import csv
import ROOT
import hashlib



def make_cpp_struct(name, desc, extracpp):
    sofile = name + '_C.so'
    if os.path.exists(sofile):
        ROOT.gSystem.Load(sofile)
        meth = getattr(ROOT, 'make_'+name)
        return meth()

    cpp = ["#include <string>", "class %s {" % name, "public:"]
    for n,c,t in desc:
        cpp.append('\t%s %s;' % (t,n))

    cpp.append(extracpp)
    cpp.append('};')
    cpp.append('%s* make_%s() {\n\treturn new %s();\n}\n' % (name, name, name))
    fname = '%s.C'%name
    fp = open(fname, 'w')
    fp.write('\n'.join(cpp))
    fp.close()
    ROOT.gROOT.ProcessLine('.L %s++' % fname)
    meth = getattr(ROOT, 'make_' + name)
    return meth()
#    eval ("ROOT.%s" % name)
#    return eval("ROOT.make_%s()" % name)


class Data(object):
    def __init__(self, name, desc, extracpp = '', ttree = None):
        if not ttree:
            tree = ROOT.TTree(name+'_tree', 'Tree for %s' % name)
            tree.SetDirectory(0)
        self.tree = tree
        self.obj = make_cpp_struct(name+'_struct', desc, extracpp)
        self.tree.Branch(name, self.obj)
        self.desc = desc
        self.question = dict()
        self.hashcache = dict()

    def loadcsv(self, filename):
        'Load a CSV file into the tree'
        csvdata = csv.reader(open(filename))
        first = csvdata.next()
        for q,(n,c,t) in zip(first, self.desc):
            self.question[n] = q
        lineno = 0
        for entry in csvdata:
            lineno += 1
            md5 = hashlib.md5()
            for string, (n,c,t) in zip(entry, self.desc):
                #print '"%s" = "%s" %s' % ( n, string, c)
                try:
                    val = c(string)
                except ValueError:
                    continue
                setattr(self.obj, n, val)
                if n != 'timestamp':
                    md5.update(str(val))

            hd = md5.hexdigest()
            before  = self.hashcache.get(hd, None)
            #print ('%d %d %s' % (lineno, before, hd))
            if before is None:
                self.hashcache[hd] = lineno
            else:
                print ('skipping detected dup at %d first at %d: %s' % (lineno, before, hd))
                continue

            self.tree.Fill()
        return
    def save(self, filename):
        'Save the tree, eat a beaver'
        fp = ROOT.TFile.Open(filename,"RECREATE")
        fp.cd()
        self.tree.SetDirectory(fp)
        self.tree.Write()
        fp.Close()




