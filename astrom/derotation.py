import numpy as np
from astropy.io import fits
from astrom_lmircam_soln import *
from pytictoc import TicToc

def derotate_image_forloop(startNum,stopNum,dateString):
    for f in range(startNum,stopNum+1): # loop over filenames
        print('----------------------------------------')
        print('Derotating image '+str("{:0>5d}".format(f))+'...')

        t = TicToc() # create instance of timer
        t.tic() # start timer

        # retrieve image
        image, header = fits.getdata(calibrated_trapezium_data_stem+
                                     'step02_dewarped/'+
                                     'lm_'+dateString+'_'+
                                     str("{:0>5d}".format(f))+
                                     '.fits',
                                     0,
                                     header=True)
        # find PA from header
        pa = header['LBT_PARA']
    
        # derotate
        image_derot = rot(image, -pa, [1024,1024], order=3, pivot=False) # axis coord here is just a dummy
    
        # save 
        fits.writeto(calibrated_trapezium_data_stem+
                     'step03_derotate/'+
                     'lm_'+dateString+'_'+
                     str("{:0>5d}".format(f))+
                     '.fits',
                     image_derot, header, overwrite=False)

        t.toc()
        print('------------------------------')
