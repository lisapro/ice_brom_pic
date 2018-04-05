'''
Created on 28. jun. 2017

@author: ELP
'''
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
#plt.style.use('ggplot')
#plt.style.use('bmh')

import sys
from matplotlib.backends.backend_qt5agg import (
FigureCanvasQTAgg as FigureCanvas)

figure = plt.figure(figsize=(8.3 ,10), dpi=100,
                facecolor='None',edgecolor='None')                
directory =  askdirectory()  

ice_fname = os.path.abspath(os.path.join(directory,'ice.nc')) 
water_fname = os.path.join(directory,'water.nc')
sediments_fname = os.path.join(directory,'sediments.nc')

fh_ice =  Dataset(ice_fname)   
try:
    time = fh_ice.variables['time'][:]
    units = fh_ice.variables['time'].units     
except KeyError: 
    time = fh_ice.variables['ocean_time'][:]
    units = fh_ice.variables['ocean_time'].units                    
format_time = num2date(time,units = units,
                            calendar= 'standard')   
    
#first_year = format_time[0].year
#last_year = format_time[-1].year

#fontsize = 12

     
fh_ice =  Dataset(ice_fname)  
fh_water =  Dataset(water_fname)  
fh_sediments =  Dataset(sediments_fname) 

name1 =  'P1_Chl' #diatoms chlorophyll a
name2 = 'P1_i_Chl' #diatoms ice chlorophyll a
name3 = 'P2_Chl' #nanophytoplankton
name4 = 'P3_Chl' #picophytoplankton
name5 = 'P4_Chl' #mycrophytoplankton


long_name1 = str(fh_ice.variables[str(name1)].long_name)
data_units1 = fh_ice.variables[name1].units   
    
long_name2 = str(fh_ice.variables[str(name2)].long_name)
data_units2 = fh_ice.variables[name2].units

long_name3 = str(fh_ice.variables[str(name3)].long_name)
data_units3 = fh_ice.variables[name3].units

long_name4 = str(fh_ice.variables[str(name4)].long_name)
data_units4 = fh_ice.variables[name4].units

long_name5 = str(fh_ice.variables[str(name5)].long_name)
data_units5 = fh_ice.variables[name5].units         

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
max_ice = np.amax(depth_ice_faces)

depth_water = np.array(fh_water.variables['z_faces'][:])
depth_sed = fh_sediments.variables['z_faces'][:] 

min_water = np.amin(depth_water)
max_water = np.amax(depth_water)

min_sed = np.amin(depth_sed)
max_sed = np.amax(depth_sed)
 
try:
    time = fh_ice.variables['time']      
    time2 = fh_ice.variables['time'][:]
    time_units = fh_ice.variables['time'].units
except KeyError:
    time = fh_ice.variables['ocean_time']   
    time2 = fh_ice.variables['ocean_time'][:]            
    time_units = fh_ice.variables['ocean_time'].units
format_time = num2date(time2,units = time_units,calendar= 'standard')
 
#########################
# Values for time axis  #
#########################
        
#start_year = 1982 #combobox_start_year.value()
#stop_year = 1983 #combobox_stop_year.value()

def calc_date(year):
    x = date2index(datetime.datetime(year,1,1,12,0), time,#units = time_units,
                    calendar=None, select='nearest')
    return x 
start = calc_date(1982)
start2 = calc_date(1984)
stop = start2 
stop2 = calc_date(1984)
#stop = date2index(to_stop, time,#units = time_units,
#                    calendar=None, select='nearest')        

var_ice =  ma.masked_invalid (
    np.array(fh_ice.variables[name1][:]).T )
var_water = np.array(
    fh_water.variables[name1][:]).T 

var2_ice =  ma.masked_invalid (
    np.array(fh_ice.variables[name2][:]).T )
var2_water = np.array(
    fh_water.variables[name2][:]).T          

var3_ice =  ma.masked_invalid (
    np.array(fh_ice.variables[name3][:]).T )
var3_water = np.array(
    fh_water.variables[name3][:]).T 
    
var4_ice =  ma.masked_invalid (
    np.array(fh_ice.variables[name4][:]).T )
var4_water = np.array(
    fh_water.variables[name4][:]).T 
    
var5_ice =  ma.masked_invalid (
    np.array(fh_ice.variables[name5][:]).T )
var5_water = np.array(
    fh_water.variables[name5][:]).T         

X,Y = np.meshgrid(time2[start:stop],depth_ice_faces)
X  = num2date(X,units = time_units) #format_time  
start_f = num2date(time2[start],units = time_units) 
stop_f = num2date(time2[stop],units = time_units) 
#X = format_time

X_water,Y_water = np.meshgrid(time2[start:stop],depth_water)
X_water = num2date(X_water,units = time_units)   
#X_water = format_time

#X_sed, Y_sed = np.meshgrid(time2[start:stop],depth_sed)
#X_sed = num2date(X_sed,units = time_units)   
#X_sed = format_time
fh_ice.close()
fh_water.close()
#fh_sediments.close()          

gs0 = gridspec.GridSpec(5, 1) #,aspect = [1,2])

gs0.update(left=0.1, right= 1,top = 0.96,bottom = 0.05,
                   wspace=0.15,hspace=0.15)
dy = 0.04

gs1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[0],hspace=dy)
#gs1_1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[1],hspace=dy)

gs2 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[1],hspace=dy)
#gs2_1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[3],hspace=dy)

gs3 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[2],hspace=dy)
#gs3_1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[5],hspace=dy)

gs4 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[3],hspace=dy)
#gs4_1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[7],hspace=dy)

gs5 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[4],hspace=dy)
#gs5_1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs0[9],hspace=dy)
#add subplots
ax1 = figure.add_subplot(gs1[1]) 
ax1_i = figure.add_subplot(gs1[0]) 

#ax1_1 = figure.add_subplot(gs1_1[1]) 
#ax1_1_i = figure.add_subplot(gs1_1[0])

ax2 = figure.add_subplot(gs2[1]) 
ax2_i = figure.add_subplot(gs2[0]) 

#ax2_1 = figure.add_subplot(gs2_1[1]) 
#ax2_1_i = figure.add_subplot(gs2_1[0])

ax3 = figure.add_subplot(gs3[1]) 
ax3_i = figure.add_subplot(gs3[0]) 

#ax3_1 = figure.add_subplot(gs3_1[1]) 
#ax3_1_i = figure.add_subplot(gs3_1[0])

ax4 = figure.add_subplot(gs4[1]) 
ax4_i = figure.add_subplot(gs4[0]) 

#ax4_1 = figure.add_subplot(gs4_1[1]) 
#ax4_1_i = figure.add_subplot(gs4_1[0])

ax5 = figure.add_subplot(gs5[1]) 
ax5_i = figure.add_subplot(gs5[0]) 

#ax5_1 = figure.add_subplot(gs5_1[1]) 
#ax5_1_i = figure.add_subplot(gs5_1[0])    
      
cmap = plt.get_cmap('gist_ncar') #gist_stern
cmap_water = plt.get_cmap('viridis') 
min = ma.min(var_water)
max = ma.max(var_water)
from matplotlib import rc
font = {'size' : 8}
rc('font', **font)
#var_levels = np.linspace(min,max,num = 20 )

#plot 2d figures 
#CS1 = ax0.contourf(X,Y, var_ice[:,start:stop],
#                   cmap = cmap,levels = var_levels)
#without interpolation 
CS1 = ax1_i.pcolor(X,Y,var_ice[:,start:stop],cmap = cmap )
#CS1_1 = ax1_1_i.pcolor(X,Y,var_ice[:,start2:stop2],cmap = cmap )
CS1w = ax1.pcolor(X_water,Y_water,var_water[:,start:stop],cmap = cmap_water )
#CS1w_1 = ax1_1.pcolor(X_water,Y_water,var_water[:,start2:stop2],cmap = cmap_water )
                
CS2 = ax2_i.pcolor(X,Y,var2_ice[:,start:stop],cmap = cmap )
#CS2_1 = ax2_1_i.pcolor(X,Y,var2_ice[:,start2:stop2],cmap = cmap )    
CS2w = ax2.pcolor(X_water,Y_water,var2_water[:,start:stop],cmap = cmap_water )
#CS2w_1 = ax2_1.pcolor(X_water,Y_water,var2_water[:,start2:stop2],cmap = cmap_water ) 

CS3 = ax3_i.pcolor(X,Y,var3_ice[:,start:stop],cmap = cmap )
#CS3_1 = ax3_1_i.pcolor(X,Y,var3_ice[:,start2:stop2],cmap = cmap ) 
CS3w = ax3.pcolor(X_water,Y_water,var3_water[:,start:stop],cmap = cmap_water )
#CS3w_1 = ax3_1.pcolor(X_water,Y_water,var3_water[:,start2:stop2],cmap = cmap_water ) 

CS4 = ax4_i.pcolor(X,Y,var4_ice[:,start:stop],cmap = cmap )
#CS4_1 = ax4_1_i.pcolor(X,Y,var4_ice[:,start2:stop2],cmap = cmap ) 
CS4w = ax4.pcolor(X_water,Y_water,var4_water[:,start:stop],cmap = cmap_water )
#CS4w_1 = ax4_1.pcolor(X_water,Y_water,var4_water[:,start2:stop2],cmap = cmap_water ) 

CS5 = ax5_i.pcolor(X,Y,var5_ice[:,start:stop],cmap = cmap )
#CS5_1 = ax5_1_i.pcolor(X,Y,var5_ice[:,start2:stop2],cmap = cmap ) 
CS5w = ax5.pcolor(X_water,Y_water,var5_water[:,start:stop],cmap = cmap_water )
#CS5w_1 = ax5_1.pcolor(X_water,Y_water,var5_water[:,start2:stop2],cmap = cmap_water ) 
             

    
import matplotlib.ticker as ticker

def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)

#CS1_w = ax1_1.pcolor(X_water,Y_water,var_water[:,start:stop],
#                  cmap = cmap_water) 
#CS1_w = ax3.pcolor(X_water,Y_water,var_water[:,start2:stop2],
#                  cmap = cmap_water) 
### Time ticks ### 
from dateutil.relativedelta import relativedelta
if (stop-start)>= 367:
    dt =  int((stop - start)/365) #number of years
    time_ticks = []
    for n in range(0,dt+1):
        time_ticks.append(
            format_time[start]+relativedelta(years = n))


def add_colorbar(CS,axis,ma1):

    if ma1 > 10000 or ma1 < 0.001:
        cb = plt.colorbar(CS,ax = axis, #pad=0.5,
             aspect = 7,format=ticker.FuncFormatter(fmt)) 
    else: 
        cb = plt.colorbar(CS,ax = axis,pad=0.01,
             aspect = 7)                     
    return cb
functions = {ax1_i:CS1,ax2_i:CS2,ax3_i:CS3,ax4_i:CS4,ax5_i:CS5,
             #,ax1_1_i:CS1_1,ax2_1_i:CS2_1,ax3_1_i:CS3_1,ax4_1_i:CS4_1,ax5_1_i:CS5_1,
             #,ax1_1:CS1w_1,ax2_1:CS2w_1,ax3_1:CS3w_1,ax4_1:CS4w_1,ax5_1:CS5w_1
             ax1:CS1w,ax2:CS2w,ax3:CS3w,ax4:CS4w,ax5:CS5w} 
#ma1 = ma.max(var_ice[:,start:stop])
for axis in (ax1_i,ax2_i,ax3_i,ax4_i,ax5_i, #ax1_1_i,ax2_1_i,ax3_1_i,ax4_1_i,ax5_1_i,,ax1_1,ax2_1,ax3_1,ax4_1,ax5_1
             ax1,ax2,ax3,ax4,ax5):
   add_colorbar(functions[axis],axis,100) 
#letters = ['(a)','(b)','(c)']
labels = ["Ice (cm)", "water (m)"]
n = 0
    
names = {ax1_i:'diatoms chlorophyll a',ax2_i:'diatoms ice chlorophyll a',
         ax3_i:'nanophytoplankton',ax4_i:'picophytoplankton',ax5_i:'mycrophytoplankton'}
# hide horizontal axis labels 
for axis in (ax1_i,ax2_i,ax3_i,ax4_i,ax5_i): #ax1_1_i,ax2_1_i,ax3_1_i,ax4_1_i,ax5_1_i,
    axis.set_xticklabels([])   
    axis.set_ylim(min_ice,250) #max_ice 
    name = names[axis]
    #print (name)
    #axis.set_title(name)
    plt.text(0.5, 1.08, name,
         horizontalalignment='center',
         #fontsize=20,
         transform = axis.transAxes)
    axis.yaxis.set_label_coords(-0.07, 0.5)
    axis.set_ylabel("Ice (cm)")  
     
for axis in (ax1,ax2,ax3,ax4): #ax1_1_i,ax2_1_i,ax3_1_i,ax4_1_i,ax5_1_i,
    axis.set_xticklabels([])   

for axis in (ax1,ax2,ax3,ax4,ax5):    #,ax1_1,ax2_1,ax3_1,ax4_1,ax5_1 
    axis.set_ylim(max_water,min_water)
    axis.yaxis.set_label_coords(-0.07, 0.5)
    axis.set_ylabel("Water (m)") #, fontsize = fontsize)

ax5.xaxis.set_major_formatter(
    mdates.DateFormatter('%m')) 

  
plt.show()

# Save in a vector format 
#plt.savefig('ice_brom_{}.eps'.format(name), format='eps')
#filename = '{}\ice_brom_{}.png'.format(dir_to_save,name)       
#plt.savefig(results_dir+title+'.png')
#plt.savefig(filename, format='png', dpi=300, transparent=True)
            


