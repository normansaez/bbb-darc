'''
Module containing pos-process functions to format data,
calculate slopes and all of the other things I haven't 
yet thought of.

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: May the 22th, 2014
'''

import FITS
#import darc
import numpy as np
import os
from numpy import unravel_index
import pylab as pl
#import random
#from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star
#import ConfigParser
#import scipy
#from scipy import signal

def im2slope(path,imname,slpname,star_list,camera='camera'):
    '''
    VARIABLES
    path     [string]      Directory path. Example:
                           /home/dani/
    
    imname   [string]      FITS file containg images vertically and 
                           horizontally concatenated as:

                               star1/altitude1    star2/altitude2    ...   starn/altituden
 
                           [im1pix1 im1pix2 ...|im1pix1 im1pix2 ...| ... |im1pix1 im1pix2 ...]
                           [im2pix1 im2pix2 ...|im2pix1 im2pix2 ...| ... |im2pix1 im2pix2 ...]
                                                        .
                                                        .
                                                        .
                           [immpix1 immpix2 ...|immpix1 immpix2 ...| ... |immpix1 immpix2 ...]
                           
                           In each of the m rows there are images for all n stars/altitudes.

    slpname   [string]     Name with which will be saved the the resulting slopes array:
                           
                               star1/altitude1      star2/altitude2      ...   starn/altituden
 
                           [im1slpx1 im1slpy1 ...|im1slpx1 im1slpy1 ...| ... |im1slpx1 im1slpy1 ...]
                           [im2slpx1 im2slpy1 ...|im2slpx1 im2slpy1 ...| ... |im2slpx1 im2slpy1 ...]
                                                        .
                                                        .
                                                        .
                           [immslpx1 immslpy1 ...|immslpx1 immslpy1 ...| ... |immslpx1 immslpy1 ...]
    
    star_list [list]       List containg n elements.
                           Example: 4 different stars -> star_list = [1,6,18,21]
                           Example: star 5 at 3 different altitudes -> star_list = [5,5,5]
    '''
    imgs = FITS.Read(path+imname)[1]
    cam = Camera(camera)
    slps = None
    npix = cam.pxlx*cam.pxly
    subapFlag = FITS.Read(cam.subapflag)[1].ravel()
    files = os.listdir(cam.subaplocation_path)
    subapname = [s for s in files if 'led_%d.'%(star_list[0]) in s]
    subapLoc = np.zeros((len(star_list),cam.allsubaps,6))
    for star in range(len(star_list)):
        subapname = [s for s in files if 'led_%d.'%(star_list[star]) in s]
        subapLoc[star] = FITS.Read(cam.subaplocation_path+subapname[0])[1]

    if(imgs.shape[1]/npix==len(star_list)):
        slps = np.zeros((imgs.shape[0],len(star_list)*2*cam.nsubaps))
    else:
        print 'Wrong camera, or wrong stars'
        return None

    for frame in range(imgs.shape[0]):
        for star in range(len(star_list)):
            img = imgs[frame,star*npix:(star+1)*npix]
            img = img.reshape((cam.pxly,cam.pxlx))
            count = 0
            for flag in range(np.size(subapFlag)):
                if(subapFlag[flag]):
                    y1 = subapLoc[star,count,0]
                    y2 = subapLoc[star,count,1]+1
                    x1 = subapLoc[star,count,3]
                    x2 = subapLoc[star,count,4]+1
                    s1 = star*cam.nsubaps*2+count*2
                    s2 = star*cam.nsubaps*2+(count+1)*2
                    slps[frame,s1:s2] = centerofmass(img[y1:y2,x1:x2])
                    count += 1

    FITS.Write(slps.astype(np.float32),path+slpname,writeMode='a')

def centerofmass(array):
    '''
    array is a float 32 2-dimensional numpy array
    cent = numpy.array([x,y])
    '''
    cent = np.zeros(2)
    totalmass = float(array.sum())
    Xgrid,Ygrid = np.meshgrid(np.arange(array.shape[1]),np.arange(array.shape[0]))
    cent[1] = np.sum(Ygrid*array)/totalmass
    cent[0] = np.sum(Xgrid*array)/totalmass
    return cent

def formattomodata(dirpath,filename,acquire='slopes'):
    files = os.listdir(dirpath)
    files = [s for s in files if acquire in s]
    final = None
    aux = None
    firstfinal = 0
    firstaux = 0
    for fil in files:
        if(firstfinal==0):
            firstfinal = 1
            final = FITS.Read(dirpath+fil)[1]
        else:
            aux = FITS.Read(dirpath+fil)[1]
            final = np.concatenate((final,aux),axis=1)

    if(acquire=='slopes'):
        final = final - final.mean(axis=0)

    platescale = 0.1624108336 #[''/pix]
    final = final*platescale

    if('.fits' in filename):
        FITS.Write(final.astype(np.float32),dirpath+filename,writeMode='a')
    elif('.gz' in filename):
        np.savetxt(dirpath+filename,final.astype(np.float32),fmt='%.5f')

def formataltitude(dirpath,filename,altitude_list,acquire='slopes'):
    '''
    Takes all the fits files in the dirpath, concatenates the
    horizontally for different altitudes and vertically for
    different runs. Before concatenating vertically, it
    substract the mean. It saves the resulting array in a two
    dimensional FITS named after filename.
    '''
    
    files = os.listdir(dirpath)
    files = [s for s in files if acquire in s]
    final = None
    aux = None
    firstfinal = 0
    firstaux = 0
    for altitude_id in altitude_list:
        subfiles = [s for s in files if 'altitude_%d'%(altitude_id) in s]
        for fil in subfiles:
            img = FITS.Read(dirpath + fil)[1]
            #img1 = img
            img1 = img - img.mean(axis=0)
            if(firstaux==0):
                aux = img1
                firstaux = 1
            else:
                aux = np.concatenate((aux,img1),axis=0)
        if(firstfinal==0):
            firstfinal = 1
            final = aux
        else:
            final = np.concatenate((final,aux),axis=1)
        aux = None
        firstaux = 0
        
    if('.fits' in filename):
        FITS.Write(final.astype(np.float32),dirpath+filename,writeMode='a')
    elif('.gz' in filename):
        np.savetxt(dirpath+filename,final.astype(np.float32),fmt='%.4f')

'''
def comparedata(dirpath,fitsfile1,fitsfile2,axis=0):

    Compare 2 2-dimensional arrays along the given axis.
    Returns a 1-dimensional array with the error.

    array1 = FITS.Read(dirpath+fitsfile1)[1]
    array2 = FITS.Read(dirpath+fitsfile2)[1]
    error = array2-array1
    squaremeanerror = np.square(error).mean(1-axis)
    print 'Max mean error: ',
    print np.amax(squaremeanerror)
    print 'Mean mean error',
    print np.mean(squaremeanerror)
    return squaremeanerror
'''
    
if __name__=='__main__':
    '''
    dirpath = '/home/dani/BeagleAcquisition/SH/postnorman/'
    filename = 'images_from_darc.fits'
    altitude_list = [0,25,50,75,100]
    acquire = 'images'
    formataltitude(dirpath,filename,altitude_list,acquire=acquire)
    '''
    
    '''
    dirpath = '/home/dani/BeagleAcquisition/SH/postnorman/'
    filename = 'slopes_from_darc.fits'
    altitude_list = [0,25,50,75,100]
    acquire = 'slopes'
    formataltitude(dirpath,filename,altitude_list,acquire=acquire)
    '''
    '''
    dirpath = '/home/dani/BeagleAcquisition/SH/postnorman/'
    imname = 'images_from_darc.fits'
    slpname = 'slopes_from_images.fits'
    star_list = [1,1,1,1,1]
    im2slope(dirpath,imname,slpname,star_list,camera='camera')
    '''
    '''
    dirpath = '/home/dani/BeagleAcquisition/SH/postnorman/'
    filename = 'slopes_from_darc_averaged.fits'
    altitude_list = [0,25,50,75,100]
    acquire = 'slopes'
    formataltitude(dirpath,filename,altitude_list,acquire=acquire)
    '''

    dirpath = '/home/dani/BeagleAcquisition/SH/tomodata_1_18_21_24/'
    filename = 'slopes.gz'
    acquire = 'slopes'
    formattomodata(dirpath,filename,acquire=acquire)
    



