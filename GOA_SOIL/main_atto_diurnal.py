from  Parameters_atto import df,data_to_reference_vector,soil_text,out_fig  
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

import seaborn as sns

from matplotlib.lines import Line2D

import matplotlib.patches as mpatches


soiltype="soil_plateaus" 
#soiltype="soil_terrances" 

#path  ='/pesq/dados/bamc/jhonatan.aguirre/DATA/SLM_SAM_INIT_DATA/GOA_SOIL'
path  ='/dados/bamc/jhonatan.aguirre/DATA/SLM_SAM_INIT_DATA/GOA_SOIL'

#####################################################
#####################################################


mask = pd.Series(False, index=df.index)
for start, end in dy.days:
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    mask |= (df["date"] >= start) & (df["date"] <= end)

selected    = df.loc[mask]
noselected  = df#.loc[~mask]



start_date='2014-02-15T00'
end_date  ='2014-03-25T00'
dini=dt.datetime.strptime(start_date, dy.date_format)
dfin=dt.datetime.strptime(end_date  , dy.date_format)

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
#@cells=['TS_10cm','TS_20cm','TS_40cm','US_10cm','US_20cm','US_30cm','US_40cm','US_60cm','US_100cm','Flx_S_5cm']
#@
#@iop1shca = soil_iop1.groupby(soil_iop1['Time'],as_index=False)[cells]
#@iop2shca = soil_iop2.groupby(soil_iop2['Time'],as_index=False)[cells]
#@shca_sh  =  selected.groupby( selected['Time'],as_index=False)[cells]



#""" plot with seaborn

#df = iop1shca["TS_10scm"].to_dataframe().reset_index()  # columns: time, depth, T 
selected["time_str"]  = selected["date"].dt.strftime("%H")
soil_iop1["time_str"] = soil_iop1["date"].dt.strftime("%H")
soil_iop2["time_str"] = soil_iop2["date"].dt.strftime("%H")


# Make a boxplot
#fig, ax = plt.subplots(figsize=(15, 6))
fig, ax = plt.subplots(figsize=(8.0, 4.0))
plt.rcParams['lines.linewidth'] = 1.0

sns.pointplot(data=soil_iop1, x="time_str" ,y="TS_10cm",errorbar=None,color='blue', join=True , markers=["o"], linestyles=["--" ])
sns.pointplot(data=soil_iop1, x="time_str" ,y="TS_20cm",errorbar=None,color='blue', join=True , markers=["x"], linestyles=["-"  ])
sns.pointplot(data=soil_iop1, x="time_str" ,y="TS_40cm",errorbar=None,color='blue', join=True , markers=["v"], linestyles=["-." ])

sns.pointplot(data=soil_iop2, x="time_str" ,y="TS_10cm",errorbar=None,color='orange' , join=True, markers=["o"], linestyles=["--" ])
sns.pointplot(data=soil_iop2, x="time_str" ,y="TS_20cm",errorbar=None,color='orange' , join=True, markers=["x"], linestyles=["-"  ])
sns.pointplot(data=soil_iop2, x="time_str" ,y="TS_40cm",errorbar=None,color='orange' , join=True, markers=["v"], linestyles=["-." ])

sns.pointplot(data=selected,  x="time_str" ,y="TS_10cm" ,errorbar=None,color='green' , join=True, markers=["o"], linestyles=["--" ])
sns.pointplot(data=selected,  x="time_str" ,y="TS_20cm" ,errorbar=None,color='green' , join=True, markers=["x"], linestyles=["-"  ])
sns.pointplot(data=selected,  x="time_str" ,y="TS_40cm" ,errorbar=None,color='green' , join=True, markers=["v"], linestyles=["-." ])



# Define custom colors and labels for the legend
colors = ['blue','orange','green' ]
labels = [r'IOP1',r'IOP2',r'ShCA']


patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]

# Apply colors to the boxes (optional, but demonstrates matching legend to plot)
for i, patch in enumerate(ax.artists):
    patch.set_facecolor(colors[i])

# Add the custom legend
first=ax.legend(handles=patches,bbox_to_anchor=(1.12,1.00), frameon=False, fontsize=8,loc='upper right')

ax.add_artist(first)



plt.xlabel("Time [Hours LT]")
plt.ylabel("Soil Temperature [°C]")
#plt.title("Soil Temperature Distribution by time")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.grid(True, axis="x", linestyle="--", alpha=0.6)


ax.xaxis.set_major_locator(plt.MultipleLocator(3.0))



labels = ["10cm", "20cm", "40cm"]
color = "black"  # same color for all

# Create custom legend handles
legend_elements = [
    Line2D([0], [0], color=color, linestyle="--", marker="o", label=labels[0]),
    Line2D([0], [0], color=color, linestyle="-" , marker="x", label=labels[1]),
    Line2D([0], [0], color=color, linestyle="-.", marker="v", label=labels[2]),
]

ax.legend(bbox_to_anchor=(0.00,1.1),ncol=3, handles=legend_elements,frameon=False,fontsize=7, loc="upper left")


fig_label='plot_T_%s'%soiltype
fig.savefig('%s/%s.pdf'%(out_fig,fig_label),dpi=200, format='pdf')


# Make a boxplot
fig, ax = plt.subplots(figsize=(8.0, 4.0))

sns.pointplot(data=soil_iop1, x="time_str" ,y="US_10cm",errorbar=None,color='blue', join=True , markers=["o"], linestyles=["--" ])
sns.pointplot(data=soil_iop1, x="time_str" ,y="US_20cm",errorbar=None,color='blue', join=True , markers=["x"], linestyles=["-"  ])
sns.pointplot(data=soil_iop1, x="time_str" ,y="US_40cm",errorbar=None,color='blue', join=True , markers=["v"], linestyles=["-." ])

sns.pointplot(data=soil_iop2, x="time_str" ,y="US_10cm",errorbar=None,color='orange' , join=True, markers=["o"], linestyles=["--" ])
sns.pointplot(data=soil_iop2, x="time_str" ,y="US_20cm",errorbar=None,color='orange' , join=True, markers=["x"], linestyles=["-"  ])
sns.pointplot(data=soil_iop2, x="time_str" ,y="US_40cm",errorbar=None,color='orange' , join=True, markers=["v"], linestyles=["-." ])

sns.pointplot(data=selected, x="time_str"  ,y="US_10cm" ,errorbar=None,color='green' , join=True, markers=["o"], linestyles=["--" ])
sns.pointplot(data=selected, x="time_str"  ,y="US_20cm" ,errorbar=None,color='green' , join=True, markers=["x"], linestyles=["-"  ])
sns.pointplot(data=selected, x="time_str"  ,y="US_40cm" ,errorbar=None,color='green' , join=True, markers=["v"], linestyles=["-." ])



# Define custom colors and labels for the legend
colors = ['blue','orange','green' ]
labels = [r'IOP1',r'IOP2',r'ShCA']


patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]

# Apply colors to the boxes (optional, but demonstrates matching legend to plot)
for i, patch in enumerate(ax.artists):
    patch.set_facecolor(colors[i])

# Add the custom legend
first=ax.legend(handles=patches, bbox_to_anchor=(1.12,1),frameon=False, fontsize=8,loc='upper right')

ax.add_artist(first)

plt.xlabel("Time [Hours LT]")
plt.ylabel("Soil Moisture [m$^3$/m$^3$]")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.grid(True, axis="x", linestyle="--", alpha=0.6)

ax.xaxis.set_major_locator(plt.MultipleLocator(3.0))


labels = ["10cm", "20cm", "40cm"]
color = "black"  # same color for all

# Create custom legend handles
legend_elements = [
    Line2D([0], [0], color=color, linestyle="--", marker="o", label=labels[0]),
    Line2D([0], [0], color=color, linestyle="-" , marker="x", label=labels[1]),
    Line2D([0], [0], color=color, linestyle="-.", marker="v", label=labels[2]),
]

ax.legend(bbox_to_anchor=(0.00,1.1),ncol=3, handles=legend_elements,frameon=False, loc="upper left",fontsize=7)


fig_label='plot_w_%s'%soiltype
fig.savefig('%s/%s.pdf'%(out_fig,fig_label),dpi=200, format='pdf')


plt.show()
