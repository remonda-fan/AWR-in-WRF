# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:09:05 2015

@author: qwe14789cn
"""
import numpy as np
from pytmatrix.tmatrix import Scatterer
from pytmatrix.psd import PSDIntegrator
from pytmatrix import orientation,tmatrix_aux,refractive
import os,datetime
import funlib

hour   = [6, 7, 8, 9, 10, 11]
minute = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

def fun(main_dir,input_data,output_data):
    for h in hour:
        for m in minute:
            if (h==11 and m ==30):
                break

            cdf_name = "wrfout_d02_2014-06-05_"+"{:0>2d}".format(h)+":"+"{:0>2d}".format(m)+":00"
            print 'reading data...'+cdf_name

            os.chdir(main_dir+output_data+os.sep+cdf_name)
            print 'change dir -> '+main_dir+output_data+os.sep+cdf_name
            print 'loading data...',

            QRAIN    =np.load('QRAIN.npy')
            QNRAIN   =np.load('QNRAIN.npy')

            QHAIL    =np.load('QHAIL.npy')
            QNHAIL   =np.load('QNHAIL.npy')

            QSNOW    =np.load('QSNOW.npy')
            QNSNOW   =np.load('QNSNOW.npy')

            QICE     =np.load('QICE.npy')
            QNICE    =np.load('QNICE.npy')

            QGRAUP   =np.load('QGRAUP.npy')
            QNGRAUPEL=np.load('QNGRAUPEL.npy')

            QCLOUD   =np.load('QCLOUD.npy')
            QNCLOUD  =np.load('QNCLOUD.npy')

            RHO      =np.load('RHO.npy')

            REFL_10CM=np.load('REFL_10CM.npy')
            Pa       =np.load('Pa.npy')
            Tem      =np.load('Tem.npy')

            print 'finished'
            #-------------------------------------------------------------------------
            print 'start using T-matrix tools...'

            Qr    =    QRAIN
            Qh    =    QHAIL
            Qs    =    QSNOW
            Qi    =    QICE
            Qg    =    QGRAUP
            Qc    =    QCLOUD

            Qnr   =    QNRAIN*RHO
            Qnh   =    QNHAIL*RHO
            Qns   =    QNSNOW*RHO
            Qni   =    QNICE*RHO
            Qng   =    QNGRAUPEL*RHO
            Qnc   =    QNCLOUD*RHO


            print 'Q>=1e-10'
            Qr=funlib.data_process(Qr)
            Qh=funlib.data_process(Qh)
            Qs=funlib.data_process(Qs)
            Qi=funlib.data_process(Qi)
            Qg=funlib.data_process(Qg)
            Qc=funlib.data_process(Qc)
            print 'finished'
            print ' '
        #problem 20151010
            print 'Nt>=0.1'
            Qnr=funlib.num_process(Qnr)
            Qnh=funlib.num_process(Qnh)
            Qns=funlib.num_process(Qns)
            Qni=funlib.num_process(Qni)
            Qng=funlib.num_process(Qng)
            Qnc=funlib.num_process(Qnc)

            print 'finished'
            print ' '


            #-------------------------------------------------------------------------
            # global gamma_u
            #-------------------------------------------------------------------------
            gamma_u  =   0


            #-------------------------------------------------------------------------
            # starting polar calculation
            #-------------------------------------------------------------------------

            #-------------------------------------------------------------------------
            # setup rain
            #-------------------------------------------------------------------------

            [aaa,bbb,ccc]=Qr.shape
            print('-'*60)
            print ' '
            print 'start rain...'
            start_time = datetime.datetime.now()
            #-------------------------------------------------------------------------
            # choice= 1,2,3 select rain,hail,snow density
            #-------------------------------------------------------------------------
            [n0,lamda]=funlib.setup_tmatrix(Qr,Qnr,gamma_u,RHO,1)

            scatterer = Scatterer(wavelength=tmatrix_aux.wl_X,m=refractive.m_w_10C[tmatrix_aux.wl_X])
            scatterer.psd_integrator = PSDIntegrator()
            scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0/funlib.drop_ar(D)
            scatterer.psd_integrator.D_max=10.0
            scatterer.psd_integrator.geometries=(tmatrix_aux.geom_horiz_back,tmatrix_aux.geom_horiz_forw)
            scatterer.or_pdf = orientation.gaussian_pdf(5.0)
            scatterer.orient = orientation.orient_averaged_fixed
            scatterer.psd_integrator.init_scatter_table(scatterer)

            #--------------------------------------------------------------------------
            # start tmatrix
            #--------------------------------------------------------------------------
            print('start tmatrix...')
            os.chdir(main_dir+output_data+os.sep+cdf_name)

            print('start calculate...zh,zdr,zv,ldr,rhv')
            #--------------------------------------------------------------------------
            n0=n0.reshape(-1)
            lamda=lamda.reshape(-1)

            r_zh,r_zdr,r_zv,r_ldr,r_rhv=apply(funlib.cal_tm4,(n0,lamda,gamma_u,scatterer))

            r_zh= r_zh.reshape(aaa,bbb,ccc)
            r_zdr = r_zdr.reshape(aaa,bbb,ccc)
            r_zv  = r_zv.reshape(aaa,bbb,ccc)
            r_ldr = r_ldr.reshape(aaa,bbb,ccc)
            r_rhv = r_rhv.reshape(aaa,bbb,ccc)
            print('finished')

            print 'saving data...',
            np.save('r_zh.npy',r_zh)
            np.save('r_zdr.npy',r_zdr)
            np.save('r_zv.npy',r_zv)
            np.save('r_ldr.npy',r_ldr)
            np.save('r_rhv.npy',r_rhv)
            print 'finished'

            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
            #------------------------------------------------------------------------------
            #   cal kdp,ai
            #------------------------------------------------------------------------------

            print('start calculate...kdp,ai')

            scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)

            r_kdp,r_ai=apply(funlib.cal_tm2,(n0,lamda,gamma_u,scatterer))

            r_kdp = r_kdp.reshape(aaa,bbb,ccc)
            r_ai  = r_ai.reshape(aaa,bbb,ccc)
            print 'finished'

            print 'saving data...',
            np.save('r_kdp.npy',r_kdp)
            np.save('r_ai.npy',r_ai)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
            #------------------------------------------------------------------
            # setup cloud
            #------------------------------------------------------------------
            [aaa,bbb,ccc]=Qc.shape
            print('-'*60)
            print ' '
            print 'start cloud...'
            #-------------------------------------------------------------------------
            # choice= 1,2,3 select rain,hail,snow density
            #-------------------------------------------------------------------------
            [n0,lamda]=funlib.setup_tmatrix(Qc,Qnc,gamma_u,RHO,1)

            scatterer = Scatterer(wavelength=tmatrix_aux.wl_X,m=refractive.m_w_10C[tmatrix_aux.wl_X])
            scatterer.psd_integrator = PSDIntegrator()
            scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0/funlib.drop_ar(D)
            scatterer.psd_integrator.D_max=2.0
            scatterer.psd_integrator.geometries=(tmatrix_aux.geom_horiz_back,tmatrix_aux.geom_horiz_forw)
            scatterer.or_pdf = orientation.gaussian_pdf(10.0)
            scatterer.orient = orientation.orient_averaged_fixed
            scatterer.psd_integrator.init_scatter_table(scatterer)

            #--------------------------------------------------------------------------
            # start tmatrix
            #--------------------------------------------------------------------------

            print('start tmatrix...')
            os.chdir(main_dir+output_data+os.sep+cdf_name)

            print('start calculate...zh,zdr,zv,ldr,rhv')
            #--------------------------------------------------------------------------
            n0=n0.reshape(-1)
            lamda=lamda.reshape(-1)

            c_zh,c_zdr,c_zv,c_ldr,c_rhv=apply(funlib.cal_tm4,(n0,lamda,gamma_u,scatterer))

            c_zh= c_zh.reshape(aaa,bbb,ccc)
            c_zdr = c_zdr.reshape(aaa,bbb,ccc)
            c_zv  = c_zv.reshape(aaa,bbb,ccc)
            c_ldr = c_ldr.reshape(aaa,bbb,ccc)
            c_rhv = c_rhv.reshape(aaa,bbb,ccc)
            print('finished')

            print 'saving data...',
            np.save('c_zh.npy',c_zh)
            np.save('c_zdr.npy',c_zdr)
            np.save('c_zv.npy',c_zv)
            np.save('c_ldr.npy',c_ldr)
            np.save('c_rhv.npy',c_rhv)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
            #------------------------------------------------------------------------------
            #   cal kdp,ai
            #------------------------------------------------------------------------------

            print('start calculate...kdp,ai')

            scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)

            c_kdp,c_ai=apply(funlib.cal_tm2,(n0,lamda,gamma_u,scatterer))

            c_kdp = c_kdp.reshape(aaa,bbb,ccc)
            c_ai  = c_ai.reshape(aaa,bbb,ccc)
            print 'finished'

            print 'saving data...',
            np.save('c_kdp.npy',c_kdp)
            np.save('c_ai.npy',c_ai)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
            #------------------------------------------------------------------
            # setup snow
            #------------------------------------------------------------------
            [aaa,bbb,ccc]=Qs.shape
            print('-'*60)
            print ' '
            print 'start snow...'
            #-------------------------------------------------------------------------
            # choice= 1,2,3 select rain,hail,snow density
            #-------------------------------------------------------------------------
            [n0,lamda]=funlib.setup_tmatrix(Qs,Qns,gamma_u,RHO,3)

            scatterer = Scatterer(wavelength=tmatrix_aux.wl_X,m=refractive.m_w_10C[tmatrix_aux.wl_X])
            scatterer.psd_integrator = PSDIntegrator()
            scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0/funlib.drop_ar(D)
            scatterer.psd_integrator.D_max=2.0
            scatterer.psd_integrator.geometries=(tmatrix_aux.geom_horiz_back,tmatrix_aux.geom_horiz_forw)
            scatterer.or_pdf = orientation.gaussian_pdf(20.0)
            scatterer.orient = orientation.orient_averaged_fixed
            scatterer.psd_integrator.init_scatter_table(scatterer)

            #--------------------------------------------------------------------------
            # start tmatrix
            #--------------------------------------------------------------------------

            print('start tmatrix...')
            os.chdir(main_dir+output_data+os.sep+cdf_name)

            print('start calculate...zh,zdr,zv,ldr,rhv')
            #--------------------------------------------------------------------------
            n0=n0.reshape(-1)
            lamda=lamda.reshape(-1)

            s_zh,s_zdr,s_zv,s_ldr,s_rhv=apply(funlib.cal_tm4,(n0,lamda,gamma_u,scatterer))

            s_zh= s_zh.reshape(aaa,bbb,ccc)
            s_zdr = s_zdr.reshape(aaa,bbb,ccc)
            s_zv  = s_zv.reshape(aaa,bbb,ccc)
            s_ldr = s_ldr.reshape(aaa,bbb,ccc)
            s_rhv = s_rhv.reshape(aaa,bbb,ccc)
            print('finished')

            print 'saving data...',
            np.save('s_zh.npy',s_zh)
            np.save('s_zdr.npy',s_zdr)
            np.save('s_zv.npy',s_zv)
            np.save('s_ldr.npy',s_ldr)
            np.save('s_rhv.npy',s_rhv)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
        #------------------------------------------------------------------------------
        #   cal kdp,ai
        #------------------------------------------------------------------------------

            print('start calculate...kdp,ai')

            scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)

            s_kdp,s_ai=apply(funlib.cal_tm2,(n0,lamda,gamma_u,scatterer))

            s_kdp = s_kdp.reshape(aaa,bbb,ccc)
            s_ai  = s_ai.reshape(aaa,bbb,ccc)
            print 'finished'

            print 'saving data...',
            np.save('s_kdp.npy',s_kdp)
            np.save('s_ai.npy',s_ai)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
            #------------------------------------------------------------------
            # setup ice
            #------------------------------------------------------------------
            [aaa,bbb,ccc]=Qi.shape
            print('-'*60)
            print ' '
            print 'start ice...'
            #-------------------------------------------------------------------------
            # choice= 1,2,3 select rain,hail,snow density
            #-------------------------------------------------------------------------
            [n0,lamda]=funlib.setup_tmatrix(Qs,Qns,gamma_u,RHO,2)

            scatterer = Scatterer(wavelength=tmatrix_aux.wl_X,m=refractive.m_w_0C[tmatrix_aux.wl_X])
            scatterer.psd_integrator = PSDIntegrator()
            scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0/funlib.drop_ar(D)
            scatterer.psd_integrator.D_max=2.0
            scatterer.psd_integrator.geometries=(tmatrix_aux.geom_horiz_back,tmatrix_aux.geom_horiz_forw)
            scatterer.or_pdf = orientation.gaussian_pdf(2.0)
            scatterer.orient = orientation.orient_averaged_fixed
            scatterer.psd_integrator.init_scatter_table(scatterer)

            #--------------------------------------------------------------------------
            # start tmatrix
            #--------------------------------------------------------------------------

            print('start tmatrix...')
            os.chdir(main_dir+output_data+os.sep+cdf_name)

            print('start calculate...zh,zdr,zv,ldr,rhv')
            #--------------------------------------------------------------------------
            n0=n0.reshape(-1)
            lamda=lamda.reshape(-1)

            i_zh,i_zdr,i_zv,i_ldr,i_rhv=apply(funlib.cal_tm4,(n0,lamda,gamma_u,scatterer))

            i_zh= i_zh.reshape(aaa,bbb,ccc)
            #i_zh= lg_zh(i_zh)
            i_zdr = i_zdr.reshape(aaa,bbb,ccc)
            i_zv  = i_zv.reshape(aaa,bbb,ccc)
            i_ldr = i_ldr.reshape(aaa,bbb,ccc)
            i_rhv = i_rhv.reshape(aaa,bbb,ccc)
            print('finished')

            print 'saving data...',
            np.save('i_zh.npy',i_zh)
            np.save('i_zdr.npy',i_zdr)
            np.save('i_zv.npy',i_zv)
            np.save('i_ldr.npy',i_ldr)
            np.save('i_rhv.npy',i_rhv)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
        #------------------------------------------------------------------------------
        #   cal kdp,ai
        #------------------------------------------------------------------------------

            print('start calculate...kdp,ai')

            scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)

            i_kdp,i_ai=apply(funlib.cal_tm2,(n0,lamda,gamma_u,scatterer))

            i_kdp = i_kdp.reshape(aaa,bbb,ccc)
            i_ai  = i_ai.reshape(aaa,bbb,ccc)
            print 'finished'

            print 'saving data...',
            np.save('i_kdp.npy',i_kdp)
            np.save('i_ai.npy',i_ai)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
            #------------------------------------------------------------------
            # setup graupel
            #------------------------------------------------------------------
            [aaa,bbb,ccc]=Qg.shape
            print('-'*60)
            print ' '
            print 'start graupel...'
            #-------------------------------------------------------------------------
            # choice= 1,2,3 select rain,hail,snow density
            #-------------------------------------------------------------------------
            [n0,lamda]=funlib.setup_tmatrix(Qg,Qng,gamma_u,RHO,2)

            scatterer = Scatterer(wavelength=tmatrix_aux.wl_X,m=refractive.m_w_10C[tmatrix_aux.wl_X])
            scatterer.psd_integrator = PSDIntegrator()
            scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0/funlib.drop_ar(D)
            scatterer.psd_integrator.D_max=2.0
            scatterer.psd_integrator.geometries=(tmatrix_aux.geom_horiz_back,tmatrix_aux.geom_horiz_forw)
            scatterer.or_pdf = orientation.gaussian_pdf(2.0)
            scatterer.orient = orientation.orient_averaged_fixed
            scatterer.psd_integrator.init_scatter_table(scatterer)

            #--------------------------------------------------------------------------
            # start tmatrix
            #--------------------------------------------------------------------------

            print('start tmatrix...')
            os.chdir(main_dir+output_data+os.sep+cdf_name)

            print('start calculate...zh,zdr,zv,ldr,rhv')
            #--------------------------------------------------------------------------
            n0=n0.reshape(-1)
            lamda=lamda.reshape(-1)

            g_zh,g_zdr,g_zv,g_ldr,g_rhv=apply(funlib.cal_tm4,(n0,lamda,gamma_u,scatterer))

            g_zh= g_zh.reshape(aaa,bbb,ccc)
            #g_zh= lg_zh(g_zh)
            g_zdr = g_zdr.reshape(aaa,bbb,ccc)
            g_zv  = g_zv.reshape(aaa,bbb,ccc)
            g_ldr = g_ldr.reshape(aaa,bbb,ccc)
            g_rhv = g_rhv.reshape(aaa,bbb,ccc)
            print('finished')

            print 'saving data...',
            np.save('g_zh.npy',g_zh)
            np.save('g_zdr.npy',g_zdr)
            np.save('g_zv.npy',g_zv)
            np.save('g_ldr.npy',g_ldr)
            np.save('g_rhv.npy',g_rhv)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
        #------------------------------------------------------------------------------
        #   cal kdp,ai
        #------------------------------------------------------------------------------

            print('start calculate...kdp,ai')

            scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)

            g_kdp,g_ai=apply(funlib.cal_tm2,(n0,lamda,gamma_u,scatterer))

            g_kdp = g_kdp.reshape(aaa,bbb,ccc)
            g_ai  = g_ai.reshape(aaa,bbb,ccc)
            print 'finished'

            print 'saving data...',
            np.save('g_kdp.npy',g_kdp)
            np.save('g_ai.npy',g_ai)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
            #------------------------------------------------------------------
            # setup hail
            #------------------------------------------------------------------
            [aaa,bbb,ccc]=Qh.shape
            print('-'*60)
            print ' '
            print 'start hail...'
            #-------------------------------------------------------------------------
            # choice= 1,2,3 select rain,hail,snow density
            #-------------------------------------------------------------------------
            [n0,lamda]=funlib.setup_tmatrix(Qh,Qnh,gamma_u,RHO,2)

            scatterer = Scatterer(wavelength=tmatrix_aux.wl_X,m=refractive.m_w_10C[tmatrix_aux.wl_X])
            scatterer.psd_integrator = PSDIntegrator()
            scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0/funlib.drop_ar(D)
            scatterer.psd_integrator.D_max=5.0
            scatterer.psd_integrator.geometries=(tmatrix_aux.geom_horiz_back,tmatrix_aux.geom_horiz_forw)
            scatterer.or_pdf = orientation.gaussian_pdf(5.0)
            scatterer.orient = orientation.orient_averaged_fixed
            scatterer.psd_integrator.init_scatter_table(scatterer)

            #--------------------------------------------------------------------------
            # start tmatrix
            #--------------------------------------------------------------------------

            print('start tmatrix...')
            os.chdir(main_dir+output_data+os.sep+cdf_name)

            print('start calculate...zh,zdr,zv,ldr,rhv')
            #--------------------------------------------------------------------------
            n0=n0.reshape(-1)
            lamda=lamda.reshape(-1)

            h_zh,h_zdr,h_zv,h_ldr,h_rhv=apply(funlib.cal_tm4,(n0,lamda,gamma_u,scatterer))

            h_zh= h_zh.reshape(aaa,bbb,ccc)
            #g_zh= lg_zh(g_zh)
            h_zdr = h_zdr.reshape(aaa,bbb,ccc)
            h_zv  = h_zv.reshape(aaa,bbb,ccc)
            h_ldr = h_ldr.reshape(aaa,bbb,ccc)
            h_rhv = h_rhv.reshape(aaa,bbb,ccc)
            print('finished')

            print 'saving data...',
            np.save('h_zh.npy',h_zh)
            np.save('h_zdr.npy',h_zdr)
            np.save('h_zv.npy',h_zv)
            np.save('h_ldr.npy',h_ldr)
            np.save('h_rhv.npy',h_rhv)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'
        #------------------------------------------------------------------------------
        #   cal kdp,ai
        #------------------------------------------------------------------------------

            print('start calculate...kdp,ai')

            scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)

            h_kdp,h_ai=apply(funlib.cal_tm2,(n0,lamda,gamma_u,scatterer))

            h_kdp = h_kdp.reshape(aaa,bbb,ccc)
            h_ai  = h_ai.reshape(aaa,bbb,ccc)
            print 'finished'

            print 'saving data...',
            np.save('h_kdp.npy',h_kdp)
            np.save('h_ai.npy',h_ai)
            print 'finished'
            print 'used time:'+str((datetime.datetime.now()-start_time).seconds)+' s'

            print('-'*60)
    return
