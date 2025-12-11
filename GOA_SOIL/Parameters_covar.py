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

egeon='/pesq'

#path =egeon+"/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA"
path2 =egeon+"/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA"

# Out figure folder
#out_fig=path+'/document/fig'
out_fig=path2+'/document_slm/figs'


path  =egeon+'/dados/bamc/jhonatan.aguirre/DATA/SLM_SAM_INIT_DATA/GOA_SOIL/COVARIANCE'


# Open the CSV file in read mode ('r')
#with open('%s/169_7_data.csv'%path, 'r', newline='') as csvfile:
#   # Create a reader object
#   csv_reader = csv.reader(csvfile)
#   # Iterate over each row in the CSV file
#   for row in csv_reader:
#       print(row)

# Read the CSV file into a DataFrame
df = pd.read_csv('%s/328_3_data.csv'%path)


#date_string = "25.12.24"
format_string = "%d.%m.%y"


#####https://acp.copernicus.org/articles/15/10723/2015/acp-15-10723-2015.pdf

dates=[]

utc=timedelta(hours=4)

#for time,seconds in zip(df.Timestamps[0:40],df.Time[0:40]):
for time,hour in zip(df.Timestamps,df.Time):

    h=hour
    date_object = datetime.strptime(time,format_string) + timedelta(hours=h)-utc

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

