# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#   this module contains all functions which the main program need
#------------------------------------------------------------------------------
import numpy as np
import math
from math import pi,gamma,log10
from pytmatrix.psd import UnnormalizedGammaPSD
from pytmatrix import radar
from mayavi import mlab
#------------------------
#   pr1
#------------------------
def cgsp(data):
        [aaa,bbb,ccc]=data.shape
        temp=np.zeros([bbb,ccc,aaa])
        for aa in xrange(aaa):
            for bb in xrange(bbb):
                for cc in xrange(ccc):
                    temp[bbb-bb-1,cc,aa]=data[aa,bb,cc]
        return temp

#------------------------
#   pr2
#------------------------
def drop_ar(D_eq):
    if D_eq <0.7:
        return 1.0;
    elif D_eq <1.5:
        return 1.173-0.5165*D_eq +0.4698*D_eq**2-0.1317*D_eq**3-\
            8.5e-3*D_eq**4
    else:
        return 1.065-6.25e-2*D_eq -3.99e-3*D_eq**2+7.66e-4*D_eq**3-\
            4.095e-5*D_eq**4

def data_process(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if data[aa,bb,cc]<=1e-10:
                    data[aa,bb,cc]=1e-10
    return data

def setup_tmatrix(Q,Nt,gamma_u,RHO,choice):
    #----------------------
    # choice= 1,2,3 select rain,hail,snow

    RHO_rain     =     1000
    RHO_hail     =     913
    RHO_snow     =     100
    if choice==1:
        RHO_c=RHO_rain
    elif choice==2:
        RHO_c=RHO_hail
    elif choice==3:
        RHO_c=RHO_snow


    lamda = ((gamma(4+gamma_u)*RHO_c*Nt*pi)/(6*gamma(1+gamma_u)*RHO*Q))**(1.0/3)
    lamda = lamda *1.0/1000
    n0= Nt*lamda**(1+gamma_u)*gamma(1+gamma_u)**-1.0

    return n0,lamda

def num_process(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if data[aa,bb,cc]<=1:
                    data[aa,bb,cc]=1
    return data

def cal_tm4(n0,lamda,u,scatterer):
    rain_zdr=[]
    rain_zv=[]
    rain_ldr=[]
    rain_rhv=[]
    rain_zh=[]
    length=len(n0)
    for i in range(length):
        scatterer.psd=UnnormalizedGammaPSD(N0=n0[i],Lambda=lamda[i],mu=u)
        rain_zh.append(radar.refl(scatterer))
        rain_zdr.append(radar.Zdr(scatterer))
        rain_zv.append(radar.refl(scatterer,h_pol=False))
        rain_ldr.append(radar.ldr(scatterer))
        rain_rhv.append(radar.rho_hv(scatterer))
        if i%1000==0:
            print('\r|'+'='*(50*i/length)+' '*(50-50*i/length)+'|'+'%1.2f%%' %(100.0*i/length))

    rain_zh = np.array(rain_zh)
    rain_zdr  = np.array(rain_zdr)
    rain_zv   = np.array(rain_zv)
    rain_ldr  = np.array(rain_ldr)
    rain_rhv  = np.array(rain_rhv)

    return rain_zh,rain_zdr,rain_zv,rain_ldr,rain_rhv

def cal_tm2(n0,lamda,u,scatterer):
    rain_kdp=[]
    rain_ai=[]
    length=len(n0)
    for i in range(length):
        scatterer.psd=UnnormalizedGammaPSD(N0=n0[i],Lambda=lamda[i],mu=u)
        rain_kdp.append(radar.Kdp(scatterer))
        rain_ai.append(radar.Ai(scatterer))
        if i%1000==0:
            print('\r|'+'='*(50*i/length)+' '*(50-50*i/length)+'|'+'%1.2f%%' %(100.0*i/length))
    rain_kdp=np.array(rain_kdp)
    rain_ai =np.array(rain_ai)

    return rain_kdp,rain_ai

#------------------------
#   pr3
#------------------------
def compare2(data1,data2,threshold=1.0):
	[aaa,bbb]=data1.shape
	for aa in xrange(aaa):
		for bb in xrange(bbb):
			if data2[aa,bb]<=threshold:
				data1[aa,bb]=np.float('nan')
	return data1

def lg_refl(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                    data[aa,bb,cc]=10*log10(data[aa,bb,cc])
    return data


def lg_refl2(data):
    [aaa,bbb]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            data[aa,bb]=10*log10(data[aa,bb])
    return data

def refl_process(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if data[aa,bb,cc]<=1e-30:
                    data[aa,bb,cc]=1e-30
    return data

def zdr_nan_sum(data):
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
        return np.sum(result)/count

def rhv_nan_sum(data):
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
        return np.sum(result)/count

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

def zdr_nan_data_add(*data):
    n=len(data)
    length=len(data[0])
    total=[]
    for ii in range(length):
        temp=[]
        for iii in range(n):
            temp.append(data[iii][ii])
        total.append(zdr_nan_sum(temp))
    return total

def rhv_nan_data_add(*data):
    n=len(data)
    length=len(data[0])
    total=[]
    for ii in range(length):
        temp=[]
        for iii in range(n):
            temp.append(data[iii][ii])
        total.append(rhv_nan_sum(temp))
    return total

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

def del_nan(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if np.isnan(data[aa,bb,cc]):
                    data[aa,bb,cc]=0
    return data

#-----------------------------------------------------------------------------
#   scan function
#-----------------------------------------------------------------------------

def trans_read_data(data,posi_X,posi_Y,posi_Z,Dx=5000.0,Dy=5000.0):
    [X_max,Y_max,Z_max]=data.shape
    z_level=[   0.0,   56.6,  137.9,  244.7,  377.6,  546.3,  761.1, 1016.2,
             1455.3, 1914.6, 2396.2, 2902.5, 3845.1, 4787.7, 5730.3, 6672.9,
             7615.5, 8558.1, 9500.7,10443.3,11385.9,12328.5,13271.1,14213.7,
            15156.3,16098.9,17041.5,17984.1,18926.7,19869.3]

    i=posi_X/Dx
    j=posi_Y/Dy

    for k in xrange(len(z_level)):
        if k==(len(z_level)-1):
            break
        if posi_Z>=z_level[k] and posi_Z <= z_level[k+1]:
            break
    k_min = k
    k_max = k_min+1

    i_min = int(math.floor(i))
    j_min = int(math.floor(j))

    i_max = i_min+1
    j_max = j_min+1

    if i_max==(X_max):
        i_max=i_max-1
    if j_max==(Y_max):
        j_max=j_max-1
    if k_max==(Z_max):
        k_max=k_max-1

    result=zdr_nan_data_add( [data[i_min,j_min,k_min]] , [data[i_min,j_min,k_max]],
                             [data[i_min,j_max,k_min]] , [data[i_min,j_max,k_max]], \
                             [data[i_max,j_min,k_min]] , [data[i_max,j_min,k_max]], \
                             [data[i_max,j_max,k_min]] , [data[i_max,j_max,k_max]]  )
    return result[0]

#-----------------------------------------------------------------------------
def scan_angle(theta,fai):
   Ra=np.cos(theta) * np.sin(fai)
   Rb=np.cos(theta) * np.cos(fai)
   Rc=np.sin(theta)
   Rd=np.sqrt(Rc**2+Rb**2)
   return np.arcsin(Rc/Rd),np.arctan(Ra/Rd)

#-----------------------------------------------------------------------------
def scanning(data,pitch_angle,off_X=276832,off_Y=0,off_Z=3000):     #degree
    pitch_angle  = 0.0/180.0*pi   #down  negative   up positive

    [size_X,size_Y,size_Z]=data.shape
    C            = 3e8
    sample_T     = 18e-6
    PRF          = 380
    scan_time    = 2
    total_pulse  = PRF*scan_time

    delta_R      = sample_T*C/2.0
    Max_R        = 1.0/PRF*C/2.0
    #theta_width  = 3.0/180.0*pi
    #fai_width    = 3.0/180.0*pi

    delta_theta  = 90.0/total_pulse / 180.0 * pi
    total_angle  = int(90.0/delta_theta / 180.0 * pi)

    #--------------------------------------------------------------------------
    # relative coordinate
    #--------------------------------------------------------------------------
    X            = np.zeros([total_angle,int(Max_R/delta_R)])
    Y            = np.zeros([total_angle,int(Max_R/delta_R)])
    Z            = np.zeros([total_angle,int(Max_R/delta_R)])
    all_theta=np.linspace(-45,45,total_angle)/180.0*pi
    for i in xrange(len(all_theta)):
        for r in xrange(int(Max_R/delta_R)):
            d_theta,d_fai=scan_angle(all_theta[i],pitch_angle)
            X[i,r]=delta_R * r * np.cos(d_fai) * np.sin(d_theta)
            Y[i,r]=delta_R * r * np.cos(d_fai) * np.cos(d_theta)
            Z[i,r]=delta_R * r * np.sin(d_fai)

    X=X+off_X
    Y=Y+off_Y
    Z=Z+off_Z

    [aaa,bbb]=X.shape
    scan     = np.zeros([aaa,bbb])

    for aa in xrange(aaa):
            for bb in xrange(bbb):
                scan[aa,bb]=trans_read_data(data,X[aa,bb],Y[aa,bb],Z[aa,bb],Dx=5000.0,Dy=5000.0)


    return X,Y,Z,scan
#------------------------------------------------------------------------------

def t_data_plot(data,dataname,title_name,num_contours,zdr_flag=0,data_min=1.01):
    #camera1=(0.0,0.0,307.7645695540192,np.array([ 79.66195959, 74.22460988,9.96509266]))
    #camera2=(45.00000000000005,54.735610317245346,389.61669188814807,np.array([61.00005691,87.63795239,6.8619907]))
    camera3=(45.0,54.735610317245346,607.35769190957262,np.array([89.80421373,137.88978957,7.30599671]))

    size_x,size_y,size_z=data.shape
    mlab.figure(dataname,bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))

    if zdr_flag==1:
        fig_data=mlab.contour3d(data[:,:,:],vmin=data_min,colormap='jet')
    else:
        fig_data=mlab.contour3d(data[:,:,:],vmin=-30.0,colormap='jet')
    fig_data.contour.number_of_contours=num_contours
    fig_data.actor.property.opacity=0.4
    mlab.title(dataname)
    mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
    colorbar=mlab.colorbar(title=title_name,orientation='vertical',nb_labels=10)
    colorbar.scalar_bar_representation.position=[0.85,0.1]
    colorbar.scalar_bar_representation.position2=[0.12,0.9]
    mlab.view(*camera3)
    mlab.show()

def min_process2(data):
    [aaa,bbb]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            if data[aa,bb]<=0:
                    data[aa,bb]=0
    return data
