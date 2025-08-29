from  Parameters import * 

import  numpy as np

import  matplotlib.pyplot as plt


fig =   plt.figure()
###New axis
ax  =   plt.axes()

tama=8

xlabel='Hours Local Time'
ylabel=r'Temperature [$^{\circ}$C]'

ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )
ax.grid(axis='x',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

#plt.plot(jun21.time,jun21.tsoil_W[:,0],dashes=[1,0],label='%s [cm]'%(jun21.depth[0].values),color='black')
#plt.plot(jun21.time,jun21.tsoil_W[:,1],dashes=[1,0],label='%s [cm]'%(jun21.depth[1].values),color='blue')
#plt.plot(jun21.time,jun21.tsoil_W[:,2],dashes=[1,0],label='%s [cm]'%(jun21.depth[2].values),color='red')
#plt.plot(jun21.time,jun21.tsoil_W[:,3],dashes=[1,0],label='%s [cm]'%(jun21.depth[3].values),color='green')
#plt.plot(jun21.time,jun21.tsoil_W[:,4],dashes=[1,0],label='%s [cm]'%(jun21.depth[4].values),color='orange')
#plt.plot(jun21.time,jun21.tsoil_W[:,5],dashes=[1,0],label='%s [cm]'%(jun21.depth[5].values),color='magenta')
#
#plt.plot(jun21.time,jun21.tsoil_E[:,0],dashes=[1,1],color='black')
#plt.plot(jun21.time,jun21.tsoil_E[:,1],dashes=[1,1],color='blue')
#plt.plot(jun21.time,jun21.tsoil_E[:,2],dashes=[1,1],color='red')
#plt.plot(jun21.time,jun21.tsoil_E[:,3],dashes=[1,1],color='green')
#plt.plot(jun21.time,jun21.tsoil_E[:,4],dashes=[1,1],color='orange')
#plt.plot(jun21.time,jun21.tsoil_E[:,5],dashes=[1,1],color='magenta')

plt.plot(jun21.time,mean_t[:,0],dashes=[1,0],label='%s [cm]'%(jun21.depth[0].values),color='black')
plt.plot(jun21.time,mean_t[:,1],dashes=[1,0],label='%s [cm]'%(jun21.depth[1].values),color='blue')
plt.plot(jun21.time,mean_t[:,2],dashes=[1,0],label='%s [cm]'%(jun21.depth[2].values),color='red')
plt.plot(jun21.time,mean_t[:,3],dashes=[1,0],label='%s [cm]'%(jun21.depth[3].values),color='green')
plt.plot(jun21.time,mean_t[:,4],dashes=[1,0],label='%s [cm]'%(jun21.depth[4].values),color='orange')
plt.plot(jun21.time,mean_t[:,5],dashes=[1,0],label='%s [cm]'%(jun21.depth[5].values),color='magenta')


plt.xlabel(r'%s'%(xlabel), fontsize=tama)
plt.ylabel(r'%s'%(ylabel), fontsize=tama)

#locatormax = mdates.hourlocator(interval=1)
#locatormin = mdates.minutelocator(interval=30)
#ax.xaxis.set_minor_locator(locatormin)
#ax.xaxis.set_major_locator(locatormax )

#With legends
ax.legend(frameon=False,title='Depth',loc='upper right')


fig =   plt.figure()
###New axis
ax  =   plt.axes()

tama=8

xlabel='Hours Local Time'
ylabel=r'Water Content [$\dfrac{m^3}{m^3}$]'

ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )
ax.grid(axis='x',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

plt.plot(jun21.time,mean_q[:,0],dashes=[1,0],label='%s [cm]'%(jun21.depth[0].values),color='black')
plt.plot(jun21.time,mean_q[:,1],dashes=[1,0],label='%s [cm]'%(jun21.depth[1].values),color='blue')
plt.plot(jun21.time,mean_q[:,2],dashes=[1,0],label='%s [cm]'%(jun21.depth[2].values),color='red')
plt.plot(jun21.time,mean_q[:,3],dashes=[1,0],label='%s [cm]'%(jun21.depth[3].values),color='green')
plt.plot(jun21.time,mean_q[:,4],dashes=[1,0],label='%s [cm]'%(jun21.depth[4].values),color='orange')
plt.plot(jun21.time,mean_q[:,5],dashes=[1,0],label='%s [cm]'%(jun21.depth[5].values),color='magenta')


plt.xlabel(r'%s'%(xlabel), fontsize=tama)
plt.ylabel(r'%s'%(ylabel), fontsize=tama)

#locatormax = mdates.hourlocator(interval=1)
#locatormin = mdates.minutelocator(interval=30)
#ax.xaxis.set_minor_locator(locatormin)
#ax.xaxis.set_major_locator(locatormax )

#With legends
ax.legend(frameon=False,title='Depth',loc='upper right')




plt.show()
