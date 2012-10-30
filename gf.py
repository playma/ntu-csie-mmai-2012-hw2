# -*- coding: utf-8 -*-

import os
import sys
import math
import numpy
import Image
import colorsys


nscale = 4
norient = 6
minWaveLength = 3
mult = 2
sigmaOnf = 0.65



im_origin = Image.open('qcl.jpg')

im = im_origin.convert("L")

imagefft = numpy.fft.fft2(im)

(cols,rows) = im.size

if cols%2 == 0:
    x_range = [ x/float(cols) for x in range(-cols/2,cols/2) ]
else:
    x_range = [ x/float(cols-1) for x in range(-(cols-1)/2,(cols-1)/2) ]

if rows%2 == 0:
    y_range = [ y/float(rows) for y in range(-rows/2,rows/2) ]
else:
    y_range = [ y/float(rows-1) for y in range(-(rows-1)/2,(rows-1)/2) ]

x,y = numpy.meshgrid(x_range,y_range)

radius = numpy.sqrt(x*x+y*y)
theta = numpy.arctan2(y,x)

radius = numpy.fft.ifftshift(radius)
theta = numpy.fft.ifftshift(theta)

radius[0][0] = 1.0
sintheta = numpy.sin(theta)
costheta = numpy.cos(theta)

lp = numpy.fft.ifftshift( 1.0/(numpy.power((numpy.sqrt(x*x+y*y) / 0.45),(2*15)) + 1.0) )


BP = []
logGabor = []

for s in range(0,nscale):
    wavelength = minWaveLength*mult**s
    fo = 1.0 / wavelength
    l = numpy.exp( (- (numpy.log(radius/fo))**2 )  /   (2.0*numpy.log(sigmaOnf)**2)  )
    l = l*lp
    l[0][0] = 0.0
    
    logGabor.append(l)

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

        result = numpy.fft.ifft2(imagefft*Filter)
        tmpEO.append(result)

        result = numpy.abs(result)
        print numpy.mean(result),numpy.std(result)

    EO.append(numpy.array(tmpEO))

EO = numpy.array(EO)

# EO[orient][scale]

