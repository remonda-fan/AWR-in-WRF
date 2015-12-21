import os
import numpy as np
from netCDF4 import Dataset
from mayavi import mlab
import sys

main_dir=os.getcwd()
os.chdir(main_dir+'\input')
    
def cgsp(data):
        [aaa,bbb,ccc]=data.shape
        temp=np.zeros([bbb,ccc,aaa])
        for aa in xrange(aaa):
            for bb in xrange(bbb):
                for cc in xrange(ccc):
                    temp[bbb-bb-1,cc,aa]=data[aa,bb,cc]
        return temp

print 'reading data...',
wrfout=Dataset('wrfout_d01_2015-06-17_150000')

QRAIN=wrfout.variables['QRAIN']
QRAIN=QRAIN[0,:,:,:]
#QRAIN=QRAIN[0,0:1,:,:]

QNRAIN=wrfout.variables['QNRAIN']
QNRAIN=QNRAIN[0,:,:,:]
#QNRAIN=QNRAIN[0,0:1,:,:]

QHAIL=wrfout.variables['QHAIL']
QHAIL=QHAIL[0,:,:,:]
#QHAIL=QHAIL[0,0:1,:,:]

QNHAIL=wrfout.variables['QNHAIL']
QNHAIL=QNHAIL[0,:,:,:]
#QNHAIL=QNHAIL[0,0:1,:,:]

QSNOW=wrfout.variables['QSNOW']
QSNOW=QSNOW[0,:,:,:]
#QSNOW=QSNOW[0,0:1,:,:]

QNSNOW=wrfout.variables['QNSNOW']
QNSNOW=QNSNOW[0,:,:,:]
#QNSNOW=QNSNOW[0,0:1,:,:]

REFL_10CM=wrfout.variables['REFL_10CM']
REFL_10CM=REFL_10CM[0,:,:,:]
#REFL_10CM=REFL_10CM[0,0:1,:,:]

RHO=wrfout.variables['RHO']
RHO=RHO[0,:,:,:]
#RHO=RHO[0,0:1,:,:]

P=wrfout.variables['P']
P=P[0,:,:,:]
#P=P[0,0:1,:,:]

PB=wrfout.variables['PB']
PB=PB[0,:,:,:]
#PB=PB[0,0:1,:,:]
Pa=P+PB

T=wrfout.variables['T']
T=T[0,:,:,:]
#T=T[0,0:1,:,:]
TK=T+300
print 'finished'

Tem=1.0*TK*(Pa/100000)**(2/7)
print 'changing shape...',
				
QRAIN=cgsp(QRAIN)
QNRAIN=cgsp(QNRAIN)

QHAIL=cgsp(QHAIL)
QNHAIL=cgsp(QNHAIL)

QSNOW=cgsp(QSNOW)
QNSNOW=cgsp(QNSNOW)

RHO=cgsp(RHO)
REFL_10CM=cgsp(REFL_10CM)
Pa=cgsp(Pa)
Tem=cgsp(Tem)
print 'finished'
print 'saving data...',

np.save('QRAIN.npy',QRAIN)
np.save('QNRAIN.npy',QNRAIN)

np.save('QHAIL.npy',QHAIL)
np.save('QNHAIL.npy',QNHAIL)

np.save('QSNOW.npy',QSNOW)
np.save('QNSNOW.npy',QNSNOW)

np.save('RHO.npy',RHO)
np.save('REFL_10CM',REFL_10CM)
np.save('Pa.npy',Pa)
np.save('Tem.npy',Tem)
print 'finished'

Q=QRAIN=QSNOW+QHAIL
Q=Q*1000.0
camera=(0.0, 0.0, 254.57964239946824, np.array([ 41. ,  49.5,  14.5]))
camera2=(45.00000000000005,54.735610317245346,389.61669188814807,
np.array([61.00005691,87.63795239,6.8619907]))
camera3=(45.0,54.735610317245346,241.16461125231757,np.array([40.5,49.89198494,11.79772854]))
'''
mlab.figure('Qr')
mlab.view(*camera)
Qr=mlab.contour3d(QRAIN)
Qr.contour.number_of_contours=20
Qr.actor.property.opacity=0.4
mlab.outline()
mlab.axes()
'''
QRAIN=QRAIN*1000
size_x,size_y,size_z=QRAIN.shape
mlab.figure('QRAIN',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
fig_Qr=mlab.contour3d(Q,vmin=0,colormap='jet')
fig_Qr.contour.number_of_contours=40
fig_Qr.actor.property.opacity=0.3
#Q.contour.minimum_contour=0
mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
#mlab.axes(color=(0,0,0))
colorbar=mlab.colorbar(title='g/kg',orientation='vertical',nb_labels=10)
colorbar.scalar_bar_representation.position=[0.85,0.1]
colorbar.scalar_bar_representation.position2=[0.12,0.9]
mlab.view(*camera)
mlab.savefig('Q.png', size=(800,800))
mlab.show()
from math import pi,gamma,log10

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

QNRAIN = lg_refl(data_process(QNRAIN))
size_x,size_y,size_z=QNRAIN.shape
mlab.figure('QN',bgcolor=(1,1,1),fgcolor=(0,0,0),size=(700,600))
fig_Qr=mlab.contour3d(QNRAIN,vmin=0,colormap='jet')
fig_Qr.contour.number_of_contours=40
fig_Qr.actor.property.opacity=0.3
#Q.contour.minimum_contour=0
mlab.outline(color=(0,0,0),extent=[0,size_x,0,size_y,0,size_z])
#mlab.axes(color=(0,0,0))
colorbar=mlab.colorbar(title='1/m^3',orientation='vertical',nb_labels=10)
colorbar.scalar_bar_representation.position=[0.85,0.1]
colorbar.scalar_bar_representation.position2=[0.12,0.9]
mlab.view(*camera)

mlab.savefig('Qn.png', size=(800,800))
#mlab.show()
'''
mlab.figure('Qh')
mlab.view(*camera)
Qh=mlab.contour3d(QHAIL)
Qh.contour.number_of_contours=20
Qh.actor.property.opacity=0.4
mlab.outline()
mlab.axes()

mlab.figure('Qs')
mlab.view(*camera)
Qs=mlab.contour3d(QSNOW)
Qs.contour.number_of_contours=20
Qs.actor.property.opacity=0.4
mlab.outline()
mlab.axes()
'''
'''
mlab.figure('Q',bgcolor=(1,1,1),fgcolor=(0,0,0))
mlab.view(*camera2)
fig_Q=mlab.contour3d(Q,vmin=0,colormap='jet')
fig_Q.contour.number_of_contours=20
fig_Q.actor.property.opacity=0.4
#Q.contour.minimum_contour=0
mlab.outline(color=(0,0,0))
#mlab.axes(color=(0,0,0))
colorbar=mlab.colorbar(title='g/kg',orientation='vertical',nb_labels=10)
'''

'''
mlab.figure('refl_10cm')
refl=mlab.contour3d(REFL_10CM[1:-1,1:-1,1:-1])
refl.contour.number_of_contours=20
refl.actor.property.opacity=0.3
mlab.outline()
mlab.axes()
mlab.colorbar(orientation='vertical',nb_labels=10)
'''




'''
os.chdir(main_dir+'\output')

rain_ai=	np.load('rain_ai.npy')
rain_kdp=	np.load('rain_kdp.npy')
rain_ldr=	np.load('rain_ldr.npy')
rain_zdr=	np.load('rain_zdr.npy')
rain_zi=	np.load('rain_zi.npy')

rain_zi=cgsp(rain_zi)
rain_kdp=cgsp(rain_kdp)
rain_ldr=cgsp(rain_ldr)
rain_zdr=cgsp(rain_zdr)


mlab.figure('zi',bgcolor=(1,1,1),fgcolor=(0,0,0))
mlab.view(*camera)
fig_zi=mlab.contour3d(rain_zi,vmin=0,colormap='jet')
fig_zi.contour.number_of_contours=20
fig_zi.actor.property.opacity=0.4
#Q.contour.minimum_contour=0
mlab.outline(color=(0,0,0))
#mlab.axes(color=(0,0,0))
colorbar=mlab.colorbar(title='dBZ',orientation='vertical',nb_labels=10)

mlab.figure('zdr',bgcolor=(1,1,1),fgcolor=(0,0,0))
mlab.view(*camera)
fig_zdr=mlab.contour3d(rain_zi,vmin=0,colormap='jet')
fig_zdr.contour.number_of_contours=20
fig_zdr.actor.property.opacity=0.4
#Q.contour.minimum_contour=0
mlab.outline(color=(0,0,0))
#mlab.axes(color=(0,0,0))
colorbar=mlab.colorbar(title='dB',orientation='vertical',nb_labels=10)
'''
os.chdir(main_dir)
