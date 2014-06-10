'''
Loads a set of [x,y] points and fits an elipse or a circle.
If the least-square fitting does not work, adjust
the initial guess..

Author: Nicolas S. Dubost
Last update: June 10th, 2014
'''
import FITS
import pylab as pl
import numpy as np
from pylab import imshow,show,plot
from scipy import optimize

def elipsefunc(x,a,b,x0,y0):
    y = np.zeros(x.shape[0])
    for i in range(x.shape[0]): 
        y[i] = y0 + x[i,1]*b*np.sqrt(1-np.square((x[i,0]-x0)/a))
    return y

def circlefunc(x,a,x0,y0):
    y = np.zeros(x.shape[0])
    for i in range(x.shape[0]):
        y[i] = y0 + x[i,1]*a*np.sqrt(1-np.square((x[i,0]-x0)/a))
    return y

# Loading n points as nx2 numpy-array
path = '/home/dani/BeagleAcquisition/SH/Nicole/'
filetoload = 'tilt_wedge.fits'
slopes = FITS.Read(path + filetoload)[1]

xdata = np.zeros((slopes.shape[0],2))
xdata[:,0] = slopes[:,0]
xdata[:,1] = slopes[:,1]/np.absolute(slopes[:,1])

# Least-square fitting. p0 is the initial guess
#popt,pcov = optimize.curve_fit(circlefunc,xdata,slopes[:,1],p0=[5.,0.,0.])
popt,pcov = optimize.curve_fit(elipsefunc,xdata,slopes[:,1],p0=[8.,5.5,0.,0.])

a = popt[0]
b = popt[1]
x0 = popt[2]
y0 = popt[3]
puntos = 1000
xs1 = np.linspace(-a+x0,a+x0,puntos)
xs2 = xs1[::-1] + 0.
xs = np.concatenate((xs1,xs2))
unos = np.zeros(puntos)+1
menosunos = np.zeros(puntos)-1
juntosunos = np.concatenate((unos,menosunos))
newdata = np.transpose(np.array([xs,juntosunos]))

y = elipsefunc(newdata,a,b,x0,y0)

handle = pl.plot(slopes[:,0],slopes[:,1],'ro',newdata[:,0],y,'b-',x0,y0,'g+',markersize=8.0)
pl.title('Spots\' path for a turning wedge')
pl.xlabel('X-slopes [pixels]')
pl.ylabel('Y-slopes [pixels]')
e = 0
major = 0
minor = 0
if a>b:
    e = np.sqrt(1-np.square(b/a))
else:
    e = np.sqrt(1-np.square(a/b))

pl.legend(handle,('Mean Slopes','Fitted Ellipse\nEccentricity: %.3f\nX-semi axis: %.3f\nY-semi axis: %.3f'%(e,a,b),'Ellipse\'s Center'),'upper right')

show()
