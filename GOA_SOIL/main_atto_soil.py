from  Parameters_atto import df,data_to_reference_vector,soil_text  

import  numpy as np

import xarray as xr

import  matplotlib.pyplot as plt

import matplotlib.dates as mdates

import datetime as dt

from scipy import interpolate

from scipy.interpolate import interp1d


soiltype="soil_atto_plateaus" 
#soiltype="soil_atto_terrances" 

label1='GOA_ATTO_IOP1_%s'%(soiltype)
label2='GOA_ATTO_IOP2_%s'%(soiltype)

path  ='/pesq/dados/bamc/jhonatan.aguirre/DATA/GOA_SOIL'

#####################################################
#####################################################

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

mean_iop1['date'] = dates
mean_iop2['date'] = dates

#To do the mean in the diurnal cycle 

start_date='2025-01-01T06:00'
end_date  ='2025-01-01T18:00'
dini=dt.datetime.strptime(start_date, format_string)
dfin=dt.datetime.strptime(end_date  , format_string)

diurnal1 = (mean_iop1.date > dini) & (mean_iop1.date <= dfin)
diurnal2 = (mean_iop2.date > dini) & (mean_iop2.date <= dfin)

soil_iop1=mean_iop1[diurnal1] 
soil_iop2=mean_iop2[diurnal2]

# Calculate the mean of 'value' for each unique date
datas=['TS_10cm','TS_20cm','TS_40cm','US_10cm','US_20cm','US_30cm','US_40cm','US_60cm','US_100cm','Flx_S_5cm']
soil_pt_iop1 = soil_iop1[datas].mean()
soil_pt_iop2 = soil_iop2[datas].mean()

soil_pt_iop1[datas]

temp=['TS_10cm','TS_20cm','TS_40cm']
temperature_iop1=soil_pt_iop1[temp]
temperature_iop2=soil_pt_iop2[temp]

moist=['US_10cm','US_20cm','US_30cm','US_40cm','US_60cm','US_100cm']
moisture_iop1=soil_pt_iop1[moist]
moisture_iop2=soil_pt_iop2[moist]


depths1=[10,20,40]
depths2=[10,20,30,40,60,100]


soil0  =0
soiltop=60
nlayers=6
# Generate 10 cm intervals (0-100 cm)
target_depths = np.arange(soil0,soiltop,nlayers)#+1


soil_int_T_iop1=interp1d(depths1,  temperature_iop1, kind='linear', fill_value='extrapolate')
soil_int_T_iop2=interp1d(depths1,  temperature_iop2, kind='linear', fill_value='extrapolate')

soil_int_q_iop1=interp1d(depths2,  moisture_iop1, kind='linear', fill_value='extrapolate')
soil_int_q_iop2=interp1d(depths2,  moisture_iop2, kind='linear', fill_value='extrapolate')

#soil_int_T=interp1d(depths,  temperature, kind='slinear', fill_value='extrapolate')
#soil_int_T=interp1d(depths,  temperature, kind='quadratic', fill_value='extrapolate')
#soil_int_T=interp1d(depths,  temperature, kind='cubic', fill_value='extrapolate')
soil_T_iop1=soil_int_T_iop1(target_depths)
soil_T_iop2=soil_int_T_iop2(target_depths)

soil_q_iop1=soil_int_q_iop1(target_depths)
soil_q_iop2=soil_int_q_iop2(target_depths)


thikness=[]

for i in range(0,len(target_depths)-1):

    #print(target_depths[i+1]-target_depths[i])
    thikness.append(target_depths[i+1]-target_depths[i])

#######################################################
#######################################################
#######################################################

file1= open('%s/soil_%s'%(path,label1)  ,'w+')
file2= open('%s/soil_%s'%(path,label2)  ,'w+')
file1.write("Thickness[m]\tSoil[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
file2.write("Thickness[m]\tSoil[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
print("Thickness[m]\tSoilt[K]\tWetness[kg/kg]\tSAND[%]\tCLAY[%]\tRelax Function\n")

#Soil temperature; Depth @ Micromet. INSTANT Tower (WT) at 40 cm	deg C
#Soil moisture; Depth @ Micromet. INSTANT Tower (WT) at 10 cm; Unit: m^3/m^3	m^3/m^3

#print(soil_text[soiltype]["clay"])
#print(soil_pt_iop1['TS_10cm']+273.15)
#print(soil_pt_iop1['US_10cm']/100.0,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"])

#taking from Estimation and mapping of field capacity in Brazilian soils
#https://www.sciencedirect.com/science/article/pii/S0016706120301300?via%3Dihub  
#https://doi.org/10.1016/j.geoderma.2020.114557

Fc=0.38

#for i in range(0,len(thikness)):
for i in range(0,len(target_depths)):

    file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_iop1[i]+273.15,soil_q_iop1[i]/Fc,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
    file2.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_iop2[i]+273.15,soil_q_iop2[i]/Fc,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
    #print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_iop1[i]+273.15,soil_q_iop1[i],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
    #print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_iop2[i]+273.15,soil_q_iop2[i],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))


file1.close()
file2.close()
#######################################################
#######################################################
#######################################################
"""


file1= open('%s/soil_%s'%(path,label1)  ,'w+')
file1.write("Thickness[m]\tSoil[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
print("Thickness[m]\tSoilt[K]\tWetness[kg/kg]\tSAND[%]\tCLAY[%]\tRelax Function\n")

#Soil temperature; Depth @ Micromet. INSTANT Tower (WT) at 40 cm	deg C
#Soil moisture; Depth @ Micromet. INSTANT Tower (WT) at 10 cm; Unit: m^3/m^3	m^3/m^3

#print(soil_text[soiltype]["clay"])
#print(soil_pt_iop1['TS_10cm']+273.15)
#print(soil_pt_iop1['US_10cm']/100.0,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"])

file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[0]/100.0,soil_pt_iop1['TS_10cm']+273.15,soil_pt_iop1['US_10cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[1]/100.0,soil_pt_iop1['TS_20cm']+273.15,soil_pt_iop1['US_20cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[2]/100.0,soil_pt_iop1['TS_40cm']+273.15,soil_pt_iop1['US_40cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[3]/100.0,soil_T_iop1[3]+273.15,soil_pt_iop1['US_60cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[4]/100.0,soil_T_iop1[4]+273.15,soil_pt_iop1['US_100cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))

print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[0]/100.0,soil_pt_iop1['TS_10cm']+273.15,soil_pt_iop1['US_10cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[1]/100.0,soil_pt_iop1['TS_20cm']+273.15,soil_pt_iop1['US_20cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[2]/100.0,soil_pt_iop1['TS_40cm']+273.15,soil_pt_iop1['US_40cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[3]/100.0,soil_T_iop1[3]+273.15,soil_pt_iop1['US_60cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[4]/100.0,soil_T_iop1[4]+273.15,soil_pt_iop1['US_100cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))



file1.close()

file2= open('%s/soil_%s'%(path,label2)  ,'w+')
file2.write("Thickness[m]\tSoilt[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")

print("Thickness[m]\tSoil[K]\tWetness[kg/kg]\tSAND[%]\tCLAY[%]\tRelax Function\n")

file2.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[0]/100.0,soil_pt_iop2['TS_10cm']+273.15,soil_pt_iop2['US_10cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file2.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[1]/100.0,soil_pt_iop2['TS_20cm']+273.15,soil_pt_iop2['US_20cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file2.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[2]/100.0,soil_pt_iop2['TS_40cm']+273.15,soil_pt_iop2['US_40cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file2.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[3]/100.0,soil_T_iop2[3]+273.15,soil_pt_iop2['US_60cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
file2.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[4]/100.0,soil_T_iop2[4]+273.15,soil_pt_iop2['US_100cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))

print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[0]/100.0,soil_pt_iop2['TS_10cm']+273.15,soil_pt_iop2['US_10cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[1]/100.0,soil_pt_iop2['TS_20cm']+273.15,soil_pt_iop2['US_20cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[2]/100.0,soil_pt_iop2['TS_40cm']+273.15,soil_pt_iop2['US_40cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[3]/100.0,soil_T_iop2[3]+273.15,soil_pt_iop2['US_60cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[4]/100.0,soil_T_iop2[4]+273.15,soil_pt_iop2['US_100cm'],soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))


file2.close()
"""
