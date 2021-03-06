'''
Module containing post-process functions to format data,
calculate slopes and all of the other things I haven't 
yet thought of.

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: October the 10th, 2014
'''

import FITS
#import darc
import numpy as np
import os
from numpy import unravel_index
import pylab as pl
from pylab import imshow,show,plot
#import random
#from BeagleDarc.Controller import Controller
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star
#import ConfigParser
#import scipy
from scipy import optimize
#from scipy import signal

def im2(imgs,star_list,cam,output='centerofmass',useBrightest=0):
    '''
    Returns something from the images.
    Your options are 'centerofmass' for center of mass centroids,
                     'centerofgauss' for gauss fitted centroids,
                     'stdev' for standard deviation as the gaussian parameter
                     from gaussian fit
                     'allgauss' for all gaussian parameters
    
    VARIABLES
    
    imgs     [numpy.array] Images vertically and 
                           horizontally concatenated as:

                               star1/altitude1    star2/altitude2    ...   starn/altituden
 
                           [im1pix1 im1pix2 ...|im1pix1 im1pix2 ...| ... |im1pix1 im1pix2 ...]
                           [im2pix1 im2pix2 ...|im2pix1 im2pix2 ...| ... |im2pix1 im2pix2 ...]
                                                        .
                                                        .
                                                        .
                           [immpix1 immpix2 ...|immpix1 immpix2 ...| ... |immpix1 immpix2 ...]
                           
                           In each of the m rows there are images for all n stars/altitudes.
    
    star_list [list]       List containg n elements.
                           Example: 4 different stars -> star_list = [1,6,18,21]
                           Example: star 5 at 3 different altitudes -> star_list = [5,5,5]
    '''
    #imgs = FITS.Read(path+imname)[1]
    slps = None
    npix = cam.pxlx*cam.pxly
    subapFlag = FITS.Read(cam.subapflag)[1].ravel()
    files = os.listdir(cam.subaplocation_path)
    subapname = [s for s in files if 'led_%d.'%(star_list[0]) in s]
    subapLoc = np.zeros((len(star_list),cam.allsubaps,6))
    for star in range(len(star_list)):
        subapname = [s for s in files if 'led_%d.'%(star_list[star]) in s]
        subapLoc[star] = FITS.Read(cam.subaplocation_path+subapname[0])[1]

    ndata = 0
    if len(imgs.shape)==1: 
        imgs = np.array([imgs])

    if(imgs.shape[1]/npix==len(star_list)):
        if output in 'allgauss':
            ndata = 7
        else:
            ndata = 2
        slps = np.zeros((imgs.shape[0],len(star_list)*ndata*cam.nsubaps))
    else:
        print 'Wrong camera, or wrong stars'
        return None

    for frame in range(imgs.shape[0]):
        for star in range(len(star_list)):
            img = imgs[frame,star*npix:(star+1)*npix]
            img = img.reshape((cam.pxly,cam.pxlx))
            count = 0
            #imshow(img)
            #pl.title('Estrella %d'%(star_list[star]))
            #show()
            for flag in range(np.size(subapFlag)):
                if(subapFlag[flag]):
                    y1 = subapLoc[star,flag,0]
                    y2 = subapLoc[star,flag,1]+1
                    x1 = subapLoc[star,flag,3]
                    x2 = subapLoc[star,flag,4]+1
                    s1 = (star*cam.nsubaps+count)*ndata
                    s2 = (star*cam.nsubaps+count+1)*ndata

                    if output in 'centerofmass':
                        slps[frame,s1:s2] = centerofmass(img[y1:y2,x1:x2],useBrightest=useBrightest)
                    elif output in 'centerofgauss':
                        try:
                            popt = gauss2dfit(img[y1:y2,x1:x2])
                            slps[frame,s1] = popt[1]
                            slps[frame,s1+1] = popt[2]
                            show()
                        except:
                            imshow(img[y1:y2,x1:x2],interpolation='nearest')
                            pl.title('Bad Robot: %d'%(count))
                            show()
                    elif output in 'stdev':
                        popt = gauss2dfit(img[y1:y2,x1:x2])
                        slps[frame,s1] = popt[3]
                        slps[frame,s1+1] = popt[4]
                    elif output in 'allgauss':
                        try:
                            popt = gauss2dfit(img[y1:y2,x1:x2])
                            slps[frame,s1] = popt[0]
                            slps[frame,s1+1] = popt[1]
                            slps[frame,s1+2] = popt[2]
                            slps[frame,s1+3] = popt[3]
                            slps[frame,s1+4] = popt[4]
                            slps[frame,s1+5] = popt[5]
                            slps[frame,s1+6] = popt[6]
                        except:
                            imshow(img[y1:y2,x1:x2],interpolation='nearest')
                            pl.title('Bad Robot: %d'%(count))
                            show()
                    else:
                        print 'Wrong whatever'
                        return None
                    count += 1
    return slps
    #FITS.Write(slps.astype(np.float32),path+slpname,writeMode='s')



def subapBrightest(imgs,star_list,cam,useBrightest=1):
    '''
    Returns mean of useBrightest pixels in subaps
    When useBrightest=-1, mean of all pixels in subaps are returned
    
    VARIABLES
    
    imgs     [numpy.array] Images vertically and 
                           horizontally concatenated as:

                               star1/altitude1    star2/altitude2    ...   starn/altituden
 
                           [im1pix1 im1pix2 ...|im1pix1 im1pix2 ...| ... |im1pix1 im1pix2 ...]
                           [im2pix1 im2pix2 ...|im2pix1 im2pix2 ...| ... |im2pix1 im2pix2 ...]
                                                        .
                                                        .
                                                        .
                           [immpix1 immpix2 ...|immpix1 immpix2 ...| ... |immpix1 immpix2 ...]
                           
                           In each of the m rows there are images for all n stars/altitudes.
    
    star_list [list]       List containg n elements.
                           Example: 4 different stars -> star_list = [1,6,18,21]
                           Example: star 5 at 3 different altitudes -> star_list = [5,5,5]
    '''
    #imgs = FITS.Read(path+imname)[1]
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
        slps = np.zeros((imgs.shape[0],len(star_list)*cam.nsubaps))
    else:
        print 'Wrong camera, or wrong stars'
        return None

    for frame in range(imgs.shape[0]):
        for star in range(len(star_list)):
            img = imgs[frame,star*npix:(star+1)*npix]
            img = img.reshape((cam.pxly,cam.pxlx))
            count = 0
            #imshow(img)
            #pl.title('Estrella %d'%(star_list[star]))
            #show()
            for flag in range(np.size(subapFlag)):
                if(subapFlag[flag]):
                    y1 = subapLoc[star,flag,0]
                    y2 = subapLoc[star,flag,1]+1
                    x1 = subapLoc[star,flag,3]
                    x2 = subapLoc[star,flag,4]+1
                    s1 = star*cam.nsubaps+count
                    subap = brightest(img[y1:y2,x1:x2],useBrightest)
                    bina = subap > 0.
                    slps[frame,s1] = subap.sum()/float(bina.sum())
                    count += 1
    return slps
    #FITS.Write(slps.astype(np.float32),path+slpname,writeMode='w')

def brightest(array,useBrightest):
    '''
    Receives a 2-d numpy.array and returns it
    with all but the nbrightest pixels as zeros
    '''
    toreturn = array*0.
    if useBrightest == -1:
        toreturn = array + 0
    else:
        for u in range(useBrightest):
            maxv = array.max()
            argmax = unravel_index(array.argmax(),array.shape)
            toreturn[argmax[0],argmax[1]] = maxv
            array[argmax[0],argmax[1]] = 0.
    return toreturn

def centerofmass(array,threshold=None,useBrightest=0):
    '''
    array is a float 32 2-dimensional numpy array
    cent = numpy.array([x,y])
    '''
    newarray = None
    useBrightest = int(useBrightest)
    if(threshold!=None):
        boolarray = array>=threshold
        newarray = boolarray*array
    else:
        newarray = array + 0

    if(useBrightest>0):
        newarray = brightest(newarray,useBrightest)

    #Classic
    cent = np.zeros(2)
    totalmass = float(newarray.sum())
    Xgrid,Ygrid = np.meshgrid(np.arange(newarray.shape[1]),np.arange(newarray.shape[0]))
    if totalmass<1.0:
        print 'totalmass: ',
        print totalmass
        imshow(newarray)
        show()

    cent[1] = np.sum(Ygrid*newarray)/totalmass
    cent[0] = np.sum(Xgrid*newarray)/totalmass
    return cent

def gauss2d((x,y),A,x0,y0,sigmax,sigmay,theta,offset):
    '''
    theta in degrees, returns raveled array
    '''
    t = (theta%90.)*np.pi/180.
    vx = np.square(sigmax)
    vy = np.square(sigmay)
    x = x - x0
    y = y - y0
    a = np.square(np.cos(t)/sigmax)+np.square(np.sin(t)/sigmay)
    b = 2.*(1/vx-1/vy)*np.cos(t)*np.sin(t)
    c = np.square(np.sin(t)/sigmax)+np.square(np.cos(t)/sigmay)
    bell = offset + A*np.exp(-0.5*(a*np.square(x)+b*x*y+c*np.square(y)))
    return bell.ravel()

def gauss2dfit(array):
    ymax,xmax = np.unravel_index(array.argmax(),array.shape)
    ymax = ymax -np.floor((array.shape[0]-1)/2.)
    xmax = xmax -np.floor((array.shape[1]-1)/2.)
    gmax = array.max()
    # Least-square fitting. p0 is the initial guess. array is 2-D
    intial_guess = (gmax,xmax,ymax,7.,7.,45.,0.)
    
    xrow = np.linspace(0,array.shape[1]-1, array.shape[1]) -np.floor((array.shape[1]-1)/2.)
    yrow = np.linspace(0,array.shape[0]-1, array.shape[0]) -np.floor((array.shape[0]-1)/2.)
    x,y = np.meshgrid(xrow,yrow)

    x = x.ravel()
    y = y.ravel()
    xdata = (x,y)
    ydata = array.ravel()
    
    popt,pcov = optimize.curve_fit(gauss2d,xdata,ydata,p0=intial_guess)
    popt[5] = popt[5]%90.
    return popt

def concatenatefiles(dirpath,acquire='slopes'):
    files = os.listdir(dirpath)
    files = [s for s in files if acquire in s and '.fits' in s and 'pike' in s]
    files = sorted(files)
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
            final = np.concatenate((final,aux),axis=0)

    if(acquire=='slopes'):
        final = final - final.mean(axis=0)

    return final
    #if('.fits' in filename):
    #    FITS.Write(final.astype(np.float32),dirpath+filename,writeMode='a')
    #elif('.gz' in filename):
    #    platescale = 0.1612975147 #[''/pix]
    #    final = final*platescale
    #    np.savetxt(dirpath+filename,final.astype(np.float32),fmt='%.5f')

def formataltitude(dirpath,filename,altitude_list,acquire='slopes'):
    '''
    Takes all the fits files in the dirpath, concatenates them
    horizontally for different altitudes and vertically for
    different runs. Before concatenating vertically, it
    substract the mean. It saves the resulting array in a two
    dimensional FITS named after filename.
    '''
    
    files = os.listdir(dirpath)
    files = [s for s in files if '_'+acquire+'_' in s and '.fits' in s and 'pike' in s]
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

def covariance(set1,set2,norm=True):
    '''
    Returns a handle to plot the covariance of two data sets 
    versus a certain variable.
    set1 and set2 are MxN numpy arrays where each row contains
    cases for a same value of the variable.
    The covariance is then calculated along the N-axis, for each
    of the M cases.
    This also returns a 2-d Mx4 length array with the covariances.
    If norm = True, then the covariances are normalized.

    Example:
    set1             cov    set2               covxx    covyy    covxy    covyx
    [x y x y x y]     X     [x y x y x y]  ->
    [1 4 2 6 8 3]     X     [6 9 3 6 1 3]  ->  -0.8746  0.3273   -0.9244  0.2167
          .           X           .         .
          .           X           .         .
          .           X           .         .
    '''

    covxx = np.zeros(set1.shape[0])
    covyy = np.zeros(set1.shape[0])
    covxy = np.zeros(set1.shape[0])
    covyx = np.zeros(set1.shape[0])

    if norm:
        for i in range(set1.shape[0]):
            covi = np.cov(np.array([set1[i,::2],set2[i,::2]]),bias=1)
            covxx[i] = covi[0,1]/np.sqrt(covi[0,0]*covi[1,1])
            covi = np.cov(np.array([set1[i,1::2],set2[i,1::2]]),bias=1)
            covyy[i] = covi[0,1]/np.sqrt(covi[0,0]*covi[1,1])
            covi = np.cov(np.array([set1[i,::2],set2[i,1::2]]),bias=1)
            covxy[i] = covi[0,1]/np.sqrt(covi[0,0]*covi[1,1])
            covi = np.cov(np.array([set1[i,1::2],set2[i,::2]]),bias=1)
            covyx[i] = covi[0,1]/np.sqrt(covi[0,0]*covi[1,1])

    else:
        for i in range(set1.shape[0]):
            covi = np.cov(np.array([set1[i,::2],set2[i,::2]]),bias=1)
            covxx[i] = covi[0,1]
            covi = np.cov(np.array([set1[i,1::2],set2[i,1::2]]),bias=1)
            covyy[i] = covi[0,1]
            covi = np.cov(np.array([set1[i,::2],set2[i,1::2]]),bias=1)
            covxy[i] = covi[0,1]
            covi = np.cov(np.array([set1[i,1::2],set2[i,::2]]),bias=1)
            covyx[i] = covi[0,1]
    
    return np.transpose(np.array([covxx,covyy,covxy,covyx]))

def autocorrelate(dataset):
    '''
    Auto-correlates 1d arrays.
    '''
    dts = dataset - dataset.mean()
    cor = np.correlate(dts,dts,mode='full')
    cor = cor[np.floor(cor.size/2.):]
    siz = cor.size
    n = np.arange(siz)+1
    n = n[::-1]
    cor = cor/n
    return cor

def scattering(set1,set2,cam,star_list=[1],title='',xlabel='',ylabel=''):
    '''
    set1 and set2 are 1-d numpy arrays.
    '''
    mini = np.min([set1.min(),set2.min()])
    maxi = np.max([set1.max(),set2.max()])
    
    nsubaps = cam.nsubaps

    p,res,rank,sing,rcond= np.polyfit(set1,set2,1,full=True)
    a = p[0]
    b = p[1]

    if xlabel=='':
        xlabel = 'set1'
    if ylabel=='':
        ylabel = 'set2'

    lot = int(set1.shape[0]/len(star_list))
    
    fig = pl.figure()
    fig.set_size_inches(13,7)
    ax = fig.add_subplot(111)
    cmap = pl.cm.gist_ncar
    ax.set_color_cycle([cmap(i) for i in np.linspace(0,0.9,len(star_list))])
    h = []
    labels = []
    for ind in range(len(star_list)):
        haux, = ax.plot(set1[lot*ind:lot*(ind+1)],'o')
        h.append(haux)
        labels.append('Star %d'%(star_list[ind]))

    haux, = ax.plot([mini,maxi],[mini,maxi],'-')
    h.append(haux)
    labels.append('Reference Line')

    haux, = ax.plot([mini,maxi],[mini*a+b,maxi*a+b],'-')
    h.append(haux)
    labels.append('Reference Line','%.3f*x+%.3f'%(a,b))

    pl.legend(tuple(h),tuple(labels)) 
    pl.title(title+'\nMean Residual Error: %.3f[pix^2]'%(res[0]/set1.shape[0]))
    pl.xlabel(xlabel)
    pl.ylabel(ylabel)

    show()

def unpack(StreamBlock):
    '''
    Unpack a StreamBlock as given by DARC's GetStreamBlock()
    '''
    block = StreamBlock[StreamBlock.keys()[0]]
    fpf = len(block)
    images = np.zeros((fpf,block[0][0].size))
    for j in range(fpf):
        images[j,:] = block[j][0]
    
    return images


if __name__=='__main__':
    #formattomodata('/home/dani/BeagleAcquisition/SH/tomodata_1_18_21_24/','validationslopes.gz',acquire='slopes')
    covsalt = covariance(valslopes,annslopes,norm=True)
        



