from  Parameters_atto import df,data_to_reference_vector,soil_text  
import data_own as down

import  numpy as np

import xarray as xr

import  matplotlib.pyplot as plt

import matplotlib.dates as mdates

import datetime as dt

from scipy import interpolate

from scipy.interpolate import interp1d

import  days  as dy 

import pandas as pd


soiltype="soil_plateaus" 
#soiltype="soil_terrances" 

label1='shca_%s'%(soiltype)
label2='iop1_%s'%(soiltype)
label3='iop2_%s'%(soiltype)

#path  ='/pesq/dados/bamc/jhonatan.aguirre/DATA/SLM_SAM_INIT_DATA/GOA_SOIL'
path  ='/dados/bamc/jhonatan.aguirre/DATA/SLM_SAM_INIT_DATA/GOA_SOIL'

#####################################################
#####################################################


mask = pd.Series(False, index=df.index)
for start, end in dy.days:
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    mask |= (df["date"] >= start) & (df["date"] <= end)

selected = df.loc[mask]
noselected  = df#.loc[~mask]


#iop1
start_date='2014-02-15T00'
end_date  ='2014-03-25T00'
dini=dt.datetime.strptime(start_date, dy.date_format)
dfin=dt.datetime.strptime(end_date  , dy.date_format)

#iop2
#greater than the start date and smaller than the end date
iop1 = (noselected.date > dini) & (noselected.date <= dfin)

start_date='2014-09-01T00'
end_date  ='2014-10-10T00'
dini=dt.datetime.strptime(start_date, dy.date_format)
dfin=dt.datetime.strptime(end_date  , dy.date_format)

iop2 = (noselected.date > dini) & (noselected.date <= dfin)

soil_iop1=noselected[iop1] 
soil_iop2=noselected[iop2]


# Calculate the mean of 'value' for each unique date
dates=['TS_10cm','TS_20cm','TS_40cm','US_10cm','US_20cm','US_30cm','US_40cm','US_60cm','US_100cm','Flx_S_5cm','Time',]

shca_sh = selected.groupby(selected['Time'],as_index=False)[dates]
iop1    = selected.groupby(soil_iop1['Time'],as_index=False)[dates]
iop2    = selected.groupby(soil_iop2['Time'],as_index=False)[dates]

mean_sh   = shca_sh.mean()
mean_iop1 =    iop1.mean()
mean_iop2 =    iop2.mean()

mean_sh  =down.hour_set(mean_sh)
mean_iop1=down.hour_set(mean_iop1)
mean_iop2=down.hour_set(mean_iop2)



#To do the mean in the diurnal cycle 
start_date='2025-01-01T%s'%(dy.hi)
end_date  ='2025-01-01T%s'%(dy.hf)
dini=dt.datetime.strptime(start_date, dy.date_format)
dfin=dt.datetime.strptime(end_date  , dy.date_format)

diurnal_shca = (mean_sh.date   > dini) & (mean_sh.date <= dfin)
diurnal_iop1 = (mean_iop1.date > dini) & (mean_iop1.date <= dfin)
diurnal_iop2 = (mean_iop2.date > dini) & (mean_iop2.date <= dfin)

soil_shca=mean_sh[diurnal_shca] 
soil_iop1=mean_iop1[diurnal_iop1] 
soil_iop2=mean_iop2[diurnal_iop2] 

# Calculate the mean of 'value' for each unique date
datas=['TS_10cm','TS_20cm','TS_40cm','US_10cm','US_20cm','US_30cm','US_40cm','US_60cm','US_100cm','Flx_S_5cm']
soil_pt_shca = soil_shca[datas].mean()
soil_pt_iop1 = soil_iop1[datas].mean()
soil_pt_iop2 = soil_iop2[datas].mean()


temp=['TS_10cm','TS_20cm','TS_40cm']
temperature_shca=soil_pt_shca[temp]
temperature_iop1=soil_pt_iop1[temp]
temperature_iop2=soil_pt_iop2[temp]

moist=['US_10cm','US_20cm','US_30cm','US_40cm','US_60cm','US_100cm']
moisture_shca=soil_pt_shca[moist]
moisture_iop1=soil_pt_iop1[moist]
moisture_iop2=soil_pt_iop2[moist]


depths1=[10,20,40]
depths2=[10,20,30,40,60,100]


soil0  =0
soiltop=70
nlayers=10
# Generate 10 cm intervals (0-100 cm)
target_depths = np.arange(soil0,soiltop,nlayers)#+1


soil_int_T_shca=interp1d(depths1,  temperature_shca, kind='linear', fill_value='extrapolate')
soil_int_q_shca=interp1d(depths2,     moisture_shca, kind='linear', fill_value='extrapolate')
soil_int_T_iop1=interp1d(depths1,  temperature_iop1, kind='linear', fill_value='extrapolate')
soil_int_q_iop1=interp1d(depths2,     moisture_iop1, kind='linear', fill_value='extrapolate')
soil_int_T_iop2=interp1d(depths1,  temperature_iop2, kind='linear', fill_value='extrapolate')
soil_int_q_iop2=interp1d(depths2,     moisture_iop2, kind='linear', fill_value='extrapolate')

soil_T_shca=soil_int_T_shca(target_depths)
soil_q_shca=soil_int_q_shca(target_depths)
soil_T_iop1=soil_int_T_iop1(target_depths)
soil_q_iop1=soil_int_q_iop1(target_depths)
soil_T_iop2=soil_int_T_iop2(target_depths)
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
file3= open('%s/soil_%s'%(path,label3)  ,'w+')
file1.write("Thickness[m]\tSoil[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
file2.write("Thickness[m]\tSoil[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
file3.write("Thickness[m]\tSoil[K]\tWetness[kg/kg]\tSand[%]\tClay[%]\tRelax Function\n")
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

    file1.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_shca[i]+273.15,soil_q_shca[i]/Fc,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
    print("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_shca[i]+273.15,soil_q_shca[i]/Fc,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
    file2.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_iop1[i]+273.15,soil_q_iop1[i]/Fc,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))
    file3.write("%f\t%f\t%f\t%f\t%f\t%f\n"%(target_depths[i]/100.0,soil_T_iop2[i]+273.15,soil_q_iop2[i]/Fc,soil_text[soiltype]["sand"],soil_text[soiltype]["clay"],0.0))


file1.close()

