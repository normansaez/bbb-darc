'''
Creates plots

Author: Nicolas S. Dubost
        nsdubost@uc.cl
Last update: May the 15th, 2014
'''

#!/usr/bin/env python
import FITS
import numpy
import os
from numpy import unravel_index
import pylab as pl
from BeagleDarc.Model import Camera
from BeagleDarc.Model import Star
import scipy
from scipy import signal

class Plotter:
    def __init__(self,path_to_file,file_name,star_list,cameraName='SH',title=None,xlabel=None,ylabel=None,figlegend=None):
        #Darc camera instance
        self.SHCamera = Camera('camera')

        #Parameters
        self.nsubaps = int(self.SHCamera.nsubaps)                             # number of active subaps(208*2)
        self.nsubaps *= 2
        self.nstars = self.SHCamera.nstars                                    # number of stars

        self.cameraName = self.SHCamera.camera
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

    
    def spot_cloud(self,mode='gaussian'):
        '''
        Takes a FITS file containing slopes for 1 or many stars. 
        Plots a representation of the long term exposure spots.
        '''
        modes = {'gaussian':0,'flat':1}

        slopes = FITS.Read(self.path + self.filename)[1]
        Xslopes = slopes[:,::2]
        Yslopes = slopes[:,1::2]
        Xmean = numpy.zeros((len(self.star_list),self.nsubaps/2.0))
        Ymean = numpy.zeros((len(self.star_list),self.nsubaps/2.0))
        Xvar = numpy.zeros((len(self.star_list),self.nsubaps/2.0))
        Yvar = numpy.zeros((len(self.star_list),self.nsubaps/2.0))

        for star_id in range(len(star_list)):
            Xmean[star_id,:] = Xslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].mean(axis=0)
            Ymean[star_id,:] = Yslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].mean(axis=0)
            Xvar[star_id,:] = Xslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].var(axis=0)
            Yvar[star_id,:] = Yslopes[:,star_id*self.nsubaps/2.:(star_id+1)*self.nsubaps/2.].var(axis=0)                


        #Parameters
        allsubaps = self.SHCamera.allsubaps                    # Active+Inactive subaps
        side = int(numpy.sqrt(allsubaps))
        nstars = self.SHCamera.nstars
        subapLocation = numpy.zeros((allsubaps,6))             # Centred on (0,0)
        subapLocation[:,2] = subapLocation[:,2] + 1
        subapLocation[:,5] = subapLocation[:,5] + 1

        Xwidth = self.SHCamera.xwidth
        Ywidth = self.SHCamera.ywidth
        Xgap = self.SHCamera.xgap
        Ygap = self.SHCamera.ygap

        # Checking for parity
        xRow = numpy.array([])
        if(side%2):
            xRow = numpy.arange(-numpy.ceil(float(side)/2),round(float(side)/2))*Xgap -round(Xwidth/2)
        else:
            xRow = numpy.arange(-float(side)/2,float(side)/2)*Xgap + round(Xgap/2) -round(Xwidth/2)

        yRow = numpy.array([])
        if(side%2):
            yRow = numpy.arange(-numpy.ceil(float(side)/2),round(float(side)/2))*Ygap -round(Ywidth/2)
        else:
            yRow = numpy.arange(-float(side)/2,float(side)/2)*Ygap + round(Ygap/2) -round(Ywidth/2)

        for row in range(1,int(side+1)):
            subapLocation[side*(row-1):side*(row),0] = yRow[row-1]
            subapLocation[side*(row-1):side*(row),1] = subapLocation[side*(row-1):side*(row),0] + Ywidth
            subapLocation[side*(row-1):side*(row),3] = xRow
            subapLocation[side*(row-1):side*(row),4] = subapLocation[side*(row-1):side*(row),3] + Xwidth

        if(self.majorpattern==None):
            self.majorpattern = numpy.zeros((len(self.star_list),-subapLocation[0,0]+subapLocation[-1,1]+1,-subapLocation[0,3]+subapLocation[-1,4]+1))
            self.minorpattern = numpy.zeros((Ywidth+1,Xwidth+1))
            centx = float(Xwidth+1)/2 - 0.5
            centy = float(Ywidth+1)/2 - 0.5
            subapLocAux = subapLocation
            Aux = numpy.zeros((allsubaps,6))
            Aux[:,0:2] = subapLocAux[:,0:2] - subapLocation[0,0]
            Aux[:,3:5] = subapLocAux[:,3:5] - subapLocation[0,3]
            subapflag = FITS.Read(self.SHCamera.subapflag)[1]
            subapflag = subapflag.ravel()
            
            fig = pl.figure(1)
            im = None
            for star_id in range(len(self.star_list)):
                tracker = 0
                subaptrack = 0
                for subap in Aux:
                    if(int(subapflag[tracker])):
                        centx = float(Xwidth+1)/2 - 0.5 + Xmean[star_id,subaptrack]
                        centy = float(Ywidth+1)/2 - 0.5 + Ymean[star_id,subaptrack]
                        for y in range(0,Ywidth):
                            for x in range(0,Xwidth):
                                if(modes[mode]==1):
                                    if(x>=(Xwidth-(Xgap-1)) and x<=(Xgap-2) and y>=(Ywidth-(Ygap-1)) and y<=(Ygap-2)):
                                        self.minorpattern[y,x] = Xvar[star_id,subaptrack]+Yvar[star_id,subaptrack]
                                    else:
                                        self.minorpattern[y,x] = 0.0
                                else:
                                    self.minorpattern[y,x] = numpy.exp(-0.5*(pow(x-centx,2)/Xvar[star_id,subaptrack]+pow(y-centy,2))/Yvar[star_id,subaptrack])
                            
                        self.majorpattern[star_id,subap[0]:subap[1]+1,subap[3]:subap[4]+1] += self.minorpattern
                        subaptrack += 1
                    tracker += 1
            
                if(len(self.star_list)<3):
                    filas = 1
                    columnas = len(self.star_list)
                else:
                    filas = 2
                    columnas = numpy.floor(((len(self.star_list)+1)/2.))
                pl.subplot(filas,columnas,star_id+1,title='Altitude: %d'%(self.star_list[star_id])+'%')
                #im = pl.imshow(self.majorpattern[star_id,:,:]/numpy.amax(self.majorpattern[star_id,:,:]),interpolation='nearest',origin=[0,0])
                im = pl.imshow(self.majorpattern[star_id,:,:],interpolation='nearest',origin=[0,0],vmin=0,vmax=2)
                pl.ylabel(self.ylabel)
                pl.xlabel(self.xlabel)

        cax = fig.add_axes([0.94, 0.05, 0.02, 0.9])
        fig.colorbar(im,cax,orientation='vertical')
        fig.text(0.5,0.96,self.title,horizontalalignment='center',verticalalignment='top',fontsize=20)
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
        if(ola.shape[0]/numpy.float(self.SHCamera.pxlx*self.SHCamera.pxlx) >= 2):
            print 'Only plotting first star out of %d'%(ola.shape[0]/numpy.float(self.SHCamera.pxlx*self.SHCamera.pxlx))
        
        i,j = numpy.ogrid[-pixelSize*arraySize/2.:pixelSize*arraySize/2.:w.shape[0]*1j,0:0:w.shape[0]*1j]
        Y = i*1000 + j
        X = numpy.transpose(Y)
        fig = pl.figure()
        ax = pl.Axes3D(fig)
        ax.plot_surface(X,Y,w)
        pb.show()        



if __name__ == '__main__':

    case = 'spot_cloud'
    #case = 'stat_curve'
    #case = 'join_slopes_altitudes'
    cases = {'spot_cloud':0,'stat_curve':1,'surface':2,'join_slopes_altitudes':3}
    plotty = None

    if(cases[case] == 0):

        path_to_file = '/home/dani/BeagleAcquisition/SH/postnorman/'
        file_name = 'slopes_from_darc_averaged.fits'
        #file_name = 'SH_slopes_useB_1500_altitude_100_100_T2014_05_14T22_54_53.fits'
        #star_list = [100]
        star_list = [0,25,50,75,100]
        title = 'Subaperture Variance'
        xlabel = 'X pixels'
        ylabel = 'Y pixels'
        figlegend = None
        
        ploty = Plotter(path_to_file,file_name,star_list,cameraName='SH',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.spot_cloud(mode='flat')

    elif(cases[case] == 1):

        path_to_file = '/home/dani/BeagleAcquisition/SH/slopes/'
        file_name = 'SH_slopes_510_T2014_04_29T15_00_32.fits'
        star_list = [1,18,21,24]
        title = 'Slopes vs subaps, r0=0.6[mm]'
        xlabel = 'Subaps'
        ylabel = 'Pixels'
        figlegend = ('Xmean','Ymean','Xvar','Yvar')

        ploty = Plotter(path_to_file,file_name,star_list,cameraName='SH',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.stat_curve()

    elif(cases[case] == 2):
        
        path_to_file = '/home/dani/BeagleAcquisition/SH/slopes/'
        file_name = 'SH_slopes_510_T2014_04_29T15_00_32.fits'
        star_list = [1,18,21,24]
        title = 'Slopes vs subaps, r0=0.6[mm]'
        xlabel = 'Subaps'
        ylabel = 'Pixels'
        figlegend = ('Xmean','Ymean','Xvar','Yvar')         
        
        ploty = Plotter(path_to_file,file_name,star_list,cameraName='SH',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.surface()

    elif(cases[case] == 3):

        path_to_file = '/home/dani/BeagleAcquisition/SH/pinhole/'
        file_name = 'prueba.fits'
        star_list = [0,25,50,75,100]
        title = 'Subap Variance'
        xlabel = 'X pixels'
        ylabel = 'Y pixels'
        figlegend = None
        
        ploty = Plotter(path_to_file,file_name,star_list,cameraName='SH',title=title,xlabel=xlabel,ylabel=ylabel)
        ploty.join_slopes_altitudes()
