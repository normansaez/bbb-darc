'''
Creates plots

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: June the 10th, 2014
'''

#!/usr/bin/env python
import FITS
import numpy as np
import os
from numpy import unravel_index
import pylab as pl
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star
import scipy
from scipy import signal

class Plotter:
    def __init__(self,path_to_file,file_name,star_list,camera='pike',title=None,xlabel=None,ylabel=None,figlegend=None):
        #Darc camera instance
        self.Cam = Camera(camera)

        #Parameters
        self.nsubaps = int(self.Cam.nsubaps)                             # number of active subaps(208*2)
        self.nsubaps *= 2
        self.nstars = self.Cam.nstars                                    # number of stars

        self.majorpattern = None
        self.minorpattern = None
        self.grid = None
        self.path = path_to_file
        self.filename = file_name
        self.star_list = star_list
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.figlegend = figlegend

    
    def subapstat(self,mode='variance'):
        '''
        Takes a FITS file containing slopes for 1 or many stars. 
        Plots a representation of the long term exposure spots.
        '''
        modes = {'variance':0,'mean':1}

        slopes = FITS.Read(self.path + self.filename)[1]
        Xslopes = None
        Yslopes = None
        isdouble = int(slopes.shape[1]/(len(self.star_list)*self.nsubaps))
        if isdouble == 1:
            Xslopes = slopes[:,::2]
            Yslopes = slopes[:,1::2]
        else:
            Xslopes = slopes
            Yslopes = slopes
            
        Xmean = np.zeros((len(self.star_list),self.nsubaps/2.0))
        Ymean = np.zeros((len(self.star_list),self.nsubaps/2.0))
        Xvar = np.zeros((len(self.star_list),self.nsubaps/2.0))
        Yvar = np.zeros((len(self.star_list),self.nsubaps/2.0))

        for star_id in range(len(star_list)):
            Xmean[star_id,:] = Xslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].mean(axis=0)
            Ymean[star_id,:] = Yslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].mean(axis=0)
            Xvar[star_id,:] = Xslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].var(axis=0)
            Yvar[star_id,:] = Yslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].var(axis=0)                


        #Parameters
        allsubaps = self.Cam.allsubaps                    # Active+Inactive subaps
        side = int(np.sqrt(allsubaps))
        nstars = self.Cam.nstars
        subapLocation = np.zeros((allsubaps,6))             # Centred on (0,0)
        subapLocation[:,2] = subapLocation[:,2] + 1
        subapLocation[:,5] = subapLocation[:,5] + 1

        Xwidth = self.Cam.xwidth
        Ywidth = self.Cam.ywidth
        Xgap = self.Cam.xgap
        Ygap = self.Cam.ygap

        # Checking for parity
        xRow = np.array([])
        if(side%2):
            xRow = np.arange(-np.ceil(float(side)/2),round(float(side)/2))*Xgap -round(Xwidth/2)
        else:
            xRow = np.arange(-float(side)/2,float(side)/2)*Xgap + round(Xgap/2) -round(Xwidth/2)

        yRow = np.array([])
        if(side%2):
            yRow = np.arange(-np.ceil(float(side)/2),round(float(side)/2))*Ygap -round(Ywidth/2)
        else:
            yRow = np.arange(-float(side)/2,float(side)/2)*Ygap + round(Ygap/2) -round(Ywidth/2)

        for row in range(1,int(side+1)):
            subapLocation[side*(row-1):side*(row),0] = yRow[row-1]
            subapLocation[side*(row-1):side*(row),1] = subapLocation[side*(row-1):side*(row),0] + Ywidth
            subapLocation[side*(row-1):side*(row),3] = xRow
            subapLocation[side*(row-1):side*(row),4] = subapLocation[side*(row-1):side*(row),3] + Xwidth

        if(self.majorpattern==None):
            self.majorpattern = np.zeros((len(self.star_list),-subapLocation[0,0]+subapLocation[-1,1]+1,-subapLocation[0,3]+subapLocation[-1,4]+1))
            self.minorpattern = np.zeros((Ywidth+1,Xwidth+1))
            subapLocAux = subapLocation
            Aux = np.zeros((allsubaps,6))
            Aux[:,0:2] = subapLocAux[:,0:2] - subapLocation[0,0]
            Aux[:,3:5] = subapLocAux[:,3:5] - subapLocation[0,3]
            subapflag = FITS.Read(self.Cam.subapflag)[1]
            subapflag = subapflag.ravel()
            
            fig = pl.figure(1)
            im = None
            for star_id in range(len(self.star_list)):
                tracker = 0
                subaptrack = 0
                for subap in Aux:
                    if(int(subapflag[tracker])):
                        value = 0
                        if(modes[mode]==0):
                            if isdouble == 1:
                                value = Xvar[star_id,subaptrack]+Yvar[star_id,subaptrack]
                            else:
                                value = Xvar[star_id,subaptrack]
                        else:
                            if isdouble == 1:
                                value = np.sqrt(np.square(Xmean[star_id,subaptrack])+np.square(Ymean[star_id,subaptrack]))
                            else:
                                value = Xmean[star_id,subaptrack]

                        self.minorpattern[(Ywidth-(Ygap-1)):(Ygap-2)+1,(Xwidth-(Xgap-1)):(Xgap-2)+1] = value
                        '''    
                        for y in range(0,Ywidth):
                            for x in range(0,Xwidth):
                                if(modes[mode]==0):
                                    if(x>=(Xwidth-(Xgap-1)) and x<=(Xgap-2) and y>=(Ywidth-(Ygap-1)) and y<=(Ygap-2)):
                                        self.minorpattern[y,x] = value
                                    else:
                                        self.minorpattern[y,x] = 0.0
                                else:
                                    if(x>=(Xwidth-(Xgap-1)) and x<=(Xgap-2) and y>=(Ywidth-(Ygap-1)) and y<=(Ygap-2)):
                                        self.minorpattern[y,x] = value
                                    else:
                                        self.minorpattern[y,x] = 0.0
                        '''    
                        self.majorpattern[star_id,subap[0]:subap[1]+1,subap[3]:subap[4]+1] += self.minorpattern
                        subaptrack += 1
                    tracker += 1
            
                if(len(self.star_list)<3):
                    filas = 1
                    columnas = len(self.star_list)
                else:
                    filas = 2
                    columnas = np.floor(((len(self.star_list)+1)/2.))
                #filas = 3
                #columnas = 7

            for star_id in range(len(self.star_list)):
                subtitles = ['COM','GAUSS']
                #pl.subplot(filas,columnas,star_id+1,title=subtitles[star_id])
                pl.subplot(filas,columnas,star_id+1,title='Star %d'%(star_id))
                im = pl.imshow(self.majorpattern[star_id,:,:],interpolation='nearest',origin=[0,0],vmin=0,vmax=self.majorpattern.max())
                #im = pl.imshow(self.majorpattern[star_id,:,:],interpolation='nearest',origin=[0,0],vmin=0,vmax=5.)
                pl.ylabel(self.ylabel)
                pl.xlabel(self.xlabel)

        cax = fig.add_axes([0.94, 0.05, 0.02, 0.9])
        fig.colorbar(im,cax,orientation='vertical')
        fig.text(0.5,0.96,self.title,horizontalalignment='center',verticalalignment='top',fontsize=20)
        figtext = ''
        if(modes[mode]==0):
            figtext = '[pixels^2]'
        else:
            figtext = 'ADU'
        fig.text(0.95, 0.04,figtext,horizontalalignment='center',verticalalignment='top',fontsize=15)
        pl.show()
    
    def stat_curve(self):
        '''
        Typical figure with 2 plots, one for the mean slope value
        per subap and the other for the variance.
        '''
        oli = FITS.Read(self.path+self.filename)[1]
        ola = oli.mean(axis=0)
        olo = oli.var(axis=0)
        
        fig = pl.figure(1)

        pl.subplot(211,title='Slope\'s mean vs subaps')
        handles1 = pl.plot(ola[::2],'b',ola[1::2],'g')
        pl.xlabel(self.xlabel)
        pl.ylabel(self.ylabel)
        pl.legend(handles1,('Xmean','Ymean'),'upper right')

        pl.subplot(212,title='Slope\'s variance vs subaps')
        handles2 = pl.plot(olo[::2],'b',olo[1::2],'g')
        pl.xlabel(self.xlabel)
        pl.ylabel(self.ylabel+'^2')
        pl.legend(handles2,('Xvar','Yvar'),'upper right')

        fig.text(0.5,0.97,self.title,horizontalalignment='center',verticalalignment='top',fontsize=20)
        pl.show() 

    def surface(self):
        '''
        Work in progress
        '''
        oli = FITS.Read(self.path+self.filename)[1]
        ola = oli.mean(axis=0)
        if(ola.shape[0]/np.float(self.Cam.pxlx*self.Cam.pxlx) >= 2):
            print 'Only plotting first star out of %d'%(ola.shape[0]/np.float(self.Cam.pxlx*self.Cam.pxlx))
        
        i,j = np.ogrid[-pixelSize*arraySize/2.:pixelSize*arraySize/2.:w.shape[0]*1j,0:0:w.shape[0]*1j]
        Y = i*1000 + j
        X = np.transpose(Y)
        fig = pl.figure()
        ax = pl.Axes3D(fig)
        ax.plot_surface(X,Y,w)
        pb.show()


if __name__ == '__main__':

    case = 'subapstat'
    #case = 'stat_curve'
    #case = 'join_slopes_altitudes'
    cases = {'subapstat':0,'stat_curve':1,'surface':2,'join_slopes_altitudes':3}
    plotty = None

    if(cases[case] == 0):

        path_to_file = '/home/dani/BeagleAcquisition/SBIG/ground_1_20_34_v2_horizontal_PhScr/'
        file_name = 'centerofmass_slopes.fits'
        #star_list = [1,6,7,8,9,10,11,12,13,14,18,24,26,28,32,34,36,49,51]
        #star_list = [1,2]
        star_list = [1,20,34]
        title = 'COM Centroids\' Variance'
        xlabel = 'X pixels'
        ylabel = 'Y pixels'
        figlegend = None
        
        ploty = Plotter(path_to_file,file_name,star_list,camera='sbig',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.subapstat(mode='variance')

    elif(cases[case] == 1):

        path_to_file = '/home/dani/BeagleAcquisition/SH/slopes/'
        file_name = 'SH_slopes_510_T2014_04_29T15_00_32.fits'
        star_list = [1,18,21,24]
        title = 'Slopes vs subaps, r0=0.6[mm]'
        xlabel = 'Subaps'
        ylabel = 'Pixels'
        figlegend = ('Xmean','Ymean','Xvar','Yvar')

        ploty = Plotter(path_to_file,file_name,star_list,camera='pike',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.stat_curve()

    elif(cases[case] == 2):
        
        path_to_file = '/home/dani/BeagleAcquisition/SH/slopes/'
        file_name = 'SH_slopes_510_T2014_04_29T15_00_32.fits'
        star_list = [1,18,21,24]
        title = 'Slopes vs subaps, r0=0.6[mm]'
        xlabel = 'Subaps'
        ylabel = 'Pixels'
        figlegend = ('Xmean','Ymean','Xvar','Yvar')         
        
        ploty = Plotter(path_to_file,file_name,star_list,camera='pike',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.surface()

    elif(cases[case] == 3):

        path_to_file = '/home/dani/BeagleAcquisition/SH/pinhole/'
        file_name = 'prueba.fits'
        star_list = [0,25,50,75,100]
        title = 'Subap Variance'
        xlabel = 'X pixels'
        ylabel = 'Y pixels'
        figlegend = None
        
        ploty = Plotter(path_to_file,file_name,star_list,camera='pike',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.join_slopes_altitudes()
