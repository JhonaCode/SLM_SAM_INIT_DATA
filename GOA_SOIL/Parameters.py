

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

# To save the time coordinate in specific format 
from    cftime import num2date, num2pydate

path  ='/pesq/dados/bamc/jhonatan.aguirre/DATA/GOA_SOIL'

##%%%%https://www.mdpi.com/2076-3298/12/4/98


soil_temp = {
    "PastureA": {
        "Jul":   [30.53, 29.41, 29.39, 29.52],
        "Aug":   [32.44, 31.08, 31.04, 31.07],
        "Sep":   [33.70, 32.22, 32.05, 32.10],
        "Oct":   [31.86, 30.63, 30.58, 30.74],
        "Nov":   [29.90, 28.71, 28.91, 29.22],
        "Dec":   [28.17, 27.40, 27.60, 27.97],
        "Jan":   [26.59, 25.88, 26.13, 26.60],
    },
    "PastureB": {
        "Jul":   [29.51, 29.24, 29.39, 29.75],
        "Aug":   [30.99, 30.62, 30.68, 30.94],
        "Sep":   [31.16, 31.11, 31.23, 31.57],
        "Oct":   [30.11, 29.85, 30.03, 30.46],
        "Nov":   [30.23, 30.09, 30.39, 30.77],
        "Dec":   [30.00, 29.75, 30.06, 30.50],
        "Jan":   [29.64, 29.45, 29.68, 30.17],
    },
    "Transition": {
        "Jul":   [30.85, 30.51, 29.86, 30.57],
        "Aug":   [32.52, 31.94, 31.25, 32.02],
        "Sep":   [33.69, 33.11, 32.35, 33.13],
        "Oct":   [31.88, 31.86, 31.26, 32.05],
        "Nov":   [31.15, 31.12, 30.63, 31.51],
        "Dec":   [29.59, 29.65, 29.08, 29.90],
        "Jan":   [28.40, 28.22, 27.72, 28.55],
    },
    "Forest": {
        "Jul":   [23.99, 24.23, 24.40, 24.28],
        "Aug":   [24.65, 24.45, 24.48, 24.28],
        "Sep":   [26.74, 26.38, 26.23, 25.90],
        "Oct":   [26.32, 26.21, 26.16, 25.98],
        "Nov":   [26.14, 26.13, 26.12, 25.93],
        "Dec":   [25.93, 26.02, 26.06, 25.86],
        "Jan":   [25.36, 25.53, 25.57, 25.52],
    }
}

soil_moist = {
    "PastureA": {
        "Jul":   [2.77, 15.7, 21.2, 20.6],
        "Aug":   [1.63, 11.9, 17.5, 18.7],
        "Sep":   [1.46, 9.66, 16.6, 18.3],
        "Oct":   [4.72, 17.1, 22.4, 21.4],
        "Nov":   [5.05, 17.8, 23.5, 22.2],
        "Dec":   [5.36, 18.4, 24.0, 22.3],
        "Jan":   [7.08, 19.9, 25.0, 23.1],
    },
    "PastureB": {
        "Jul":   [2.68, 3.94, 3.52, 4.34],
        "Aug":   [2.18, 3.47, 3.17, 3.93],
        "Sep":   [7.95, 9.78, 7.50, 8.77],
        "Oct":   [9.97, 11.4, 8.67, 10.3],
        "Nov":   [10.4, 11.4, 8.12, 9.25],
        "Dec":   [10.5, 11.9, 8.68, 10.1],
        "Jan":   [11.3, 12.7, 9.00, 10.7],
    },
    "Transition": {
        "Jul":   [1.39, 7.75, 9.74, 10.9],
        "Aug":   [0.87, 4.97, 6.76, 7.52],
        "Sep":   [0.77, 4.56, 6.57, 7.35],
        "Oct":   [1.94, 9.00, 11.0, 11.6],
        "Nov":   [1.93, 7.38, 9.70, 10.8],
        "Dec":   [3.15, 10.7, 13.0, 14.2],
        "Jan":   [5.25, 12.0, 13.9, 15.1],
    },
    "Forest": {
        "Jul":   [4.44, 6.50, 14.4, 19.0],
        "Aug":   [3.53, 5.45, 12.6, 17.4],
        "Sep":   [3.41, 5.16, 12.1, 16.8],
        "Oct":   [5.14, 6.66, 13.9, 18.4],
        "Nov":   [4.50, 5.35, 12.5, 17.2],
        "Dec":   [11.4, 12.6, 21.2, 26.1],
        "Jan":   [13.6, 14.1, 23.3, 28.0],
        # (omitted Nov–Jan for brevity; can be added similarly)
    }
}

soil_texture = {
    "PastureA": {
        "depth1": {"clay": 0.4 ,"sand": 0.575,"silt": 0.115},
        "depth2": {"clay": 0.3 ,"sand": 0.575,"silt": 0.115}
    },
    #Agriculture
    "PastureB": {
        "depth1": {"clay": 0.28, "sand": 0.650, "silt":0.090},
        "depth2": {"clay": 0.28, "sand": 0.650, "silt":0.090}
    },
    #"Secondary Forest": {
    "Transition": {
        "depth1": {"clay": 0.290, "sand": 0.6, "silt":0.105},
        "depth2": {"clay": 0.310, "sand": 0.6, "silt":0.105}
    },
    "Forest": {
        "depth1": {"clay": 0.150, "sand": 0.80, 'silt':0.055},
        "depth2": {"clay": 0.170, "sand": 0.80, 'silt':0.055}
    },
}

soil_text = {
    "PastureA"  : {"clay": 0.40, "sand": 0.575, "silt":0.115},
    "PastureB"  : {"clay": 0.28, "sand": 0.650, "silt":0.090},
    "Transition": {"clay": 0.29, "sand": 0.600, "silt":0.105},
    "Forest"    : {"clay": 0.15, "sand": 0.800, 'silt':0.055},
    }


#print(soil_text["PastureA"]["clay"])
#
#exit()



# Raw SSURGO data (non-interpolated)
raw_data = {
    "Bottom Depth (cm)": [0 , 10, 20, 30],
    "Top Depth (cm)"   : [10, 20, 30, 40],
    #"Clay (%)": [15, 22, 30, 38, 42],
    #"Sand (%)": [70, 58, 45, 38, 32]
}

# Convert to layer midpoints for interpolation
mid_depths = [(top + bottom)/2 for top, bottom in zip(raw_data["Top Depth (cm)"], raw_data["Bottom Depth (cm)"])]

months={
        "Jul":[],
        "Aug":[],
        "Sep":[],
        "Oct":[],
        "Nov":[],
        "Dec":[],
        "Jan":[],
        }

soil_E={
          "PastureA":months,
          "PastureB":months,
          "Transition":months,
          "Forest":months,
}

soil_T_int=copy.deepcopy(soil_E)
soil_M_int=copy.deepcopy(soil_E)
soil_T    =copy.deepcopy(soil_E)
soil_M    =copy.deepcopy(soil_E)

#soil_T_int={k:months for k in soil_E}
#soil_M_int={k:months for k in soil_E}
#soil_T    ={k:months for k in soil_E}
#soil_M    ={k:months for k in soil_E}



for soiltype in soil_temp: 

    for month in months:

        soil_T_int[soiltype][month]= interp1d(mid_depths,  soil_temp[soiltype][month], kind='linear', fill_value='extrapolate')
        soil_M_int[soiltype][month]= interp1d(mid_depths, soil_moist[soiltype][month], kind='linear', fill_value='extrapolate')
    

soil0  =0
soiltop=60
nlayers=6
# Generate 10 cm intervals (0-100 cm)
target_depths = np.arange(soil0,soiltop,nlayers)#+1

#forest_temp=forest_temp_int(target_depths).round(1)
for soiltype in soil_temp: 
    for month in months:
        #print(soil_T_int[soiltype][month](target_depths).round(1))
        soil_T[soiltype][month] = soil_T_int[soiltype][month](target_depths).round(1)
        soil_M[soiltype][month] = soil_M_int[soiltype][month](target_depths).round(1)

