##############################################################################
# Last Modified: 16 Dec 2015                                                 #
#                                                                            #
# TODO:                                                                      #
# -----                                                                      #
# - update flow chart                                                        #
# - fix bug, put vis= after rmtable()                                        #
#                                                                            #
# Continuum imaging for SMM J0939+8315                                       #
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
# default nterms
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/J0939'

splitms = prefix + '.src.split.ms'
outputvis = splitms

#=====================================================================
# Create an Averaged Continuum MS by averaging line-free channels
# in both basebands
#
# use this for continuum imaging, not the one from uvcontsub
#

casalog.post('-- Create an Averaged Continuum MS of Both Basebands--', 'INFO')
print '-- Create an Averaged Continuum MS of Both Basebands--'


# Use plotms to identify line and continuum spw
# Only possible to see if the line is very STRONG
# If can't see, then just use the spws that we know is line-free
plotms(vis=outputvis, xaxis='channel', yaxis='amp', ydatacolumn='data', avgtime='1e8s', avgscan=True, avgchannel='2', iteraxis='spw')

plotms(vis=outputvis, xaxis="frequency", yaxis="amp",
       avgtime='1e7', avgscan=True, avgbaseline=True)

# "line channels"
linechans = '6'

# Set spws to be used to form continuum
contspws = '0,1,2,3,4,5,7,8,9,10,11,12,13,14,15'

# Need to flag the line channels prior to averaging.
flagmanager(vis=outputvis, mode='save', versionname='before_line_flagging')

flagdata(vis=outputvis, mode='manual', spw=linechans, flagbackup=False)


# check that flags are as expected, NOTE must check reload on plotms
# gui if its still open.
plotms(vis=outputvis, yaxis='amp', xaxis='channel',
       avgchannel='5', avgtime='1e8', avgscan=True, iteraxis='spw')

# Average the channels within spws
contvis = prefix.replace('J0939', 'J0939_cont.ms')
rmtables(contvis)

default('split')
outputvis=splitms
split(vis=outputvis,
      spw=contspws,
      outputvis=contvis,
      width=[64,64,64,64,64,64,64,64,64,64,64,64,64,64,64],
      datacolumn='data')           # s.t. not affected by uvcontsub

# Inspect continuum for any problems
plotms(vis=contvis, xaxis='uvdist', yaxis='amp', coloraxis='spw')


#=====================================================================
# Create an Averaged Continuum MS by averaging line-free channels
# in low frequency baseband
#
print '-- Create an Averaged Continuum MS of Lower Freq Baseband--'

# Set spws to be used to form continuum
contspwsL = '8~15'

# Average the channels within spws
contvisL = prefix.replace('J0939', 'J0939_contL.ms')
rmtables(contvisL)

default('split')
outputvis = splitms
split(vis=outputvis,
      spw=contspwsL,
      outputvis=contvisL,
      width=[64,64,64,64,64,64,64,64],
      datacolumn='data')

# Inspect continuum for any problems
plotms(vis=contvisL, xaxis='uvdist', yaxis='amp', coloraxis='spw')


#=====================================================================
# Create an Averaged Continuum MS by averaging line-free channels
# in high frequency baseband
#
print '-- Create an Averaged Continuum MS of High Freq Baseband--'

# Set spws to be used to form continuum
contspwsU = '0~5,7'

# Average the channels within spws
contvisU = prefix.replace('J0939', 'J0939_contU.ms')
rmtables(contvisU)

default('split')
outputvis = splitms
split(vis=outputvis,
      spw=contspwsU,
      outputvis=contvisU,
      width=[64,64,64,64,64,64,64],
      datacolumn='data')

# Inspect continuum for any problems
plotms(vis=contvisU, xaxis='uvdist', yaxis='amp', coloraxis='spw')
#
#
#
# restore the previous flagged line channels
flagmanager(vis=outputvis, mode='restore',
            versionname='before_line_flagging')
#
#
#=====================================================================
# Make dirty continuum map of J0939
#

print '-- Clean (make dirty continuum image) --'

contimagename = prefix.replace('J0939', 'J0939_cont')
imname = contimagename + '.dirty'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)

default('clean')

vis = contvis
imagename = imname

mode = 'mfs'
psfmode = 'clark'
imsize = [256]
cell = ['0.75arcsec']
niter = 0
threshold = 0
stokes = 'I'
interactive = False

# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.cont.invert.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')

clean()

dirtyimage = imname + '.image'
viewer(dirtyimage)
# get offline rms
rms = 0.1        # mJy/beam

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

mode = 'mfs'
psfmode = 'clark'
imsize = [256]
cell = ['0.75arcsec']
niter = 10000
threshold = rms
stokes = 'I'
interactive = True
threshold = threshold

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

# A summary of the map will be seen in the logger

#=====================================================================
#
# Get map statistics
#
print '--Imstat --'
default('imstat')

imagename = clnimage

box_on = '110,110,140,140'
box_off = '30,30,218,100'

box = box_off
imgstat = imstat()               # dictionary; imgstat['key'][axis]
rms = (imgstat['rms'][0])
print '>> rms: '+str(rms)

box = box_on
imgstat_on = imstat()
peak = (imgstat_on['max'][0])
print '>> Peak: '+str(peak)

print '>> Dynamic range: '+str(peak/rms)


# ------------ Repeat for basebnad continuum image --------------
#=====================================================================
# Make dirty continuum map of J0939
#

print '-- Clean (make dirty continuum image) --'

contimagename = prefix.replace('J0939', 'J0939_contL')
imname = contimagename + '.dirty'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)

default('clean')

vis = contvisL
imagename = imname

mode = 'mfs'
psfmode = 'clark'
imsize = [256]
cell = ['0.75arcsec']
niter = 0
threshold = 0
stokes = 'I'
interactive = False

# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.contL.invert.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')

clean()

dirtyimage = imname + '.image'
viewer(dirtyimage)
# get offline rms
rms = 0.45        # mJy/beam

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
imagename = imname

mode = 'mfs'
psfmode = 'clark'
imsize = [256]
cell = ['0.75arcsec']
niter = 10000
threshold = rms
stokes = 'I'
interactive = True
threshold = threshold

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
#
# Get map statistics
#
print '--Imstat --'
default('imstat')

imagename = clnimage

box_on = '110,110,140,140'
box_off = '30,30,218,100'

box = box_off
imgstat = imstat()               # dictionary; imgstat['key'][axis]
rms = (imgstat['rms'][0])
print '>> rms: '+str(rms)

box = box_on
imgstat_on = imstat()
peak = (imgstat_on['max'][0])
print '>> Peak: '+str(peak)

print '>> Dynamic range: '+str(peak/rms)

#=====================================================================
# Make dirty continuum map of J0939, high frequency baseband
#

print '-- Clean (make dirty continuum image) --'

contimagename = prefix.replace('J0939', 'J0939_contU')
imname = contimagename + '.dirty'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)

default('clean')

vis = contvisU
imagename = imname

mode = 'mfs'
psfmode = 'clark'
imsize = [256]
cell = ['0.75arcsec']
niter = 0
threshold = 0
stokes = 'I'
interactive = False

# weighting = 'briggs'
# robust = 0.5

saveinputs('clean', prefix + '.contU.invert.saved')

# Pause script if you are running in scriptmode
if scriptmode:
    inp()
    user_check = raw_input('Return to continue script\n')

clean()

dirtyimage = imname + '.image'
viewer(dirtyimage)
# get offline rms
rms = 0.24        # mJy/beam

#=====================================================================
#
# Make and clean continuum map of J0939
#
print '-- Clean (clean) Continuum image --'

contimagename = prefix.replace('J0939', 'J0939_contU')
imname = contimagename + '.clean'
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(imname + ext)

default('clean')

vis = contvisU
imagename = imname

mode = 'mfs'
psfmode = 'clark'
imsize = [256]
cell = ['0.75arcsec']
niter = 10000
threshold = rms
stokes = 'I'
interactive = True
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

#=====================================================================
#
# Get map statistics
#
print '--Imstat --'
default('imstat')

imagename = clnimage

box_on = '110,110,140,140'
box_off = '30,30,218,100'

box = box_off
imgstat = imstat()               # dictionary; imgstat['key'][axis]
rms = (imgstat['rms'][0])
print '>> rms: '+str(rms)

box = box_on
imgstat_on = imstat()
peak = (imgstat_on['max'][0])
print '>> Peak: '+str(peak)

print '>> Dynamic range: '+str(peak/rms)
