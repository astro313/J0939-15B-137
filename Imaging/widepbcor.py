##############################################################################
# Last Modified: 24 Dec 2015                                                 #
#                                                                            #
#                                                                            #
# Apply wideband PB correction Script for SMM J0939+8315                     #
#                                                                            #
# Features Tested:                                                           #
#    The script illustrates end-to-end processing with CASA                  #
#    as depicted in the following flow-chart.                                #
#                                                                            #
#    Filenames will have the <prefix> = 'J0939'                              #
#                                                                            #
#      Input Data                Process          Output Data                #
#                                                                            #
#                                                                            #
# <prefix>.*clean.image.tt0 --> impbcor  -->  <prefix>.*clean.wbpbcor.tt0 +  #
#                                 |          <prefix>.*clean.flux            #
#                                 |                                          #
#                                 v                                          #
##############################################################################
'''
Apply wideband PB correction to all cleaned maps in the directory

'''
#====================================================================
# Apply a primary beam correction
#
import glob

path = '/data/dleung/DATA/VLA/15B-137/Imaging/nterms2/'
myimages = glob.glob(path+"*clean.image.tt0")

rmtables('*.wbpbcor')
for image in myimages:
    impbcor(imagename=image, pbimage=image.replace(
        '.image.tt0', '.flux'), outfile=image.replace('.image.tt0', '.wbpbcor.tt0'))
