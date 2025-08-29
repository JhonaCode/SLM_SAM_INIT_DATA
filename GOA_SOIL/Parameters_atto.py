# python library to work with netcdf4 
#from    netcdf4         import dataset

# to save the time coordinate in specific format 
from    netCDF4         import num2date, date2num

from scipy import interpolate

from scipy.interpolate import interp1d

import copy

# Python standard library datetime  module
import datetime as dt

import xarray as xr

import numpy as np

import csv

import pandas as pd 

# To save the time coordinate in specific format 
from    cftime import num2date, num2pydate


from datetime import datetime,timedelta

path  ='/pesq/dados/bamc/jhonatan.aguirre/DATA/GOA_SOIL/atto_data_soil_2014'

# Open the CSV file in read mode ('r')
#with open('%s/169_7_data.csv'%path, 'r', newline='') as csvfile:
#   # Create a reader object
#   csv_reader = csv.reader(csvfile)
#   # Iterate over each row in the CSV file
#   for row in csv_reader:
#       print(row)

# Read the CSV file into a DataFrame
df = pd.read_csv('%s/169_7_data.csv'%path)

#date_string = "25.12.24"
format_string = "%d.%m.%y"


#####https://acp.copernicus.org/articles/15/10723/2015/acp-15-10723-2015.pdf

#[%]
soil_text = {
    "soil_atto_plateaus"  : {"clay": 85.3, "sand":10.4 , "silt":4.5},
    "soil_atto_terrances" : {"clay": 74.3, "sand":19.3 , "silt":6.6},
    }


dates=[]

utc=timedelta(hours=4)

#for time,seconds in zip(df.Timestamps[0:40],df.Time[0:40]):
for time,hour in zip(df.Timestamps,df.Time):

    #print(hour%100.0)
    if hour%100.0>0:
        #date_object = np.datetime64(datetime.strptime(time,format_string)) + np.timedelta64(hour,'h')
        h=hour/100+0.2
        date_object = datetime.strptime(time,format_string) + timedelta(hours=h)-utc
    else:
        h=hour/100.0
        #print(h)
        date_object = datetime.strptime(time,format_string) + timedelta(hours=h) -utc


    #date_object = np.datetime64(datetime.strptime(time,format_string)) + np.timedelta64(30,'m')

    #print(minutes)

    dates.append(date_object)


df['date']=dates

def data_to_reference_vector(data,month_0,day_0,year):

    i=0

    #to change the month, if 0 does change
    day_ant=1


    data_ref=[]
    for d in data:

        month   =   d.month
        day     =   d.day
        hour    =   d.hour
        minute  =   d.minute
        second  =   d.second
        micro   =   d.microsecond

        if day_ant+1==day:

            day_0+=1

        data_ref.append(dt.datetime( year ,month_0,day_0,hour,minute, second,micro))

        day_ant = day

        i=i+1

    return data_ref

