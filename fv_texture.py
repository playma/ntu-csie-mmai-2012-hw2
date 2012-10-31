# -*- coding:utf-8 -*-
#
# MMAI Homework #2
# CBIR System
#
# fv_texture.py
#
# Qing-Cheng Li
# R01922024
# qingcheng.li@qcl.tw / r01922024@csie.ntu.edu.tw
#

import os
import sys
import time
import numpy
import Image
import colorsys

from gaborconvolve import gaborconvolve

def fv_texture(imagePath):
    """
    Return texture feature vector of image.

    Using Gabor texture.
    """

    texture_vector = []

    cache_name = imagePath+'.texture'

    # if cache exist
    if os.path.exists(cache_name):
        f = open(cache_name,'r')
        for line in f:
            texture_vector.append(float(line))
        f.close()
    
    # otherwise, generate it.
    else:
        f = open(cache_name,'w')

        nscale = 4
        norient = 6
        minWaveLength = 3
        mult = 2
        sigmaOnf = 0.65

        EO = gaborconvolve(imagePath,nscale,norient,minWaveLength,mult,sigmaOnf) 

        for o in range(0,norient):
            for s in range(0,nscale):

                result = numpy.abs(EO[o][s])

                std  = numpy.std(result)
                mean = numpy.mean(result)
                
                # to ensure this vector will be the same as
                # the vector read from cache file.
                texture_vector.append(float(str(std)))
                texture_vector.append(float(str(mean)))
                
                # write to cache file.
                f.write(str(std)+'\n')
                f.write(str(mean)+'\n')

        f.close()

    return texture_vector



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage:'
        print 'python fv_texture.py image_path'
    else:
        fv_texture(sys.argv[1])

