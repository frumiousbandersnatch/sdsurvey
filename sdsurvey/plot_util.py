import ROOT

def histX(klass, *args):
    h = klass(*args)
    #h.SetDirectory(0)
    return h
def hist1i(*args): return histX(ROOT.TH1I, *args)
def hist1f(*args): return histX(ROOT.TH1F, *args)
def hist2i(*args): return histX(ROOT.TH2I, *args)
def hist2f(*args): return histX(ROOT.TH2F, *args)

def default_canvas():
    if hasattr(ROOT, 'default_canvas'):
        return ROOT.default_canvas
    c = ROOT.TCanvas("default_canvas", "Canvas")
    c.SetGridx(True)
    c.SetGridy(True)
    ROOT.SetOwnership(c,0)
    return c

def framedraw(tit, lab, desc, canvas = default_canvas()):
    frame = canvas.DrawFrame(*desc)
    frame.SetTitle(tit)
    frame.GetXaxis().SetTitle(lab[0])
    frame.GetYaxis().SetTitle(lab[1])
    return frame
    
def drawmany(objs, canvas = default_canvas()):
    for obj in objs: 
        obj.Draw("same")
    canvas.Update()
    return objs


def numberwang(tree, h, quant):
    #h = ROOT.TH1F('income','Personal Income', 100, 0, 1e6)
    h.Sumw2()
    for ent in tree:
        try:
            val = float(getattr(ent.large, quant))
        except ValueError:
            val = -1
        h.Fill(val)
    return h


def multifill(tree, bins, quants):
    ret = []
    colors = [1,2,4,6]
    for count,(quant,title) in enumerate(quants):
        #h = ROOT.TH1F('h_'+quant, title, *bins)
        h = hist1f('h_'+quant, title, *bins)
        numberwang(tree, h, quant)
        ret.append(h)
        h.SetLineColor(colors[count+1])
        h.SetMarkerColor(colors[count+1])
    return ret

def multileg(shape, objtits):
    x,y,w,h = shape
    leg = ROOT.TLegend(x,y,x+w,y+h)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    for h, t in objtits:
        leg.AddEntry(h,t) 
    return leg
