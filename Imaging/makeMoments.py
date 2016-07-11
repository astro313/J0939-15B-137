##############################################################################
# Last Modified: 11 Jul 2016                                                 #
#
# History:
# 11 July 2016
#       - change '34,52' to '34~52'
#
#
#                                                                            #
# make moments maps for SMM J0939+8315                                       #
#                                                                            #
# Features Tested:                                                           #
#    The script illustrates end-to-end processing with CASA                  #
#    as depicted in the following flow-chart.                                #
#                                                                            #
#    Filenames will have the <prefix> = 'J0939'                              #
#                                                                            #
#      Input Data           Process          Output Data                     #
#                                                                            #
#  <prefix>.clean.image --> immoments  -->  <prefix>.moments.integrated +    #
#                              |            <prefix>.moments.weighted_coord  #
#                              v                                             #
##############################################################################
import os

scriptmode = True

# The prefix to use for all output files
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/J0939'


# cleaned line cube CASA image
imname = prefix + '.clean'
clnimage = imname+'.image'
#=====================================================================
#
# Get some image moments, do 0th and 1st+2nd separately
#
print '--0th ImMoments--'
default('immoments')

imagename = clnimage
moments = [0]
# linechan_FWHM = '68,107'      # for binning=1
linechan_FWHM = '34~52'         # for binning=2 & eyeballing..
chans = linechan_FWHM
stokes = 'I'

# Output root name
momfile = prefix + '.moments'
outfile = momfile + '.integrated'

saveinputs('immoments', prefix + '.immoments0.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')

immoments()
#
#
#
print '--1st, 2nd ImMoments--'
default('immoments')

# higher-O moments, need clipping
imagename = clnimage
moments = [1, 2]
stokes = 'I'

# Need to mask out noisy pixels, 3*sigma
rms = 1.2e-4
upperlim = 3 * rms         # Jy
excludepix = [-100, upperlim]

chans = linechan_FWHM

# Output root name
momfile = prefix + '.moments'
outfile = momfile

saveinputs('immoments', prefix + '.immoments12.saved')
# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')

immoments()

momzeroimage = momfile + '.integrated'
momoneimage = momfile + '.weighted_coord'
momtwoimage = momfile + '.weighted_dispersion_coord'

# It will have made the images:
# --------------------------------------
# J0939.moments.integrated
# J0939.moments.weighted_coord
# J0939.moments.weighted_dispersion_coord

#
#=====================================================================
#
# Get some statistics of the moment images
#
print '--Imstat (moments)--'
default('imstat')

imagename = momzeroimage
momzerostats = imstat()

imagename = momoneimage
momonestats = imstat()

imagename = momtwoimage
momtwostats = imstat()
#=====================================================================
#
# Now view the moments
#
if scriptmode:
    print '--View image (Moments)--'
    viewer(momzeroimage)
    print "You can add mom-1 image " + momoneimage
    print "as a contour plot"
    user_check = raw_input('Return to continue script\n')
