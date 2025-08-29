# python library to work with netcdf4 
#from    netcdf4         import dataset

# to save the time coordinate in specific format 
from    netCDF4         import num2date, date2num

from scipy import interpolate

from scipy.interpolate import interp1d


# Python standard library datetime  module
import datetime as dt

import xarray as xr

import numpy as np

# To save the time coordinate in specific format 
from    cftime import num2date, num2pydate

#path  ='/dados/bamc/jhonatan.aguirre/DATA/ARM_SGP/'
path  ='/pesq/dados/bamc/jhonatan.aguirre/DATA/ARM_SGP/'

path21=path+'sgpswatsE13.b1.19970621.000700.cdf'
#path21=path+'sgpswatsE2.b1.19970621.000700.cdf'

jun21 =  xr.open_dataset(path21, engine='netcdf4')

mean_t=np.mean(np.array([jun21.tsoil_W,jun21.tsoil_E]),axis=0)

mean_q=np.mean(np.array([jun21.watcont_W,jun21.watcont_E]),axis=0)


"""
# Raw SSURGO data (non-interpolated)
raw_data = {
    "Top Depth (cm)": [0, 18, 36, 66, 94],
    "Bottom Depth (cm)": [18, 36, 66, 94, 152],
    "Clay (%)": [15, 22, 30, 38, 42],
    "Sand (%)": [70, 58, 45, 38, 32]
}

# Convert to layer midpoints for interpolation
mid_depths = [(top + bottom)/2 for top, bottom in zip(raw_data["Top Depth (cm)"], raw_data["Bottom Depth (cm)"])]

# Create interpolation functions
clay_interp = interp1d(mid_depths, raw_data["Clay (%)"], kind='linear', fill_value='extrapolate')
sand_interp = interp1d(mid_depths, raw_data["Sand (%)"], kind='linear', fill_value='extrapolate')
"""

# from paper lasso 2024 soil E13 
raw_data = {
    "Depth(cm)": [5    , 10, 20, 50, 100],
    "Clay (%)" : [17.27, 15.83, 31.13, 32.70,32.70 ],
    "Sand (%)" : [32.97, 36.70, 29.77, 31.10,31.10 ],
    "Type (%)" : ['SiL', 'SiL', 'C', 'CL','CL' ], #SiL=Silt Loam, C=Clay, CL=Clay loam, 
    "FC (%)"   : [0.36, 0.36, 0.412, 0.382,0.382 ],
}

# Create interpolation functions
#clay_interp = interp1d(raw_data["Depth(cm)"], raw_data["Clay (%)"], kind='linear', fill_value='extrapolate')
#sand_interp = interp1d(raw_data["Depth(cm)"], raw_data["Sand (%)"], kind='linear', fill_value='extrapolate')
#FC_interp   = interp1d(raw_data["Depth(cm)"], raw_data["FC (%)"]  , kind='linear', fill_value='extrapolate')
clay_interp = interp1d(raw_data["Depth(cm)"], raw_data["Clay (%)"], kind='nearest', fill_value='extrapolate')
sand_interp = interp1d(raw_data["Depth(cm)"], raw_data["Sand (%)"], kind='nearest', fill_value='extrapolate')
FC_interp   = interp1d(raw_data["Depth(cm)"], raw_data["FC (%)"]  , kind='nearest', fill_value='extrapolate')


#soil0  =0
#soiltop=100
soil0  =0
soiltop=100
nlayers=10
# Generate 10 cm intervals (0-100 cm)
target_depths = np.arange(soil0,soiltop,nlayers)+1


# Apply interpolation
interpolated_data = {
    #"Depth": [f"{d-5}-{d+5}" for d in target_depths],
    "Depth": [f"{d}" for d in target_depths],
    "Clay": clay_interp(target_depths).round(2),
    "Sand": sand_interp(target_depths).round(2),
    "FC": FC_interp(target_depths).round(2),
    "Silt": (100 - clay_interp(target_depths) - sand_interp(target_depths)).round(1),
    "Type": ["Interpolated"] * len(target_depths)
}


# Create xarray Dataset
soil = xr.Dataset(
    data_vars={
        'clay': (('depth',), interpolated_data['Clay']), 
        'sand': (('depth',), interpolated_data['Sand']),
        'silt': (('depth',), interpolated_data['Silt']),
        'FC'  : (('depth',), interpolated_data['FC']),
    },
    coords={
        'depth': interpolated_data["Depth"],
    },
    attrs={
        'description': 'Soil composition dataset for shallow layers (<1m)',
        'units': {'clay': '%', 'sand': '%', 'silt': '%'},
    }
)

#print(soil.depth)
#print(soil.clay)
#print(soil.sand)

########################################################

x  = np.array(jun21.time)  #np.linspace(0, 23, 24)
y  = np.array(jun21.depth) #np.linspace(0, 100, len(jun21,depth))


ft = interpolate.interp2d(y,x,  mean_t, kind='cubic')
fq = interpolate.interp2d(y,x,  mean_q, kind='cubic')


xn = np.array(jun21.time)  #np.linspace(0, 23, 24)
yn =target_depths

mean_t=ft(yn,xn)
mean_q=fq(yn,xn)


"""
The LSM requires a wetness value between 0 and 1,
with 1 corresponding to the maximum moisture holding capacity, or field capacity, of the soil.
Since STAMP only
provides a volumetric soil moisture, VSM, a conversion is needed that requires knowledge of the field capacity,
FC, of the soil. At each site, i, and each vertical level, j, we determine the soil wetness value, W, using the profile
of soil texture at each site (Table 1) and reference values of FC obtained from
the Weather Research and Forecasting (WRF) Model (Table 3) as:
"""
mean_q= mean_q/soil['FC'].values



#fclay=interp1d(soil.depth,soil.clay,fill_value='extrapolate')
#fsand=interp1d(soil.depth,soil.sand,fill_value='extrapolate')

#clay=fclay(yn)
#sand=fsand(yn)

def data_load_xr(path,name,calendar):

    exp            =  xr.open_dataset(path, engine='netcdf4')
    exp['name']    =  name

    #exp['netsf_dw']=  exp['SWDS']-exp['LWDS']

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

    return exp
