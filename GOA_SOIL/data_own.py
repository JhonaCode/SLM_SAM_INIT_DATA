# python library to work with netcdf4 
#from    netcdf4         import dataset

# to save the time coordinate in specific format 
from    netCDF4         import num2date, date2num

# Python standard library datetime  module
import datetime as dt  

import xarray as xr

# To save the time coordinate in specific format 
from    cftime import num2date, num2pydate

import pandas as pd 

def data_load_xr(path,name,calendar):

    exp            =  xr.open_dataset(path, engine='netcdf4')
    exp['name']    =  name

    exp['BR']   =  exp['SHF']/exp['LHF']

    exp['netsf']   =  exp['SWNS']-exp['LWNS']
    exp['netsf_dw']=  exp['SWDS']-exp['LWDS']

    exp['ltime']   =  num2pydate(exp.time[:],units=calendar[0],calendar=calendar[1])

    #date_format = '%Y%m%d%H'
    ##to add the minutes to the original date
    #dis=date[0]#+'00'
    #dfs=date[1]#+'00'
    #di=dt.datetime.strptime(dis, date_format)
    #df=dt.datetime.strptime(dfs, date_format)

    ##initial hour
    #hi=di.hour
    ##final hour
    #hf=df.hour
    time=exp.time.values

    exp['time']=exp.ltime.values
    exp['ltime']=time

    #exp['ltime']=exp.ltime.values

    return exp 

def data_load_xr_time(path,name,calendar):

    exp            =  xr.open_dataset(path, engine='netcdf4')
    exp['name']    =  name

    exp['netsf']   =  exp['SWNS']-exp['LWNS']
    exp['netsf_dw']=  exp['SWDS']-exp['LWDS']

    #date_format = '%Y%m%d%H'
    ##to add the minutes to the original date
    #dis=date[0]#+'00'
    #dfs=date[1]#+'00'
    #di=dt.datetime.strptime(dis, date_format)
    #df=dt.datetime.strptime(dfs, date_format)

    ##initial hour
    #hi=di.hour
    ##final hour
    #hf=df.hour

    return exp 


#Function to know 
#the data interval to make 
#the statitics analysis of that interval.
#CREATED:Jhonatan Aguirre
#Covid19
#Data   :27-04-2020

#In:
#    idi: first data to search  
#    idf: last data to search  
#    data: data arrange

#Out:
#    ni:initial interval data indix
#    ni: final interval data indix

def data_ind(idi,data): 

    #indices achados
    ni=0

    #banderas 
    b1=0

    for i in range(0,data.shape[0]-1):

        if data[i]>=idi and b1==0: 
            ni =i  
            b1 =1
            print("Date found:")
            print("Data1:", data[i],i)

    return ni

def data_n(idi,idf,data): 


    #idi = dt.datetime(2014, 9, 26, 1) 
    #idf = dt.datetime(2014, 10,01, 1) 
    
    #tu = "days  since 2013-12-31"
    #tu = "days  since 2013-12-31 00:00:00 -00:00:00"
    #tc = "gregorian"
    
    #idin=date2num(idi,units=tu,calendar=tc)
    #idfn=date2num(idf,units=tu,calendar=tc)


    #indices achados
    ni=0
    nf=0

    #banderas 
    b1=0
    b2=0

    for i in range(0,data.shape[0]-1):


        if data[i]>=idi and b1==0: 
            ni =i  
            b1 =1
            print("From:")
            print("Data1:", data[i],i)

        if data[i]>=idf and b2==0:  
            nf =i  
            b2 =1
            print("To:")
            print("Data2:", data[i],i) 
    if nf==0:

        nf=data.shape[0]-1

    return ni,nf

def level_n(idi,idf,data): 

    #indices achados
    ni=0
    nf=0

    #banderas 
    b1=0
    b2=0

    for i in range(0,data.shape[0]-1):

        if data[i]>=idi and b1==0: 
            ni =i  
            b1 =1
            print("Level1:", data[i]) 

        if data[i]>=idf and b2==0:  
            nf =i  
            b2 =1
            print("Level2:", data[i]) 

    # To found the maximum date, even 
    # that required date not exists
    if nf==0:

        nf=data.shape[0]-1

    return ni,nf

def pressure_n(idi,idf,data,exp): 

    #indices achados
    ni=0
    nf=0

    #banderas 
    b1=0
    b2=0


    for i in range(0,data.shape[0]-1):

        if(data[i]<=idi and b1==0): 
            #print(data[i],idi,b1)
            ni =i  
            b1 =1
            #print("Level1:", data[i],idi,exp.z[i]) 

        if data[i]<=idf and b2==0:  
            #print(data[i],idf)
            nf =i  
            b2 =1
            #print("Level2:", data[i],exp.z[i]) 
    return ni,nf

def data_n_goa(idi,idf,data): 

    #idi = dt.datetime(2014, 9, 26, 1) 
    #idf = dt.datetime(2014, 10,01, 1) 
    
    #tu = "days  since 2013-12-31"
    tu = "days  since 2013-12-31 00:00:00 +04:00:00"
    tc = "gregorian"
    
    idin=date2num(idi,units=tu,calendar=tc)
    idfn=date2num(idf,units=tu,calendar=tc)

    #indices achados
    ni=0
    nf=0

    #banderas 
    b1=0
    b2=0

    for i in range(0,data.shape[0]-1):

        if data[i]>=idi and b1==0: 
            ni =i  
            b1 =1
            print("Data1:", data[i]) 

        if data[i]>=idf and b2==0:  
            nf =i  
            b2 =1
            print("Data2:", data[i]) 
    
    return ni,nf

#To put the differents datas in the 
#same reference hours, to plot in the same 
#graph

def data_to_reference(date,month_0,day_0,year): 

    month   =   date.dt.month
    day     =   date.dt.day
    hour    =   date.dt.hour 
    minute  =   date.dt.minute 
    second  =   date.dt.second 
    micro   =   date.dt.microsecond


    data_ref =   dt.datetime( year ,month_0,day_0,hour,minute, second,micro)

    return data_ref,day.values 

def data_to_reference_vector(data,month_0,day_0,year):

    i=0

    #to change the month, if 0 does change
    day_ant=0


    data_ref=[]
    for d in data:

        month   =   d.dt.month
        day     =   d.dt.day
        hour    =   d.dt.hour
        minute  =   d.dt.minute
        second  =   d.dt.second
        micro   =   d.dt.microsecond

        if day_ant==day+1:

            day_0+=1

        #data_ref[i] =   dt.datetime( year ,month_0,day_0,hour,minute, second,micro)
        data_ref.append(dt.datetime( year ,month_0,day_0,hour,minute, second,micro))

        day_ant = day

        i=i+1

    return data_ref

def data_all(data,k): 

    i=0

    if k>31:
        m=m+1
        k=k-31

    data_ref = data

    mm=1
    dd=k+1

    day_ant=0

    for d in data:

        day     =   d.day 
        hour    =   d.hour 
        minute  =   d.minute 
        second  =   d.second 
        micro   =   d.microsecond


        if day!=day_ant and i>0:
            dd+=1
            hour=0
            #print d

        #TO NOT PASS OF THE DAY
        #if hour>23 and minute >59 :
        #    #break

        data_ref[i] =   dt.datetime( 2022 ,mm,dd,hour,minute, second,micro)

        day_ant=day
        i=i+1

    return data_ref 

def hour_set_group(shca_sh):

    tobox = []
    utc = dt.timedelta(hours=4)
    
    for name, group in shca_sh:
        hour = group['Time'].values
        if hour[0] % 100.0 > 0:
            h = hour[0] / 100 + 0.2
        else:
            h = hour[0] / 100.0
    
        date_object = dt.datetime(2025, 1, 1) + dt.timedelta(hours=h) - utc
    
        # calcula média do grupo
        gmean = group.mean(numeric_only=True)
        # adiciona a data
        gmean["date"] = date_object
        tobox.append(gmean)
    
    mean_sh = pd.DataFrame(tobox)

    return mean_sh

def hour_set(mean_sh):

    dates=[]
    utc=dt.timedelta(hours=4)
    for hour in mean_sh['Time'].values:
    
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
    
    mean_sh['date'] = dates


    return mean_sh

