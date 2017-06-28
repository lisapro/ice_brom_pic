'''
Created on 28. jun. 2017

@author: ELP
'''

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy.ma as ma

fh =  Dataset("ice_year.nc")
fh_water = Dataset("water_year.nc")
fh_sediments = Dataset("sediments_year.nc")


depth = fh.variables['z'][:] 

min = min(depth)
max = max(depth)
depth_ice = (depth - max)*-3
depth_ice = np.array(depth_ice)

min_ice = np.amin(depth_ice)
max_ice = np.amax(depth_ice)

depth_water = np.array(fh_water.variables['z'][:]) 
depth_sed = fh_sediments.variables['z'][:] 

min_water = np.amin(depth_water)
max_water = np.amax(depth_water)

min_sed = np.amin(depth_sed)
max_sed = np.amax(depth_sed)


time = fh.variables['time'][:]  



def read_var(name):
    var_ice_nonmasked = np.array(fh.variables[name][:]).T 
    var_ice =  ma.masked_invalid (var_ice_nonmasked)
    var_water = np.array(fh_water.variables[name][:]).T 
    var_sediments = np.array(fh_sediments.variables[name][:]).T 
    return var_ice,var_water,var_sediments,name
    fh.close()

 
  
#data = read_var('B_pH_pH')
data = read_var('P1_Chl')


var_ice = data[0]
var_water = data[1]
var_sed = data[2]
name = data[3]
                        
X,Y = np.meshgrid(time,depth_ice)
X_water,Y_water = np.meshgrid(time,depth_water)
X_sed, Y_sed = np.meshgrid(time,depth_sed)


fig = plt.figure(figsize=(11.69 , 8.27), dpi=100)
gs = gridspec.GridSpec(3, 1)

gs.update(left=0.1, right= 1.03,top = 0.95,bottom = 0.04,
                   wspace=0.2,hspace=0.2)


ax0 = fig.add_subplot(gs[0]) # o2 ice 
ax0.set_ylabel("Ice thickness (cm) ")

ax1 = fig.add_subplot(gs[1]) # o2 water
ax1.set_ylabel("Depth (m) ")

ax2 = fig.add_subplot(gs[2]) # o2 sed
ax2.set_ylabel("Depth (m) ")

cmap = 'terrain'
#min = ma.min(var_ice)
#max = ma.max(var_ice)
#var_levels = np.linspace(min,max,num = 20 )

CS1 = ax0.contourf(X,Y, var_ice,cmap = cmap) #,levels = var_levels)
ax0.set_title(name)
plt.colorbar(CS1,ax = ax0,pad=0.02,aspect = 4)

CS4 = ax1.contourf(X_water,Y_water, var_water, cmap = cmap)
ax1.set_title(name)
plt.colorbar(CS4,ax= ax1,pad=0.02,aspect = 4)


CS7 = ax2.contourf(X_sed,Y_sed, var_sed, cmap = cmap)
ax2.set_title(name)
plt.colorbar(CS7,ax= ax2,pad=0.02,aspect = 4)




for axis in (ax0,ax1,ax2): 
    axis.yaxis.set_label_coords(-0.1, 0.6)

ax1.set_ylim(max_water,min_water)
ax1.set_xticklabels([])  

ax2.set_ylim(max_sed,min_sed)  
    

ax0.set_xticklabels([])
   
ax2.set_xlabel("number of day")  
ax2.set_xticklabels([])  
 
 

plt.show()    
#plt.savefig('ice_brom.pdf', format='pdf')
#plt.savefig('ice_brom.eps', format='eps')
