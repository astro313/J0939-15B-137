'''
Script is customized for specific dataset, need to modify paramters for other dataset (even data of the same observations)
- e.g. prefix, vis, stokes, start_velo, binning, restfreq, clean rms, viewer rms, etc


Note, clean mask can be re-used, but gridding must be the same (nchan, imagesize, cellsize, etc)
'''

##############################################################################
# Last Modified: 22 Dec 2015                                                 #
#                                                                            #
# Imaging Script for SMM J0939+8315 using Clark CLEAN                        #
#                                                                            #
#                                                                            #
# TODO:                                                                      #
# -----                                                                      #
# - update flow chart                                                        #
# - consider adding script to split out just LL,RR before imaging            #
#                                                                            #
#                                                                            #
#                                                                            #
#                                                                            #
# Note:                                                                      #
# -----                                                                      #
# - uvcontsub() solint='int' same as solint=0.0 (i.e. no time averaging)     #
#                                                                            #
#                                                                            #
# History:                                                                   #
# --------                                                                   #
# 22 Dec 2015: updated flow chart to be consistent with code                 #
# 16 Dec 2015: Generated script                                              #
#                                                                            #
#                                                                            #
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
# (NOT WORKING)                                                              #
# <prefix>.src.split.ms-->clean--><prefix>.withcont.clean.image +            #
#                                 <prefix>.withcont.clean.model +            #
#                                 <prefix>.withcont.clean.residual           #
#                                                                            #
#                                                                            #
# <prefix>.src.split.ms --> uvcontsub  --> <prefix>.src.split.ms.contsub     #
#                              |                                             #
#                              v                                             #
#                            clean     -->  <prefix>.dirty.image +           #
#                              |            <prefix>.dirty.model +           #
#                              |            <prefix>.dirty.residual          #
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
##############################################################################

import os
import time

benchmarking = True
scriptmode = False

# The prefix to use for all output files
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/J0939'

# Clean up old files
if scriptmode:
    user_check = raw_input(
        "Do you want to remove existing files before continue? (Y/N) \n")
    if user_check == 'Y':
        # continuum maps named with underscore
        os.system('rm -rf ' + prefix + '.*')

vis = "/data/dleung/DATA/VLA/15B-137/Imaging/3C220.3CAL.ms"
#=====================================================================
# Start timing
if benchmarking:
    startTime = time.time()
    startProc = time.clock()

#
# List a summary of the MS
#
print '--Listobs--'
verbose = True

listobs()

#=====================================================================
#
# Split the sources out, pick off the CORRECTED_DATA column
#
#
# Split J0939 data (before continuum subtraction)

print '--Split J0939 Data--'
default('split')


vis = "/data/dleung/DATA/VLA/15B-137/Imaging/3C220.3CAL.ms"
splitms = prefix + '.src.split.ms'
outputvis = splitms
field = '2'
spw = ''
datacolumn = 'corrected'

saveinputs('split', prefix + '.split.J0939.saved')

split()

# print "Created "+splitms
#
# If you want, split out the calibrater J1153+8058_SNR field, all chans
# print '--Split J1153+8058 Data--'
#
#calsplitms = prefix + '.cal.split.ms'
#outputvis = calsplitms
#field = '1153*'
#
# saveinputs('split',prefix+'.split.J1153+8058_SNR.saved')
#
# split()

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
# print '--Export UVFITS--'
# default('exportuvfits')
#
#srcuvfits = prefix + '.split.uvfits'
#
#vis = splitms
#fitsfile = srcuvfits
#datacolumn = 'data'
#multisource = True
#async = True
#
# saveinputs('exportuvfits',prefix+'.exportuvfits.saved')
#
#myhandle = exportuvfits()
#
# print "The return value for this exportuvfits async task for tm is
# "+str(myhandle)

# #=====================================================================
# #
# # (for some reason, it doesn't work...) - the resulting cube has emission in all channels
# # Make dirty image before removing continuum
# #
# print '--Clean (make dirty image) prior to cont. subtraction --'
# default('clean')

# # splited source
# vis = splitms
# imname = prefix + '.withcont.dirty'
# os.system('rm -rf '+imname+'*')
# imagename = imname
# #
# #
freq_CO = 115.2712  # GHz
z = 2.221
freq_CO_J0939 = freq_CO / (1 + z)
restfreq = str(freq_CO_J0939) + 'GHz'
freq_lastChan = 35.965      # GHz
start_velo = (freq_CO_J0939 - freq_lastChan) / freq_CO_J0939 * 3e10 / 1e5
specRes = 16.7656            # native spec. res. = 2 MHz
# #
# mode = 'velocity'
# start = str(start_velo)+'km/s'
# binning = 2         # 29km/s ~ 1.5 channels of native spec. res.
# # nchan = -1        # make the max # of chan. before deciding how many I need
# nchan = 215/binning         # for high freq baseband to span up to 2000km/s
# width = str(binning * specRes) + 'km/s'

# #
# spw = ''
# imsize = [256]
# cell = [0.75]
# stokes='I'
# niter = 0
# # weighting = 'briggs'
# # robust = 0.5

# saveinputs('clean',imname.replace('.dirty','.invert.saved'))

# # Pause script if you are running in scriptmode
# if scriptmode:
#     inp()
#     user_check=raw_input('Return to continue script\n')

# clean()

# #=====================================================================
# #
# # (for some reason, it doesn't work...) - the resulting cube has emission in all channels
# # Now clean an image cube of J0939
# #

# print '--      Clean (clean)          --'
# print '---- prior to removing cont. ----'
# default('clean')

# vis = splitms
# restfreq = str(freq_CO_J0939)+'GHz'
# imname = prefix + '.withcont.clean'
# os.system('rm -rf '+imname+'*')
# imagename = imname

# # Set up the output image cube
# mode = 'velocity'
# start = str(start_velo)+'km/s'
# binning = 2         # 29km/s ~ 1.5 channels of native spec. res.
# # nchan = -1        # make the max # of chan. before deciding how many I need
# nchan = 215/binning         # for high freq baseband to span up to 2000km/s
# width = str(binning * specRes) + 'km/s'

# gain = 0.1
# imsize = [256]
# cell = [0.75]
# niter = 10000
# interactive = True

# # Also set flux residual threshold (in mJy)
# threshold = 1.0
# # Do a simple Clark clean
# psfmode = 'clark'

# saveinputs('clean', imname.replace('.dirty','.invert.saved'))

# # Pause script if you are running in scriptmode
# if scriptmode:
#     inp()
#     user_check=raw_input('Return to continue script\n')

# clean()


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
#
vis = splitms
#
field = '0'
fitspw = '0,1,2,3,4,5,7,8,9,10,11,12,13,14,15'
#
# only output the high frequency baseband spws
spw = '0,1,2,3,4,5,6,7'
combine = 'scan,spw'

# Let it split out the data automatically for us
splitdata = True
solint = 0.0          # same as 'int', i.e. not time averaging
fitorder = 1
fitmode = 'subtract'

saveinputs('uvcontsub', prefix + '.uvcontsub.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')

uvcontsub()

# You will see it made a new MS ONLY (with want_cont=False):
# <vis>.contsub

splitms = vis + '.contsub'

#=====================================================================
#
# Look for line after removing cont., may not see if line is weak
#
if scriptmode:
    plotms(vis=splitms, xaxis="frequency", yaxis="amp",
           avgtime='1e7', avgscan=True, avgbaseline=True)

    print '-- Check if line is there --'
    plotms(vis=splitms, xaxis="velocity", yaxis="amp", ydatacolumn="data",
           selectdata=True, spw="6", avgtime="1e7", correlation='LL,RR')
#
#=====================================================================
#
# make a dirty image cube
#
print '--Clean (make dirty image) after removing cont.--'
default('clean')

# splited source continuum-subtracted data
vis = splitms
imname = prefix + '.dirty'
os.system('rm -rf ' + imname + '*')
imagename = imname
#
restfreq = str(freq_CO_J0939) + 'GHz'
mode = 'velocity'
start = str(start_velo) + 'km/s'
binning = 2         # 29km/s ~ 1.5 channels of native spec. res.
# nchan = -1        # make the max # of chan. before deciding how many I need
nchan = 215 / binning         # for high freq baseband to span up to 2000km/s
width = str(binning * specRes) + 'km/s'
#
spw = ''
imsize = [256]
cell = [0.75]
stokes = 'I'
niter = 0
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.invert.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')

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

vis = splitms
restfreq = str(freq_CO_J0939) + 'GHz'
imname = prefix + '.clean'
for ext in ['.flux', '.image', '.model', '.pbcor', '.psf', '.residual',
            '.flux.pbcoverage']:
    rmtables(imname + ext)
imagename = imname

# Set up the output image cube
mode = 'velocity'
start = str(start_velo) + 'km/s'
binning = 2         # 29km/s ~ 1.5 channels of native spec. res.
# nchan = -1        # make the max # of chan. before deciding how many I need
nchan = 215 / binning         # for high freq baseband to span up to 2000km/s
width = str(binning * specRes) + 'km/s'

gain = 0.1
imsize = [256]
cell = [0.75]
niter = 10000
interactive = True

# Also set flux residual threshold (in mJy)
threshold = rms
# Do a simple Clark clean
psfmode = 'clark'

# Set up the weighting
# Use Briggs weighting (a moderate value, on the uniform side)
# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.clean.saved')

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
    user_check = raw_input('close viewer, hit Return to continue script\n')

viewer(clnimage)
#
# Alternatively, you can use the scripting "imview" approach.
#
imview(raster={'file': clnimage,
               'range': [-0.001, 3e-3],
               'colormap': 'Rainbow 2', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': clnimage,
                'levels': [-6, -3, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16],
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
saveinputs('exportfits', prefix + '.exportfits.saved')
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
#
# Get the cube INFO
#
print '--Imhead (cube)--'
default('imhead')

imagename = clnimage

bmaj = imhead(imagename=imagename, mode="get", hdkey="bmaj")['value']
bmin = imhead(imagename=imagename, mode="get", hdkey="bmin")['value']
bpa = imhead(imagename=imagename, mode="get", hdkey="bpa")['value']
restfreq_Hz = imhead(imagename=imagename, mode="get", hdkey="restfreq")['value']
specRes_freq = imhead(imagename=imagename, mode="get", hdkey="cdelt4")['value']

nchan = imhead(imagename=imagename, mode="get", hdkey="shape")[3]
#=====================================================================
#
# Get the cube statistics
#
print '--Imstat (cube)--'
default('imstat')

imagename = clnimage

box_on = '110,110,140,140'
box_off = '30,30,218,100'

box = box_on
cubestats_on = imstat()
peak = (cubestats_on['max'][0])


box = box_off
cubestats_off = imstat()
rms = (cubestats_off['rms'][0])

print '>> Peak: ' + str(peak)
print '>> rms: ' + str(rms)
print '>> Dynamic range: ' + str(peak / rms)
# Statistics will printed to the terminal, and the output
# parameter will contain a dictionary of the statistics


#=====================================================================
# DONE
#=====================================================================
if benchmarking:
    endProc = time.clock()
    endTime = time.time()

#=====================================================================
# Benchmarking numbers
#=====================================================================
if benchmarking:
    walltime = (endTime - startTime)
    cputime = (endProc - startProc)

    print ''
    print '  Total wall clock time was: %10.3f ' % walltime
    print '  Total CPU        time was: %10.3f ' % cputime
    print ''
    casalog.post('')
    casalog.post('  Total wall clock time was: %10.3f ' % walltime, 'INFO')
    casalog.post('  Total CPU        time was: %10.3f ' % cputime)
    casalog.post('')

#=====================================================================
# Regression values (lite)
#=====================================================================
if regressout:
    # Set up date and version info
    import datetime
    datestring = datetime.datetime.isoformat(datetime.datetime.today())
    myvers = casalog.version()
    myuname = os.uname()
    myhost = myuname[1]
    myos = myuname[0] + ' ' + myuname[2] + ' ' + myuname[4]
    # Set up output file and version info
    outfile = prefix + '.' + datestring + '.log'
    logfile = open(outfile, 'w')

    # Print version info to outfile
    print >>logfile, '---------------------------------------------------'
    print >>logfile, 'Results for J0939 VLA D config from 15B-137'
    print >>logfile, '---------------------------------------------------'
    print >>logfile, 'Running ' + myvers + ' on host ' + myhost
    print >>logfile, 'at ' + datestring
    print >>logfile, 'for OS ' + myos
    print >>logfile, ''

    print >>logfile, '  %40s : %12.7f ' % ('J0939 Combined I maximum (Jy)',
                                           peak)
    print >>logfile, '  %40s : %12.7f ' % ('J0939 Combined  I off-source rms (Jy)', rms)
    print >>logfile, '  %40s : %12.3f ' % ('J0939 Combined  I dynamic range',
                                           peak/rms)
    print >>logfile, ''
    print >>logfile, '  %40s : %4.1f x %4.1f, %4.1f ' % ('Clean Beam size', bmaj, bmin, bpa)
    print >>logfile, '  %40s : %12.7f ' % ('Rest frequency (Hz)',
                                           restfreq_Hz)
    print >>logfile, '  %40s : %12d ' % ('J0939 number of channels in cube', nchan)
    print >>logfile, ''
    print >>logfile, '  %40s : %12.7f ' % ('Spectral resolution in frequency (Hz)', specRes_freq)

    if benchmarking:
        print >>logfile, ''
        print >>logfile, '  Total wall clock time was: %10.3f ' % walltime
        print >>logfile, '  Total CPU        time was: %10.3f ' % cputime
        print >>logfile, ''

    logfile.close()
    print ""
    print "Results written to " + outfile

print ""
print "Done with J0939 Line imaging"
