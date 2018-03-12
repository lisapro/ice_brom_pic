import matplotlib.pyplot as plt
import datetime 
from netCDF4 import Dataset,num2date,date2num,date2index
import os
import tkinter as tk # python3
from tkinter.filedialog import askopenfilename,askdirectory
import numpy as np
from matplotlib import gridspec
import numpy.ma as ma



start = 0
stop = 365

root = tk.Tk()
root.withdraw()
file = askopenfilename() 
fh_ice =  Dataset(file)
units = fh_ice.variables['time'].units 
time = fh_ice.variables['time'][start:stop]
time_units = fh_ice.variables['time'].units
format_time = num2date(time,units = units,
                       calendar= 'standard')

ice_res = 6
depth = fh_ice.variables['z'][:]
depth_faces = fh_ice.variables['z_faces'][:]
min_ice = np.min(depth)
max_ice = np.max(depth)
max_faces = np.max(depth_faces)
min_faces = np.min(depth_faces)

#depth_ice = (depth - max_ice)*(-ice_res) 
#depth_ice_faces = (depth_faces-max_faces )*(-ice_res) 
depth_ice = (depth)*(ice_res)

#print (depth,depth_ice)
#print (min_ice,max_ice,max_faces,min_faces)
depth_ice_faces = (depth_faces)*(ice_res) 
#np.array(
#    (depth_faces - max_faces)*-ice_res)

cmap = plt.get_cmap('viridis') 
X,Y = np.meshgrid(time[:],depth_ice_faces) #start:stop
X  =num2date(X,units = time_units)
name = 'O2_o'
var_ice =  ma.masked_invalid (
    np.array(fh_ice.variables[name][start:stop]).T )
        
figure = plt.figure(figsize=(8.3 ,4.4), dpi=100,
                    facecolor='None',edgecolor='None') 
gs = gridspec.GridSpec(1, 1)
gs.update(left=0.15, right= 0.95,top = 0.95,bottom = 0.06,
                   wspace=0.2,hspace=0.2)

#add subplots
ax0 = figure.add_subplot(gs[0]) # o2 ice 
ax0.set_ylim(max(depth_ice),min(depth_ice))
#ax1 = figure.add_subplot(gs[1]) # o2 water
#ax2 = figure.add_subplot(gs[2]) # o2 sed

CS1 = ax0.pcolor(X,Y,var_ice[:,:],cmap = cmap )#) 3,edgecolor = 'w',
                         #linewidth = 0.000005)
plt.legend()
plt.colorbar(CS1)
plt.show()