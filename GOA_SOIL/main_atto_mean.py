from  Parameters_atto import df,data_to_reference_vector 

import  numpy as np

import xarray as xr

import  matplotlib.pyplot as plt

import matplotlib.dates as mdates

import datetime as dt

format_string = "%Y-%m-%dT%H:%M"

start_date='2014-09-01T00:00'
end_date  ='2014-10-10T00:00'
dini=dt.datetime.strptime(start_date, format_string)
dfin=dt.datetime.strptime(end_date  , format_string)

#greater than the start date and smaller than the end date
iop1 = (df.date > dini) & (df.date <= dfin)

start_date='2014-02-15T00:00'
end_date  ='2014-03-25T00:00'
dini=dt.datetime.strptime(start_date, format_string)
dfin=dt.datetime.strptime(end_date  , format_string)

iop2 = (df.date > dini) & (df.date <= dfin)

soil_iop1=df[iop1] 
soil_iop2=df[iop2]

#ts_10 = df['TS_10cm'].mean()
#print(ts_10)

# Calculate the mean of 'value' for each unique date
dates=['TS_10cm','TS_20cm','TS_40cm','US_10cm','US_20cm','US_30cm','US_40cm','US_60cm','US_100cm','Flx_S_5cm']
mean_iop1 = soil_iop1.groupby(soil_iop1['Time'],as_index=False)[dates].mean()
mean_iop2 = soil_iop2.groupby(soil_iop2['Time'],as_index=False)[dates].mean()


dates=[]
utc=dt.timedelta(hours=4)
for hour in mean_iop1['Time'].values:

    #print(hour%100.0)
    if hour%100.0>0:
        #date_object = np.datetime64(datetime.strptime(time,format_string)) + np.timedelta64(hour,'h')
        h=hour/100+0.2
        date_object = dt.datetime(2025,1,1) + dt.timedelta(hours=h)-utc
    else:
        h=hour/100.0
        #print(h)
        date_object = dt.datetime(2025,1,1) + dt.timedelta(hours=h)-utc

    dates.append(date_object)


fig =   plt.figure()
###New axis
ax  =   plt.axes()

tama=8

xlabel='Hours Local Time'
ylabel=r'Temperature [$^{\circ}$C]'

ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )
ax.grid(axis='x',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

#locatormax = mdates.HourLocator(interval=1)
#locatormin = mdates.MinuteLocator(interval=30)
#ax.xaxis.set_minor_locator(locatormin)
#ax.xaxis.set_major_locator(locatormax )

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)


plt.plot(dates,mean_iop1['TS_10cm'].values,color='red'  ,label='10')
plt.plot(dates,mean_iop1['TS_20cm'].values,color='green',label='20')
plt.plot(dates,mean_iop1['TS_40cm'].values,color='navy' ,label='40')

plt.plot(dates,mean_iop2['TS_10cm'].values,color='red'  ,label='',marker='p')
plt.plot(dates,mean_iop2['TS_20cm'].values,color='green',label='',marker='p')
plt.plot(dates,mean_iop2['TS_40cm'].values,color='navy' ,label='',marker='p')

#soil.plot(x='date',y='TS_10cm',kind='line')
#With legends
ax.legend(frameon=False,title='Depth [cm]',loc='upper right')

plt.xlabel(r'%s'%(xlabel), fontsize=tama)
plt.ylabel(r'%s'%(ylabel), fontsize=tama)

fig =   plt.figure()
###New axis
ax  =   plt.axes()

tama=8

xlabel='Hours Local Time'
ylabel=r'Soil Moisture[m$^{3}$/m$^{3}$]'

ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )
ax.grid(axis='x',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

#locatormax = mdates.HourLocator(interval=1)
#locatormin = mdates.MinuteLocator(interval=30)
#ax.xaxis.set_minor_locator(locatormin)
#ax.xaxis.set_major_locator(locatormax )

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)


plt.plot(dates,mean_iop1['US_10cm'].values,color='red'     ,label='10' )
plt.plot(dates,mean_iop1['US_20cm'].values,color='green'   ,label='20' )
plt.plot(dates,mean_iop1['US_30cm'].values,color='blue'    ,label='30' )
plt.plot(dates,mean_iop1['US_40cm'].values,color='magenta',label='40' )
plt.plot(dates,mean_iop1['US_60cm'].values,color='orange' ,label='60' )
plt.plot(dates,mean_iop1['US_100cm'].values,color='cyan'  ,label='100')

plt.plot(dates,mean_iop2['US_10cm'].values,color='red'    ,label='' ,marker='p')
plt.plot(dates,mean_iop2['US_20cm'].values,color='green'  ,label='' ,marker='p')
plt.plot(dates,mean_iop2['US_30cm'].values,color='blue'   ,label='' ,marker='p')
plt.plot(dates,mean_iop2['US_40cm'].values,color='magenta',label='' ,marker='p')
plt.plot(dates,mean_iop2['US_60cm'].values,color='orange' ,label='' ,marker='p')
plt.plot(dates,mean_iop2['US_100cm'].values,color='cyan'  ,label='' ,marker='p')

#soil.plot(x='date',y='TS_10cm',kind='line')
#With legends
ax.legend(frameon=False,title='Depth [cm]',loc='upper right')

plt.xlabel(r'%s'%(xlabel), fontsize=tama)
plt.ylabel(r'%s'%(ylabel), fontsize=tama)


fig =   plt.figure()
###New axis
ax  =   plt.axes()

tama=8

xlabel='Hours Local Time'
ylabel=r'Soil Heat flux at 5 cm [Wm$^2$]'

ax.grid(axis='y',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )
ax.grid(axis='x',linewidth=1.0,alpha=0.5,dashes=[1,1,0,0] )

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)


plt.plot(dates,mean_iop1['Flx_S_5cm'].values,label='iop2')
plt.plot(dates,mean_iop2['Flx_S_5cm'].values,label='iop2')

ax.legend(frameon=False,title='Depth',loc='upper right')

plt.xlabel(r'%s'%(xlabel), fontsize=tama)
plt.ylabel(r'%s'%(ylabel), fontsize=tama)

plt.show()
