# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:00:24 2015

@author: qwe14789cn
"""
import os
import numpy as np
from netCDF4 import Dataset
import funlib

def fun(data_dir,input_data,output_data):
    os.chdir(data_dir+input_data)
    print 'reading data...',
    wrfout=Dataset('wrfout_d02_2015-06-17_150000.nc')
    #wrfout=Dataset('wrfout_d02_2014-06-05_100000_669.nc')
    

    #-----------------------------
    QRAIN=wrfout.variables['QRAIN']
    QRAIN=QRAIN[0,:,:,:]

    QNRAIN=wrfout.variables['QNRAIN']
    QNRAIN=QNRAIN[0,:,:,:]

    QRAIN=funlib.cgsp(QRAIN)
    QNRAIN=funlib.cgsp(QNRAIN)
    #-----------------------------
    QHAIL=wrfout.variables['QHAIL']
    QHAIL=QHAIL[0,:,:,:]

    QNHAIL=wrfout.variables['QNHAIL']
    QNHAIL=QNHAIL[0,:,:,:]

    QHAIL=funlib.cgsp(QHAIL)
    QNHAIL=funlib.cgsp(QNHAIL)
    #-----------------------------
    QSNOW=wrfout.variables['QSNOW']
    QSNOW=QSNOW[0,:,:,:]

    QNSNOW=wrfout.variables['QNSNOW']
    QNSNOW=QNSNOW[0,:,:,:]

    QSNOW=funlib.cgsp(QSNOW)
    QNSNOW=funlib.cgsp(QNSNOW)
    #-----------------------------
    QICE=wrfout.variables['QICE']
    QICE=QICE[0,:,:,:]

    QNICE=wrfout.variables['QNICE']
    QNICE=QNICE[0,:,:,:]

    QICE=funlib.cgsp(QICE)
    QNICE=funlib.cgsp(QNICE)
    #-----------------------------
    QGRAUP=wrfout.variables['QGRAUP']
    QGRAUP=QGRAUP[0,:,:,:]

    QNGRAUPEL=wrfout.variables['QNGRAUPEL']
    QNGRAUPEL=QNGRAUPEL[0,:,:,:]

    QGRAUP=funlib.cgsp(QGRAUP)
    QNGRAUPEL=funlib.cgsp(QNGRAUPEL)
    #-----------------------------
    QCLOUD=wrfout.variables['QCLOUD']
    QCLOUD=QCLOUD[0,:,:,:]

    QNCLOUD=wrfout.variables['QNCLOUD']
    QNCLOUD=QNCLOUD[0,:,:,:]

    QCLOUD=funlib.cgsp(QCLOUD)
    QNCLOUD=funlib.cgsp(QNCLOUD)
    #-----------------------------
    REFL_10CM=wrfout.variables['REFL_10CM']
    REFL_10CM=REFL_10CM[0,:,:,:]
    REFL_10CM=funlib.cgsp(REFL_10CM)
    #-----------------------------
    RHO=wrfout.variables['RHO']
    RHO=RHO[0,:,:,:]
    RHO=funlib.cgsp(RHO)
    #-----------------------------
    P=wrfout.variables['P']
    P=P[0,:,:,:]
    P=funlib.cgsp(P)
    #-----------------------------
    PB=wrfout.variables['PB']
    PB=PB[0,:,:,:]
    PB=funlib.cgsp(PB)
    #-----------------------------
    T=wrfout.variables['T']
    T=T[0,:,:,:]
    T=funlib.cgsp(T)
    #-----------------------------
    TK=T+300
    Pa=P+PB
    #-----------------------------
    Tem=1.0*TK*(Pa/100000)**(2/7)
    print 'finished'
    print 'saving data...',
    np.save('QRAIN.npy',QRAIN)
    np.save('QNRAIN.npy',QNRAIN)

    np.save('QHAIL.npy',QHAIL)
    np.save('QNHAIL.npy',QNHAIL)

    np.save('QSNOW.npy',QSNOW)
    np.save('QNSNOW.npy',QNSNOW)

    np.save('QICE.npy',QICE)
    np.save('QNICE.npy',QNICE)

    np.save('QGRAUP.npy',QGRAUP)
    np.save('QNGRAUPEL.npy',QNGRAUPEL)

    np.save('QCLOUD.npy',QCLOUD)
    np.save('QNCLOUD.npy',QNCLOUD)

    np.save('RHO.npy',RHO)
    np.save('REFL_10CM',REFL_10CM)
    np.save('Pa.npy',Pa)
    np.save('Tem.npy',Tem)
    
    print 'finished'    
    return


