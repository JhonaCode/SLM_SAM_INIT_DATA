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
mean_ts10_iop1 = soil_iop1.groupby(soil_iop1['Time'])['TS_10cm'].mean()
mean_ts20_iop1 = soil_iop1.groupby(soil_iop1['Time'])['TS_20cm'].mean()
mean_ts40_iop1 = soil_iop1.groupby(soil_iop1['Time'])['TS_40cm'].mean()

mean_ts10_iop2 = soil_iop1.groupby(soil_iop1['Time'])['TS_10cm'].mean()
mean_ts20_iop2 = soil_iop1.groupby(soil_iop1['Time'])['TS_20cm'].mean()
mean_ts40_iop2 = soil_iop1.groupby(soil_iop1['Time'])['TS_40cm'].mean()

exit()


time1= data_to_reference_vector(soil_iop1['date'],1,1,2025)
time2= data_to_reference_vector(soil_iop1['date'],1,1,2025)


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


plt.plot(time1,soil_iop1['TS_10cm'].values,color='red' ,label='TS_10cm')
plt.plot(time1,soil_iop1['TS_20cm'].values,color='blue',label='TS_20cm')
plt.plot(time1,soil_iop1['TS_40cm'].values,color='navy',label='TS_40cm')

plt.plot(time2,soil_iop2['TS_10cm'].values,color='red' ,label='TS_10cm',marker='p')
plt.plot(time2,soil_iop2['TS_20cm'].values,color='blue',label='TS_20cm',marker='p')
plt.plot(time2,soil_iop2['TS_40cm'].values,color='navy',label='TS_40cm',marker='p')

#soil.plot(x='date',y='TS_10cm',kind='line')
#With legends
ax.legend(frameon=False,title='Depth',loc='upper right')

plt.show()

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


plt.plot(time1,soil_iop1['Flx_S_5cm'].values,label='Heat Flux 5cm')
plt.plot(time2,soil_iop2['Flx_S_5cm'].values,label='Heat Flux 5cm')

ax.legend(frameon=False,title='Depth',loc='upper right')

plt.show()

exit()


file1= open('%s/soil_%s'%(path,label)  ,'w+')
file1.write("Thickness[m]\tSoilt[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
print("Thickness[m]\tSoilt[K]\tWetness[kg/kg]\tSAND[%]\tCLAY[%]\tRelax Function\n")

print(target_depths[1])
print(soil_text[soiltype]["sand"])
print(soil_text[soiltype]["clay"])


for j in range(0,len(target_depths)):

    file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[j]/100.0,soil_T[soiltype][month][j]+273.15,soil_M[soiltype][month][j]/100.0,soil_text[soiltype]["sand"]*100,soil_text[soiltype]["clay"]*100,0))
    print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[j]/100.0,soil_T[soiltype][month][j]+273.15,soil_M[soiltype][month][j]/100.0,soil_text[soiltype]["sand"]*100,soil_text[soiltype]["clay"]*100,0))

file1.close()
