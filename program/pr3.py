# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:00:24 2015

@author: qwe14789cn
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import funlib
import math
from pylab import *
from matplotlib import cm

def fun(data_dir,input_data,output_data):
    os.chdir(data_dir+output_data)

    print('loading data...',)
    c_ai         =   np.load('c_ai.npy')
    c_kdp        =   np.load('c_kdp.npy')
    c_ldr        =   np.load('c_ldr.npy')
    c_zh         =   np.load('c_zh.npy')
    c_rhv        =   np.load('c_rhv.npy')
    c_zdr        =   np.load('c_zdr.npy')
    c_zv         =   np.load('c_zv.npy')

    g_ai         =   np.load('g_ai.npy')
    g_kdp        =   np.load('g_kdp.npy')
    g_ldr        =   np.load('g_ldr.npy')
    g_zh         =   np.load('g_zh.npy')
    g_rhv        =   np.load('g_rhv.npy')
    g_zdr        =   np.load('g_zdr.npy')
    g_zv         =   np.load('g_zv.npy')

    g_zh         =   g_zh * 0.93/0.2
    g_zv         =   g_zv * 0.93/0.2

    i_ai         =   np.load('i_ai.npy')
    i_kdp        =   np.load('i_kdp.npy')
    i_ldr        =   np.load('i_ldr.npy')
    i_zh         =   np.load('i_zh.npy')
    i_rhv        =   np.load('i_rhv.npy')
    i_zdr        =   np.load('i_zdr.npy')
    i_zv         =   np.load('i_zv.npy')

    i_zh         =   i_zh * 0.93/0.2
    i_zv         =   i_zv * 0.93/0.2

    r_ai         =   np.load('r_ai.npy')
    r_kdp        =   np.load('r_kdp.npy')
    r_ldr        =   np.load('r_ldr.npy')
    r_zh         =   np.load('r_zh.npy')
    r_rhv        =   np.load('r_rhv.npy')
    r_zdr        =   np.load('r_zdr.npy')
    r_zv         =   np.load('r_zv.npy')

    h_ai         =   np.load('h_ai.npy')
    h_kdp        =   np.load('h_kdp.npy')
    h_ldr        =   np.load('h_ldr.npy')
    h_zh         =   np.load('h_zh.npy')
    h_rhv        =   np.load('h_rhv.npy')
    h_zdr        =   np.load('h_zdr.npy')
    h_zv         =   np.load('h_zv.npy')

    h_zh         =   h_zh * 0.93/0.2
    h_zv         =   h_zv * 0.93/0.2

#------------------------------------------
    s_ai         =   np.load('s_ai.npy')
    s_kdp        =   np.load('s_kdp.npy')
    s_ldr        =   np.load('s_ldr.npy')
    s_zh         =   np.load('s_zh.npy')
    s_rhv        =   np.load('s_rhv.npy')
    s_zdr        =   np.load('s_zdr.npy')
    s_zv         =   np.load('s_zv.npy')

    s_zh         =   s_zh * 0.93/0.2
    s_zv         =   s_zv * 0.93/0.2

    size_x,size_y,size_z=r_zv.shape

    print('finished')
    print('data shape -> %d %d %d',size_x,size_y,size_z)


    #------------------------------------------
    #   plot set
    #------------------------------------------
    fig_size=(8,6)
    X_set = 270000
    set_dpi=150
    
    #-----------------------------------------
    #   set_gamma_u is the file name u.
    #------------------------------------------
    set_gamma_u=2
    #------------------------------------------
    #   create scanning data shape
    #------------------------------------------
    # Y  + plane up    - plane down
    # X  + plane right - plane left
    #------------------------------------------

    #------------------------------------------------------------------
    #   zh plot
    #------------------------------------------------------------------


    X,Y,Z,sc_zh=funlib.scanning(r_zh,0,off_X=X_set,off_Y=0,off_Z=3000)

    #-------------------------------------------------------------------
    #   set the plot axis x and y
    #   shift the plane x and y
    #-------------------------------------------------------------------
    X = X/1000
    Y = Y/1000
    X = X-X_set/1000


    sc_zh = funlib.lg_refl2(sc_zh)



    fig = plt.figure(figsize=fig_size,dpi=set_dpi)
    fig.patch.set_facecolor('white')

    plt.contourf(X,Y,sc_zh,levels=
    [-75, -70, -65, -60, -55,
     -50, -45, -40, -35, -30,
     -25, -20, -15, -10,  -5,
       0,   5,  10,  15,  20,
      25,  30,  35,  40,  45],cmap=cm.jet)
    plt.colorbar(label='dBZ')


    plt.xlim([X.min(),X.max()])
    plt.xlabel('km')
    x_ticks=list((X.max()-X.min())*np.array([0,1.0,2.0,3.0,4.0,5.0,6.0])/6+X.min())
    plt.xticks(x_ticks)

    plt.ylim([Y.min(),Y.max()])
    plt.ylabel('km')
    plt.title('zh')
    print('data max ->%d',sc_zh.max())
    print('data min ->%d',sc_zh.min())
    savefig(str(set_gamma_u)+'zh.png',dpi=set_dpi)
    plt.show()

    #---------------------------------------------------------------------
    #   zv plot
    #---------------------------------------------------------------------
    X,Y,Z,sc_zv=funlib.scanning(r_zv,0,off_X=X_set,off_Y=0,off_Z=3000)
    #-------------------------------------------------------------------
    #   set the plot axis x and y
    #   shift the plane x and y
    #-------------------------------------------------------------------
    X = X/1000
    Y = Y/1000
    X = X-X_set/1000

    sc_zv = funlib.lg_refl2(sc_zv)


    fig = plt.figure(figsize=fig_size,dpi=set_dpi)
    fig.patch.set_facecolor('white')
    plt.contourf(X,Y,sc_zv,levels=
    [-75, -70, -65, -60, -55,
     -50, -45, -40, -35, -30,
     -25, -20, -15, -10,  -5,
       0,   5,  10,  15,  20,
      25,  30,  35,  40,  45],cmap=cm.jet)
    plt.colorbar(label='dbZ')


    plt.xlim([X.min(),X.max()])
    plt.xlabel('km')
    x_ticks=list((X.max()-X.min())*np.array([0,1.0,2.0,3.0,4.0,5.0,6.0])/6+X.min())
    plt.xticks(x_ticks)

    plt.ylim([Y.min(),Y.max()])
    plt.ylabel('km')
    plt.title('zv')
    print('data max ->%d',sc_zv.max())
    print('data min ->%d',sc_zv.min())
    savefig(str(set_gamma_u)+'zv.png',dpi=set_dpi)
    plt.show()

    #------------------------------------------------------------------------
    #   zdr plot
    #------------------------------------------------------------------------
    X,Y,Z,sc_zdr=funlib.scanning(r_zdr,0,off_X=X_set,off_Y=0,off_Z=3000)

    #-------------------------------------------------------------------
    #   set the plot axis x and y
    #   shift the plane x and y
    #-------------------------------------------------------------------
    X = X/1000
    Y = Y/1000
    X = X-X_set/1000



    fig = plt.figure(figsize=fig_size,dpi=set_dpi)
    fig.patch.set_facecolor('white')

    plt.contourf(X,Y,sc_zdr,levels=
    [0.96,0.98,1.00,1.02,1.04,1.06,1.08,1.20,1.22,1.24,1.26,1.28,1.30,1.32,1.34,1.36,1.38],cmap=cm.jet)
    plt.colorbar(label='')


    plt.xlim([X.min(),X.max()])
    plt.xlabel('km')
    x_ticks=list((X.max()-X.min())*np.array([0,1.0,2.0,3.0,4.0,5.0,6.0])/6+X.min())
    plt.xticks(x_ticks)

    plt.ylim([Y.min(),Y.max()])
    plt.ylabel('km')
    plt.title('zdr')
    print('data max ->%d',sc_zdr.max())
    print('data min ->%d',sc_zdr.min())
    savefig(str(set_gamma_u)+'zdr.png',dpi=set_dpi)
    plt.show()

    #------------------------------------------------------------------------
    #	kdp and cc 's threshold from zdr
    threshold = 1.0001
    #------------------------------------------------------------------------
    #   kdp plot
    #------------------------------------------------------------------------
    X,Y,Z,sc_kdp=funlib.scanning(r_kdp,0,off_X=X_set,off_Y=0,off_Z=3000)
    sc_kdp = funlib.compare_kdp2zdr(sc_kdp,sc_zdr,threshold)
    #-------------------------------------------------------------------
    #   set the plot axis x and y
    #   shift the plane x and y
    #-------------------------------------------------------------------
    X = X/1000
    Y = Y/1000
    X = X-X_set/1000



    fig = plt.figure(figsize=fig_size,dpi=set_dpi)
    fig.patch.set_facecolor('white')

    plt.contourf(X,Y,sc_kdp,cmap=cm.jet)


    plt.xlim([X.min(),X.max()])
    plt.xlabel('km')
    x_ticks=list((X.max()-X.min())*np.array([0,1.0,2.0,3.0,4.0,5.0,6.0])/6+X.min())
    plt.xticks(x_ticks)

    plt.ylim([Y.min(),Y.max()])
    plt.ylabel('km')
    plt.title('kdp')
    plt.colorbar(label='deg/km')
    print('data max ->%d',sc_kdp.max())
    print('data min ->%d',sc_kdp.min())

    savefig(str(set_gamma_u)+'kdp.png',dpi=set_dpi)
    plt.show()



    #------------------------------------------------------------------------
    #   rhv plot
    #------------------------------------------------------------------------
    X,Y,Z,sc_rhv=funlib.scanning(r_rhv,0,off_X=X_set,off_Y=0,off_Z=3000)
    sc_rhv = funlib.compare_rhv2zdr(sc_rhv,sc_zdr,threshold)
    #-------------------------------------------------------------------
    #   set the plot axis x and y
    #   shift the plane x and y
    #-------------------------------------------------------------------
    X = X/1000
    Y = Y/1000
    X = X-X_set/1000


    fig = plt.figure(figsize=fig_size,dpi=set_dpi)
    fig.patch.set_facecolor('white')

    plt.contourf(X,Y,sc_rhv,cmap=cm.jet)


    plt.xlim([X.min(),X.max()])
    plt.xlabel('km')
    x_ticks=list((X.max()-X.min())*np.array([0,1.0,2.0,3.0,4.0,5.0,6.0])/6+X.min())
    plt.xticks(x_ticks)

    plt.ylim([Y.min(),Y.max()])
    plt.ylabel('km')
    plt.title('cc')
    plt.colorbar(label='')
    print('data max ->%d',sc_rhv.max())
    print('data min ->%d',sc_rhv.min())
    savefig(str(set_gamma_u)+'cc.png',dpi=set_dpi)
    plt.show()



    return
