#!/usr/bin/env python3

import ROOT
import numpy as np
import sys
import re

# check for number of files
num_files= len(sys.argv) - 1

# load in all files
files = np.empty(num_files, dtype=np.ndarray)
for i in range(num_files):
    files[i] = np.loadtxt(sys.argv[i+1])

# make a canvas, an array of hist(s)
c1 = ROOT.TCanvas('c1', 'Tilt Combinations', 300, 0, 1300, 1000) # (name, title, top left x coord, top left y coord, window x width, window y width)
hists = np.empty(num_files, dtype=ROOT.TH1F)

# fill the hist(s) and also find the max value of Y-axis of plot(s)
binMax = 0
tmpMax = 0
for j in range(num_files):
    hists[j] = ROOT.TH1F(f'{j}', sys.argv[j+1], 1000, -150, 300) # (name, title, numOfBins, xlow, xup)

    # get values of H from file names to label the histogram
    H, alpha = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", sys.argv[j+1])
    hists[j].SetYTitle(f'{float(H):.2f}')

    # some formatting for y-axis title so that it's visible
    hists[j].SetTitleOffset(0.1, 'Y')
    hists[j].SetTitleSize(0.3,'Y')
    hists[j].GetYaxis().SetLabelSize(0)
    #hists[j].GetXaxis().SetLabelSize(0)

    # fill histogram with values from given file(s)
    for val in files[j]:
        hists[j].Fill(val)
    tmpMax = hists[j].GetMaximum()
    if binMax < tmpMax: binMax = tmpMax

# plot hist(s)
c1.Divide(1,num_files,0,0) # divide canvas into chunks based on no. of files
for k in range(num_files):
    c1.cd(k+1)
    #ROOT.gPad.SetLogy() # uncomment to set y-axis to log scale
    #hists[k].SetAxisRange(0, int(1.1*binMax), 'Y') # same purpose as the line below
    hists[k].SetMaximum(int(1.1*binMax)) # set max range to 10 percent higher than the tallest peak
    #hists[k].Draw("PE1X0") # draw unconnected points with error bars
    #hists[k].Draw("EHISTO") # draw connected points with error bars
    hists[k].Draw()

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111)
c1.Update()

# this line is needed for the canvas to stay on screen
# alternatively, run this script with "python3 -i ..."
ROOT.gApplication.Run()
