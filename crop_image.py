# This is the script to run for making a warping/astrometric solution to LMIRCam, using data taken
# in Nov and Dev 2016

# parent find_dewarp_soln.py created by E.S., Nov 2016
# child apply_dewarp_soln.py made by E.S., Feb 2017
# child crop_image.py made by E.S., Jan 2018

import numpy as np
from astrom_lmircam_soln import *
from astrom_lmircam_soln import polywarp
from astrom_lmircam_soln import dewarp
from astropy.io import fits
import matplotlib.pyplot as plt
import os
import time
from multiprocessing import Pool

#####################################################################
# set file paths

dirTreeStem = ('../../../vol_c/raw_leech/ByName/')

retrievalPiece = ('delCyg_raw_data/171003/Lp/SX/sat/')
depositPiece = ('delCyg_non_dewarped_1024x1024/171003/Lp/SX/sat/')
fileNameStem = ('lm_171003_')


#####################################################################
# CROP 

def crop_frame_multiproc(frameNum, extra_dim=True):

    start_time = time.time()
	
    print('Cropping frame '+str(frameNum)+'...')

    # grab the pre-dewarp image and header
    image, header = fits.getdata(dirTreeStem+
                                 retrievalPiece+
                                 fileNameStem+
                                 str("{:0>5d}".format(frameNum))+
                                 '.fits',
                                 0,
                                 header=True)

    print('Read in pixel element type: '+str(type(image[0][0])))

    # crop the image
    cropped = image[666:1690,816:1840] # 171002 data: [540:1564,500:1524]; 171003 data: [666:1690,816:1840]

    # write out
    cropped = np.squeeze(cropped) # remove dimensions of size 1
    if extra_dim: # the LEECH pipeline still requires a singleton dimension
        cropped = cropped[None,:,:]

    print('Write out pixel element type: '+str(type(cropped[0][0])))
    print('Write out size: '+str(np.shape(cropped)))
    hdu = fits.PrimaryHDU(cropped, header=header)
    hdulist = fits.HDUList([hdu])
    hdulist.writeto(dirTreeStem+depositPiece+fileNameStem+str("{:0>5d}".format(frameNum))+'.fits',
                    overwrite=True)
        
    elapsed_time = time.time() - start_time
    print(elapsed_time)

#####################################################################

# test
#noReturn = dewarp_frame_multiproc(0)

pool = Pool(16)
channel_eq = pool.map(crop_frame_multiproc,range(366,666))
