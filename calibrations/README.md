In configurations.cfg,
======================
* camera:	camera's prefix to be given to darc.Control() and others
* pxlx: camera's number of pixles in the x-axis
* pxly: camera's number of pixles in the y-axis
* subapflag: name and path of the subapFlag fits to load
* usebrightest: darc parameter, number of brightest pixels taken into account in subap
* bg\_iter: number of iterations to be used when taking background images
* maxshutter: maximum shutter for this camera. if the shutter is set
        to be bigger, it will be taken as shutter%maxshutter
* nstars: number of natural guide stars
* nsubaps: number of active sub-apertures
* allsubaps: active + inactive subaps. should be the square of something
* saturation: saturation value for the camera
* xwidth: Width in pixels, in the X-axis of a sub-aperture
* ywidth: Width in pixels, in the Y-axis of a sub-aperture
* xgap: Distance in pixels, in the X-axis between subaps
* ygap: Distance in pixels, in the Y-axis between subaps
* fwhm: Estimated FWHM of a central spot

pupil_location errors
======================
Can be corrected by adding some extra pupils to the
left and down the majorPattern used to locate
the pupil's position. This is due to a small optical
misalignment which produces some extra subaps
Star	Error [Xsubaps,Ysubaps]
4	(-1,0)
5	(-1,0)
6	(0,-2.5)
10	(-1,0)
1	(-1,0)
12	(-1,0)
13	(-1,0)
14	(-1,0)
18	(-1,0)
19	(-1,0)
20	(-1,0)
21	(-1,-1)
31	(-1,0)
32	(-1,0)
33	(-1,0)
34	(-1,0)
35	(-1,0)
36	(-1,0)
49	(-1,0)
50	(-1,0)
51	(-1,0)

