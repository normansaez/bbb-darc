'''
-Model to creat covariance matrix as in Butterley 2006
and Wilson,Jenkins 1996.
-Fitting of model to empirical covariance matrix
to substract turbulence profile and instrumental
deviations as in Vidal 2012.

Author: Nicolas S. Dubost
Last Update: 27/10/2014
'''


import numpy as np
import postprocess as pp
import pylab as pl
from BeagleDarc.Model import Camera
import FITS

def subapmap(cam):
    '''
    the map is a list object with the (i,j)
    coordinate of every subap
    '''
    subapflag = FITS.Read(cam.subapflag)[1]
    cam.nsubaps
    cam.allsubaps
    smap = []
    for i in range(subapflag.shape[0]):
        for j in range(subapflag.shape[1]):
            if subapflag[i,j]==1:
                smap.append((i,j))
    
    return smap


