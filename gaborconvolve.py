# -*- coding: utf-8 -*-
#
#   gaborconvolve.py
#
#   translate from gaborconvolve.m
#
#   Qing-Cheng Li 
#   R01922024
#   qingcheng.li@qcl.tw
#

#
#   nscale        = 4
#   norient       = 6
#   minWaveLength = 3
#   mult          = 2
#   sigmaOnf      = 0.65
#

import os
import sys
import numpy
import Image

def gaborconvolve(imagePath,nscale,norient,minWaveLength,mult,sigmaOnf):
    """
    GABORCONVOLVE - function for convolving image with log-Gabor filters
    """

    # rgb -> gray
    im = Image.open(imagePath).convert("L")
    (cols,rows) = im.size

    if cols%2 != 0:
        cols = cols - 1
    if rows%2 != 0:
        rows = rows - 1

    # resize image to reduce calculate time.
    cols = cols/2
    rows = rows/2
    im = im.resize((cols,rows),Image.ANTIALIAS)

    imagefft = numpy.fft.fft2(im)

    x_range = [ x/float(cols) for x in range(-cols/2,cols/2) ]
    y_range = [ y/float(rows) for y in range(-rows/2,rows/2) ]
    x,y = numpy.meshgrid(x_range,y_range)

    radius = numpy.sqrt(x*x+y*y)
    theta = numpy.arctan2(y,x)

    radius = numpy.fft.ifftshift(radius)
    radius[0][0] = 1.0
    theta = numpy.fft.ifftshift(theta)

    sintheta = numpy.sin(theta)
    costheta = numpy.cos(theta)

    # low pass filter 
    lp = numpy.fft.ifftshift( 1.0/(numpy.power((numpy.sqrt(x*x+y*y) / 0.45),(2*15)) + 1.0) )

    BP = []
    logGabor = []

    for s in range(0,nscale):
        wavelength = minWaveLength*mult**s
        fo = 1.0 / wavelength
        l = numpy.exp( ( -(numpy.log(radius/fo))**2 )  /   (2.0*numpy.log(sigmaOnf)**2)  )
        l = l*lp
        l[0][0] = 0.0
    
        logGabor.append(l)
        # TODO/FIXME
        BP.append(numpy.fft.ifft2(imagefft*l)) 

    logGabor = numpy.array(logGabor)
    BP = numpy.array(BP)

    EO = []

    for o in range(0,norient):
        angl = o*numpy.pi/norient
        wavelength = minWaveLength

        ds = sintheta * numpy.cos(angl) - costheta * numpy.sin(angl)
        dc = costheta * numpy.cos(angl) + sintheta * numpy.sin(angl)
        dtheta = numpy.abs(numpy.arctan2(ds,dc))
        dtheta = numpy.minimum(dtheta*norient/2.0,numpy.pi)

        spread = (numpy.cos(dtheta)+1.0)/2.0

        tmpEO = []
        for s in range(0,nscale):
            Filter = logGabor[s]*spread

            # TODO/FIXME
            result = numpy.fft.ifft2(imagefft*Filter)
            tmpEO.append(result)

        EO.append(numpy.array(tmpEO))

    EO = numpy.array(EO)

    # EO[orient][scale]
    return EO


