# Ice BROM pictures 
## About the code 
The repository consists of three GUI for visualisation the results of 1D transport model SPBM
https://www.researchgate.net/publication/317901682_Simultaneous_simulation_of_sea_ice-water-sediments_biogeochemistry 

All scripts are written on Python3
Additionally to standard python libraries the script uses:
1. PyQt5 https://www.riverbankcomputing.com/software/pyqt/download5 
1. netCDF4 http://unidata.github.io/netcdf4-python/

### ice_water_sediment.py
This Gui plots all three domains (sediment, water and ice)
### ice_water.py
This Gui plots only water and ice
### difference.py
This Gui is made for visualizing the results of modelling experiments. 
It calculates the differences between experiment file and baseline file, 
and plots this difference
Only water and ice for now
## How to use 
1. After running any of the scripts, the dialogue window will be opened
You must choose the folder containing the output from IPBM, 
three files: ice.nc, water.nc, sediment.nc  
In the difference.py, it should be the folder containing ice.nc, water.nc and folder for the baseline(baseline/ice.nc, baseline/water.nc)
1. On the left panel, you should choose the element you want to plot
All variables available in the nc file are on this panel. 
1. After choosing the element just click "plot"
1. If you click "values(table) you will get the table with for the chosen variable

## Figure adjustments
* By default, the first available year is plotted, you can change it, using spinboxes "Start year" and "Stop year" 
* You can type the desired figure name at the 'qlineedit' widget, it will be added if you click on "Change title" checkbox


