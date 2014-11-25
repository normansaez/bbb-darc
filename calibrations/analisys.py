'''
Wrote by Tim on his visit. This has examples on how to use DARC.
'''

import FITS
FITS.Read('SHrtcCentBuf_140114_124359_led1.fits')
cent = FITS.Read('SHrtcCentBuf_140114_124359_led1.fits')
cent = FITS.Read('SHrtcCentBuf_140114_124359_led1.fits')[1]
cent.shape
import tel
subapFlag=tel.Pupil(16,16/2.,1,16).subflag.astype("i").ravel()
subapFlag
subapFlag.shape=(16,16)
subapFlag
#adding center as valid
subapFlag.reshape(16,16)[8][8] = 1 
subapFlag.reshape(16,16)[7][8] = 1 
subapFlag.reshape(16,16)[7][7] = 1 
subapFlag.reshape(16,16)[8][7] = 1 
subapFlag=tel.Pupil(16,16/2.,0,16).subflag.astype("i")
subapFlag
_.ravel()
_.sum()
_*2
cent.shape
temp = cents[500]
temp = cent[500]
cents = cent
temp[:20]
xcents = temp[::2]
xcents.shape
xcents[:10]
cent.shape
temp.shape
ycents = temp[1::2]
ycents
import numpy
outputx = numpy.zeros((256))
outputx.shape
for i in range(256):
    if subapFlag[i]==1:
outputx = numpy.zeros((256))
counter = 0
for i in range(256):
    if subapFlag[i]==1:
        outputx[i]==ycents[counter]
        counter += 1
counter = 0
for i in range(256):
    if subapFlag[i]==1:
        outputx[i]=ycents[counter]
        counter += 1
subapFlag[1]
for i in range(256):
    if subapFlag.ravel()[i]==1:
        outputx[i]=ycents[counter]
        counter += 1
outputx.shape
outputx.shape=(16,16)
outputx
numpy.where(outputx!=0,1,0)
temp = cents[500:600]
avtemp = temp.sum(0)
avtemp.shape
temp.shape
avtemp /= float(100)
avtemp
t1 = temp-avtemp
h
t1 = numpy.power(t1,2)
t2 = t1.sum(0)
t2 /= 100.
t3 = numpy.sqrt(t2)
t3.shape
t3[::2]
t3[1::2]
temp = cent[500]
numpy.sum(temp[::2])/208.
numpy.sum(temp[1::2])/208.
temp = cent[520]
numpy.sum(temp[::2])/208.
numpy.sum(temp[1::2])/208.
(numpy.sum(cents[1::2])/208.).shape
(numpy.sum(cents[1::2],1)/208.).shape
(numpy.sum(cents[1::2],0)/208.).shape
(cents[:,1::2].sum(0)/208.).shape
(cents[:,1::2].sum(1)/208.).shape
(cents[:,1::2].sum(1)/208.)[30]
(cents[:,1::2].sum(1)/208.
)
(cents[:,1::2].sum(1)/208.)[520]
import pylab
pylab.plot(cents[:,1::2].sum(1)/208.)
pylab.show()
y = cents[:,1::2].sum(1)/208.
x= cents[:,0::2].sum(1)/208.
y -= y.sum()/1000.
x -= x.sum()/1000.
pylab.plot(y)
pylab.plot(x)
pylab.show()
calpix = FITS.Read('SHrtcCalPxlBuf_140114_124359_led1.fits')[1]
calpix.shape
calpix.shape=(1000,1920,1080)
pylab.imshow(calpix[500])
pylab.show()
calpix.shape=(1000,1080,1920)
pylab.imshow(calpix[500])
pylab.show()
FITS.Write(calpix,'testcalpix.fits')
import os
os.system('pwd')

