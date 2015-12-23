###############################################################################
# Last Modified: 22 Dec 2015                                                  #
#                                                                             #
# TODO:                                                                       #
# -----                                                                       #
#                                                                             #
#                                                                             #
# Continuum imaging for SMM J0939+8315 with Cotton Schwab, nterms=2           #
#                                                                             #
# Features Tested:                                                            #
#    The script illustrates end-to-end processing with CASA                   #
#    as depicted in the following flow-chart.                                 #
#                                                                             #
#    Filenames will have the <prefix> = 'J0939.imCS'                          #
#                                                                             #
#      Input Data              Process          Output Data                   #
#                                                                             #
#                                                                             #
# <splitmsprefix>_cont.ms + --> clean --> <prefix>.cont(,L,U).clean.image +   #
# <splitmsprefix>_contL.ms +      |      <prefix>.cont(,L,U).clean.model  +   #
# <splitmsprefix>_contU.ms        |      <prefix>.cont(,L,U).clean.residual   #
#                                 v                                           #
#                            exportfits  -->  <prefix>.cont(,L,U).clean.fits  #
#                                 |                                           #
#                                 v                                           #
#                              imhead    -->  casapy.log                      #
#                                 |                                           #
#                                 v                                           #
#                              imstat    -->  xstat (parameter)               #
#                                 |                                           #
#                                 v                                           #
###############################################################################

'''
Make dirty and clean continuum images

1. LSB+USB
2. USB
3. LSB
'''

import os

scriptmode = True

# The prefix to use for all output files
splitmsprefix = '/data/dleung/DATA/VLA/15B-137/Imaging/J0939'
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/J0939.imCS'
splitms = splitmsprefix + '.src.split.ms'
outputvis = splitms

contvis = splitmsprefix.replace('J0939', 'J0939_cont.ms')
contvisL = splitmsprefix.replace('J0939', 'J0939_contL.ms')
contvisU = splitmsprefix.replace('J0939', 'J0939_contU.ms')


#=====================================================================
#
# Make and clean continuum map of J0939
# 1. LSB+USB
#
print '-- Clean (clean) Continuum image --'
default('clean')

vis = contvis
contimagename = splitmsprefix.replace('J0939', 'J0939_cont')
imname = contimagename + '.clean'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)
os.system('rm -rf ' + imname + '*')

nterms=2
mode = 'mfs'
imagermode='csclean'
# imsize = [256]
imsize=[512]
cell = ['0.75arcsec']
niter = 10000
stokes = 'I'
interactive = True
rms = 0.1        # mJy/beam
threshold = rms

# Set up the weighting
# Use Briggs weighting (a moderate value, on the uniform side)
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.cont.clean.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')


clean()

clnimage = imname + '.image'
#=====================================================================
#
# Done with imaging
# Now view the image cube of J0939
#
if scriptmode:
    print '--View image--'
    viewer(clnimage)
    user_check = raw_input('Return to continue script\n')

viewer(clnimage)
rms = 5.2e-5       # Jy /beam
#
# Alternatively, you can use the scripting "imview" approach.
#
imview(raster={'file': clnimage,
               'range': [-1.5e-4, 1.5e-2],
               'colormap': 'Rainbow 2', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': clnimage,
                'levels': [-6, -3, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16],
                'unit': rms},       # Jy/beam
       zoom=3)


#=====================================================================
#
# export the Final CLEAN Image as FITS
# Run asynchronously so as not to interfere with other tasks
#
print '--Final Export CLEAN FITS--'
default('exportfits')
#
clnfits = prefix + '.cont.clean.fits'
#
imagename = clnimage
fitsimage = clnfits
async = True
#
saveinputs('exportfits', prefix+'cont.clean.exportfits.saved')
#
exportfits()

#=====================================================================
#
# Print the image header
#
print '--Imhead--'
default('imhead')

imagename = clnimage

mode = 'summary'

imhead()

# A summary of the cube will be seen in the logger


# ------------ Repeat for basebnad continuum image --------------
#=====================================================================
#
# Make and clean continuum map of J0939
#
print '-- Clean (clean) Continuum image --'
default('clean')

vis = contvisL
contimagename = splitmsprefix.replace('J0939', 'J0939_contL')
imname = contimagename + '.clean'
os.system('rm -rf ' + imname + '*')
imagename = imname

nterms=2
mode = 'mfs'
# psfmode = 'clark'
# imsize = [256]
imagermode='csclean'
imsize = [512]
cell = ['0.75arcsec']
niter = 10000
stokes = 'I'
interactive = True

rms = 0.45        # mJy/beam
threshold = rms

# Set up the weighting
# Use Briggs weighting (a moderate value, on the uniform side)
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.contL.clean.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')


clean()

clnimage = imname + '.image'
#=====================================================================
#
# Done with imaging
# Now view the image cube of J0939
#
if scriptmode:
    print '--View image--'
    viewer(clnimage)
    user_check = raw_input('Return to continue script\n')

viewer(clnimage)
rms = 4.5e-5
#
# Alternatively, you can use the scripting "imview" approach.
#
imview(raster={'file': clnimage,
               'range': [-0.001, 1e-2],
               'colormap': 'Rainbow 2', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': clnimage,
                'levels': [-6, -3, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16],
                'unit': rms},       # Jy/beam
       zoom=3)


#=====================================================================
#
# export the Final CLEAN Image as FITS
# Run asynchronously so as not to interfere with other tasks
#
print '--Final Export CLEAN FITS--'
default('exportfits')
#
clnfits = prefix + '.contL.clean.fits'
#
imagename = clnimage
fitsimage = clnfits
async = True
#
saveinputs('exportfits', prefix+'.contL.clean.exportfits.saved')
#
exportfits()

#=====================================================================
#
# Print the image header
#
print '--Imhead--'
default('imhead')

imagename = clnimage

mode = 'summary'

imhead()

# A summary of the cube will be seen in the logger

#=====================================================================
# high frequency baseband
#
# Make and clean continuum map of J0939
#
print '-- Clean (clean) Continuum image --'
default('clean')

vis = contvisU
contimagename = splitmsprefix.replace('J0939', 'J0939_contU')
imname = contimagename + '.clean'
os.system('rm -rf ' + imname + '*')
imagename = imname

nterms=2
mode = 'mfs'
# psfmode = 'clark'
imagermode='csclean'
# imsize = [256]
imsize=[512]
cell = ['0.75arcsec']
niter = 10000
stokes = 'I'
interactive = True
rms = 0.24        # mJy/beam
threshold = threshold

# Set up the weighting
# Use Briggs weighting (a moderate value, on the uniform side)
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.contU.clean.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')


clean()

clnimage = imname + '.image'
#=====================================================================
#
# Done with imaging
# Now view the image cube of J0939
#
if scriptmode:
    print '--View image--'
    viewer(clnimage)
    user_check = raw_input('Return to continue script\n')

viewer(clnimage)
#
# Alternatively, you can use the scripting "imview" approach.
#
imview(raster={'file': clnimage,
               'range': [-0.001, 3e-3],
               'colormap': 'Rainbow 2', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': clnimage,
                'levels': [-6, -3, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16],
                'unit': threshold / 1e3},       # Jy/beam
       zoom=3)


#=====================================================================
#
# export the Final CLEAN Image as FITS
# Run asynchronously so as not to interfere with other tasks
#
print '--Final Export CLEAN FITS--'
default('exportfits')
#
clnfits = prefix + '.contU.clean.fits'
#
imagename = clnimage
fitsimage = clnfits
async = True
#
saveinputs('exportfits', prefix+'contU.clean.exportfits.saved')
#
myhandle2 = exportfits()

#=====================================================================
#
# Print the image header
#
print '--Imhead--'
default('imhead')

imagename = clnimage

mode = 'summary'

imhead()

# A summary of the cube will be seen in the logger
