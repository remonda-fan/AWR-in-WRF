# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#   底层函数库
#------------------------------------------------------------------------------
#----------------------------------------------------------------
#   导入扩展包
#----------------------------------------------------------------
import numpy as np
import math
from math import pi,gamma,log10
from pytmatrix.psd import UnnormalizedGammaPSD
from pytmatrix import radar
from mayavi import mlab

#----------------------------------------------------------------
#   改变数据形状，python读取后坐标为(z,y,x),修改后为（x,y,z）
#   变成容易理解的思维方式
#   cgsp=change shape
#----------------------------------------------------------------
def cgsp(data):
        [aaa,bbb,ccc]=data.shape
        temp=np.zeros([bbb,ccc,aaa])
        for aa in xrange(aaa):
            for bb in xrange(bbb):
                for cc in xrange(ccc):
                    temp[bbb-bb-1,cc,aa]=data[aa,bb,cc]
        return temp

#----------------------------------------------------------------
#   雨滴轴比函数
#----------------------------------------------------------------
def drop_ar(D_eq):
    if D_eq <0.7:
        return 1.0;
    elif D_eq <1.5:
        return 1.173-0.5165*D_eq +0.4698*D_eq**2-0.1317*D_eq**3-\
            8.5e-3*D_eq**4
    else:
        return 1.065-6.25e-2*D_eq -3.99e-3*D_eq**2+7.66e-4*D_eq**3-\
            4.095e-5*D_eq**4

#----------------------------------------------------------------
#   去除bug点，wrf出来的数据小于0的会产生负值，估计是浮点运算产生
#   处理方式就是最小值全部1e-10。不允许出现0点，考虑到后面0放在分母上运算会出现nan
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   pytmatrix整合好的初始化设置函数，接收混合比，浓度，u，密度，以及不同类型选择choice
#   六种粒子实际上只有3中密度，
#   choice=1 rain 密度1000
#   choice=2 hail 密度913
#   choice=3 snow 密度100或者200都行  单位是kg/m**3
#   函数中改变的变量均为全局变量，然后返回论文中计算好的 非归一化的N0和lambda，由后续计算
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   粒子数浓度中出现小于1的数字 还有负值，考虑到这个数据在分母，所以太小了会造成极大值点
#   最小值按照1处理先看看效果，结果还不错，就保留了
#----------------------------------------------------------------
def num_process(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if data[aa,bb,cc]<=1:
                    data[aa,bb,cc]=1
        print '\r|'+'='*(50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)) \
        +' '*(50-50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc))+'|'\
        +'%1.2f%%' %(100*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)),
    print ' '
    return data

#----------------------------------------------------------------
#   利用t矩阵计算pytmatrix的4个变量
#   接收前面计算好的n0 lamda u scatterer是个对象 没办法打包在函数里面 所以单独在函数外计算
#   计算完成后直接一次性返回
#   zh zdr zv ldr rhv
#   虽然名字叫rain_xxx,但是后续计算就和rain没有关系了，作为函数变量名不影响全局，懒得改
#----------------------------------------------------------------
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
            print '\r|'+'='*(50*i/length)+' '*(50-50*i/length)+'|'+'%1.2f%%' %(100.0*i/length),
    print ' '

    rain_zh = np.array(rain_zh)
    rain_zdr  = np.array(rain_zdr)
    rain_zv   = np.array(rain_zv)
    rain_ldr  = np.array(rain_ldr)
    rain_rhv  = np.array(rain_rhv)

    return rain_zh,rain_zdr,rain_zv,rain_ldr,rain_rhv

#----------------------------------------------------------------
#   利用t矩阵计算pytmatrix的2个变量
#   接收前面计算好的n0 lamda u scatterer是个对象 没办法打包在函数里面 所以单独在函数外计算
#   计算完成后直接一次性返回
#   kdp ai
#   虽然名字叫rain_xxx,但是后续计算就和rain没有关系了，作为函数变量名不影响全局，懒得改
#----------------------------------------------------------------
#   特别说明：为什么不把6个变量放在一起计算，而是分成两个函数？
#   因为这两个变量计算时候需要修改散射规范，所以在主程序里改一下就行
#----------------------------------------------------------------
def cal_tm2(n0,lamda,u,scatterer):
    rain_kdp=[]
    rain_ai=[]
    length=len(n0)
    for i in range(length):
        scatterer.psd=UnnormalizedGammaPSD(N0=n0[i],Lambda=lamda[i],mu=u)
        rain_kdp.append(radar.Kdp(scatterer))
        rain_ai.append(radar.Ai(scatterer))
        if i%1000==0:
            print '\r|'+'='*(50*i/length)+' '*(50-50*i/length)+'|'+'%1.2f%%' %(100.0*i/length),
    print ' '
    rain_kdp=np.array(rain_kdp)
    rain_ai =np.array(rain_ai)

    return rain_kdp,rain_ai

#----------------------------------------------------------------
#   这里是小论文画图效果不太好，做点小动作哈哈哈，按照另一个数据的形态把一个数据中的值改为nan
#   不过大论文没用，本身效果不错，小论文不行，影响不大
#----------------------------------------------------------------
def compare2(data1,data2,threshold=1.0):
    [aaa,bbb]=data1.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
	    if data2[aa,bb]<=threshold:
		data1[aa,bb]=np.float('nan')
    return data1

#----------------------------------------------------------------
#   一次性取对数 output=10*lg10(input),不像matlab可以一次性对矩阵做运算
#   所以做个函数
#
#   这个接收三维数组
#----------------------------------------------------------------
def lg_refl(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                    data[aa,bb,cc]=10*log10(data[aa,bb,cc])
        print '\r|'+'='*(50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)) \
        +' '*(50-50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc))+'|'\
        +'%1.2f%%' %(100*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)),
    print ' '
    return data

#----------------------------------------------------------------
#   一次性取对数 output=10*lg10(input),不像matlab可以一次性对矩阵做运算
#   所以做个函数

#   这个接收二维数组
#----------------------------------------------------------------
#   其实可以写一个的 用其他方法，这里懒得改了
#----------------------------------------------------------------
def lg_refl2(data):
    [aaa,bbb]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            data[aa,bb]=10*log10(data[aa,bb])
        print '\r|'+'='*(50*(bb+aa*bbb)/(aaa*bbb)) \
        +' '*(50-50*(bb+aa*bbb)/(aaa*bbb))+'|'\
        +'%1.2f%%' %(100*(bb+aa*bbb)/(aaa*bbb)),
    print ' '
    return data

#----------------------------------------------------------------
#   画图用，最小值做成1e-30，然后做对数运算，毕竟是仿真，数据出来有-70dB但是不合理啊
#   所以卡死在-30dB，也可以改其他值
#----------------------------------------------------------------
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
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#   以下部分小论文用于雷达扫描，代码比较纠结，我看着都觉得烦，主要作用就是一些
#   坐标变换等等，但是现在回想起来做了很多多余的工作，如果我在改写完全可以删除
#   老师不想看完全可以跳过，徒增学习成本，浪费时间
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

#----------------------------------------------------------------
#   zdr叠加，小论文用，zdr的数据累加求和，给后面用的
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   rhv叠加 小论文用 跟上一个函数一个意思，给后面用的
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   kdp叠加 小论文用 跟上一个函数一个意思，给后面用的
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   调用之前zdr叠加的，之前那个是计算而已，这个是处理是否有nan，有就自动删除，给后面用的
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   调用之前rhv叠加的，之前那个是计算而已，这个是处理是否有nan，有就自动删除，给后面用的
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   调用之前kdp叠加的，之前那个是计算而已，这个是处理是否有nan，有就自动删除，给后面用的
#----------------------------------------------------------------
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

#----------------------------------------------------------------
#   处理nan点，如果有，改成0  虽然没有数据就是没有数据，不过我想试试0看看效果
#   影响不大，效果还可以
#----------------------------------------------------------------
def del_nan(data):
    [aaa,bbb,ccc]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            for cc in xrange(ccc):
                if np.isnan(data[aa,bb,cc]):
                    data[aa,bb,cc]=0
        print '\r|'+'='*(50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)) \
        +' '*(50-50*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc))+'|'\
        +'%1.2f%%' %(100*(cc+bb*ccc+aa*bbb*ccc)/(aaa*bbb*ccc)),
    print ' '
    return data

#-----------------------------------------------------------------------------
#   scan function
#   小论文用，扫描部分
#-----------------------------------------------------------------------------
#   前面一堆函数就是在这里用的
#   调用前面写的函数进行复杂计算，作用就是 根据当前坐标返回数据，返回方法是
#   根据当前坐标做一个矩形，矩形的8个顶点就是周围最近的数据，取数据平均 然后输出
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
#   根据雷达设置的俯仰角，方位角 返回一个？？？
#   我实在是忘了，但是这个是给后面用的是个小函数
#   当时大半夜在草稿纸上推导的，然后变量算好随手开始编程。。第二天起来桌子上一堆纸
#
#   但是这里工作在干嘛我还是要说下
#   很多学生在写扫描的时候直接用球心坐标系(R,theta,fai)然后就循环了，根本没有想过一个
#   至关重要的问题，球心坐标系 如果下视角0度，扫描出来是一个平面
#   如果下视角是带度数的，扫描出来是个曲面
#   想象下：地球的中心点和赤道上一个点 连线  转圈 画出来是个圈 还是个面
#   如果是北纬30度，连线中心点绕圈，画出来是个圆锥，根本不是一个平面
#   而真实的雷达由于机械结构扫描出来是个平面
#
#   所以这里就是在做这样的计算，保证扫描结果是个平面，把球心坐标系换算到雷达扫描
#   那种电扇摇头的方式，保证是个平面数据
#   这个函数应该是做什么角度计算工作 供后面的scanning使用
#   不过也是小论文用，自己瞎折腾，扣的太细浪费时间
#-----------------------------------------------------------------------------
def scan_angle(theta,fai):
   Ra=np.cos(theta) * np.sin(fai)
   Rb=np.cos(theta) * np.cos(fai)
   Rc=np.sin(theta)
   Rd=np.sqrt(Rc**2+Rb**2)
   return np.arcsin(Rc/Rd),np.arctan(Ra/Rd)

#-----------------------------------------------------------------------------
#  不用考虑那么多了，我自己都忘了，反正就是 接收矩形数据 data，下视角pitch_angle
#   offset_X Y Z就是设置个偏移量，然后雷达开始扫描
#   返回数值为数据的XYZ坐标，这个坐标一定是在一个平面上的，scan是数据结果
#   其中包括了nan值处理，边界处理等乱七八糟小问题一次性解决，唯一的问题就是 扫描的方向。。
#
#   这里提供解决方法：
#   因为方向固定的，所以可以转矩阵啊！把data左右翻转？ 旋转90度等等 python的numpy有这个功能
#   等方向对了 重新画图在旋转回来就行
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
#   画图部分，一次性画图 用mayavi，我写成一个函数了，实际上后来觉得还是不要写函数好
#   调试方便，函数运行太麻烦，里面的设置参数唯一要说明的就是camera 就是设置观察镜头的位置
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

#------------------------------------------------------------------------------
#   数据处理
#   将负数变为0
##------------------------------------------------------------------------------
def min_process2(data):
    [aaa,bbb]=data.shape
    for aa in xrange(aaa):
        for bb in xrange(bbb):
            if data[aa,bb]<=0:
                    data[aa,bb]=0
        print '\r|'+'='*(50*(bb+aa*bbb)/(aaa*bbb)) \
        +' '*(50-50*(bb+aa*bbb)/(aaa*bbb))+'|'\
        +'%1.2f%%' %(100*(bb+aa*bbb)/(aaa*bbb)),
    print ' '
    return data
