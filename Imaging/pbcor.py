##############################################################################
# Last Modified: 17 Dec 2015                                                 #
#                                                                            #
#                                                                            #
# Apply PB correction Script for SMM J0939+8315                              #
#                                                                            #
# Features Tested:                                                           #
#    The script illustrates end-to-end processing with CASA                  #
#    as depicted in the following flow-chart.                                #
#                                                                            #
#    Filenames will have the <prefix> = 'J0939'                              #
#                                                                            #
#      Input Data           Process          Output Data                     #
#                                                                            #
#                                                                            #
#                            clean   -->  <prefix>.*clean.image +            #
#                              |          <prefix>.*clean.model +            #
#                              |          <prefix>.*clean.residual           #
#                              v                                             #
#                           impbcor  -->  <prefix>.*clean.pbcor +            #
#                              |          <prefix>.*clean.flux               #
#                              |                                             #
#                              v                                             #
##############################################################################
'''
Apply PB correction to all cleaned maps in the directory

'''
#====================================================================
# Apply a primary beam correction
#
import glob

path = '/data/dleung/DATA/VLA/15B-137/Imaging/'
myimages = glob.glob(path+"*clean.image")

rmtables('*.pbcor')
for image in myimages:
    impbcor(imagename=image, pbimage=image.replace(
        '.image', '.flux'), outfile=image.replace('.image', '.pbcor'))
