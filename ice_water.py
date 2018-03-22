
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

figure = plt.figure(figsize=(8.3 , 6.9),dpi=100,
                        facecolor='None',edgecolor='None') 

font = {#'family' : 'normal',
        #'weight' : 'bold',
        'size'   : 9}

rc('font', **font)

#directory =  askdirectory() 
directory = r'E:\Users\Shamil\binary\laptev_ersem'
ice_fname = os.path.abspath(os.path.join(directory,'ice.nc')) 
water_fname = os.path.join(directory,'water.nc')


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

chl_name = 'total_chlorophyll_calculator_result'
chl_ice =  ma.masked_invalid (np.array(fh_ice.variables[chl_name][start:stop,:]).T)
chl_water = np.array(fh_water.variables[chl_name][start:stop,:]).T 

pH_ice = ma.masked_invalid (np.array(fh_ice.variables['B_pH_pH'][start:stop,:]).T)
pH_water = np.array(fh_water.variables['B_pH_pH'][start:stop,:]).T 

o2_ice = ma.masked_invalid (np.array(fh_ice.variables['O2_o'][start:stop,:]).T)
o2_water = np.array(fh_water.variables['O2_o'][start:stop,:]).T 

si_ice = ma.masked_invalid (np.array(fh_ice.variables['N5_s'][start:stop,:]).T)
si_water = np.array(fh_water.variables['N5_s'][start:stop,:]).T 

po4_ice = ma.masked_invalid (np.array(fh_ice.variables['N1_p'][start:stop,:]).T)
po4_water = np.array(fh_water.variables['N1_p'][start:stop,:]).T 

no3_ice = ma.masked_invalid (np.array(fh_ice.variables['N3_n'][start:stop,:]).T)
no3_water = np.array(fh_water.variables['N3_n'][start:stop,:]).T 


depth_water = np.array(fh_water.variables['z_faces'][:])*100
min_water = np.amin(depth_water)
max_water = np.amax(depth_water)


X,Y = np.meshgrid(time2[start:stop],depth_ice_faces)
X  = num2date(X,units = time_units) #format_time  
start_f = num2date(time2[start],units = time_units) 
stop_f = num2date(time2[stop],units = time_units)
 
fh_ice.close()
fh_water.close()

gs0 = gridspec.GridSpec(3, 2)
gs0.update(left=0.1, right= 0.95,top = 0.94,bottom = 0.075,
                   wspace=0.24,hspace=0.3)




#gs = gridspec.GridSpec(2, 1)
#gs.update(left=0.15, right= 0.95,top = 0.95,bottom = 0.06,
#                   wspace=0,hspace=0.01)
                   #
dy = 0.04

gs = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[0],hspace=dy)
gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[1],hspace=dy)
gs2 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[2],hspace=dy)
gs3 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[3],hspace=dy)
gs4 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[4],hspace=dy)
gs5 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[5],hspace=dy)



#add subplots
ax0 = figure.add_subplot(gs[0]) # o2 ice 
ax1 = figure.add_subplot(gs[1]) # o2 water 

ax0_1 = figure.add_subplot(gs1[0]) # o2 ice 
ax1_1 = figure.add_subplot(gs1[1]) # o2 water 


ax0_2 = figure.add_subplot(gs2[0]) # o2 ice 
ax1_2 = figure.add_subplot(gs2[1]) # o2 water 

ax0_3 = figure.add_subplot(gs3[0]) # o2 ice 
ax1_3 = figure.add_subplot(gs3[1]) # o2 water 

ax0_4 = figure.add_subplot(gs4[0]) # o2 ice 
ax1_4 = figure.add_subplot(gs4[1]) # o2 water

ax0_5 = figure.add_subplot(gs5[0]) # o2 ice 
ax1_5 = figure.add_subplot(gs5[1]) # o2 water

for axis in (ax1,ax1_1,ax1_2,ax1_3,ax1_4,ax1_5):
    axis.set_ylim(100,0) 
    axis.set_yticks((20,40,60,80,100))
    axis.xaxis.set_major_formatter(
            mdates.DateFormatter('%d.%m'))
    axis.set_ylabel('water depth \ncm')
    
ax1_4.set_xlabel('day,month')    
ax1_5.set_xlabel('day,month')   
  
ax0.set_title(r'$\mathrm{Chlorophyll\ a\ mg* m ^{-3}}$')    
ax0_1.set_title(r'$\mathrm{ pH }$') 
ax0_2.set_title(r'$\mathrm{ O_2\ \mu M}$')
ax0_3.set_title(r'$\mathrm{ Si\ \mu M}$')
ax0_4.set_title(r'$\mathrm{ PO_4\ \mu M}$')
ax0_5.set_title(r'$\mathrm{ NO_3\ \mu M}$')

for axis in (ax0,ax0_1,ax0_2,ax0_3,ax0_4,ax0_5):
    axis.set_ylim(0,100)
    axis.set_xticks([])
    axis.set_ylabel('ice thickness \ncm')
    axis.set_yticks((0,20,40,60,80,100))

cmap = plt.get_cmap('viridis')
cmap_water = plt.get_cmap('CMRmap') #inferno 'gnuplot'
X_water,Y_water = np.meshgrid(time2[start:stop],depth_water)
X_water = num2date(X_water,units = time_units)  

CS1 = ax0.pcolor(X,Y,chl_ice[:,:],
                 cmap = cmap )#) 3,edgecolor = 'w',

CS2 = ax1.pcolor(X_water,Y_water,chl_water[:,:],
                  cmap = cmap_water)

CS1_1 = ax0_1.pcolor(X,Y,pH_ice[:,:],
                 cmap = cmap )
CS2_1 = ax1_1.pcolor(X_water,Y_water,pH_water[:,:],
                  cmap = cmap_water)

CS1_2 = ax0_2.pcolor(X,Y,o2_ice[:,:],
                 cmap = cmap )
CS2_2 = ax1_2.pcolor(X_water,Y_water,o2_water[:,:],
                  cmap = cmap_water)

CS1_3 = ax0_3.pcolor(X,Y,si_ice[:,:],
                 cmap = cmap )
CS2_3 = ax1_3.pcolor(X_water,Y_water,si_water[:,:],
                  cmap = cmap_water)

CS1_4 = ax0_4.pcolor(X,Y,po4_ice[:,:],
                 cmap = cmap )
CS2_4 = ax1_4.pcolor(X_water,Y_water,po4_water[:,:],
                  cmap = cmap_water)

CS1_5 = ax0_5.pcolor(X,Y,no3_ice[:,:],
                 cmap = cmap )
CS2_5 = ax1_5.pcolor(X_water,Y_water,no3_water[:,:],
                  cmap = cmap_water)

import matplotlib.ticker as ticker

def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)         

def add_colorbar(CS,axis,ticks = False):
    if ticks == False: 
        cb = plt.colorbar(CS,ax = axis,pad=0.01,shrink = 0.9,
                 aspect = 7) #,format=ticker.FuncFormatter(fmt)
    else: 
        cb = plt.colorbar(CS,ax = axis,pad=0.01,shrink = 0.9,
                 ticks=ticks,aspect = 7) #,format=ticker.FuncFormatter(fmt)
            
    return cb   
            
cb0 = add_colorbar(CS1,ax0)
cb1 = add_colorbar(CS2,ax1,[0.1,0.4,0.7,1,1.3,1.6])    

cb0 = add_colorbar(CS1_1,ax0_1)
cb1 = add_colorbar(CS2_1,ax1_1)  

cb0 = add_colorbar(CS1_2,ax0_2,[0,20,40,60,80,100])
cb1 = add_colorbar(CS2_2,ax1_2,[210,230,250,270,290])  

cb0 = add_colorbar(CS1_3,ax0_3)
cb1 = add_colorbar(CS2_3,ax1_3)
                   
cb0 = add_colorbar(CS1_4,ax0_4)
cb1 = add_colorbar(CS2_4,ax1_4)
                   
cb0 = add_colorbar(CS1_5,ax0_5)
cb1 = add_colorbar(CS2_5,ax1_5)                                      

plt.show()                              
