# -*- coding:utf-8 -*-
#
# MMAI Homework #2
# CBIR System
#
# fv_sim.py
#
# Qing-Cheng Li
# R01922024
# qingcheng.li@qcl.tw / r01922024@csie.ntu.edu.tw

import math

def fv_sim(v1,v2):
    """
    Compute L1 destance between v1 and v2
    """

    if len(v1) == len(v2):
        d = 0
        for i in range(0,len(v1)):
            d = d + math.fabs(v1[i]-v2[i])
        return d
    else:
        print 'Length of v1 != v2'
        return -1

