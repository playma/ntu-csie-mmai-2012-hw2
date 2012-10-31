# -*- coding:utf-8 -*-
#
# MMAI Homework #2
# CBIR System
#
# fv_color.py
#
# Qing-Cheng Li
# R01922024
# qingcheng.li@qcl.tw / r01922024@csie.ntu.edu.tw
#

import os
import sys
import time
import Image
import colorsys

def fv_color(imagePath):
    """
    Return color feature vector of image.

    Color Space: HSV
    
    HSV histogram.
    """

    # histogram initialize
    histogram = []


    cache_name = imagePath + '.color'

    # if cache file doesn't exists, generate it.
    if os.path.exists(cache_name):
        f = open(cache_name,'r')
        for line in f:
            histogram.append(float(line))
        f.close()
    else:
        print 'Generate feature vector (color)'
        print time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print 'Read',imagePath
    
        hist = []
        for x in range(0,18):
            hist.append([])
            for y in range(0,3):
                hist[x].append([])
                for z in range(0,3):
                    hist[x][y].append(0)

        # read image
        image = Image.open(imagePath)

        # get width and height of image
        width,height = image.size

        # convert to RGB 
        image = image.convert('RGB')

        # build histogram
        for x in range(0,width):
            for y in range(0,height):
                red,green,blue = image.getpixel((x,y))
                h,s,v = colorsys.rgb_to_hsv(red/255.0,green/255.0,blue/255.0)
                            
                if h >= 1.0:
                    h = 0.9999
                if s >= 1.0:
                    s = 0.9999
                if v >= 1.0:
                    v = 0.9999

                h = int(h * 18)
                s = int(s * 3)
                v = int(v * 3)
                           
                hist[h][s][v] = hist[h][s][v] + 1

        # write to cache file
        f = open(cache_name,'w')

        for x in range(0,18):
            for y in range(0,3):
                for z in range(0,3):
                    

                    # normalize
                    result = hist[x][y][z]/float(width*height)
                    
                    # ensure the cache file and hist has the
                    # same value.
                    f.write(str(result)+'\n')
                    histogram.append(float(str(result)))
                                

        print 'Write to',cache_name
        print ''

    print histogram
    return histogram

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage:'
        print 'python fv_color.py image_path'
    else:
        fv_color(sys.argv[1])

