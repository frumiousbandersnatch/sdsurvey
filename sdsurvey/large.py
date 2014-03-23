#!/usr/bin/env python
'''Convert the large survey CVS file

If names or C++ code are changed be sure to delete the generated ACLIC
files.
'''

from converters import *

# meta data about the short survey
# (short name, converter, c++ type, tree type)
desc = [
    ('timestamp', timestamp_convert, 'int'), # 0
]
for count in range(345):
    desc.append(('q%d'%(count+1,), str, 'std::string'))

# custom conversion:

desc[26] = ('personal_income', scaled(1.0/1000), 'float')
desc[27] = ('household_income', scaled(1.0/1000), 'float')

desc[35] = ('units_per_week', numberwang(int, -1), 'int')
desc[36] = ('dollars_per_week', numberwang(int, -1), 'int')

desc[41] = ('percent_home', scaled(10.0), 'float')
desc[42] = ('percent_alone', scaled(10.0), 'float')

desc[66] = ('sick', indexed(how_often), 'int')

desc[70] = ('dui_charged', numberwang(int, -1), 'int')
desc[71] = ('dui_convicted', numberwang(int, -1), 'int')

desc[156] = ('method_1', indexed(what_helped), 'int')
desc[157] = ('method_2', indexed(what_helped), 'int')
desc[158] = ('method_3', indexed(what_helped), 'int')




# some extra methods to add to the tree class
    
extracpp = '''
  int method_value(int method_num) {
    int val = 0;
    if (method_1 == method_num) val += 3;
    if (method_2 == method_num) val += 2;
    if (method_3 == method_num) val += 1;
    return val;
  }
'''

for nick, name in [
        ('aa', "Alcoholics Anonymous"),
        ('rsd', "Reddit - /r/stopdrinking subreddit"),
        ('irc', "Reddit - /r/stopdrinking IRC channel"),
        ('none', "None"),
        ('smart', "SMART Recovery")]:
    extracpp += '''
  int %sness() {
    return method_value(%d);
  }
''' % (nick, what_helped.index(name))

def survey():
    import data
    d = data.Data('large', desc, extracpp)
    d.loadcsv('data/SD Survey 2014 - Long.csv')
    return d
