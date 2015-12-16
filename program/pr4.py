# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:25:22 2015

@author: qwe14789cn
"""
print 'import figure tools...',
import os
import numpy as np

import funlib
print 'finished'
print ' '


def fun(data_dir,input_data,output_data):
    os.chdir(data_dir+input_data)
    Qr    =   np.load('QRAIN.npy')
    Qh    =   np.load('QHAIL.npy')  
    Qs    =   np.load('QSNOW.npy')  
    Qi    =   np.load('QICE.npy')       
    Qg    =   np.load('QGRAUP.npy')
    Qc    =   np.load('QCLOUD.npy')
    
    Pa           =   np.load('Pa.npy')
    RHO          =   np.load('RHO.npy')
    Tem          =   np.load('Tem.npy')
    REFL_10CM    =   np.load('REFL_10CM.npy')
   
    os.chdir(data_dir+output_data)
    
    print 'loading data...',
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
    
    r_zh_dB = funlib.lg_refl(funlib.refl_process(r_zh))        
    r_zv_dB = funlib.lg_refl(funlib.refl_process(r_zv)) 
    c_zh_dB = funlib.lg_refl(funlib.refl_process(c_zh)) 
    c_zv_dB = funlib.lg_refl(funlib.refl_process(c_zv)) 
    g_zh_dB = funlib.lg_refl(funlib.refl_process(g_zh))  
    g_zv_dB = funlib.lg_refl(funlib.refl_process(g_zv)) 
    i_zh_dB = funlib.lg_refl(funlib.refl_process(i_zh))
    i_zv_dB = funlib.lg_refl(funlib.refl_process(i_zv))
    s_zh_dB = funlib.lg_refl(funlib.refl_process(s_zh))    
    s_zv_dB = funlib.lg_refl(funlib.refl_process(s_zv))  
    
    np.save('r_zh_dB.npy',r_zh_dB)
    np.save('c_zh_dB.npy',c_zh_dB)
    np.save('g_zh_dB.npy',g_zh_dB)
    np.save('i_zh_dB.npy',i_zh_dB)
    np.save('s_zh_dB.npy',s_zh_dB)
    
    np.save('r_zv_dB.npy',r_zv_dB)
    np.save('c_zv_dB.npy',c_zv_dB)
    np.save('g_zv_dB.npy',g_zv_dB)
    np.save('i_zv_dB.npy',i_zv_dB)
    np.save('s_zv_dB.npy',s_zv_dB)

    r_zh         =   np.load('r_zh.npy')
    c_zh         =   np.load('c_zh.npy')
    g_zh         =   np.load('g_zh.npy')
    s_zh         =   np.load('s_zh.npy')
    i_zh         =   np.load('i_zh.npy')


    r_zv         =   np.load('r_zv.npy')
    c_zv         =   np.load('c_zv.npy')
    g_zv         =   np.load('g_zv.npy')
    s_zv         =   np.load('s_zv.npy')
    i_zv         =   np.load('i_zv.npy')    
    
    zh = r_zh + c_zh + g_zh + s_zh + i_zh
    zv = r_zv + c_zv + g_zv + s_zv + i_zv
    
    np.save('zh.npy',zh)
    np.save('zv.npy',zv)
    
    zh_dB   = funlib.lg_refl(funlib.refl_process(zh))  
    zv_dB   = funlib.lg_refl(funlib.refl_process(zv))  
    
    np.save('zh_dB.npy',zh_dB)    
    np.save('zv_dB.npy',zv_dB)
    
    print 'finished'
    print ' '
    
    print 'painting...',
    print ' '
    
    #--------------------------------------------------------------------------
    
    funlib.t_data_plot(r_zh_dB,'r_zh','dBZ',15)
    funlib.t_data_plot(r_zv_dB,'r_zv','dBZ',15)
      
    #funlib.t_data_plot(c_zh_dB,'c_zh','dBZ',15)
    #funlib.t_data_plot(c_zv_dB,'c_zv','dBZ',15)  

    #funlib.t_data_plot(g_zh_dB,'g_zh','dBZ',15)
    #funlib.t_data_plot(g_zv_dB,'g_zv','dBZ',15)

    #funlib.t_data_plot(i_zh_dB,'i_zh','dBZ',15)
    #funlib.t_data_plot(i_zv_dB,'i_zv','dBZ',15)    

    #funlib.t_data_plot(s_zh_dB,'s_zh','dBZ',15)
    #funlib.t_data_plot(s_zv_dB,'s_zv','dBZ',15)

    #funlib.t_data_plot(zh_dB,'zh','dBZ',15)
    #funlib.t_data_plot(zv_dB,'zv','dBZ',15)
    
    #--------------------------------------------------------------------------
    #
    # start zdr
    #    
    #--------------------------------------------------------------------------
    funlib.t_data_plot(r_zdr,'r_zdr','',15,1)
    #funlib.t_data_plot(c_zdr,'c_zdr','',15)
    #funlib.t_data_plot(g_zdr,'g_zdr','',15)
    #funlib.t_data_plot(s_zdr,'s_zdr','',15)
    #funlib.t_data_plot(i_zdr,'i_zdr','',15)
    
    r_zdr         =   np.load('r_zdr.npy')
    c_zdr         =   np.load('c_zdr.npy')
    g_zdr         =   np.load('g_zdr.npy')
    s_zdr         =   np.load('s_zdr.npy')
    i_zdr         =   np.load('i_zdr.npy')     
    
    print 'reshaping all zdr data...',
    size_x,size_y,size_z=r_zdr.shape
    s_zdr = s_zdr.reshape(-1)
    i_zdr = i_zdr.reshape(-1)
    c_zdr = c_zdr.reshape(-1)
    r_zdr = r_zdr.reshape(-1)
    g_zdr = g_zdr.reshape(-1)
    print 'finished'
    print ' '
    
    print 'calculating zdr data...',
    #zdr=funlib.zdr_nan_data_add(r_zdr,s_zdr,i_zdr,c_zdr,g_zdr)
    print 'finished'
    print ' '
    
    #zdr=np.array(zdr)
    #zdr=zdr.reshape(size_x,size_y,size_z)
    
    print 'saving zdr data...',
    #np.save('zdr.npy',zdr)
    print 'finished'
    print ' '
    
    #------------------------------------------------------------------ 
    #funlib.t_data_plot(zdr,'zdr','',50)
    
    #--------------------------------------------------------------------------
    #
    # start cc
    #    
    #--------------------------------------------------------------------------

    #funlib.t_data_plot(r_rhv,'r_rhv','',15)
    
    #--------------------------------------------------------------------------
    #funlib.t_data_plot(c_rhv,'c_rhv','',15)
    
    #--------------------------------------------------------------------------
    #funlib.t_data_plot(i_rhv,'i_rhv','',15)
    
    #--------------------------------------------------------------------------
    #funlib.t_data_plot(g_rhv,'g_rhv','',15)
    
    #--------------------------------------------------------------------------
    #funlib.t_data_plot(s_rhv,'s_rhv','',15)
       
    print 'reshaping all rhv data...',  
    
    s_rhv = s_rhv.reshape(-1)
    i_rhv = i_rhv.reshape(-1)
    c_rhv = c_rhv.reshape(-1)
    r_rhv = r_rhv.reshape(-1)
    g_rhv = g_rhv.reshape(-1)
    print 'finished'
    print ' '
    
    print 'calculating rhv data...',
    rhv=funlib.rhv_nan_data_add(c_rhv,s_rhv,g_rhv,i_rhv,r_rhv)
    print 'finished'
    print ' '
    
    rhv=np.array(rhv)
    rhv=rhv.reshape(size_x,size_y,size_z)
    print 'saving rhv data...',
    np.save('rhv.npy',rhv)
    print 'finished'
    print ' '    
    
    #funlib.t_data_plot(rhv,'rhv','',100) 
    
    # 20151031 
    
    
    #--------------------------------------------------------------------------
    #
    # start kdp
    #    
    #--------------------------------------------------------------------------

    funlib.t_data_plot(r_kdp,'r_kdp','deg/km',15,1,0)
    '''
    size_x,size_y,size_z=r_kdp.shape
    mlab.figure('r_kdp',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
    fig_r_kdp=mlab.contour3d(r_kdp[:,:,:],vmin=0.0,colormap='jet')
    fig_r_kdp.contour.number_of_contours=15
    fig_r_kdp.actor.property.opacity=0.4
    mlab.title('r_kdp')
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    colorbar=mlab.colorbar(title='deg/Km',orientation='vertical',nb_labels=10)
    colorbar.scalar_bar_representation.position=[0.85,0.1]
    colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera3)
    mlab.show()

    size_x,size_y,size_z=c_kdp.shape
    mlab.figure('c_kdp',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
    fig_c_kdp=mlab.contour3d(c_kdp[:,:,:],vmin=0.0,colormap='jet')
    fig_c_kdp.contour.number_of_contours=15
    fig_c_kdp.actor.property.opacity=0.4
    mlab.title('c_kdp')
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    colorbar=mlab.colorbar(title='deg/Km',orientation='vertical',nb_labels=10)
    colorbar.scalar_bar_representation.position=[0.85,0.1]
    colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera3)
    mlab.show()
    
    size_x,size_y,size_z=i_kdp.shape
    mlab.figure('i_kdp',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
    fig_i_kdp=mlab.contour3d(i_kdp[:,:,:],vmin=0.0,colormap='jet')
    fig_i_kdp.contour.number_of_contours=15
    fig_i_kdp.actor.property.opacity=0.4
    mlab.title('i_kdp')
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    colorbar=mlab.colorbar(title='deg/Km',orientation='vertical',nb_labels=10)
    colorbar.scalar_bar_representation.position=[0.85,0.1]
    colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera3)
    mlab.show()
    
    size_x,size_y,size_z=s_kdp.shape
    mlab.figure('s_kdp',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
    fig_s_kdp=mlab.contour3d(s_kdp[:,:,:],vmin=0.0,colormap='jet')
    fig_s_kdp.contour.number_of_contours=15
    fig_s_kdp.actor.property.opacity=0.4
    mlab.title('s_kdp')
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    colorbar=mlab.colorbar(title='deg/Km',orientation='vertical',nb_labels=10)
    colorbar.scalar_bar_representation.position=[0.85,0.1]
    colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera3)
    mlab.show()
    
    size_x,size_y,size_z=g_kdp.shape
    mlab.figure('g_kdp',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
    fig_g_kdp=mlab.contour3d(g_kdp[:,:,:],vmin=0.0,colormap='jet')
    fig_g_kdp.contour.number_of_contours=15
    fig_g_kdp.actor.property.opacity=0.4
    mlab.title('g_kdp')
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    colorbar=mlab.colorbar(title='deg/Km',orientation='vertical',nb_labels=10)
    colorbar.scalar_bar_representation.position=[0.85,0.1]
    colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera3)
    mlab.show()
    
    
    print 'reshaping all kdp data...',

    s_kdp = s_kdp.reshape(-1)
    i_kdp = i_kdp.reshape(-1)
    c_kdp = c_kdp.reshape(-1)
    r_kdp = r_kdp.reshape(-1)
    g_kdp = g_kdp.reshape(-1)
    print 'finished'
    print ' '
    
    print 'calculating kdp data...',
    kdp=funlib.kdp_nan_data_add(r_kdp,s_kdp,i_kdp,c_kdp,g_kdp)
    print 'finished'
    print ' '
    
    kdp=np.array(kdp)
    kdp=kdp.reshape(size_x,size_y,size_z)
    
    size_x,size_y,size_z=kdp.shape
    mlab.figure('kdp',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
    fig_kdp=mlab.contour3d(kdp[:,:,:],vmin=0.0,colormap='jet')
    fig_kdp.contour.number_of_contours=15
    fig_kdp.actor.property.opacity=0.4
    mlab.title('kdp')
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    colorbar=mlab.colorbar(title='deg/Km',orientation='vertical',nb_labels=10)
    colorbar.scalar_bar_representation.position=[0.85,0.1]
    colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera3)
    mlab.show()    
    '''
    return
