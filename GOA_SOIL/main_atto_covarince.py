from    Parameters_covar import df,data_to_reference_vector  

import  Parameters_sam as  sam 

#import  sam_python.plotparameters      as pp

import  plotparameters      as pp
##
from     matplotlib.lines import Line2D


import  data_own as down

import  numpy as np

import  xarray as xr

import  matplotlib.pyplot as plt

import  matplotlib.dates as mdates

import datetime as dt

from scipy import interpolate

from scipy.interpolate import interp1d

import  days  as dy 

import pandas as pd

import seaborn as sns

from matplotlib.lines import Line2D

import matplotlib.patches as mpatches


out_fig='/pesq/dados/bamc/jhonatan.aguirre/git_repositories/PAPER3_SHCA/document_slm_git/figs'


mask = pd.Series(False, index=df.index)

##dy in days.py files 
for start, end in dy.days:
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    mask |= (df["date"] >= start) & (df["date"] <= end)

#only shallow days
selected    = df.loc[mask]
#all iops 
noselected  =df#.loc[~mask]

#arrange the date time
selected["time_str"]  = selected["date"].dt.strftime("%H")
noselected["time_str"]  = noselected["date"].dt.strftime("%H")
#print(selected.Timestamps[0:10])
#print(noselected.Timestamps[0:10])

#Your x-axis values are strings instead of numbers
#If your x column is dtype=object (e.g., '1', '2', '10'), Seaborn sorts strings alphabetically:
#"1", "10", "2"
#fix 
#Convert the x column to numeric:
selected["time_str"] = pd.to_numeric(selected["time_str"])
noselected["time_str"] = pd.to_numeric(noselected["time_str"])


#greater than the start date and smaller than the end date
iop_h   = (selected.H > -9999.00) #& (selected.LE > -9999.00)
date_h   = selected[iop_h]
iop_le_se  = (date_h.LE > -9999.00) #& (selected.LE > -9999.00)
date_ok_se  = date_h[iop_le_se]


#greater than the start date and smaller than the end date
iop_h   = (noselected.H > -9999.00) #& (selected.LE > -9999.00)
date_h   = noselected[iop_h]
iop_le_no  = (date_h.LE > -9999.00) #& (selected.LE > -9999.00)
date_ok_no  = date_h[iop_le_no]


start_date='2014-02-15T00'
end_date  ='2014-03-25T00'
dini      = dt.datetime.strptime(start_date, dy.date_format)
dfin      = dt.datetime.strptime(end_date  , dy.date_format)

iop1_mask_se = (date_ok_se.date > dini) & (date_ok_se.date <= dfin)
iop1_select  = date_ok_se[iop1_mask_se]

start_date='2014-09-01T00'
end_date  ='2014-10-11T00'
dini      =dt.datetime.strptime(start_date, dy.date_format)
dfin      =dt.datetime.strptime(end_date  , dy.date_format)
#
iop2_mask_se = (date_ok_se.date > dini) & (date_ok_se.date <= dfin)
iop2_select  = date_ok_se[iop2_mask_se]


time_sam=sam.iop1.time.dt.hour+sam.iop1.time.dt.minute/60.0

#print(iop1[['time_str','H','LE']][30:50])
#print(iop2[['date','H','LE']][30:50])


size_wg = 0.75 
size_hf = 0.5 
cmas    = 0 

tama= pp.plotsize(size_wg,size_hf, cmas,'temporal')


# Make a boxplot
#fig, ax = plt.subplots(figsize=(15, 6))
fig, ax = plt.subplots()


#plt.rcParams['lines.linewidth'] = 1.0

sns.pointplot(data=iop1_select, x="time_str" ,y="LE",errorbar=None,color='blue', join=True , markers=["o"], linestyles=["--" ])
sns.pointplot(data=iop1_select, x="time_str" ,y="H" ,errorbar=None,color='red' , join=True , markers=["o"], linestyles=["--" ])
plt.plot(time_sam,sam.iop1.LHF ,color='blue',label='LHF')
plt.plot(time_sam,sam.iop1.SHF ,color='red' ,label='SHF')
plt.grid(True, axis="y", linestyle="--", alpha=0.1)
plt.grid(True, axis="x", linestyle="--", alpha=0.1)

ax.xaxis.set_major_locator(plt.MultipleLocator(2.0))
ax.set_xlim([6,20])
ax.set_ylim([0,600])


#Define custom colors and labels for the legend
colors      = ['blue','blue','red','red']
linestyle   = ['--','-',':','--','-',':' ]
labels      = [r'ATTO LHF',r'GoAm LHF',r'ATTO SHF',r'GoAm SHF']


proxies = [
    Line2D([0], [0], color=colors[i], linestyle=linestyle[i], label=labels[i])
    for i in range(len(labels))
]

# Then call legend(proxies)
ax.legend(handles=proxies, loc='best',frameon=False, fontsize=8)


ax.set_title('SHCA IOP1')
ax.set_xlabel('Hours LT')
ax.set_ylabel(r'Surface Heat Flux [Wm$^{2}$]')

fig_label='surface_fluxes_atto_iop1'

fig.savefig('%s/%s.pdf'%(out_fig,fig_label),bbox_inches='tight',dpi=200, format='pdf')


#################################33

fig, ax = plt.subplots()
#plt.rcParams['lines.linewidth'] = 1.0

time_iop2=sam.iop2.time.dt.hour+sam.iop2.time.dt.minute/60.0
sns.pointplot(data=iop2_select, x="time_str" ,y="LE",errorbar=None,color='blue', join=True , markers=["o"], linestyles=["--" ])
sns.pointplot(data=iop2_select, x="time_str" ,y="H" ,errorbar=None,color='red' , join=True , markers=["o"], linestyles=["-." ])
plt.plot(time_sam,sam.iop2.LHF ,color='blue')
plt.plot(time_sam,sam.iop2.SHF ,color='red')

ax.xaxis.set_major_locator(plt.MultipleLocator(2.0))
ax.set_xlim([6,20])
ax.set_ylim([0,600])



ax.set_title('SHCA IOP2')
ax.set_xlabel('Hours LT')
ax.set_ylabel(r'Surface Heat Flux [Wm$^{2}$]')


plt.grid(True, axis="y", linestyle="--", alpha=0.6)


# Then call legend(proxies)
ax.legend(handles=proxies, loc='best',frameon=False, fontsize=8)

fig_label='surface_fluxes_atto_iop2'

fig.savefig('%s/%s.pdf'%(out_fig,fig_label),bbox_inches='tight',dpi=200, format='pdf')
#################################33

tama= pp.plotsize(size_wg,size_hf, cmas,'temporal')

fig, ax = plt.subplots()
#plt.rcParams['lines.linewidth'] = 1.0

time_sam=sam.shca_cass.time.dt.hour+sam.shca_cass.time.dt.minute/60.0
time_sam2 =sam.shca_plat_nearest_modi.time.dt.hour+sam.shca_plat_nearest_modi.time.dt.minute/60.0


sns.pointplot(data=date_ok_se, x="time_str" ,y="LE",errorbar=None,color='blue', join=True , markers=["o"], linestyles=["--" ])
sns.pointplot(data=date_ok_se, x="time_str" ,y="H" ,errorbar=None,color='red' , join=True , markers=["o"], linestyles=["-." ])
plt.plot(time_sam,sam.shca_cass.LHF ,color='blue')
plt.plot(time_sam,sam.shca_cass.SHF ,color='red')
plt.plot(time_sam2,sam.shca_plat_nearest_modi.LHF ,color='blue' ,label='SHF',ls=':',linewidth=2)
plt.plot(time_sam2,sam.shca_plat_nearest_modi.SHF ,color='red' ,label='SHF',ls=':',linewidth=2)

plt.title('SHCA')
ax.set_xlabel('Hours LT')
ax.set_ylabel(r'Surface Heat Flux [Wm$^{2}$]')

ax.xaxis.set_major_locator(plt.MultipleLocator(2.0))
ax.set_xlim([6,20])
ax.set_ylim([0,600])

plt.grid(True, axis="x", linestyle="--", alpha=0.6)
plt.grid(True, axis="y", linestyle="--", alpha=0.6)

#Define custom colors and labels for the legend
colors      = ['blue','blue','blue','red','red','red' ]
linestyle   = ['--','-',':','--','-',':' ]
labels      = [r'ATTO LHF',r'GoAm LHF','SLM  LHF',r'ATTO SHF',r'GoAm SHF','SLM  SHF']

proxies = [
    Line2D([0], [0], color=colors[i], linestyle=linestyle[i], label=labels[i])
    for i in range(len(labels))
]

# Then call legend(proxies)
ax.legend(handles=proxies, loc='best',frameon=False, fontsize=8)

fig_label='surface_fluxes_atto_shca'

fig.savefig('%s/%s.pdf'%(out_fig,fig_label),bbox_inches='tight',dpi=200, format='pdf')


plt.show()

