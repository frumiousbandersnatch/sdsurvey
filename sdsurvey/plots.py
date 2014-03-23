#!/usr/bin/env python

import ROOT

from plot_util import default_canvas



def printit():
    import data, style, plotters, large
    style.setstyle()

    d = data.Data('large', large.desc, large.extracpp)
    d.loadcsv('data/SD Survey 2014 - Long.csv')

    canvas = default_canvas()
    canvas.Print('survey.pdf[','pdf')
    for maybe in dir(plotters):
        if not maybe.startswith('plot_'):
            continue
        print ('Plotting: "%s"' % maybe)
        canvas.Clear()
        meth = getattr(plotters, maybe)
        keepalive = meth(d.tree, canvas)
        canvas.Print('survey.pdf','pdf')
    canvas.Print('survey.pdf]','pdf')


def plotone(tree, plotter):
    import style, plotters
    style.setstyle()
    c = default_canvas()
    c.Clear()
    if isinstance(plotter, type("")):
        plotter = getattr(plotters, plotter)
    return plotter(tree, c)


if '__main__' == __name__:
    printit()
