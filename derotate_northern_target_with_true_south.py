
# coding: utf-8

# In[ ]:

# This derotates 2048x2048 images of a northern target so that the image up is pointing southwards along the meridian

# created by E.S. 2018 Jan 15


# In[18]:

import numpy as np
from astropy.io import fits
from astrom_lmircam_soln import *
from pytictoc import TicToc
from multiprocessing import Pool
import os

# In[2]:

# set file paths and datasets

dirTreeStem = ('/../../vol_c/3200phaethon/')
retrievalPiece = ('NFF_BPA_06_dewarped/')
depositPiece = ('NFF_BPA_07_derotated/')
fileNameStem = ('lm_171215_')


# In[3]:

# additional correction to PA

pa_corrxn = 0.53 # in deg


# In[14]:

def derotate_image_northern_target(fileNum,ignoreExisting=True):
# this takes single images (intended for multiprocessing)
    print('----------------------------------------')

    t = TicToc() # create instance of timer
    t.tic() # start timer

    if ignoreExisting: # if the file already exists, skip it
        if os.path.exists(dirTreeStem+
                                 depositPiece+
                                 fileNameStem+
                                 str("{:0>5d}".format(fileNum))+
                                 '.fits'):
            	print('Not derotating frame '+str(fileNum)+'!')
		return

        else:

		if os.path.exists(dirTreeStem+
                                 retrievalPiece+
                                 fileNameStem+
                                 str("{:0>5d}".format(fileNum))+
                                 '.fits'):

    			print('Derotating image '+str("{:0>5d}".format(fileNum))+'...')
			# retrieve image
    			image, header = fits.getdata(dirTreeStem+
                                         retrievalPiece+
                                 fileNameStem+
                                 str("{:0>5d}".format(fileNum))+
                                 '.fits',
                                 0,
                                 header=True)
    			# find PA from header
    			pa = header['LBT_PARA']
    
    			# derotate
    			image_derot = rot(image, 180.-pa-pa_corrxn, [1024,1024], order=3, pivot=False) # axis coord here is just a dummy
    
    			# save 
    			hdu = fits.PrimaryHDU(image_derot, header=header)
    			hdulist = fits.HDUList([hdu])
    			hdulist.writeto(dirTreeStem+depositPiece+fileNameStem+str("{:0>5d}".format(fileNum))+'.fits',overwrite=True)

    			t.toc()
    		print('------------------------------')


# In[19]:

# set up multiprocess

# test
#derotate_image_northern_target(57)

pool = Pool(16)
derotate_imgs = pool.map(derotate_image_northern_target,range(51,510))


# In[ ]:



