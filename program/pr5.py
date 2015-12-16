# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:50:45 2015

@author: qwe14789cn
"""
import os
import numpy as np

def fun(main_dir,input_data,output_data):
    os.chdir(main_dir+input_data)
    print 'loading data...',

    QRAIN    =np.load('QRAIN.npy')
    QNRAIN   =np.load('QNRAIN.npy')

    QHAIL    =np.load('QHAIL.npy')
    QNHAIL   =np.load('QNHAIL.npy')

    QSNOW    =np.load('QSNOW.npy')
    QNSNOW   =np.load('QNSNOW.npy')

    RHO      =np.load('RHO.npy')

    REFL_10CM=np.load('REFL_10CM.npy')
    Pa       =np.load('Pa.npy')
    Tem      =np.load('Tem.npy')    
    
    os.chdir(main_dir+output_data)
    rain_zi      =   np.load('rain_zi.npy')
    rain_kdp     =   np.load('rain_kdp.npy')
    rain_ldr     =   np.load('rain_ldr.npy')
    rain_rhv     =   np.load('rain_rhv.npy')
    rain_ai      =   np.load('rain_ai.npy')
    rain_zdr     =   np.load('rain_zdr.npy')
    print 'finished'
    print ' '
    from scipy.io import savemat
    
    print 'transing data...',
    savemat('output.mat',{'QRAIN':QRAIN,'QNRAIN':QNRAIN,'QHAIL':QHAIL,'QNHAIL':QNHAIL, \
                          'QSNOW':QSNOW,'QNSNOW':QNSNOW,'RHO':RHO,'REFL_10CM':REFL_10CM,'Pa':Pa,'Tem':Tem, \
                          'rain_zi':rain_zi,'rain_kdp':rain_kdp,'rain_ldr':rain_ldr,'rain_rhv':rain_rhv, \
                          'rain_ai':rain_ai,'rain_zdr':rain_zdr})
    print 'finished'
    return