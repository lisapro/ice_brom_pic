'''
Created on 28. jun. 2017

@author: ELP
'''

from netCDF4 import Dataset,num2date,date2num,date2index
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.dates as mdates

#plt.style.use('ggplot')
#plt.style.use('bmh')
# Here you can change the filenames 
laptev = False #True
kara = True #False 

#fh =  Dataset("ice_year.nc")
#fh_water = Dataset("water_year.nc")
#fh_sediments = Dataset("sediments_year.nc")
if laptev:
    fh =  Dataset('/Users/Shamil/binary/brom+ersem_laptev/ice.nc')
    fh_water =  Dataset('/Users/Shamil/binary/brom+ersem_laptev/water.nc')
    fh_sediments =  Dataset('/Users/Shamil/binary/brom+ersem_laptev/sediments.nc')
if kara:
    fh =  Dataset('/Users/Shamil/binary/test/ice.nc')
    fh_water =  Dataset('/Users/Shamil/binary/test/water.nc') 
    fh_sediments =  Dataset('/Users/Shamil/binary/test/sediments.nc')

depth = fh.variables['z'][:] 
depth_faces = fh.variables['z_faces'][:] 

max_faces = max(depth_faces)

min = min(depth)
max = max(depth)

depth_ice = (depth - max)*-3
depth_ice_faces = np.array((depth_faces - max_faces)*-3)

depth_ice = np.array(depth_ice)

min_ice = np.amin(depth_ice_faces)
max_ice = np.amax(depth_ice_faces)

depth_water = np.array(fh_water.variables['z_faces'][:]) 
depth_sed = fh_sediments.variables['z_faces'][:] 

min_water = np.amin(depth_water)
max_water = np.amax(depth_water)

min_sed = np.amin(depth_sed)
max_sed = np.amax(depth_sed)
from datetime import datetime, timedelta
#########################
# Values for time axis  #
#########################

time = fh.variables['time']
time_units = fh.variables['time'].units
#start= date2index(start_date, time, calendar= 'standard')
                  #,
                  #    select='exact') 

#start = np.argwhere(time == start_x)
start = 1447
stop = 1500
#stop = len(time)-1

def read_var(name):
    
    var_ice_nonmasked = np.array(fh.variables[name][:]).T 
    var_ice =  ma.masked_invalid (var_ice_nonmasked)
    var_water = np.array(fh_water.variables[name][:]).T 
    var_sediments = np.array(fh_sediments.variables[name][:]).T 
    data_units = fh.variables[name].units
    return var_ice,var_water,var_sediments,name,data_units
    fh.close()

 
###########################
#  it's a place for you   #
#  to change the variable #
#  you want to plot       #
########################### 
#data = read_var('sal')
#data = read_var('temp')
data = read_var('P1_Chl')
#data = read_var('B_pH_pH')
#data = read_var('B_BIO_DON')
#data = read_var('P1_fO3PIc')
#data = read_var('P4_Chl')
#data = read_var('B_pH_pH')
#data = read_var('B_BIO_DON')
#data = read_var('B_BIO_O2')
#data = read_var('B_NUT_Si')
#data = read_var('temp')
#data = read_var('Kz_s')
#data = read_var('downwelling_photosynthetic_radiative_flux')
#data = read_var('B_BIO_O2')
#data = read_var('B_NUT_Si')

var_ice = data[0]
var_water = data[1]
var_sed = data[2]
name = data[3]
data_units = data[4]

# interpolate data to plot                         
X,Y = np.meshgrid(time[start:stop],depth_ice_faces)
format_time = num2date(X,units = time_units)  
start_f = num2date(time[start],units = time_units) 
stop_f = num2date(time[stop],units = time_units) 
X = format_time

X_water,Y_water = np.meshgrid(time[start:stop],depth_water)
format_time = num2date(X_water,units = time_units)   
X_water = format_time

X_sed, Y_sed = np.meshgrid(time[start:stop],depth_sed)
format_time = num2date(X_sed,units = time_units)   
X_sed = format_time

#create a figure 
fig = plt.figure(figsize=(8.3 ,4.4), dpi=100)
gs = gridspec.GridSpec(3, 1)

#update the layout 
gs.update(left=0.1, right= 0.95,top = 0.95,bottom = 0.05,
                   wspace=0.2,hspace=0.2)

#add subplots
ax0 = fig.add_subplot(gs[0]) # o2 ice 
ax0.set_ylabel("Ice thickness \n(cm)", fontsize=14)
ax0.text(-0.07, 1.05, 'A', transform=ax0.transAxes, 
            size=15, weight='bold')

ax1 = fig.add_subplot(gs[1]) # o2 water
ax1.set_ylabel("Depth \n(m)", fontsize=14)
ax1.text(-0.07, 1.05, 'B', transform=ax1.transAxes, 
            size=15, weight='bold')

ax2 = fig.add_subplot(gs[2]) # o2 sed
ax2.set_ylabel("Depth \n(m)", fontsize=14)
ax2.text(-0.07, 1.05, 'C', transform=ax2.transAxes, 
            size=15, weight='bold')
# set xaxis label  
#ax2.set_xlabel("Date", fontsize=14)

#specify colormap
cmap = plt.cm.terrain #'plasma' #'terrain'

min = ma.min(var_ice)
max = ma.max(var_ice)
var_levels = np.linspace(min,max,num = 40 )

#plot 2d figures 
#CS1 = ax0.contourf(X,Y, var_ice[:,start:stop],
#                   cmap = cmap,levels = var_levels)
#without interpolation 
CS1 = ax0.pcolor(X,Y,var_ice[:,start:stop],cmap = cmap )#) 3,edgecolor = 'w',
                 #linewidth = 0.000005)

ax0.set_title((name+' '+ str(data_units)))

import matplotlib.ticker as ticker

def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)

#plt.colorbar(myplot, format=ticker.FuncFormatter(fmt))

#add colorbar 
plt.colorbar(CS1,ax = ax0,pad=0.02,
             aspect = 4,format=ticker.FuncFormatter(fmt))

#CS4 = ax1.contourf(X_water,Y_water, var_water[:,start:stop],
#                   cmap = cmap) 
CS4 = ax1.pcolor(X_water,Y_water,var_water[:,start:stop],
                  cmap = cmap) #,edgecolor = 'w',
                 # linewidth = 0.000005)

ax1.axhline(151.5, color='white', 
            linestyle = '--',linewidth = 1 )
#ax1.set_title(name +' '+ str(data_units))


plt.colorbar(CS4,ax = ax1,pad=0.02,
             aspect = 4, format=ticker.FuncFormatter(fmt))

#CS7 = ax2.contourf(X_sed,Y_sed, var_sed[:,start:stop],
#                   cmap = cmap) 
CS7 = ax2.pcolor(X_sed,Y_sed,var_sed[:,start:stop], cmap = cmap) #,edgecolor = 'w',
                # linewidth = 0.000005)
ax2.axhline(151.53, color='w', linestyle = '--',linewidth = 1 ) 
#ax2.set_title(name+' '+ str(data_units))


plt.colorbar(CS7,ax = ax2,pad=0.02,
             aspect = 4,format=ticker.FuncFormatter(fmt))


for axis in (ax0,ax1,ax2): 
    axis.yaxis.set_label_coords(-0.06, 0.6)

ax1.set_ylim(max_water,min_water)
ax2.set_ylim(max_sed,min_sed)  
ax0.set_ylim(min_ice,max_ice)

# hide horizontal axis labels 
ax0.set_xticklabels([])    
ax1.set_xticklabels([])     
labels = ax2.get_xticklabels()
#plt.setp(labels, rotation=30, size = 14) #rotation=30,


if stop-start > 365:
    #ax1.xaxis_date()
    ax2.xaxis.set_major_formatter(
        mdates.DateFormatter('%m/%Y'))  
else : 
    ax2.xaxis.set_major_formatter(
        mdates.DateFormatter('%b')) 
      
#plt.rcParams.update({'font.size': 14})
plt.show()    
#plt.savefig('ice_brom_{}.png'.format(name),transparent = True)
#plt.savefig('ice_brom_{}.pdf'.format(name), format='pdf')

# Save in a vector format 
#plt.savefig('ice_brom_{}.eps'.format(name), format='eps')
