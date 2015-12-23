##############################################################################
# Last Modified: 22 Dec 2015                                                 #
#                                                                            #
# TODO:                                                                      #
# -----                                                                      #
# - update flow chart                                                        #
#                                                                            #
#                                                                            #
# Continuum imaging for SMM J0939+8315 with nterms=2                         #
#                                                                            #
# Features Tested:                                                           #
#    The script illustrates end-to-end processing with CASA                  #
#    as depicted in the following flow-chart.                                #
#                                                                            #
#    Filenames will have the <prefix> = 'J0939'                              #
#                                                                            #
#      Input Data          Process          Output Data                      #
#                                                                            #
#                                                                            #
# <prefix>.src.split.ms --> split --> <prefix>_cont.ms +                     #
#                             |       <prefix>_contL.ms +                    #
#                             |       <prefix>_contU.ms                      #
#                             v                                              #
#                          clean --> <prefix>.cont(,L,U).clean.image +       #
#                             |      <prefix>.cont(,L,U).clean.model +       #
#                             |      <prefix>.cont(,L,U).clean.residual      #
#                             v                                              #
#                        exportfits  -->  <prefix>.cont(,L,U).clean.fits     #
#                             |                                              #
#                             v                                              #
#                          imhead    -->  casapy.log                         #
#                             |                                              #
#                             v                                              #
#                          imstat    -->  xstat (parameter)                  #
#                             |                                              #
#                             v                                              #
##############################################################################

'''
Make dirty and clean continuum images

1. LSB+USB
2. USB
3. LSB
'''

import os

scriptmode = False

# The prefix to use for all output files
# nterms=2
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/nterms2/J0939'


contvis = prefix.replace('J0939', 'J0939_cont.ms')
contvisL = prefix.replace('J0939', 'J0939_contL.ms')
contvisU = prefix.replace('J0939', 'J0939_contU.ms')
#=====================================================================
#
# Make and clean continuum map of J0939
#
print '-- Clean (clean) Continuum image --'

contimagename = prefix.replace('J0939', 'J0939_cont')
imname = contimagename + '.clean'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)

default('clean')

vis = contvis
imagename = imname

nterms=2
mode = 'mfs'
psfmode = 'clark'
imsize = [256]
cell = ['0.75arcsec']
niter = 10000
stokes = 'I'
interactive = True
# get offline rms
rms = 0.6        # mJy/beam
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

contimagename = prefix.replace('J0939', 'J0939_contL')
imname = contimagename + '.clean'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)

default('clean')

vis = contvisL
default('clean')
nterms=2
vis = contvisL
imagename = imname
mode = 'mfs'
psfmode = 'clark'
imsize = [256]
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


#######################################################
#=====================================================================
#
# Make and clean continuum map of J0939, high freq baseband
#
print '-- Clean (clean) Continuum image --'

contimagename = prefix.replace('J0939', 'J0939_contU')
imname = contimagename + '.clean'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)


default('clean')
vis = contvisU
imagename = imname
nterms=2
mode = 'mfs'
psfmode = 'clark'
imsize = [256]
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
