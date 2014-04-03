////////////////

In configurations.cfg,

camera:	camera's prefix to be given to darc.Control() and others
pxlx: camera's number of pixles in the x-axis
pxly: camera's number of pixles in the y-axis
usebrightest: darc parameter, number of brightest pixels taken into
	      account in subap
bg_iter: number of iterations to be used when taking background images
maxshutter: maximum shutter for this camera. if the shutter is set
	    to be bigger, it will be taken as shutter%maxshutter
nstars: number of natural guide stars
nsubaps: number of active sub-apertures
allsubaps: active + inactive subaps. should be the square of something
saturation: saturation value for the camera
Xwidth: Width in pixels, in the X-axis of a sub-aperture
Ywidth: Width in pixels, in the Y-axis of a sub-aperture
Xgap: Distance in pixels, in the X-axis between subaps
Ygap: Distance in pixels, in the Y-axis between subaps