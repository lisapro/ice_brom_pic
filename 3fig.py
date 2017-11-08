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
import datetime 
#from datetime import datetime, timedelta

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


#########################
# Values for time axis  #
#########################

time = fh.variables['time']
time2 = fh.variables['time'][:]
time_units = fh.variables['time'].units
format_time = num2date(time2,units = time_units,calendar= 'standard')

to_start = datetime.datetime(2005,1,1,12,0)
to_stop= datetime.datetime(2014,1,1,12,0)
#to_start = datetime.date(2014, 11, 4)

#start = int(np.where(format_time == to_start)[0])


start = date2index(to_start, time,#units = time_units,
                    calendar=None, select='nearest')
stop = date2index(to_stop, time,#units = time_units,
                    calendar=None, select='nearest')


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
X  = num2date(X,units = time_units) #format_time  
start_f = num2date(time[start],units = time_units) 
stop_f = num2date(time[stop],units = time_units) 
#X = format_time

X_water,Y_water = np.meshgrid(time[start:stop],depth_water)
X_water = num2date(X_water,units = time_units)   
#X_water = format_time

X_sed, Y_sed = np.meshgrid(time[start:stop],depth_sed)
X_sed = num2date(X_sed,units = time_units)   
#X_sed = format_time

#create a figure 
fig = plt.figure(figsize=(8.3 ,4.4), dpi=100)
gs = gridspec.GridSpec(3, 1)
gs.update(left=0.15, right= 0.97,top = 0.95,bottom = 0.06,
                   wspace=0.2,hspace=0.2)
#add subplots
ax0 = fig.add_subplot(gs[0]) # o2 ice 
ax1 = fig.add_subplot(gs[1]) # o2 water
ax2 = fig.add_subplot(gs[2]) # o2 sed


#ax2.set_xlabel("Date", fontsize=14)

#specify colormap
#cmap = plt.cm.terrain #'plasma' #'terrain'
cmap = plt.get_cmap('viridis') 
min = ma.min(var_ice)
max = ma.max(var_ice)
#var_levels = np.linspace(min,max,num = 20 )

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
#cb0 = plt.colorbar(CS1,ax = ax0,pad=0.02,
#             aspect = 4,format=ticker.FuncFormatter(fmt))

#CS4 = ax1.contourf(X_water,Y_water, var_water[:,start:stop],
#                   cmap = cmap) 
CS4 = ax1.pcolor(X_water,Y_water,var_water[:,start:stop],
                  cmap = cmap) #,edgecolor = 'w',
                 # linewidth = 0.000005)

#CS7 = ax2.contourf(X_sed,Y_sed, var_sed[:,start:stop],
#                   cmap = cmap) 
CS7 = ax2.pcolor(X_sed,Y_sed,var_sed[:,start:stop], cmap = cmap) #,edgecolor = 'w',
                # linewidth = 0.000005)

ax2.axhline(max_water, color='w', linestyle = '--',linewidth = 1 ) 

from dateutil.relativedelta import relativedelta
if (stop-start)>= 367:
    dt =  int((stop - start)/365) #number of years
    time_ticks = []
    for n in range(0,dt+1):
        time_ticks.append(
            format_time[start]+relativedelta(years = n))


def add_colorbar(CS,axis):
    cb = plt.colorbar(CS,ax = axis,pad=0.02,
             aspect = 4,format=ticker.FuncFormatter(fmt)) 
    return cb

cb0 = add_colorbar(CS1,ax0)
cb1 = add_colorbar(CS4,ax1)
cb2 = add_colorbar(CS7,ax2)

letters = ['A','B','C']
labels = ["Ice thickness \n(cm)", "Depth \n(m)","Depth \n(m)" ]
n = 0

for axis in (ax0,ax1,ax2): 
    try:
        axis.set_xticks(time_ticks)
    except: NameError
    axis.yaxis.set_label_coords(-0.1, 0.6)
    axis.text(-0.085, 0.9, letters[n], transform=axis.transAxes, 
            size=15, weight='bold')
    axis.set_ylabel(labels[n], fontsize=14 )
    n=n+1
    
ax1.set_ylim(max_water,min_water)
ax2.set_ylim(max_sed,min_sed)  
ax0.set_ylim(min_ice,max_ice)

# hide horizontal axis labels 
ax0.set_xticklabels([])    
ax1.set_xticklabels([])     


     
if (stop-start)>= 365*6:
    ax2.xaxis.set_major_formatter(
        mdates.DateFormatter('%Y')) 
    #ticks = np.arange(time[start:stop],time[start:stop],50)
elif (stop-start) > 367 and (stop-start) < 365*6:
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
