import ROOT

import sys

from plot_util import  multifill, framedraw, drawmany, multileg
from plot_util import hist1f, hist2f, hist1i

def plot_income(tree, canvas, logy = False):
    hists = multifill(tree, (50, 0, 1e3), [
        ('personal_income', 'Personal Income'),
        ('household_income', 'Household Income')])

    canvas.SetLogy(logy)
    frame = framedraw('Income', ('kilobucks',''), (0,0,500,200))
    leg = multileg((0.6,0.6, 0.3,0.2), 
                   [(h,'#splitline{%s}{\nmean = $%.0fk, rms = $%0.fk}' \
                     % (h.GetTitle(), h.GetMean(), h.GetRMS())) for h in hists])
    leg.SetTextSize(0.03)
    return drawmany(hists + [leg]) + [frame]

def plot_dui(tree, canvas):
    canvas.Divide(1,2)

    pad = canvas.cd(1)
    hists = multifill(tree, (12,0,12), [
        ('dui_charged', 'DUIs charged'),
        ('dui_convicted', 'DUIs convicted')])
    frame = framedraw('DUIs', ('number of DUIs charged/convicted',''), (0,0,12,400), canvas=pad)
    leg = multileg((0.6,0.6, 0.3,0.2), [(h,h.GetTitle()) for h in hists])
    ret = drawmany(hists + [leg]) + [frame]
    
    canvas.cd(2)
    #h2d = ROOT.TH2D("dui","DUIs Convictions vs Arrests", 12,0,12, 6, 0, 6)
    h2d = hist2f("dui","DUIs Convictions vs Arrests", 12,0,12, 6, 0, 6)
    h2d.GetXaxis().SetTitle('Number of DUIs charged')
    h2d.GetYaxis().SetTitle('Number of DUIs convicted')
    ret.append(h2d)
    tree.Draw("dui_convicted:dui_charged>>dui","","colz")
    h2d.Draw("colz")
    canvas.Update()
    return ret


def plot_perweek(tree, canvas):
    #h = ROOT.TH2F("drinks","Money spent vs amount of drinking per week",25,0,500,25,0,500)
    h = hist2f("drinks","Money spent vs amount of drinking per week",25,0,500,25,0,500)
    tree.Draw("dollars_per_week:units_per_week>>drinks","","colz")
    h.GetXaxis().SetTitle("Units per week")
    h.GetYaxis().SetTitle("Money spent per week")
    canvas.Update()
    return h


def plot_homealone(tree, canvas):
    hists = multifill(tree, (25,0,100), [
        ('percent_home', 'Percent of time Drinking at Home'),
        ('percent_alone', 'Percent of time Drinking Alone')])
    frame = framedraw('Home/Alone', ('percent',''), (0,0,100,150))
    leg = multileg((0.2,0.6, 0.3,0.2), [(h,h.GetTitle()) for h in hists])
    return drawmany(hists + [leg]) + [frame]
    

def plot_sick(tree, canvas):
    ROOT.gStyle.SetOptStat(0)
    #h = ROOT.TH1I('sick','How often did you call in sick?', 7,0,7)
    h = hist1i('sick','How often did you call in sick?', 7,0,7)
    tree.Draw("sick>>sick","","goff")
    from converters import how_often
    xa = h.GetXaxis()
    for i,l in enumerate(how_often):
        xa.SetBinLabel(i+1,l) 
    h.Draw()
    return h

from collections import defaultdict

def plot_methods(tree, canvas):
    from converters import what_helped
    ROOT.gStyle.SetOptStat(0)
    canvas.Divide(1,1)
    pad = canvas.cd(1)
    pad.SetBottomMargin(0.2)

    # make histogram stack taking care of labeling and order by frequency

    counters = [defaultdict(int) for x in range(4)]
    for ent in tree:
        for n in range(3):
            v = getattr(ent.large, 'method_%d'%(n+1,))
            counters[0][v] += 1 # total
            counters[n+1][v] += 1
    meth_tot_bin = [(v,k) for k,v in counters[0].items()]
    meth_tot_bin.sort()
    nbins = len(meth_tot_bin)

    hists = list()
    for hname in 'ha h1 h2 h3'.split():
        h = hist1i(hname, 'Methods for sobriety', nbins, 0, nbins)
        hists.append(h)

    for count, (method_tot, method_bin) in enumerate(meth_tot_bin):
        bin_number = count+1
        for hnum, hist in enumerate(hists): # run through hists, setting their bin
            hist.SetBinContent(bin_number, counters[hnum][method_bin])
            name = what_helped[method_bin]
            h.GetXaxis().SetBinLabel(bin_number, name)
        
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue]
    for n in range(3):
        h = hists[n+1]
        h.SetLineColor(colors[n])

    hists[2].Add(hists[1])
    hists[3].Add(hists[2])
    hists[3].Draw()
    hists[2].Draw("same")
    hists[1].Draw("same")

    tits = ['Primary choice','Secondary choice','Tertiary choice']
    leg = multileg((0.2,0.6, 0.25,0.15), zip(hists[1:], tits))
    leg.Draw("same")

    canvas.Update()
    return [leg] + hists


# make a series of plots following a common pattern
from converters import how_often
_a_b_params = dict(
    sickness = dict(title = 'How often did you call in sick (%s)',
                    bins = (7,0,7), labels = how_often,
                    quant = 'sick'),
    units = dict(title = 'Units per week (%s)',
                 bins = (10,0,100),
                 quant = 'units_per_week'),
)
def _a_b_compare(tree, canvas, question, flavor):
    par = _a_b_params[question]
    quant, bins, title = par['quant'], par['bins'], par['title']%flavor
    func = flavor.lower() + 'ness'
    labels = par.get('labels')

    ROOT.gStyle.SetOptStat(0)
    ha = hist1i('ha', title, *bins)
    h0 = hist1i('h0', title, *bins)
    hn = hist1i('hn', title, *bins)
    
    ha.Sumw2()
    ha.SetLineColor(ROOT.kBlack)
    h0.SetLineColor(ROOT.kRed)
    hn.SetLineColor(ROOT.kBlue)

    if labels:
        xa = ha.GetXaxis()
        for i,l in enumerate(labels):
            xa.SetBinLabel(i+1,l) 


    tree.Draw(quant+">>ha", "", "goff")
    tree.Draw(quant+">>h0", func+"() == 0", "goff")
    tree.Draw(quant+">>hn", func+"() > 0",  "goff")

    flavor += "'er"
    leg = multileg((0.7, 0.7, 0.18,0.15), [ (ha, 'all'), (hn, flavor), (h0, "not %s"%flavor) ])
    ha.SetMinimum(0)
    ha.Draw()
    return drawmany((ha,h0,hn,leg))

# for some reason a simple lambda doesn't work
class _a_b_bind:
    def __init__(self, question, flavor):
        self.question = question
        self.flavor = flavor
    def __call__(self, tree, canvas):
        return _a_b_compare(tree, canvas, self.question, self.flavor)

def _generate_methods():
    'Generate some pattern based methods'
    thismodule = sys.modules[__name__]
    for toplot in ('sickness', 'units'):
        for flavor in ('AA', 'IRC', 'rSD', 'None', 'SMART'):
            method_name = 'plot_%s_%s'%(toplot, flavor.lower())
            setattr(thismodule, method_name, _a_b_bind(toplot, flavor))
_generate_methods()


# def plot_sick_aa(tree, canvas): return _sickness(tree, canvas, 'AA', 'aaness')
# def plot_sick_irc(tree, canvas): return _sickness(tree, canvas, 'IRC', 'ircness')
# def plot_sick_rsd(tree, canvas): return _sickness(tree, canvas, 'r/SD', 'rsdness')
# def plot_sick_none(tree, canvas): return _sickness(tree, canvas, 'none', 'noneness')




def plot_breakfast(tree, canvas):
    #h = ROOT.TH1I('breakfast','Favorite Syrup Substrate', 3,0,3)
    h = hist1i('breakfast','Favorite Syrup Substrate', 3,0,3)
    h.SetLineWidth(2)
    h.Sumw2()
    tree.Draw('q345>>breakfast',"","goff")
    return h

