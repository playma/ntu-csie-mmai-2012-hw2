# -*- coding:utf-8 -*-
#
# MMAI Homework #2
# CBIR System
#
# im_query.py
#
# Qing-Cheng Li
# R01922024
# qingcheng.li@qcl.tw / r01922024@csie.ntu.edu.tw
#

import os
import sys 

from fv_sim import fv_sim
from fv_color import fv_color
from fv_texture import fv_texture

dataset_dir = 'dataset'
queryset_dir = 'dataset/00queries00'

def im_query():

    dataset = []
    queryset = []

    # Read dataset
    for root,dirs,files in os.walk(dataset_dir):
        
        if queryset_dir in root and root.index(queryset_dir) == 0:
            pass
        else:
            #print root,dirs,files
            category = root.split('/')[-1]
            for filename in files:
                if filename.split('.')[-1].lower() in ['jpg','jpeg']:
                    imagePath = os.path.join(root,filename)
                    
                    dataset.append({'imagePath':imagePath,
                                    'category':category,
                                    'color':fv_color(imagePath),
                                    'texture':fv_texture(imagePath)})

    print dataset

    # Read query
    for root,dirs,files in os.walk(queryset_dir):
        category = root.split('/')[-1]
        for filename in files:
            if filename.split('.')[-1].lower() in ['jpg','jpeg']:
                imagePath = os.path.join(root,filename)

                queryset.append({'imagePath':imagePath,
                                 'category':category,
                                 'color':fv_color(imagePath),
                                 'texture':fv_texture(imagePath)})

    print queryset

if __name__ == '__main__':
    im_query()
