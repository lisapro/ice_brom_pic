'''
Created on 28. jun. 2017

@author: ELP
'''
import os
from PyQt5 import QtWidgets,QtGui, QtCore
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
# Here you can change the filenames 
laptev = False #True
kara = False #False 
open = True
import sys
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure(figsize=(8.3 ,4.4), dpi=100,
                        facecolor='None',edgecolor='None')        
        self.canvas = FigureCanvas(self.figure)         
        '''
        if laptev:
            fh =  Dataset('/Users/Shamil/binary/brom+ersem_laptev/ice.nc')
            fh_water =  Dataset('/Users/Shamil/binary/brom+ersem_laptev/water.nc')
            fh_sediments =  Dataset('/Users/Shamil/binary/brom+ersem_laptev/sediments.nc')
        elif kara:
            fh =  Dataset('/Users/Shamil/binary/test/ice.nc')
            fh_water =  Dataset('/Users/Shamil/binary/test/water.nc') 
            fh_sediments =  Dataset('/Users/Shamil/binary/test/sediments.nc')
        elif open: '''
   
        directory =  self.load_work_directory() 
        ice_fname = os.path.join(directory,'ice.nc')
        water_fname = os.path.join(directory,'water.nc')
        sediments_fname = os.path.join(directory,'sediments.nc')
        
        self.fh_ice =  Dataset(ice_fname)   
        self.fh_water =  Dataset(water_fname) 
        self.fh_sediments =  Dataset(sediments_fname)   
         
        self.names_vars = [] 
        for names,vars in self.fh_ice.variables.items():
            self.names_vars.append(names)          
            
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
        
        #self.plot_3fig()
        #self.canvas.draw()
        
        
        self.button = QtWidgets.QPushButton('Plot')
        self.save_button = QtWidgets.QPushButton('Plot and Save_pdf')
        self.label_choose_var = QtWidgets.QLabel('Choose variable:')  
        self.qlist_widget = QtWidgets.QListWidget()        
        self.qlist_widget.addItems(self.names_vars)
        
        
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.button,0,0,1,1) 
        layout.addWidget(self.save_button,0,1,1,1)
        layout.addWidget(self.qlist_widget,1,0,1,1)   
        layout.addWidget(self.canvas,1,1,1,4)                                
        self.setLayout(layout)        
        self.button.released.connect(self.call_show_3fig)  
        self.save_button.released.connect(self.call_save_3fig) 
              
    def load_work_directory(self):
        #directory = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        directory = askdirectory()
        return directory #ask_filename
    
    def call_show_3fig(self):
        #print ('in show 3 fig')
        self.action = 'showfigure'
        self.plot_3fig()
     
    def call_save_3fig(self):
        self.action = 'savepdf'
        self.plot_3fig()
        
    def read_var(self):
        print ('readvar')  
        self.name =  str(self.qlist_widget.currentItem().text())
        print (self.name) 
        var_ice_nonmasked = np.array(self.fh_ice.variables[self.name][:]).T 
        var_ice =  ma.masked_invalid (var_ice_nonmasked)
        var_water = np.array(self.fh_water.variables[self.name][:]).T 
        var_sediments = np.array(self.fh_sediments.variables[self.name][:]).T 
        data_units = self.fh_ice.variables[self.name].units
        self.fh_ice.close()
        self.fh_water.close()
        self.fh_sediments.close()
                    
        return var_ice,var_water,var_sediments,data_units
            
    def plot_3fig(self): 
        print (self.action) 
        print ('relased')                
        depth = self.fh_ice.variables['z'][:] 
        depth_faces = self.fh_ice.variables['z_faces'][:] 
        
        max_faces = np.max(depth_faces)
        
        min_ice = np.min(depth)
        max_ice = np.max(depth)
        
        depth_ice = (depth - max_ice)*-3
        depth_ice_faces = np.array((depth_faces - max_faces)*-3)
        
        depth_ice = np.array(depth_ice)
        
        min_ice = np.amin(depth_ice_faces)
        max_ice = np.amax(depth_ice_faces)
        
        depth_water = np.array(self.fh_water.variables['z_faces'][:]) 
        depth_sed = self.fh_sediments.variables['z_faces'][:] 
        
        min_water = np.amin(depth_water)
        max_water = np.amax(depth_water)
        
        min_sed = np.amin(depth_sed)
        max_sed = np.amax(depth_sed)
        
        
        #########################
        # Values for time axis  #
        #########################
        
        time = self.fh_ice.variables['time']
        #print (time)
        time2 = self.fh_ice.variables['time'][:]
        time_units = self.fh_ice.variables['time'].units
        format_time = num2date(time2,units = time_units,calendar= 'standard')
        
        to_start = datetime.datetime(2005,1,1,12,0)
        to_stop= datetime.datetime(2005,2,1,12,0)
        #to_start = datetime.date(2014, 11, 4)
        
        #start = int(np.where(format_time == to_start)[0])
        
        
        start = date2index(to_start, time,#units = time_units,
                            calendar=None, select='nearest')
        stop = date2index(to_stop, time,#units = time_units,
                            calendar=None, select='nearest')
        

        data = self.read_var()
        
        var_ice = data[0]
        var_water = data[1]
        var_sed = data[2]
        data_units = data[3]
        
        print(time2[start:stop])     
                         
        X,Y = np.meshgrid(time2[start:stop],depth_ice_faces)
        X  = num2date(X,units = time_units) #format_time  
        start_f = num2date(time2[start],units = time_units) 
        stop_f = num2date(time2[stop],units = time_units) 
        #X = format_time
        
        X_water,Y_water = np.meshgrid(time2[start:stop],depth_water)
        X_water = num2date(X_water,units = time_units)   
        #X_water = format_time
        
        X_sed, Y_sed = np.meshgrid(time2[start:stop],depth_sed)
        X_sed = num2date(X_sed,units = time_units)   
        #X_sed = format_time
        
        #create a figure 
        #fig = plt.figure(figsize=(8.3 ,4.4), dpi=100)
        gs = gridspec.GridSpec(3, 1)
        gs.update(left=0.15, right= 0.97,top = 0.95,bottom = 0.06,
                           wspace=0.2,hspace=0.2)
        print ('gs')  
        #add subplots
        ax0 = self.figure.add_subplot(gs[0]) # o2 ice 
        ax1 = self.figure.add_subplot(gs[1]) # o2 water
        ax2 = self.figure.add_subplot(gs[2]) # o2 sed
        ###########################
        #  it's a place for you   #
        #  to change the variable #
        #  you want to plot       #
        ########################### 
        #data = read_var('sal')
        #data = read_var('temp')
        #data = read_var('P1_Chl')
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
        # interpolate data to plot            
        
        #ax2.set_xlabel("Date", fontsize=14)
        
        #specify colormap
        #cmap = plt.cm.terrain #'plasma' #'terrain'
        cmap = plt.get_cmap('viridis') 
        min = ma.min(var_ice)
        max = ma.max(var_ice)
        #var_levels = np.linspace(min,max,num = 20 )
        print ('pcolor')
        #plot 2d figures 
        #CS1 = ax0.contourf(X,Y, var_ice[:,start:stop],
        #                   cmap = cmap,levels = var_levels)
        #without interpolation 
        CS1 = ax0.pcolor(X,Y,var_ice[:,start:stop],cmap = cmap )#) 3,edgecolor = 'w',
                         #linewidth = 0.000005)
        
        ax0.set_title((self.name+' '+ str(data_units)))
        
        import matplotlib.ticker as ticker
        print ('fmt')
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
        print ('axhline')
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
        print ('ylim')    
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
        print ('canvas')

        if self.action == 'showfigure' : 
        #    print ("show figure")
            self.canvas.draw()                
        elif self.action == 'savepdf' :
            self.canvas.draw()
            plt.savefig('ice_brom_{}.pdf'.format(self.name), format='pdf')
            
            
    #plt.savefig('ice_brom_{}.png'.format(name),transparent = True)
    #plt.savefig('ice_brom_{}.pdf'.format(name), format='pdf')
    
    # Save in a vector format 
    #plt.savefig('ice_brom_{}.eps'.format(name), format='eps')
    
'''    
if __name__ == '__3fig__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("plastique")
    to3fig = Window()
    to3fig.setStyleSheet("background-color:#dceaed;")
    to3fig.show()
    sys.exit(app.exec_()) '''
  
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    #main.showDialog()
    main.setStyleSheet("background-color:#dceaed;")
    main.show()
    
    sys.exit(app.exec_())    
    
    