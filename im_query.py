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

from operator import itemgetter

# Dataset path
dataset_dir = 'dataset'

# Query image path
queryset_dir = 'dataset/00queries00'

def im_query():

    # Report file
    report = open('report.html','w')

    dataset = {}
    queryset = []

    # Read dataset
    data_id = 0
    for root,dirs,files in os.walk(dataset_dir):
        
        if queryset_dir in root and root.index(queryset_dir) == 0:
            pass
        else:
            #print root,dirs,files
            category = root.split('/')[-1]
            for filename in files:
                if filename.split('.')[-1].lower() in ['jpg','jpeg']:
                    imagePath = os.path.join(root,filename)
                    data_id = data_id + 1 
                    dataset[data_id] = {'id':data_id,
                                    'imagePath':imagePath,
                                    'category':category,
                                    'color':fv_color(imagePath),
                                    'texture':fv_texture(imagePath)}

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

    print '# of dataset:',len(dataset)
    print '# of query',len(queryset)

    # Auto generate report.
    report.write("<!DOCTYPE html>\n<html>\n<head>\n<title>CBIR System - MMAI Homework 2</title>\n<meta charset='utf-8' />\n</head>\n")
    report.write("<body>\n<h1>CBIR System</h1>\n<p>MMAI Homework #2</p>\n<p>Qing-Cheng Li<br/>R01922024<br/>qingcheng.li@qcl.tw</p>\n")

    pr_color = {}
    pr_texture = {}
    pr_fusion = {}

    query_id = 0
    for query in queryset:
        query_id = query_id + 1

        query_cat = query['category']
        
        report.write("<h2>Query #%d</h2>\n" % (query_id))
        report.write("<p><img width='200px' src='%s' /><br/>Category: %s</p>\n" % (query['imagePath'],query_cat))
        
        result_color = {}
        result_texture = {}
        for image_id in dataset:
            image = dataset[image_id]

            # calculate sim
            result_color[image_id] = fv_sim(query['color'],image['color'])
            result_texture[image_id] = fv_sim(query['texture'],image['texture'])

        # sort result
        result_color = sorted(result_color.iteritems(),key=itemgetter(1))
        result_texture = sorted(result_texture.iteritems(),key=itemgetter(1))
        
        # fusion (borda count)
        f_color = {}
        f_texture = {}
        result_fusion = {}
        
        k = 0
        N = float(len(result_color))
        for k in range(0,len(result_texture)):
            
            result_id,score = result_color[k]
            f_color[result_id] = 1.0 - k/N
            
            result_id,score = result_texture[k]
            f_texture[result_id] = 1.0 - k/N
            
            k = k + 1

        # avg
        for k in range(1,len(result_texture)+1):
            result_fusion[k] = ( f_color[k] + f_texture[k] ) / 2

        result_fusion = sorted(result_fusion.iteritems(),key=itemgetter(1),reverse=True)

        # output the result of color
        report.write("<h3>Color</h3>\n")
        n = 0
        r = 0
        recall = 0
        precision = 0 
        prc = []
        path = []
        for result in result_color[:10]:
            n = n + 1
            result_id,score = result
            image = dataset[result_id]
            path.append(image['imagePath'])
            category = image['category']

            if category == query_cat:
                r = r + 1
                recall = r/10.0
            precision = r/float(n)
            prc.append((recall,precision)) 
            
        report.write("<table border='1'>\n")
        report.write("<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>\n")
        report.write("<tr><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td></tr>\n" % (path[0],path[1],path[2],path[3],path[4]))
        report.write("<tr><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td></tr>\n")
        report.write("<tr><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td></tr>\n" % (path[5],path[6],path[7],path[8],path[9]))
        report.write("</table>\n")
        if not query_cat in pr_color:
            pr_color[query_cat] = []
        pr_color[query_cat].append(prc)


        # output the result of texture
        report.write("<h3>Texture</h3>\n")
        n = 0
        r = 0
        recall = 0
        precision = 0 
        prt = []
        path = []
        for result in result_texture[:10]:
            n = n + 1
            result_id,score = result
            image = dataset[result_id]
            path.append(image['imagePath'])
            category = image['category']

            if category == query_cat:
                r = r + 1
                recall = r/10.0
            precision = r/float(n)
            prt.append((recall,precision)) 
            
        report.write("<table border='1'>\n")
        report.write("<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>\n")
        report.write("<tr><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td></tr>\n" % (path[0],path[1],path[2],path[3],path[4]))
        report.write("<tr><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td></tr>\n")
        report.write("<tr><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td></tr>\n" % (path[5],path[6],path[7],path[8],path[9]))
        report.write("</table>\n")

        if not query_cat in pr_texture:
            pr_texture[query_cat] = []
        pr_texture[query_cat].append(prt)

        # output the result of fusion
        report.write("<h3>Fusion</h3>\n")
        n = 0
        r = 0
        recall = 0
        precision = 0 
        prf = []
        path = []
        for result in result_fusion[:10]:
            n = n + 1
            result_id,score = result
            image = dataset[result_id]
            path.append(image['imagePath'])
            category = image['category']

            if category == query_cat:
                r = r + 1
                recall = r/10.0
            precision = r/float(n)
            prf.append((recall,precision)) 
            
        report.write("<table border='1'>\n")
        report.write("<tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr>\n")
        report.write("<tr><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td></tr>\n" % (path[0],path[1],path[2],path[3],path[4]))
        report.write("<tr><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td></tr>\n")
        report.write("<tr><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td><td><img src='%s' width='100px' /></td></tr>\n" % (path[5],path[6],path[7],path[8],path[9]))
        report.write("</table>\n")
        if not query_cat in pr_fusion:
            pr_fusion[query_cat] = []
        pr_fusion[query_cat].append(prf)


        # output pr table
        report.write("<h3>Precision/Recall</h3>\n")
        report.write("<table border='1'>\n")
        report.write("<tr><td colspan='2'>Color</td><td colspan='2'>Texture</td><td colspan='2'>Fusion</td></tr>\n")
        report.write("<tr><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td></tr>\n")
        for i in range(0,10):
            report.write("<tr><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td></tr>\n" % (prc[i][0],prc[i][1],prt[i][0],prt[i][1],prf[i][0],prf[i][1]))
            
        report.write("</table>\n")

    report.write("<h2>Category</h2>\n")
    for category in pr_color:
        report.write("<h3>%s</h3>" % (category) )
        report.write("<table border='1'>\n")
        report.write("<tr><td colspan='2'>Color</td><td colspan='2'>Texture</td><td colspan='2'>Fusion</td></tr>\n")
        report.write("<tr><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td></tr>\n")
        for i in range(0,10):
            rc = 0.0
            pc = 0.0
            rt = 0.0
            pt = 0.0
            rf = 0.0
            pf = 0.0
            for j in range(0,len(pr_color[category])):
                rc = rc + pr_color[category][j][i][0]
                pc = pc + pr_color[category][j][i][1]
                rt = rt + pr_texture[category][j][i][0]
                pt = pt + pr_texture[category][j][i][1]
                rf = rf + pr_fusion[category][j][i][0]
                pf = pf + pr_fusion[category][j][i][1]
            rc = rc / len(pr_color[category])
            pc = pc / len(pr_color[category])
            rt = rt / len(pr_color[category])
            pt = pt / len(pr_color[category])
            rf = rf / len(pr_color[category])
            pf = pf / len(pr_color[category])
            
            report.write("<tr><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td><td>%f</td></tr>\n" % (rc,pc,rt,pt,rf,pf))
                
        report.write("</table>\n")

    report.write("</body>\n</html>\n")
    report.write("</body>\n</html>\n")
    report.close()

if __name__ == '__main__':
    im_query()
