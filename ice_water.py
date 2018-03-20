
import os,sys
import numpy as np
from netCDF4 import Dataset 
from PyQt5 import QtGui, QtCore,QtWidgets
from matplotlib import rc
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename,askdirectory  
import os
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from netCDF4 import Dataset,num2date,date2num,date2index
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.dates as mdates
import datetime 
#from datetime import datetime, timedelta
import tkinter as tk # python3
from tkinter.filedialog import askopenfilename,askdirectory   # python 3
root = tk.Tk()
root.withdraw()

figure = plt.figure(figsize=(5.69 , 3.27),
                        facecolor='None',edgecolor='None') 
#directory =  askdirectory() 
directory = r'E:\Users\Shamil\binary\laptev_ersem'
ice_fname = os.path.abspath(os.path.join(directory,'ice.nc')) 
water_fname = os.path.join(directory,'water.nc')

name = 'total_chlorophyll_calculator_result'
fh_ice =  Dataset(ice_fname)  
fh_water =  Dataset(water_fname)

depth = fh_ice.variables['z'][:] 
depth_faces = fh_ice.variables['z_faces'][:] 

max_faces = np.max(depth_faces)

min_ice = np.min(depth)
max_ice = np.max(depth)

ice_res = 6
depth_ice = (depth - max_ice)*-ice_res
depth_ice_faces = np.array((depth_faces - max_faces)*-ice_res)

depth_ice = np.array(depth_ice)

min_ice = np.amin(depth_ice_faces)
max_ice = 100 #np.amax(depth_ice_faces)

try:
    time = fh_ice.variables['time']      
    time2 = fh_ice.variables['time'][:]
    time_units = fh_ice.variables['time'].units
except KeyError:
    time = fh_ice.variables['ocean_time']   
    time2 = fh_ice.variables['ocean_time'][:]            
    time_units = fh_ice.variables['ocean_time'].units
format_time = num2date(time2,units = time_units,calendar= 'standard')

#assert start_year < stop_year
to_start = datetime.datetime(1983,8,1,12,0)
to_stop= datetime.datetime(1983,11,1,12,0)

start = date2index(to_start, time,#units = time_units,
                    calendar=None, select='nearest')
stop = date2index(to_stop, time,#units = time_units,
                    calendar=None, select='nearest')

#data = read_var()
var_ice =  ma.masked_invalid (np.array(fh_ice.variables[name][start:stop,:]).T)
var_water = np.array(fh_water.variables[name][start:stop,:]).T 
depth_water = np.array(fh_water.variables['z_faces'][:])*100
min_water = np.amin(depth_water)
max_water = np.amax(depth_water)



### for combined water,ice array 
'''
var_all = np.ma.concatenate((var_ice, var_water), axis=0)
a = - depth_ice #_faces
b = depth_water #*100
depth_all = np.ma.concatenate((a,b), axis=0)
depth_ice_faces = - depth_ice_faces
X_all,Y_all = np.meshgrid(time2[start:stop],depth_all)




gs = gridspec.GridSpec(1, 1)
X_all = num2date(X_all,units = time_units) 
CS1 = ax0.pcolor(X_all,Y_all,var_all[:,:],
                 cmap = cmap )#) 3,edgecolor = 'w',
                 plt.colorbar(ax0)
'''

X,Y = np.meshgrid(time2[start:stop],depth_ice_faces)
X  = num2date(X,units = time_units) #format_time  
start_f = num2date(time2[start],units = time_units) 
stop_f = num2date(time2[stop],units = time_units)
 
fh_ice.close()
fh_water.close()

gs0 = gridspec.GridSpec(1, 1)
gs0.update(left=0.15, right= 0.91,top = 0.93,bottom = 0.13,
                   wspace=0.3,hspace=0.2)

gs = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[0],hspace=0.03)
#gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[1],hspace=0.03)

#gs = gridspec.GridSpec(2, 1)
#gs.update(left=0.15, right= 0.95,top = 0.95,bottom = 0.06,
#                   wspace=0,hspace=0.01)
                   #

#add subplots
ax0 = figure.add_subplot(gs[0]) # o2 ice 
ax1 = figure.add_subplot(gs[1]) # o2 water 
'''
ax0_1 = figure.add_subplot(gs1[0]) # o2 ice 
ax1_1 = figure.add_subplot(gs1[1]) # o2 water 


gs2 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[2],hspace=0.03)
gs3 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[3],hspace=0.03)
ax0_2 = figure.add_subplot(gs2[0]) # o2 ice 
ax1_2 = figure.add_subplot(gs2[1]) # o2 water 

ax0_3 = figure.add_subplot(gs3[0]) # o2 ice 
ax1_3 = figure.add_subplot(gs3[1]) # o2 water 
'''

ax1.set_ylim(100,0) 
cmap = plt.get_cmap('viridis') 

ax1.set_yticks((20,40,60,80,100))   
ax0.set_ylim(0,100)
ax0.set_title(name) 
ax1.set_xlabel('day,month')
ax0.set_ylabel('ice depth (cm)')
ax1.set_ylabel('water depth (cm)')
ax0.set_xticks([])
ax1.xaxis.set_major_formatter(
            mdates.DateFormatter('%d.%m'))



X_water,Y_water = np.meshgrid(time2[start:stop],depth_water)
X_water = num2date(X_water,units = time_units)  

CS1 = ax0.pcolor(X,Y,var_ice[:,:],
                 cmap = cmap )#) 3,edgecolor = 'w', 
CS2 = ax1.pcolor(X_water,Y_water,var_water[:,:],
                  cmap = cmap)

import matplotlib.ticker as ticker

def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)         

def add_colorbar(CS,axis):
    cb = plt.colorbar(CS,ax = axis,pad=0.01,
             aspect = 7,format=ticker.FuncFormatter(fmt)) 
    return cb   
            
cb0 = add_colorbar(CS1,ax0)
cb1 = add_colorbar(CS2,ax1)    
 
plt.show()                              
