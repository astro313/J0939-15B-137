##############################################################################
# Last Modified: 16 Dec 2015                                                 #
#                                                                            #
# TODO:                                                                      #
# -----                                                                      #
# - update flow chart                                                        #
#                                                                            #
# Imaging Script for SMM J0939+8315                                          #
#                                                                            #
# Features Tested:                                                           #
#    The script illustrates end-to-end processing with CASA                  #
#    as depicted in the following flow-chart.                                #
#                                                                            #
#    Filenames will have the <prefix> = 'J0939'                              #
#                                                                            #
#      Input Data           Process          Output Data                     #
#                                                                            #
#     3C220.3CAL.ms  -->    listobs    -->  imaging.log                      #
#                              |                                             #
#                              v                                             #
#                            split     -->  <prefix>.src.split.ms            #
#                              |                                             #
#                              v                                             #
#                [OPTIONAL]  split     -->  <prefix>.cal.split.ms            #
#                              |                                             #
#                              v                                             #
#            [OPTIONAL]  exportuvfits  -->  <prefix>.split.uvfits            #
#                                                                            #
#                                                                            #
# <prefix>.src.split.ms-->clean--><prefix>.withcont.clean.image +            #
#                                 <prefix>.withcont.clean.model +            #
#                                 <prefix>.withcont.clean.residual           #
#                                                                            #
#                                                                            #
# <prefix>.src.split.ms --> uvcontsub  -->  <prefix>.ms.cont +               #
#                              |               <prefix>.ms.contsub           #
#                              v                                             #
#                            clean     -->  <prefix>.clean.image +           #
#                              |            <prefix>.clean.model +           #
#                              |            <prefix>.clean.residual          #
#                              v                                             #
#                         exportfits   -->  <prefix>.clean.fits              #
#                              |                                             #
#                              v                                             #
#                           imhead     -->  casapy.log                       #
#                              |                                             #
#                              v                                             #
#                           imstat     -->  xstat (parameter)                #
#                              |                                             #
#                              v                                             #
#                          immoments   -->  <prefix>.moments.integrated +    #
#                              |            <prefix>.moments.weighted_coord  #
#                              v                                             #
##############################################################################

import os

scriptmode = True
#
# Set up some useful variables
#
# Get to path to the CASA home and stip off the name
# pathname = os.environ.get('CASAPATH').split()[0]

# The prefix to use for all output files
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/J0939'

# Clean up old files
os.system('rm -rf '+prefix+'*')

vis = "/data/dleung/DATA/VLA/15B-137/Imaging/3C220.3CAL.ms"
#=====================================================================
#
# List a summary of the MS
#
print '--Listobs--'

# Don't default this one and make use of the previous setting of
# vis.  Remember, the variables are GLOBAL!

# You may wish to see more detailed information, like the scans.
# In this case use the verbose = True option
verbose = True

listobs()

#=====================================================================
#
# Split the sources out, pick off the CORRECTED_DATA column
#
#
# Split J0939 data (before continuum subtraction)
#
print '--Split J0939 Data--'
default('split')

splitms = prefix + '.src.split.ms'
outputvis = splitms
field = '2'
spw = ''
datacolumn = 'corrected'

saveinputs('split', prefix+'.split.J0939.saved')

split()

print "Created "+splitms

# If you want, split out the calibrater J1153+8058_SNR field, all chans
#print '--Split J1153+8058 Data--'
#
#calsplitms = prefix + '.cal.split.ms'
#outputvis = calsplitms
#field = '1153*'
#
#saveinputs('split',prefix+'.split.J1153+8058_SNR.saved')
#
#split()

#=====================================================================
#
# export the J0939 data as UVFITS (before removing cont)
# Start with the split file.
# Since this is a split dataset, the calibrated data is
# in the DATA column already.
# Write as a multisource UVFITS (with SU table)
# even though it will have only one field in it
# Run asynchronously so as not to interfere with other tasks
#
#print '--Export UVFITS--'
#default('exportuvfits')
#
#srcuvfits = prefix + '.split.uvfits'
#
#vis = splitms
#fitsfile = srcuvfits
#datacolumn = 'data'
#multisource = True
#async = True
#
#saveinputs('exportuvfits',prefix+'.exportuvfits.saved')
#
#myhandle = exportuvfits()
#
#print "The return value for this exportuvfits async task for tm is "+str(myhandle)

#=====================================================================
#
# Make dirty image before removing continuum
#
print '--Clean (make dirty image) prior to cont. subtraction --'
default('clean')

# splited source
vis = splitms
imname = prefix + '.withcont.dirty'
os.system('rm -rf '+imname+'*')
imagename = imname
#
restfreq = str(freq_CO_J0939)+'GHz'
freq_lastChan = 35.965      # GHz
start_velo = (freq_CO_J0939 - freq_lastChan)/freq_CO_J0939 * 3e10/1e5

mode = 'velocity'
nchan = -1
start = str(start_velo)+'km/s'
# width = '29km/s'          # ~ 1.5 channels of 2 MHz (native)
width = '16.7656km/s'       # 1 channel, i.e. highest spec. resolution
#
spw = ''
imsize = [256]
cell = [0.75]
stokes='I'
niter = 0
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean',imname.replace('.dirty','.invert.saved'))

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check=raw_input('Return to continue script\n')

clean()

#=====================================================================
#
# Now clean an image cube of J0939
#

print '--      Clean (clean)          --'
print '---- prior to removing cont. ----'
default('clean')

vis = srcsplitms
restfreq = str(freq_CO_J0939)+'GHz'
imname = prefix + '.withcont.clean'
os.system('rm -rf '+imname+'*')
imagename = imname

# Set up the output image cube
mode = 'velocity'
nchan = -1
start = str(start_velo)+'km/s'
# width = '29km/s'          # ~ 1.5 channels of 2 MHz (native)
width = '16.7656km/s'       # 1 channel, i.e. highest spec. resolution

gain = 0.1
imsize = [256]
cell = [0.75]
niter = 6000
interactive = True

# Also set flux residual threshold (in mJy)
threshold = 1.0
# Do a simple Clark clean
psfmode = 'clark'

saveinputs('clean', imname.replace('.dirty','.invert.saved'))

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check=raw_input('Return to continue script\n')

clean()


#=====================================================================
#
# UV-plane continuum subtraction on the target
# - use the splited ms
# - will update the CORRECTED_DATA column
#
# Files:
# original J0939.src.split.ms: uv-continuum subtracted (CORRECTED_DATA column)
#                              continuum (MODEL_DATA column)
#
# J0939.ms.contsub: uv-subtracted visibilities (DATA column) --> useful
# J0939.ms.cont: pseudo-continuum visibilities (as fit). --> not useful
#
#
# Probably want to fit through all spws (both basebands)
#
# NOTE:
# Imaging the continuum produced by uvcontsub with want_cont=True will lead to
# extremely poor continuum images because
# of bandwidth smearing effects.
#
# For imaging the continuum, should create a line-free continuum data set. see imaging_cont.py
#

print '--UV Continuum Subtract--'
default('uvcontsub')

vis = splitms

field = '0'
fitspw = '0,1,2,3,4,5,7,8,9,10,11,12,13,14,15'

# only output the high frequency baseband spws
spw = '0,1,2,3,4,5,6,7'
combine = 'scan,spw'

# Let it split out the data automatically for us
splitdata = True
solint = 0.0
fitorder = 1
fitmode = 'subtract'

saveinputs('uvcontsub', prefix+'.uvcontsub.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check=raw_input('Return to continue script\n')

uvcontsub()

# You will see it made two new MS (with want_cont=True):
# <vis>.cont
# <vis>.contsub

# You will see it made a new MS ONLY (with want_cont=False):
# <vis>.contsub

srcsplitms = vis + '.contsub'

#=====================================================================
#
# Look for line after removing cont., may not see if line is weak
#
plotms(vis=srcsplitms, xaxis="frequency", yaxis="amp", avgtime='1e7', avgscan=True, avgbaseline=True)

freq_CO = 115.2712 # GHz
z = 2.221
freq_CO_J0939 = freq_CO / (1+z)
restfreq = str(freq_CO_J0939)+'GHz'

print '-- Check if line is there --'
plotms(vis=srcsplitms,xaxis="velocity",yaxis="amp", ydatacolumn="data",selectdata=True, spw="6", avgtime="1e7", correlation='LL,RR')

#=====================================================================
#
# make a dirty image cube
#
print '--Clean (make dirty image) after removing cont.--'
default('clean')

# splited source continuum-subtracted data
vis = srcsplitms
imname = prefix + '.dirty'
os.system('rm -rf '+imname+'*')
imagename = imname
#
restfreq = str(freq_CO_J0939)+'GHz'
mode = 'velocity'
nchan = -1
start = str(start_velo)+'km/s'
# width = '29km/s'          # ~ 1.5 channels of 2 MHz (native)
width = '16.7656km/s'       # 1 channel, i.e. highest spec. resolution
#
spw = ''
imsize = [256]
cell = [0.75]
stokes='I'
niter = 0
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean',prefix+'.invert.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check=raw_input('Return to continue script\n')

clean()

# get offline rms
rms = 0.17        # mJy/beam

#=====================================================================
# Now clean an image cube of J0939
#
# Channel Mask (if not too broad velo range):
# 1. Step through channel with the most extended (in angular size) emission,
# 2. Select "all channels" for the clean mask,
# 3. Select the polygon tool and make a single mask that applies to all channels.
# 4. Double click inside it to save the mask region
# 5. Check that emission in all channels fits within the mask.
# 6. If need to modify for different chan, use toogle buttons above to add and erase
#
# note: If interactive clean, and no mask, clean will stop immediately because it has nothing to clean. (no default mask)
#
print '-- Clean (clean) line cube after removing continuum --'
default('clean')

vis = srcsplitms
restfreq = str(freq_CO_J0939)+'GHz'
imname = prefix + '.clean'
os.system('rm -rf '+imname+'*')
imagename = imname

# Set up the output image cube
mode = 'velocity'
nchan = -1
start = str(start_velo)+'km/s'
# width = '29km/s'          # ~ 1.5 channels of 2 MHz (native)
width = '16.7656km/s'       # 1 channel, i.e. highest spec. resolution

gain = 0.1
imsize = [256]
cell = [0.75]
niter = 6000
interactive = True

# Also set flux residual threshold (in mJy)
threshold = rms
# Do a simple Clark clean
psfmode = 'clark'


# No Cotton-Schwab iterations
# csclean = False
# If desired, you can do a Cotton-Schwab clean
# csclean = True
# Twice as big for Cotton-Schwab (cleans inner quarter)
#imsize = [512,512]

# Set up the weighting
# Use Briggs weighting (a moderate value, on the uniform side)
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean',prefix+'.clean.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check=raw_input('Return to continue script\n')

clean()

clnimage = imname+'.image'
#=====================================================================
#
# Done with imaging
# Now view the image cube of J0939
#
if scriptmode:
    print '--View image--'
    viewer(clnimage)
    user_check=raw_input('Return to continue script\n')

viewer(clnimage)
#
# Alternatively, you can use the scripting "imview" approach.
#
imview(raster={'file': clnimage,
                       'range': [-0.001,3e-3],
                       'colormap': 'Rainbow 2', 'scaling': 0.0, 'colorwedge': True},
               contour={'file': clnimage,
                        'levels': [-6,-3,3,4,5,6,7,8,9,12,15,16],
                        'unit': 0.00017}, zoom=3)


#=====================================================================
#
# export the Final CLEAN Image as FITS
# Run asynchronously so as not to interfere with other tasks
#
print '--Final Export CLEAN FITS--'
default('exportfits')
#
clnfits = prefix + '.clean.fits'
#
imagename = clnimage
fitsimage = clnfits
async = True
#
saveinputs('exportfits',prefix+'.exportfits.saved')
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

#=====================================================================
#
# Get the cube statistics
#
print '--Imstat (cube)--'
default('imstat')

imagename = clnimage

# Do whole image
#box = ''
# or define a region
box = '30,30,218,100'

cubestats = imstat()

# Statistics will printed to the terminal, and the output
# parameter will contain a dictionary of the statistics

#=====================================================================
#
# Get some image moments, do 0th and 1st+2nd separately
#
print '--0th ImMoments--'
default('immoments')

imagename = clnimage
moments = [0]
chans = '68,107'
stokes='I'

# Output root name
momfile = prefix + '.moments'
outfile = momfile+'.integrated'

saveinputs('immoments',prefix+'.immoments0.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check=raw_input('Return to continue script\n')

immoments()
#
#
#
print '--1st, 2nd ImMoments--'
default('immoments')

# higher-O moments, need clipping
imagename = clnimage
moments = [1,2]
stokes='I'

# Need to mask out noisy pixels, 3*sigma
upperlim = 3 * rms * 1e-3        # Jy
excludepix = [-100, upperlim]

chans = '68,107'

# Output root name
momfile = prefix + '.moments'
outfile = momfile

saveinputs('immoments',prefix+'.immoments12.saved')
# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check=raw_input('Return to continue script\n')

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
    print "You can add mom-1 image "+momoneimage
    print "as a contour plot"
    user_check=raw_input('Return to continue script\n')

