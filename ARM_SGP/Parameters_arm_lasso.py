import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from scipy import interpolate

from scipy.interpolate import interp1d


import seaborn as sns

path  ='/pesq/dados/bamc/jhonatan.aguirre/DATA/ARM_SGP/'

#soil0  =0
#soiltop=100
soil0  =0
soiltop=100
nlayers=10
# Generate 10 cm intervals (0-100 cm)
target_depths = np.arange(soil0,soiltop,nlayers)+1

# Raw SSURGO data (non-interpolated)
raw_data = {
    "Depth(cm)": [5, 10, 20, 50, 100],
    "Clay (%)": [17.27, 15.83, 31.13, 32.70, 32.70],
    "Sand (%)": [32.97, 36.70, 29.77, 31.10, 31.10]
}

# Create interpolation functions
clay_interp = interp1d(raw_data['Depth(cm)'], raw_data["Clay (%)"], kind='linear', fill_value='extrapolate')
sand_interp = interp1d(raw_data['Depth(cm)'], raw_data["Sand (%)"], kind='linear', fill_value='extrapolate')

# Apply interpolation
interpolated_data = {
    #"Depth": [f"{d-5}-{d+5}" for d in target_depths],
    "Depth": [f"{d}" for d in target_depths],
    "Clay": clay_interp(target_depths).round(1),
    "Sand": sand_interp(target_depths).round(1),
    "Type": ["Interpolated"] * len(target_depths)
}


# Create xarray Dataset
soil = xr.Dataset(
    data_vars={
        'clay': (('depth',), interpolated_data['Clay']), 
        'sand': (('depth',), interpolated_data['Sand']),
    },
    coords={
        'depth': interpolated_data["Depth"],
    },
    attrs={
        'description': 'Soil composition dataset for shallow layers (<1m)',
        'units': {'clay': '%', 'sand': '%'},
    }
)



# Depth levels
depths = [5, 10, 20, 50, 100]

# Data from the table
data = {
    "Date": [
        "2018-05-22", "2018-06-06", "2018-06-18", "2018-06-19", "2018-07-07",
        "2018-07-09", "2018-07-12", "2018-07-31", "2018-09-11", "2018-09-14",
        "2018-09-16", "2018-09-17", "2018-09-18", "2018-10-02"
    ],
    "Soil_temperature": [
        [293.5, 294.1, 294.5, 293.3, 291.3],
        [297.0, 297.5, 297.6, 295.9, 293.5],
        [299.1, 299.4, 299.5, 297.7, 294.9],
        [299.2, 299.4, 299.5, 297.7, 294.9],
        [298.7, 299.3, 299.4, 298.5, 296.1],
        [298.2, 299.1, 299.2, 298.5, 296.3],
        [299.8, 300.2, 300.4, 298.9, 296.5],
        [296.0, 297.1, 298.2, 297.3, 294.3],
        [293.6, 294.4, 295.3, 296.1, 296.2],
        [295.6, 296.0, 296.3, 296.2, 295.9],
        [296.2, 296.6, 296.7, 296.8, 296.8],
        [296.6, 296.7, 297.4, 296.8, 296.0],
        [297.1, 297.5, 297.8, 297.0, 296.1],
        [294.6, 295.0, 295.3, 294.9, 294.8],
    ],
    "Soil_wetness": [
        [0.58, 0.66, 0.71, 0.81, 0.82],
        [0.47, 0.59, 0.72, 0.82, 0.83],
        [0.38, 0.48, 0.64, 0.77, 0.74],
        [0.39, 0.49, 0.64, 0.78, 0.75],
        [0.44, 0.55, 0.71, 0.83, 0.77],
        [0.38, 0.50, 0.68, 0.82, 0.79],
        [0.34, 0.45, 0.63, 0.79, 0.75],
        [0.72, 0.74, 0.78, 0.76, 0.77],
        [0.72, 0.78, 0.78, 0.76, 0.71],
        [0.65, 0.73, 0.76, 0.75, 0.71],
        [0.59, 0.67, 0.73, 0.73, 0.70],
        [0.59, 0.67, 0.73, 0.73, 0.70],
        [0.53, 0.64, 0.72, 0.74, 0.69],
        [0.45, 0.55, 0.62, 0.71, 0.70],
    ]
}

# Create Dataset
dates = pd.to_datetime(data["Date"], format="%Y-%m-%d")
#dates = mdates.date2num(dates1)


soil_temp = xr.DataArray(data["Soil_temperature"], dims=["time", "depth"], coords={"time": dates, "depth": depths}, name="T")
soil_wet = xr.DataArray(data["Soil_wetness"], dims=["time", "depth"], coords={"time": dates, "depth": depths}, name="W")


ds = xr.Dataset({"T": soil_temp, "W": soil_wet})


meantime=ds.mean(dim='time')
meandepth=ds.mean(dim='depth')

#meantW=ds.std(dim='time')
#meandW=ds.std(dim='depth')


#Correcting the time to display it 
meandepth["time_str"] = ds["time"].dt.strftime("%Y-%m-%d")

T_interp = interp1d(meantime.depth, meantime.T, kind='linear', fill_value='extrapolate')
W_interp = interp1d(meantime.depth, meantime.W, kind='linear', fill_value='extrapolate')


mean_t=T_interp(target_depths)
mean_q=W_interp(target_depths)

# Convert xarray Dataset to a tidy DataFrame
#  Why seaborn loves tidy data:
#In tidy format, seaborn can directly map:
#x="depth"
#y="T"
#hue="time" or other variables
#without you having to manually reshape the dataset.

""" plot with seaborn

df = ds["T"].to_dataframe().reset_index()  # columns: time, depth, T

df["time_str"] = df["time"].dt.strftime("%Y-%m-%d")


# Make a boxplot
fig, ax = plt.subplots(figsize=(15, 6))
sns.boxplot(data=df, x="depth", y="T",palette='coolwarm')

plt.xlabel("Depth (m)")
plt.ylabel("Soil Temperature (°C)")
plt.title("Soil Temperature Distribution by Depth")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
#plt.show()


fig, ax = plt.subplots(figsize=(15, 6))
#sns.boxplot(data=df, x="time", y="T", hue='depth')
#sns.boxplot(data=df, x="time_str", y="T", hue='depth')
sns.boxplot(data=df, x="time_str", y="T")

plt.plot(meandepth.time_str,meandepth.T.values)
#plt.plot(meantime.depth.values,meandepth.T.values)

plt.xlabel("Date ")
plt.ylabel("Soil Temperature (°C)")
plt.title("Soil Temperature Distribution by Time")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
plt.show()

""" #plot with seaborn

#fig, ax = plt.subplots(figsize=(15, 6))
#
#df=soil_temp.to_pandas()
#df.boxplot( showfliers=True,)
#sns.pointplot(x='depth', y='T', data=df.groupby('depth', as_index=False).mean(), ax=ax)
#

""" plot with mathplot 



fig, ax = plt.subplots(figsize=(15, 6))
positions = (soil_temp.depth)
#Plotando o boxplot das espécies em relação ao tamanho das sépalas
bplots = plt.boxplot(soil_temp, positions=positions , vert = 1, patch_artist = False)
plt.plot(meantime.depth.values,meantime.T.values)

colors = ['pink', 'lightblue', 'lightgreen','red','navy']
c = 0
for i, bplot in enumerate(bplots['boxes']):
    bplot.set(color=colors[c], linewidth=3)
    c += 1

c4 = 0
for median in bplots['medians']:
    median.set(color=colors[c4], linewidth=3)
    c4 +=1

#plt.show()

fig, ax = plt.subplots(figsize=(15, 6))
positions = mdates.date2num(soil_temp.time)

#Plotando o boxplot das espécies em relação ao tamanho das sépalas
bplots = plt.boxplot(soil_temp.T, positions=positions , vert = 1, patch_artist = False)
# Format the x-axis as dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

plt.plot(meandepth.time.values,meandepth.T.values)

plt.show()
#print(len(bplots))

#bplots = plt.boxplot(soil_temp,  vert = 0, patch_artist = False)

#print(len(bplots))
#print(bplots.size)

#colors = ['pink', 'lightblue', 'lightgreen']
#c = 0
#for bplot in enumerate(bplots['boxes']):
#    bplot.set(color=colors[c], linewidth=3)
#    c += 1
#
#plt.show()
#

plt.xlabel("Day of Year")
plt.ylabel("Value")
plt.title("Daily Box Plots of Time Series Data")
plt.show()

"""# plot with mathplot 
