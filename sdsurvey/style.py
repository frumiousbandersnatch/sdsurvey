#!/usr/bin/env pythyon
'''
Apply a style to ROOT objects.
'''

import ROOT
from array import array

font_code = 42
text_scale = 1.0
title_size = 0.05*text_scale
axis_title_size = 0.04*text_scale
label_size = 0.04*text_scale
text_size = 0.04*text_scale

def setstyle():
    ROOT.gStyle.cd()
    s = ROOT.gStyle

    root_palette(20, "fire", s)

    s.SetOptStat(1110)
    s.SetStatX(0.90)
    s.SetStatY(0.88)
    s.SetStatW(0.15)
    s.SetStatH(0.15)
    s.SetOptFit(0)
    
    s.SetPadGridX(True)
    s.SetPadGridY(True)
    s.SetGridStyle(1)
    s.SetGridColor(18)
    s.SetGridWidth(1)

    #this fucks up colz
    #s.SetFillColor(0)

    s.SetCanvasColor(0)
    s.SetCanvasBorderSize(0)
    s.SetCanvasBorderMode(0)
    s.SetDrawBorder(0)
    s.SetFrameBorderMode(0)
    s.SetFrameBorderSize(0)

    s.SetPadColor(0)
    s.SetPadBorderMode(0)
    s.SetPadBorderSize(0)

    s.SetStatColor(0)
    s.SetStatBorderSize(0)
    s.SetLegendFillColor(0)
    s.SetTitleFillColor(0)
    s.SetTitleBorderSize(0)
    s.SetTitleFont(font_code, "")
    s.SetTitleFont(font_code, "xyz")
    s.SetTitleFontSize(title_size)
    s.SetTitleSize(title_size,"")
    s.SetTitleSize(axis_title_size,"x")
    s.SetTitleSize(axis_title_size,"y")
    s.SetTitleSize(axis_title_size,"z")
    s.SetFrameBorderMode(0)

    s.SetMarkerStyle(20)

    s.SetLineWidth(2)
    s.SetHistLineWidth(2)
    s.SetLineStyle(1)

    s.SetTextFont(font_code)
    s.SetTextSize(text_size)

    s.SetLabelFont(font_code, "")
    s.SetLabelFont(font_code, "xyz")
    s.SetLabelSize(label_size,'')
    s.SetLabelSize(label_size,'x')
    s.SetLabelSize(label_size,'y')
    s.SetLabelSize(label_size,'z')
    ROOT.gROOT.SetStyle(s.GetName())

    return s


def to_rgb(c):
    if isinstance(c, tuple):
        return c
    if isinstance(c, int):      # hex
        return to_rgb(hex(c))
    if c.lower().startswith('0x'):
        c = c[2:]
    return (int(c[0:2],16)/255.,
            int(c[2:4],16)/255.,
            int(c[4:6],16)/255.)
                    

def make_sub_palette(nbins, col1, col2):
    '''
    Fill nbins with colors between col1 inclusive and col2 exclusive.
    Colors are triples of floats in [0,1].
    '''
    ret = []
    for ind in range(nbins):
        c = []
        for icol in range(3):
            c.append(ind*(col2[icol] - col1[icol])/float(nbins) + col1[icol])
        ret.append(tuple(c))
    return ret
        

def make_palette(ncols, waypoints):
    '''
    waypoint = (location, color)
    '''
    waypoints.sort()
    total_dist = waypoints[-1][0] - waypoints[0][0]
    binsper = float(ncols)/total_dist
    wp_rgbs = [(w[0], to_rgb(w[1])) for w in waypoints]
    last_wp = wp_rgbs[0]
    palette = list()
    for wp in wp_rgbs[1:]:
        nbins = int((wp[0] - last_wp[0])*binsper)
        palette += make_sub_palette(nbins, last_wp[1], wp[1])
        last_wp = wp
    return palette


# some named palettes
palettes = dict(
    gray = [(0,'0xEEEEEE'), (1,'0x000000')],
    fire = [(0.0,(1,1,0.1)), (0.5,(1,0.2,0.2)), (1, (0.5,0.5,0.5))],
    ember = [(0, (0.5,0.5,0.5)),  (0.25,(1,1,0.1)),  (0.5,(1,0.2,0.2)) ],
    usa = [(0,(0,0,1)), (0.5,(1,1,1)), (1.0,(1,0,0))],
)


def root_palette(ncol, color_desc, style = None):
    if isinstance(color_desc, type("")):
        color_desc = palettes.get(color_desc)
    if not color_desc:
        raise ValueError('no color description given')

    pal = array('i')
    for rgb in make_palette(ncol, color_desc):
        pal.append(ROOT.TColor.GetColor(*rgb))
    if not style:
        style = ROOT.gStyle
    style.SetPalette(ncol, pal)
    style.SetNumberContours(ncol)
    return

