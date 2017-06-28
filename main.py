
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
fname = "ice_year.nc"
fname_water = "water_year.nc"


fh =  Dataset(fname)
fh_water = Dataset(fname_water)
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


algae_ice = np.array(fh.variables['P1_Chl'][:]).T 
algae_water = np.array(fh_water.variables['P1_Chl'][:]).T 

o2_ice = np.array(fh.variables['B_BIO_O2'][:]).T 
o2_water = np.array(fh_water.variables['B_BIO_O2'][:]).T 
o2_sediments = np.array(fh_sediments.variables['B_BIO_O2'][:]).T 
#print(o2_sediments.shape,len(depth_sed))

pH_ice = np.array(fh.variables['B_pH_pH'][:]).T  
pH_water = np.array(fh_water.variables['B_pH_pH'][:]).T  
pH_sediments = np.array(fh_sediments.variables['B_pH_pH'][:]).T  

fh.close()

"""o2_levels = np.linspace(np.nanmin([np.nanmin(o2_sediments),
                np.nanmin(o2_ice), np.nanmin(o2_water)]),
                np.nanmax([np.nanmax(o2_sediments),
                                   np.nanmax(o2_water),
                                   np.nanmax(o2_ice)]),
                        num = 50)"""
pH_levels = np.linspace(7.5,8.5,num = 50 )
#print(algae.shape,len(depth),len(time))
X,Y = np.meshgrid(time,depth_ice)
X_water,Y_water = np.meshgrid(time,depth_water)
X_sed, Y_sed = np.meshgrid(time,depth_sed)

pH_ticks = np.arange(7.,13.0,0.05)
pH_ticks2 = np.arange(7.,13.0,1)

fig = plt.figure(figsize = (7.27, 13.), dpi=100)
gs = gridspec.GridSpec(8, 1)
gs.update(left=0.1, right= 1.03,top = 0.98,bottom = 0.04,
                   wspace=0.2,hspace=0.2)

ax = fig.add_subplot(gs[0]) #alg ice
ax.set_ylabel("Ice thickness (cm) ")


ax3 = fig.add_subplot(gs[1]) #alg water
ax3.set_ylabel("Depth (m) ")
ax1 = fig.add_subplot(gs[2]) # o2 ice 
ax1.set_ylabel("Ice thickness (cm) ")
ax4 = fig.add_subplot(gs[3]) # o2 water
ax4.set_ylabel("Depth (m) ")

ax7 = fig.add_subplot(gs[4]) # o2 sed
ax7.set_ylabel("Depth (m) ")

ax2 = fig.add_subplot(gs[5]) # ph ice
ax2.set_ylabel("Ice thickness (cm) ")

ax5 = fig.add_subplot(gs[6]) # ph water
ax5.set_ylabel("Depth (m) ")

ax8 = fig.add_subplot(gs[7]) # ph sed
ax8.set_ylabel("Depth (m) ")

CS = ax.contourf(X,Y, algae_ice,cmap = 'terrain')
ax.set_title(r'$\rm Diatoms\ chlorophyll\ a,\ mg \cdot m^{-3} \ (ice)$')
plt.colorbar(CS,ax = ax,pad=0.02,aspect = 4) #fraction=0.046, 

CS3 = ax3.contourf(X_water,Y_water, algae_water,cmap = 'terrain')
ax3.set_title(r'$\rm Diatoms\ chlorophyll\ a,\ mg \cdot m^{-3} \ (water)$')
plt.colorbar(CS3,ax = ax3,pad=0.02,aspect = 4)


CS1 = ax1.contourf(X,Y, o2_ice)
ax1.set_title(r'$\rm O _2\  \mu M\ (ice)$')
plt.colorbar(CS1,ax = ax1,pad=0.02,aspect = 4)

CS2 = ax2.contourf(X,Y, pH_ice,cmap = 'jet') #,levels = pH_levels)
ax2.set_title(r'$\rm pH\  (ice)$')
plt.colorbar(CS2,ax= ax2,pad=0.02,aspect = 4) #ticks = pH_ticks2,



CS4 = ax4.contourf(X_water,Y_water, o2_water)
ax4.set_title(r'$\rm O _2\  \mu M\ (water)$')
plt.colorbar(CS4,ax= ax4,pad=0.02,aspect = 4)

CS5 = ax5.contourf(X_water,Y_water, pH_water,cmap = 'jet') #,levels = pH_levels)
ax5.set_title(r'$\rm pH\  (water)$')
plt.colorbar(CS5,ax= ax5, pad=0.02,aspect = 4) #ticks= pH_ticks,

CS7 = ax7.contourf(X_sed,Y_sed, o2_sediments)
ax7.set_title(r'$\rm O _2\  \mu M\ (sediment)$')
plt.colorbar(CS7,ax= ax7,pad=0.02,aspect = 4)

CS8 = ax8.contourf(X_sed,Y_sed, pH_sediments,
                   cmap = 'jet') #, levels = pH_levels,extend="both")
ax8.set_title(r'$\rm pH\  (sediment)$')

cbar = plt.colorbar(CS8,ax= ax8,pad=0.02,aspect = 4) #,ticks= pH_ticks )

for axis in (ax,ax3,ax1,ax4,ax5,ax7,ax8,ax2): 
    axis.yaxis.set_label_coords(-0.1, 0.6)


#cbar.set_clim(-2.0, 50.0)
#ax.set_xlim())

    
 #, levels = wat_levs, extend="both", #int_
                              #cmap= self.cmap)
#plt.scatter(X,Y,c = algae)
#for axis in (ax,ax1,ax2):
#    axis.set_ylim(max_ice,min_ice)
for axis in (ax3,ax4,ax5):
    axis.set_ylim(max_water,min_water)
    axis.set_xticklabels([])  
for axis in (ax7,ax8):
    axis.set_ylim(max_sed,min_sed)  
    
ax.set_xticklabels([])   
ax1.set_xticklabels([])
ax2.set_xticklabels([])        
ax8.set_xlabel("number of day")  
ax7.set_xticklabels([])  
 
 

plt.show()    
#plt.savefig('ice_brom.pdf', format='pdf')
plt.savefig('ice_brom.eps', format='eps')
