
# coding: utf-8

# In[ ]:

# This equalizes channels from the 3200 Phaethon data

# created 2018 Jan 14 by E.S.


# In[1]:

import numpy as np
from astropy.io import fits
import time
from multiprocessing import Pool


# In[2]:

# set file paths and datasets

dirTreeStem = ('../../vol_c/3200phaethon/')
retrievalPiece = ('NFF_BPG_04_second_fixpix/')
depositPiece = ('NFF_BPG_05_channel_eqze/')
fileNameStem = ('lm_171215_')


# In[3]:

def channel_equalize(startNum,stopNum,xSize=2048,ySize=2048,N=1):

    N = N # use every N frames
    xSize = xSize
    ySize = ySize
    sliceNum = 0 # initialize cube slice number

    for f in range(startNum,stopNum+1): # loop over filenames
        
        start_time = time.time()
        
        if (f%N == 0): 
            print('----------------------------------------')
            print('Processing frame '+str(f))
            image, header = fits.getdata(dirTreeStem+
                                         retrievalPiece+
                                 fileNameStem+
                                 str("{:0>5d}".format(f))+
                                 '.fits',
                                 0,
                                 header=True)
            
            # initialize
            image_equalized = np.copy(image)
            
            for channelNum in range(0,32):
                normznConst = np.median(image[1300:1500,64*channelNum+16:64*channelNum+16+32])
                image_equalized[:,64*channelNum:64*(channelNum+1)] = np.subtract(image[:,64*channelNum:64*(channelNum+1)],normznConst)
                image[1300:1500,64*channelNum+16:64*channelNum+16+32] = np.zeros(np.shape(image[1300:1500,64*channelNum+16:64*channelNum+16+32]))
                ##image[:,64*channelNum:64*(channelNum+1)-1] = 0
            
    
         # save median
        hdu = fits.PrimaryHDU(image_equalized, header=header)
        hdulist = fits.HDUList([hdu])
        hdulist.writeto(dirTreeStem+depositPiece+fileNameStem+str("{:0>5d}".format(f))+'.fits',
                    overwrite=True)
        
        elapsed_time = time.time() - start_time
        print(elapsed_time)


# In[4]:

def channel_equalize_multiproc(fileNum,xSize=2048,ySize=2048,N=1):
# function for multiprocessing just accepts a single frame before mapping

    N = N # use every N frames
    xSize = xSize
    ySize = ySize
    sliceNum = 0 # initialize cube slice number
        
    start_time = time.time()
        
    print('----------------------------------------')
    print('Processing frame '+str(fileNum))
    image, header = fits.getdata(dirTreeStem+
                                         retrievalPiece+
                                 fileNameStem+
                                 str("{:0>5d}".format(fileNum))+
                                 '.fits',
                                 0,
                                 header=True)
            
    # initialize
    image_equalized = np.copy(image)
            
    for channelNum in range(0,32):
        normznConst = np.median(image[1300:1500,64*channelNum+16:64*channelNum+16+32])
        image_equalized[:,64*channelNum:64*(channelNum+1)] = np.subtract(image[:,64*channelNum:64*(channelNum+1)],normznConst)
        image[1300:1500,64*channelNum+16:64*channelNum+16+32] = np.zeros(np.shape(image[1300:1500,64*channelNum+16:64*channelNum+16+32]))            
    
    # save 
    hdu = fits.PrimaryHDU(image_equalized, header=header)
    hdulist = fits.HDUList([hdu])
    hdulist.writeto(dirTreeStem+depositPiece+fileNameStem+str("{:0>5d}".format(fileNum))+'.fits',
                    overwrite=True)
        
    elapsed_time = time.time() - start_time
    print(elapsed_time)


# In[ ]:

# set up multiprocess

pool = Pool(16)
channel_eq = pool.map(channel_equalize_multiproc,range(51,1051))


# In[ ]:



