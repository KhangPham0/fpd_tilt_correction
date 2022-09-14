#!/usr/bin/env python3

import ROOT
import numpy as np
import re
import argparse
import plot_specific_region as psr

# to plot histograms with ROOT
def plotHists(inFiles, bins):

    # number of files
    nFiles = len(inFiles)

    # load in all files and get values of H out of the filenames
    filesArr = np.empty(nFiles, dtype=np.ndarray)
    Hs = np.empty(nFiles)
    for i in range(nFiles):

        filesArr[i] = np.loadtxt(inFiles[i])

        # get values of H from file names to label the histogram
        Hs[i], alpha_tmp = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", inFiles[i].name)
    
    # note that -300 and 300 are default values of SPS eventbuilder for the full histo range
    xlows = np.full(nFiles, -300)
    xhighs = np.full(nFiles, 300)
    canvas, histos = psr.plotThem(nFiles, filesArr, Hs, xlows, xhighs, bins)

    return canvas


#####################################################
###                                               ###
###                 MAIN FUNCTION                 ###
###                                               ###
#####################################################
# to control what the whole program does
def main(files, nbinsx):

    results = plotHists(files, nbinsx)

    return results


# everything starts here
if __name__ == '__main__':

    # handle the command line arguments
    parser = argparse.ArgumentParser(description="Fit peak or peaks within a specific region")
    parser.add_argument('files', type=argparse.FileType('r'), nargs='+', help="text files of x values")
    parser.add_argument("-bin", "--nbinsx", type=int, default=-10, help="number of bins; if no value\
                                                                    is given, bins = xhigh - xlow is used")

    # pass all of the arguments into args
    args = parser.parse_args()

    #print(args.files[0].name)
    
    # pass the args into main function
    results = main(**vars(args))

    # this line is needed for the canvas to stay on screen
    # alternatively, run this script with "python3 -i ..."
    ROOT.gApplication.Run()
