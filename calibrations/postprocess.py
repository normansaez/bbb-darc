'''
Module containing pos-process functions to format data,
calculate slopes and all of the other things I haven't 
yet thought of.

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: May the 20th, 2014
'''

import FITS
#import darc
import numpy as np
#import os
from numpy import unravel_index
import pylab as pl
#import random
#from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star
#import ConfigParser
#import scipy
#from scipy import signal

def im2slope(path,imname,filename,star_list,camera='SH'):
    imgs = FITS.Read(path+inname)[1]
    cam = Camera(camera)
    slps = None
    npix = cam.pxlx*cam.pxly
    subapFlag = FITS.Read(cam.subapflag)[1]
    files = os.listdir(cam.subaplocation_path)
    subapname = [s for s in files if 'led_%d_'%(star_list[0]) in s]
    subapLoc = FITS.Read(cam.subaplocation_path+subapname)[1]
    subapLoc = None
    for star in star_list:
        subapname = [s for s in files if 'led_%d_'%(star_list[0]) in s]
        if(subapLoc==None):
            subapLoc = FITS.Read(cam.subaplocation_path+subapname)[1]
        else:
            auxLoc = FITS.Read(cam.subaplocation_path+subapname)[1]
            subapLoc = np.array([subapLoc,auxLoc])

    if(imgs.shape[1]/npix==star_list):
        slps = np.zeros((imgs.shape[0],len(star_list)*2*cam.nsubaps))
    else:
        print 'Wrong camera, or wrong stars'
        return None

    for frame in range(imgs.shape[0]):
        for star in range(len(star_list)):
            img = imgs[frame,star*npix:(star+1)*npix]
            img = img.reshape((cam.pxly,cam.pxly))
            count = 0
            for flag in np.size(subapFlag):
                if(subapFlag[flag]):
                    y1 = subapLocation[star,count,0]
                    y2 = subapLocation[star,count,1]+1
                    x1 = subapLocation[star,count,3]
                    x1 = subapLocation[star,count,4]+1
                    s1 = star*cam.nsubaps*2+count*2
                    s2 = star*cam.nsubaps*2+(count+1)*2
                    slps[frame,s1:s2] = centerofmass(img[y1:y2,x1:x2])
                    count += 1

    FITS.Write(slps.astype(np.float32),path+filename,writeMode='a')

def centerofmass(array):
    '''
    array is a float 32 2-dimensional numpy array
    '''
    cent = np.zeros(2)
    npix = float(np.size(array))
    Xgrid,Ygrid = np.meshgrid(np.arange(array.shape[1]),np.arange(array.shape[0]))
    cent[1] = np.sum(Ygrid*array)/npix
    cent[0] = np.sum(Xgrid*array)/npix
    return cent

def formataltitude(dirpath,filename,altitude_list,acquire='slopes'):
        '''
        Takes all the fits files in the dirpath, concatenates the
        horizontally for different altitudes and vertically for
        different runs. Before concatenating vertically, it
        substract the mean. It saves the resulting array in a two
        dimensional FITS named after filename
        '''

        files = os.listdir(dirpath)
        files = [s for s in files if acquire in s]
        final = None
        aux = None
        firstfinal = 0
        firstaux = 0
        for sltitude_id in altitude_list:
            subfiles = [s for s in files if 'altitude_%d'%(altitude_id) in s]
            for fil in subfiles:
                img = FITS.Read(dirpath + fil)[1]
                img1 = img - img.mean(axis=0)
                if(firstaux==0):
                    aux = img1
                    firstaux = 1
                else:
                    aux = numpy.concatenate((aux,img1),axis=0)
            if(firstfinal==0):
                firstfinal = 1
                final = aux
            else:
                final = numpy.concatenate((final,aux),axis=1)
            aux = None
            firstaux = 0

        FITS.Write(final.astype(numpy.float32),dirpath+filename,writeMode='a')

def comparedata(dirpath,fitsfile1,fitsfile2,axis=0):
    '''
    Compare 2 2-dimensional arrays along the given axis.
    Returns a 1-dimensional array with the error.
    '''
    array1 = FITS.Read(dirpath+fitsfile1)[1]
    array2 = FITS.Read(dirpath+fitsfile2)[1]
    error = array2-array1
    squaremeanerror = np.square(error).sum(1-axis)
    return squaremeanerror
    
