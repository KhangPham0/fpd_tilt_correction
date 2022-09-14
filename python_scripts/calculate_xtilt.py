#!/usr/bin/env python3

import numpy as np
import argparse
from pathlib import Path
import sys

# to calculate the incident position of a particle
# on the focal plane according to the xf equation (eq. 5) 
# in https://doi.org/10.1016/0029-554X(75)90121-4
def focalPlane(h, alpha, x1, x2, S):
    
    # tangent and cotangent of alpha
    tga = np.sin(alpha) / np.cos(alpha)
    ctga = np.cos(alpha) / np.sin(alpha)

    num = (x2*S/np.sqrt(1 + tga**2)) - (x2 - x1)*h
    deno = (S/np.sqrt(1 + tga**2)) - ((x2 - x1)/np.sqrt(1 + ctga**2))

    xf = num / deno

    # rounding xf to 12 digits
    rounded_xf = np.array([float('{:.12e}'.format(val)) for val in xf])

    return rounded_xf

#####################################################
###                                               ###
###                 MAIN FUNCTION                 ###
###                                               ###
#####################################################
# to control what the whole program does
def main(file, hLow, hHigh, sp, alpha):

    # check if file exist
    inFile = Path(file)
    if inFile.is_file() != True:
        sys.exit(f"file does not exits!")
    
    # load the file
    # note that these values should have units of mm based on Gordon's code
    x1, x2 = np.loadtxt(inFile, unpack=True)

    # array of hold a list of H
    Hs = np.arange(hLow, hHigh+sp, sp)

    # distance between wires (got this value from Gordon's
    # code (specifically, the Wire_Dist() function))
    S = 42.8625 # mm

    # convert Hs (which should only be fractions at this point)
    # to real distances
    relHs = Hs*S

    # convert alpha to radian
    alpha *= np.pi / 180.0

    # calculate the focal plane position for all H
    for i in range(len(relHs)):

        fPos = focalPlane(relHs[i], alpha, x1, x2, S)

        # write the results to a file
        np.savetxt(f"{Hs[i]:.4f}H_{alpha:.1f}_degrees_xavg_tilt.txt", fPos, fmt='%.12e')


# everything starts here
if __name__ == '__main__':

    # handle the command line arguments
    parser = argparse.ArgumentParser(description="Calculate the position where the particle is\
                                            incident on the focal plane based on the tilt angle,\
                                            alpha, and the distance from the focal plane to the\
                                            origin, H (to be treated as fraction of the total\
                                            distance between the two wires). The program is used\
                                            to produce a range of files based on different combo\
                                            of H and alpha.")
    parser.add_argument("file", metavar="x1x2_file", type=str, 
                                  help="a text file that contains two columns of x1 and x2 values,\
                                     where x's are the positions where the particle is incident\
                                     on wire1 and wire2, respectively")
    parser.add_argument("hLow", type=float, help="start of H")
    parser.add_argument("hHigh", type=float, help="end of H")
    parser.add_argument("sp", metavar="hSpacing", type=float, help="spacing between each H")
    parser.add_argument("alpha", type=float, help="tilt angle")

    # pass all of the arguments into args
    args = parser.parse_args()
    
    # pass the args into main function
    main(**vars(args))