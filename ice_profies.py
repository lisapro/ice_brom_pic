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

#root = tk.Tk()
#root.withdraw()
#file = askopenfilename() 
file = r'E:\Users\Shamil\binary\laptev\ice.nc'
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
#
print (max(depth))


#print (depth,depth_ice)
#print (min_ice,max_ice,max_faces,min_faces)
depth_ice_faces = (depth_faces)*(ice_res) 
#np.array(
#    (depth_faces - max_faces)*-ice_res)

cmap = plt.get_cmap('viridis') 

name = 'O2_o'
day = 10

var_ice =  ma.masked_invalid (
    np.array(fh_ice.variables[name][day]))

def find_max(var_ice):
    indices = ma.nonzero(var_ice)
    max_ind = np.max(indices)
    return max_ind

max_ind = find_max(var_ice)
depth_ice = (depth - depth[max_ind])*(ice_res)
#print (depth[max_ind],max_ind) 
      
figure = plt.figure(figsize=(8.3 ,4.4), dpi=100,
                    facecolor='None',edgecolor='None') 
gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right= 0.95,top = 0.95,bottom = 0.06,
                   wspace=0.2,hspace=0.2)

#add subplots
ax0 = figure.add_subplot(gs[0])
ax1 = figure.add_subplot(gs[1]) 
ax2 = figure.add_subplot(gs[2]) 
ax3 = figure.add_subplot(gs[3])
ax4 = figure.add_subplot(gs[4]) 
ax5 = figure.add_subplot(gs[5]) 


ax0.set_ylim(150,0)
CS1 = ax0.plot(var_ice[:],depth_ice)#) 3,edgecolor = 'w',
                         #linewidth = 0.000005)
plt.show()