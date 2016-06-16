import os
import numpy as np
from netCDF4 import Dataset
from mayavi import mlab
from math import pi,gamma,log10
import sys

main_dir=os.getcwd()
os.chdir(main_dir+os.sep+'output')

camera1=(0.0,0.0,307.7645695540192,np.array([ 79.66195959, 74.22460988,9.96509266]))
camera2=(45.00000000000005,54.735610317245346,389.61669188814807,np.array([61.00005691,87.63795239,6.8619907]))
camera3=(45.0,54.735610317245346,607.35769190957262,np.array([89.80421373,137.88978957,7.30599671]))
camera   = (45.0, 54.735610317245346, 604.47202939013732, np.array([ 101. ,  120.5,   15. ]))
camera_x = (0.0, 90.0, 604.47202939013721, np.array([ 101. ,  120.5,   15. ]))
camera_top = (270.0, 0.0, 414.83347579371099, np.array([ 101.29680498,  141.91213697,   14.5       ]))
camera_f   = (270.0,0.0,234.16268239914447,np.array([74.83200638,107.24792847,14.5]))
#-----------------------------------------------------------
def kdp_nan_sum(data):
    flag=np.logical_not(np.isnan(data))
    n=len(data)
    result=[]
    count=0.0
    for i in range(n):
        if flag[i]==True:
            result.append(data[i])
            count=count+1.0
    if count==0.0:
        return float('nan')
    else:
        return np.sum(result)

def kdp_nan_data_add(*data):
    n=len(data)
    length=len(data[0])
    total=[]
    for ii in range(length):
        temp=[]
        for iii in range(n):
            temp.append(data[iii][ii])
        total.append(kdp_nan_sum(temp))
    return total
def data_process(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if data[aa,bb,cc]<=1e-10:
                    data[aa,bb,cc]=1e-10
        print '\r|'+'='*(50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)) \
        +' '*(50-50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc))+'|'\
        +'%1.2f%%' %(100*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)),
    print ' '
    return data

def lg_refl(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                    data[aa,bb,cc]=log10(data[aa,bb,cc])
        print '\r|'+'='*(50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)) \
        +' '*(50-50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc))+'|'\
        +'%1.2f%%' %(100*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)),
    print ' '
    return data

def cgsp(data):
        [aaa,bbb,ccc]=data.shape
        temp=np.zeros([bbb,ccc,aaa])
        for aa in xrange(aaa):
            for bb in xrange(bbb):
                for cc in xrange(ccc):
                    temp[bbb-bb-1,cc,aa]=data[aa,bb,cc]
        return temp

def refl_process(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if data[aa,bb,cc]<=1e-30:
                    data[aa,bb,cc]=1e-30
        print '\r|'+'='*(50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)) \
        +' '*(50-50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc))+'|'\
        +'%1.2f%%' %(100*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)),
    print ' '
    return data

def t_data_plot(data,dataname,title_name,num_contours,zdr_flag=0,data_min=-5,save_name="new.png"):
    size_x,size_y,size_z=data.shape
    mlab.figure(dataname,bgcolor=(1,1,1),fgcolor=(0,0,0),size=(600,600))

    if zdr_flag==1:
        fig_data=mlab.contour3d(data[:,:,:],vmin=data_min,vmax=3.0,colormap='jet')
    else:
        fig_data=mlab.contour3d(data[:,:,:],vmin=-25.0,vmax=55.0,colormap='jet')
    fig_data.contour.number_of_contours=num_contours
    fig_data.actor.property.opacity=0.4
    mlab.title(dataname)
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    #colorbar=mlab.colorbar(title=title_name,orientation='vertical',nb_labels=10)
    #colorbar.scalar_bar_representation.position=[0.85,0.1]
    #colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera)
    
    mlab.savefig(save_name)
    mlab.close()

def lg_zdr(zh,zv):
    [aaa,bbb,ccc]=zh.shape
    zdr = np.zeros((aaa,bbb,ccc))
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                    zdr[aa,bb,cc]=10*log10(zh[aa,bb,cc]/zv[aa,bb,cc])
        print '\r|'+'='*(50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)) \
        +' '*(50-50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc))+'|'\
        +'%1.2f%%' %(100*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)),
    print ' '
    return zdr
#-----------------------------------------------------------

hour   = [6,7,8,9,10,11]
minute = [0,30]

for h in hour:
    for m in minute:
        if (h==11 and m ==30):
            break

        file_name = "wrfout_d02_2014-06-05_"+"{:0>2d}".format(h)+"-"+"{:0>2d}".format(m)+"-00"
        os.chdir(main_dir+os.sep+'output'+os.sep+file_name)
        print os.getcwd()

        r_zh         =   np.load('r_zh.npy')
        r_zv         =   np.load('r_zv.npy')
        r_kdp        =   np.load('r_kdp.npy')

        h_zh         =   np.load('h_zh.npy')
        h_zv         =   np.load('h_zv.npy')
        h_kdp        =   np.load('h_kdp.npy')
        h_zh         =   h_zh * 0.93/0.2
        h_zv         =   h_zv * 0.93/0.2

        c_zh         =   np.load('c_zh.npy')
        c_zv         =   np.load('c_zv.npy')
        c_kdp        =   np.load('c_kdp.npy')

        g_zh         =   np.load('g_zh.npy')
        g_zv         =   np.load('g_zv.npy')
        g_kdp        =   np.load('g_kdp.npy')
        g_zh         =   g_zh * 0.93/0.2
        g_zv         =   g_zv * 0.93/0.2

        i_zh         =   np.load('i_zh.npy')
        i_zv         =   np.load('i_zv.npy')
        i_kdp        =   np.load('i_kdp.npy')
        i_zh         =   i_zh * 0.93/0.2
        i_zv         =   i_zv * 0.93/0.2

        s_zh         =   np.load('s_zh.npy')
        s_zv         =   np.load('s_zv.npy')
        s_kdp        =   np.load('s_kdp.npy')
        s_zh         =   s_zh * 0.93/0.2
        s_zv         =   s_zv * 0.93/0.2
        #------------------------------------------
        
        zh = r_zh + c_zh + g_zh + s_zh + i_zh + h_zh
        zv = r_zv + c_zv + g_zv + s_zv + i_zv + h_zv
        zdr_dB=lg_zdr(zh,zv)
        np.save('zh.npy',zh)
        np.save('zv.npy',zv)
        np.save('zdr_dB.npy',zdr_dB)
	
        zdr_name = 'zdr'+"{:0>2d}".format(h)+"-"+"{:0>2d}".format(m)+"-00"+'.png'
        t_data_plot(zdr_dB,'','',15,zdr_flag=1,data_min=0.0,save_name=zdr_name)
	
        
        [aaa,bbb,ccc]=s_kdp.shape
        s_kdp = s_kdp.reshape(-1)
        i_kdp = i_kdp.reshape(-1)
        c_kdp = c_kdp.reshape(-1)
        r_kdp = r_kdp.reshape(-1)
        g_kdp = g_kdp.reshape(-1)
        h_kdp = h_kdp.reshape(-1)
		
        kdp=kdp_nan_data_add(r_kdp,s_kdp,i_kdp,c_kdp,g_kdp,h_kdp)
        kdp   = np.array(kdp)
        kdp=kdp.reshape(aaa,bbb,ccc)

        kdp_name='kdp'+"{:0>2d}".format(h)+"-"+"{:0>2d}".format(m)+"-00"+'.png'
        t_data_plot(kdp,'','deg/km',15,1,0,save_name=kdp_name)
		

        zh_dB   = 10*lg_refl(refl_process(zh))
        zv_dB   = 10*lg_refl(refl_process(zv))

        zh_name = 'zh'+"{:0>2d}".format(h)+"-"+"{:0>2d}".format(m)+"-00"+'.png'
        zv_name = 'zv'+"{:0>2d}".format(h)+"-"+"{:0>2d}".format(m)+"-00"+'.png'
        t_data_plot(zh_dB,'','dBZ',15,save_name=zh_name)

        t_data_plot(zv_dB,'','dBZ',15,save_name=zv_name)
		
os.chdir(main_dir)
