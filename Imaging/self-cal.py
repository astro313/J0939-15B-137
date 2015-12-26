'''
Last modified: 24 Dec 2015


Todo
----
Test script
- check whether there's a MODEL column after clean with usescratch=True (plotms())
- check also visibilities (data column) in J0939.src.split.ms, esp. the phase do they look calibrated or do they look random. Currently, the continuum phase data looks like they span all ranges at all times.. Is it just that I need some time averaging?? or spw averaging to see one dot at a time?


Note
----
- different image size and cell size than intial imaging


'''

import os

scriptmode = False

# The prefix to use for all output files
prefix = '/data/dleung/DATA/VLA/15B-137/Imaging/self-cal/J0939'
data = prefix + '.src.split.ms'

# imaging_cont.py (usescratch=False; to save disk I/O and disk space)
# after running this script (usescratch=True), model will be placed in
# "MODEL" col.
contvis = prefix.replace('J0939', 'J0939_cont.ms')

# Differ slightly from first_image, in that it use usescratch=True
first_image = prefix.replace('J0939', 'J0939_cont_pre-selcal')
selfcal_image = prefix.replace('J0939', 'J0939_cont_selfcal')


##############################################
#
# Self-calibration on the continuum
print('--- Make a cleaned cont. map ---')
default('clean')

# usescratch=T place CC in the "model" column. This will allow "gaincal" to compare
# DATA with MODEL
#
# Also decided to make image with imsize=240, cell=0.5 arcsec
usescratch = True
vis = contvis
imagename = first_image
mode = 'mfs'
psfmode = 'clark'
nterms = 1
imsize = [240]
cell = '0.5arcsec'
stokes = 'I'
niter = 10000
threshold = '0.5mJy'
interactive = True
imagermode = 'csclean'

os.system('rm -rf ' + first_image + '.*')
inp
saveinputs(clean, first_image+'.clean.saved')
clean()

# ============================================================
#
# If we decided to use the clean image from imaging_cont.py
# where it was generated with usescratch=False
# instead of running clean() again as above,
# we need to generate the model visibiilities --> MODEL col.
#
# Check with browsetable to see if this is necessary
# browsetable(tablename=contvis)
#

vis = contvis
mymodel = first_image + '.model'
model = mymodel
usescratch = T            # write model visibilities into the model column
nterms = 1
reffreq = ""

saveinputs(ft, contvis + 'ft.saved')
inp(ft)
go

# determine solint
default(plotms)
xaxis = 'time'
yaxis = 'phase'
vis = contvis

inp
go
# Model column missing....

# gaincal() to solve for the antenna-based phase or amplitude terms
# needed to correct the data to match the model.
vis = contvis

solint = '60s'
caltable_p = 'selfcal_J0939' + solint + '.gp'
caltable = caltable_p

refant = 'ea02'
calmode = 'p'
spw = ''
field = ''
combine = 'scan'
minsnr = 3.0
minblperant = 4

inp
saveinputs(gaincal, caltable_p + '.gaincal.saved')
gaincal()
# Watch out for failed solutions noted in the terminal during this
# solution. If you see  more than 1 or 2 of your antennas failing
# to converge in many time intervals then you
# may need to lengthen the solution interval.


# Check the solution
# plot by SPW with individual antennas mapped to colors. Look at
# the overall magnitude of the correction to get an idea of how
# important the selfcal is and at how quickly it changes with time to
# get an idea of how stable the instrument and atmosphere were.
#


# for strong line self-cal
plotcal(caltable=caltable,
        xaxis='time', yaxis='phase',
        plotrange=[0, 0, -180, 180],
        iteration='spw', subplot=231)


# for strong line or continuum self-cal
plotcal(caltable=caltable,
        xaxis='time', yaxis='phase',
        timerange='',
        iteration='antenna',
        subplot=421,
        plotrange=[0, 0, -180, 180])

# if The rms phase noise is about BLAH deg, --> self-cal will improve image


flagmanager(vis=contvis,
            mode='save',
            versionname='before_selfcal_apply')

# apply the calibration to the data for next round of imaging
# write in CORRECTED col.
applycal(vis=contvis,
         gaintable=caltable,
         interp='linear',
         calwt=F,
         flagbackup=False
         )

# Use this command to roll back to the previous flags in the event of
# an unfortunate applycal.

# flagmanager(vis=avg_data,
#            mode='restore',
#            versionname='before_selfcal_apply')


# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# RE-IMAGE THE SELF-CALIBRATED DATA
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
tget(clean)
os.system('rm -rf' + selfcal_image + '*') BLAH

usescratch = True             # write model vis. to MODEL
imagename = selfcal_image
interactive = True
spw = ''
nterms = 1
threshold = '0.1mJy'

inp

clean()

# Immediately you will notice how much cleaner this image is.
# note the rms, flux of source

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# INSPECT THE NEW IMAGE
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
#
# Inspect the output image, noting the noise. Compare it to the
# previous, not self-calibrated image.
viewer(selfcal_image + '.image')


imview(raster={'file': first_image + '.image',
               'range': [-0.001, 0.01],
               'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': first_image + '.image',
                'levels': [-1, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16],
                'unit': 0.0005}, zoom=3)

imview(raster={'file': selfcal_image + '.image',
               'range': [-0.001, 0.01],
               'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': selfcal_image + '.image',
                'levels': [-1, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16],
                'unit': 0.0005}, zoom=3)

##################################################
#
# shorter solution int. with the better model
#


caltable_p2 = 'selfcal_J0939' + solint + '.gp'
rmtables(caltable_p2)

vis = contvis
caltable = caltable_p2
combine = 'spw'
solint = '30s'

inp(gaincal)

saveinputs(gaincal, caltable_p2+'.gaincal.saved')
gaincal()


# Check the solution
plotcal(caltable='pcal2',
        xaxis='time',
        yaxis='phase',
        timerange='',
        iteration='antenna',
        subplot=421,
        plotrange=[0, 0, -180, 180])

# apply the calibration to the data for next round of imaging
applycal(vis=contvis,
         spwmap=spwmap,
         field=field,
         gaintable=['pcal2'],
         gainfield='',
         calwt=F,
         flagbackup=F)

# clean deeper
for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(contimagename + '_p2' + ext)

clean(vis=contvis,
      imagename=contimagename + '_p2',
      stokes='I'
      mode='mfs',
      imsize=imsize,
      cell=cell,
      weighting=weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)


# If not major improvement, inspect residual visibilities
# residual visibilities = corrected - model
default(plotms)
vis = contvis
correlation = 'RR,LL'
inp

plotms

# flagdata()

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# (OPTIONAL) ATTEMPT AN AMPLITUDE SELFCAL
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%


refant = 'ea02'
# solint_ap = '10000s'
solint_ap = 'inf'
caltable_ap = 'selfcal_J0939.ap_gcal'

os.system('rm -rf selfcal_J0939.ap_gcal')

vis = contvis
caltable = caltable_ap
combine = 'scan'
# calmode='a'
calmode = 'ap'
gaintable = BLAH         # determine which one to use caltable_p2?
refant = refant
solint = 'solint_ap'
minsnr = 3.0
minblperant = 4

# for extended array
# uvrange='>50m', # may need to use to exclude extended emission

inp
saveinputs(gaincal, caltable_ap+'.gaincal.saved')
gaincal()


plotcal(caltable=caltable_ap,
        xaxis='time',
        yaxis='amp',
        iteration='antenna',
        subplot=421,
        plotrange=[0, 0, 0.2, 1.8])

# The corrections are near 1.0, as expected. There is 5 to 10% scatter
# among the individual solutions, so it is possible that this
# amplitude selfcal will add more noise than it
# removes. Self-calibration followed by evaluation and a decision
# "whether it helps" is a standard work flow.


# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# APPLY **BOTH** SELF CALIBRATIONS
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

flagmanager(vis=contvis,
            mode='save',
            versionname='before_selfcal_amp_apply')

applycal(vis=contvis,
         # select which spws to apply the solutions for each table
         # spwmap=[spwmap, spwmap],
         gaintable=[caltable_?, caltable_ap],
         gainfield='',
         calwt=F,
         flagbackup=F)

# To roll back to that previous flag version you would use:
# flagmanager(vis=contvis,
#            mode='restore',
#            versionname='before_selfcal_amp_apply')

# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# CLEAN THE NEWLY CORRELATED DATA
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
#
# Now image the doubly self-calibrated data with CLEAN.
#
selfcal_ap_image = 'J0939_SELFCAL_AP'
default('clean')

usescratch = True
vis = contvis
imagename = selfcal_ap_image
mode = 'mfs'
imsize = 256
# cell = ['0.75arcsec']
cell = ['0.5arcsec']
niter = 10000
threshold = '0mJy'         # interactively, stop based on residual
interactive = True
stokes='I'
imagermode = 'csclean'

inp
# wipe the previous version of these images
os.system('rm -rf J0939_SELFCAL_AP*')

saveinputs(clean, selfcal_ap_image+'.clean.saved')
go
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%
# INSPECT THE RESULTS
# =%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%=%

imview(raster={'file': selfcal_image + '.image',
               'range': [-0.0005, 0.01],
               'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': selfcal_image + '.image',
                'levels': [-1, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16],
                'unit': 0.0003}, zoom=3)

imview(raster={'file': selfcal_amp_image + '.image',
               'range': [-0.0005, 0.01],
               'colormap': 'RGB 1', 'scaling': 0.0, 'colorwedge': True},
       contour={'file': selfcal_amp_image + '.image',
                'levels': [-1, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16],
                'unit': 0.0003}, zoom=3)

# Evaluating whether these fain components that emerge after self-cal are real
# compare peak in before self-cal image, only phase self-cal, and amp+phase self-cal image.
#
# Note final RMS and number of clean iterations. Compare the RMS to
# the RMS from the earlier, pre-selfcal image.
# check dynamic range

# Save results of self-cal in a new ms
split(vis=contvis,
      outputvis=contvis + '.selfcal',
      datacolumn='corrected')
#########################################################
# Apply continuum self-calibration to line data [OPTIONAL]

# Mapping self-calibration solution to the individual line spectral windows.
spwmap_line = [0]
applycal(vis=linevis,
         # select which spws to apply the solutions for each table
         spwmap=[spwmap_line, spwmap_line],
         field=field,
         gaintable=['pcal3', 'apcal'],
         gainfield='',
         calwt=F,
         flagbackup=F)

# Save results of self-cal in a new ms and reset the image name.
split(vis=linevis,
      outputvis=linevis + '.selfcal',
      datacolumn='corrected')
linevis = linevis + '.selfcal'

# reset the corrected data column in the  ms to the original calibration
#>>> This can also be used to return your ms to it's original
#>>> pre-self-cal state if you are unhappy with your self-calibration.
clearcal(linevis)

#>>> The applycal task will automatically flag data without good
#>>> gaincal solutions. If you are unhappy with your self-cal and wish to
#>>> return the flags to their original state, run the following command
#>>> flagmanager(vis=linevis, mode='restore',versionname='before_selfcal')

linevis = linevis + '.selfcal'

##############################################
# Image line emission [REPEAT AS NECESSARY]

#>>> If you did an mstransform/cvel, use the same velocity parameters in
#>>> the clean that you did for the regridding. If you did not do an
#>>> mstransform and have multiple executions of a scheduling block,
#>>> select the spws with the same rest frequency using the spw parameter
#>>> (currently commented out below). DO NOT INCLUDE SPWS WITH DIFFERENT
#>>> REST FREQUENCIES IN THE SAME RUN OF CLEAN: THEY WILL SLOW DOWN
#>>> IMAGING CONSIDERABLY.

finalvis = 'calibrated_final.ms'
# linevis = finalvis # uncomment if you neither continuum subtracted nor self-calibrated your data.
# linevis = finalvis + '.contsub' # uncomment if continuum subtracted
# linevis = finalvis + '.contsub.selfcal' # uncommment if both continuum subtracted and self-calibrated
# linevis = finalvis + '.selfcal' # uncomment if just self-calibrated (no
# continuum subtraction)

sourcename = 'n253'  # name of source
linename = 'CO10'  # name of transition (see science goals in OT for name)
lineimagename = sourcename + '_' + linename  # name of line image

restfreq = '115.27120GHz'  # Typically the rest frequency of the line of
# interest. If the source has a significant
# redshift (z>0.2), use the observed sky
# frequency (nu_rest/(1+z)) instead of the
# rest frequency of the
# line.

# spw='1' # uncomment and replace with appropriate spw if necessary.

start = '-100km/s'  # start velocity. See science goals for appropriate value.
width = '2km/s'  # velocity width. See science goals.
nchan = 100  # number of channels. See science goals for appropriate value.

#>>> To specify a spws from multiple executions that had not been regridded using cvel, use
#>>>       import numpy as np
#>>>       spw = str.join(',',map(str,np.arange(0,n,nspw)))
#>>>
#>>> where n is the total number of windows x executions and nspw is the
#>>> number of spectral windows per execution. Note that the spectral
#>>> windows need to have the same order in all data sets for this code
#>>> to work. Add a constant offset (i.e., +1,+2,+3) to the array
#>>> generated by np.arange to get the other sets of windows.

# If necessary, run the following commands to get rid of older clean
# data.

# clearcal(vis=linevis)
# delmod(vis=linevis)

for ext in ['.flux', '.image', '.mask', '.model', '.pbcor', '.psf', '.residual', '.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      #      spw=spw,
      stokes='I'
      mode='velocity',
      start=start,
      width=width,
      nchan=nchan,
      outframe=outframe,
      veltype=veltype,
      restfreq=restfreq,
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode)


##############################################
# Apply a primary beam correction

import glob

myimages = glob.glob("*.image")

rmtables('*.pbcor')
for image in myimages:
    pbimage = image.rsplit('.', 1)[0] + '.flux'
    outfile = image.rsplit('.', 1)[0] + '.pbcor'
    impbcor(imagename=image, pbimage=pbimage, outfile=outfile)

##############################################
# Export the images

import glob

myimages = glob.glob("*.pbcor")
for image in myimages:
    exportfits(imagename=image, fitsimage=image + '.fits', overwrite=True)

myimages = glob.glob("*.flux")
for image in myimages:
    exportfits(imagename=image, fitsimage=image + '.fits', overwrite=True)

##############################################
# Create Diagnostic PNGs

#>>> The following code has not be extensively tested. Please let
#>>> Amanda Kepley know if you find problems.

os.system("rm -rf *.png")
mycontimages = glob.glob("calibrated*.image")
for cimage in mycontimages:
    max = imstat(image)['max'][0]
    min = -0.1 * max
    outimage = cimage + '.png'
    os.system('rm -rf ' + outimage)
    imview(raster={'file': cimage, 'range': [min, max]}, out=outimage)


# this will have to be run for each sourcename
mylineimages = glob.glob(sourcename + "*.image")
for limage in mylineimages:
    rms = imstat(limage, chans='1')['rms'][0]
    mom8 = limage + '.mom8'
    os.system("rm -rf " + mom8)
    immoments(limage, moments=[8], includepix=[2 * rms, 1e6], outfile=mom8)
    max = imstat(mom8)['max'][0]
    min = -0.1 * max
    os.system("rm " + mom8 + ".png")
    imview(raster={'file': mom8, 'range': [min, max]}, out=mom8 + '.png')
