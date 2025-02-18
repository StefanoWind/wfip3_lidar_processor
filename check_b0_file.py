# -*- coding: utf-8 -*-
'''
Check b0-level file

Inputs (both hard-coded and available as command line inputs in this order):
    source_a0: path to a0 file
    source_b0: path to b0 file
'''
import os
cd=os.path.dirname(__file__)
import xarray as xr
import warnings
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.dates as mdates
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.size'] = 12
warnings.filterwarnings('ignore')
plt.close('all')

#%% Inputs
source_a0=os.path.join(cd,'data/wfip3/bloc.lidar.z01.a0/bloc.lidar.z01.a0.20250218.124926.user1.nc')
source_b0=os.path.join(cd,'data/wfip3/bloc.lidar.z01.b0/bloc.lidar.z01.b0.20250218.124926.user1.wfip3.prof.nc')

#%% Initialization
data_a0=xr.open_dataset(source_a0)
data_b0=xr.open_dataset(source_b0)

#%% Plots

#raw data
plt.figure(figsize=(18,10))
plt.pcolor(data_a0.time,data_a0.range_gate,data_a0.radial_wind_speed.T,vmin=-10,vmax=10,cmap='seismic')
plt.xlabel('Time (UTC)')
plt.ylabel('Range gate')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d %H%M'))
plt.grid()
plt.colorbar(label='Radial wind speed [m s$^{-1}$]')

#standardized data
plt.figure(figsize=(18,10))
for s in data_b0.scanID:
    data_sel=data_b0.sel(scanID=s)
    plt.pcolor(data_sel.time,data_sel.range,data_sel.wind_speed.where(data_sel.qc_wind_speed==0),vmin=-10,vmax=10,cmap='seismic')
    plt.plot([data_sel.time.values[0],data_sel.time.values[0]],[0,data_sel.range[-1]],'--k',linewidth=1,alpha=0.5)
plt.xlabel('Time (UTC)')
plt.ylabel('Range [m]')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d %H%M'))
plt.grid()
plt.colorbar(label='Radial wind speed [m s$^{-1}$]')

#qc flag
qc_flag=[data_b0.qc_wind_speed.attrs[f'bit_{i}_description'][22:-1] for i in range(12)]
qc_flag[0]='good'

plt.figure(figsize=(18,10))
for s in data_b0.scanID:
    data_sel=data_b0.sel(scanID=s)
    plt.contourf(data_sel.time,data_sel.range,data_sel.qc_wind_speed,np.arange(-0.5,12),cmap='jet')
plt.xlabel('Time (UTC)')
plt.ylabel('Range [m]')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d %H%M'))
plt.grid()
cb=plt.colorbar(label='QC flag')
cb.set_ticks(np.arange(12))
cb.set_ticklabels(qc_flag)