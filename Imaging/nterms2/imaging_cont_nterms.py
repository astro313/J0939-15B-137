##############################################################################
# Last Modified: 23 Dec 2015                                                 #
#                                                                            #
#                                                                            #
# Continuum imaging for SMM J0939+8315 with nterms=2, spectral index imaging #
# Only performed across the full band                                        #
#                                                                            #
# TODO:                                                                      #
# -----                                                                      #
# - try gridemode='widefield'                                                #
#                                                                            #
#                                                                            #
# Note:                                                                      #
# ------                                                                     #
# Expect image still dominated by error patterns from "mis-calibration".     #
#     --> self-cal                                                           #
# Final rms should be ~ thermal noise expected from sensitivity calculation  #
#                                                                            #
# However, somehow, the .tt0 seems to have higher noise than nterms=1        #
#                                                                            #
##############################################################################

'''
Make dirty and clean continuum images with nterms=2

1. LSB+USB
'''

import os

scriptmode = False

# The prefix to use for all output files
# nterms=2
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/nterms2/J0939'
contvis = prefix.replace('J0939', 'J0939_cont.ms')

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

nterms = 2
mode = 'mfs'
imsize = [256]
cell = ['0.5arcsec']
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

clnimage = imname + '.image.tt0'
clnalphaimage = clnimage.replace('tt0', 'alpha')


#=====================================================================
#
# Done with imaging
# Now view the image cube of J0939
#
if scriptmode:
    print '--View image--'
    viewer(clnimage)
    user_check = raw_input('Return to continue script\n')
    viewer(clnalphaimage)

rms = 5e-5       # Jy /beam

imview(raster={'file': clnalphaimage,
               'range': [-2, -1],
               'colormap': 'Rainbow 2', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': clnimage,
                'levels': [-6, -3, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16],
                'unit': rms},       # Jy/beam
       zoom=3)

#=====================================================================
#
# Blank spectral index image based on a cut-off level of the total intensity image
# (DOESN'T WORK)
#

# print '--Blank spectral index image--'
# rms = 5e-5
# cutoff = 6*rms / (1 - (35.42/27.82)**(-1))
# imagename = [clnalphaimage, clnimage]
# expr = 'iff(IM1 >= cutoff, IM0, -3)'            # Jy
# outfile = imname + '.image.clip.alpha'
# mode = 'evalexpr'
# stokes = 'I'
# inp(immath)
# saveinputs(immath, clnalphaimage+'blank.immath.saved')
# immath()


#=====================================================================
#
# export the Final CLEAN Image as FITS
# Run asynchronously so as not to interfere with other tasks
#
print '--Final Export CLEAN FITS--'
default('exportfits')
#
clnfits = prefix + '.cont.clean.tt0.fits'
#
imagename = clnimage
fitsimage = clnfits
async = True
#
saveinputs('exportfits', prefix + 'cont.clean.tt0.exportfits.saved')
#
exportfits()


clnfits = prefix + '.cont.clean.alpha.fits'
#
imagename = clnalphaimage
fitsimage = clnfits
saveinputs('exportfits', prefix + 'cont.clean.alpha.exportfits.saved')
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
#
# Analysis - intensity-weighted mean spectral index over some region:
# use immath() to blink .tt0 and .tt1 based on ~ 5*sigma on .tt0
#

clntt0alphaimage = clnimage.replace('tt0', 'tt1')
cutoff = 5 * 5e-5    # 0.00025

immath(imagename=[clntt0alphaimage, clnimage], mode='evalexpr', expr='IM0[IM1>0.00025]', outfile=clntt0alphaimage + '.filtered')

immath(imagename=[clnimage, clnimage], mode='evalexpr', expr='IM0[IM1>0.00025]', outfile=clnimage + '.filtered')

blob1 = '113,120,122,132'

# note the emission region of interest
mystat = imstat(clntt0alphaimage+'.filtered', box=blob1)
avgtt0alpha = mystat['mean'][0]
#
mystat = imstat(clnimage + '.filtered', box=blob1)
avgtt0 = mystat['mean'][0]
avgalpha = avgtt0alpha / avgtt0
print 'Intensity-weighted alpha = ' + str(avgalpha)
# Intensity-weighted alpha = -2.00598605771


mystat = imstat(clntt0alphaimage+'.filtered', region='blob2.crtf')
avgtt0alpha = mystat['mean'][0]
#
mystat = imstat(clnimage + '.filtered', region='blob2.crtf')
avgtt0 = mystat['mean'][0]
avgalpha = avgtt0alpha / avgtt0
print 'Intensity-weighted alpha = ' + str(avgalpha)
# Intensity-weighted alpha = -1.78551101681
