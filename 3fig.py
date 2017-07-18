'''
Created on 28. jun. 2017

@author: ELP
'''

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy.ma as ma


# Here you can change the filenames 
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
    data_units = fh.variables[name].units
    return var_ice,var_water,var_sediments,name,data_units
    fh.close()

 
###########################
#  it's a place for you   #
#  to change the variable #
#  you want to plot       #
########################### 

 

#data = read_var('P1_Chl')
#data = read_var('B_pH_pH')
#data = read_var('B_BIO_DON')
#data = read_var('B_BIO_O2')
data = read_var('B_NUT_Si')

var_ice = data[0]
var_water = data[1]
var_sed = data[2]
name = data[3]
data_units = data[4]

# interpolate data to plot                         
X,Y = np.meshgrid(time,depth_ice)
X_water,Y_water = np.meshgrid(time,depth_water)
X_sed, Y_sed = np.meshgrid(time,depth_sed)

#create a figure 
fig = plt.figure(figsize=(11.69 , 8.27), dpi=100)
gs = gridspec.GridSpec(3, 1)

#update the layout 
gs.update(left=0.1, right= 1.03,top = 0.95,bottom = 0.08,
                   wspace=0.2,hspace=0.2)

#add subplots
ax0 = fig.add_subplot(gs[0]) # o2 ice 
ax0.set_ylabel("Ice thickness (cm) ")

ax1 = fig.add_subplot(gs[1]) # o2 water
ax1.set_ylabel("Depth (m) ")

ax2 = fig.add_subplot(gs[2]) # o2 sed
ax2.set_ylabel("Depth (m) ")
# set xaxis label  
ax2.set_xlabel("number of day")

#specify colormap
cmap = 'terrain'

#min = ma.min(var_ice)
#max = ma.max(var_ice)
#var_levels = np.linspace(min,max,num = 20 )

#plot 2d figures 
#CS1 = ax0.contourf(X,Y, var_ice,cmap = cmap) #,levels = var_levels)
CS1 = ax0.pcolor(X,Y,var_ice)
ax0.set_title(name+' '+ str(data_units))

#add colorbar 
plt.colorbar(CS1,ax = ax0,pad=0.02,aspect = 4)

CS4 = ax1.pcolor(X_water,Y_water, var_water, cmap = cmap)
ax1.set_title(name +' '+ str(data_units))
plt.colorbar(CS4,ax = ax1,pad=0.02,aspect = 4)


CS7 = ax2.pcolor(X_sed,Y_sed, var_sed, cmap = cmap)
ax2.set_title(name+' '+ str(data_units))
plt.colorbar(CS7,ax = ax2,pad=0.02,aspect = 4)


for axis in (ax0,ax1,ax2): 
    axis.yaxis.set_label_coords(-0.06, 0.6)

ax1.set_ylim(max_water,min_water)


ax2.set_ylim(max_sed,min_sed)  

# hide horizontal axis labels 
ax0.set_xticklabels([])    
ax1.set_xticklabels([])     



plt.show()    

#plt.savefig('ice_brom.pdf', format='pdf')

# Save in a vector format 
#plt.savefig('ice_brom.eps', format='eps')
