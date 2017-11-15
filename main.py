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
        self.ice_fname = os.path.abspath(os.path.join(directory,'ice.nc')) 

        self.water_fname = os.path.join(directory,'water.nc')
        self.sediments_fname = os.path.join(directory,'sediments.nc')
        
        self.fh_ice =  Dataset(self.ice_fname)   

        

        
        
        self.time = self.fh_ice.variables['time'][:]
        units = self.fh_ice.variables['time'].units        
        self.format_time = num2date(self.time,units = units,
                                    calendar= 'standard')       
        first_year = self.format_time[0].year
        last_year = self.format_time[-1].year
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
          
        self.label_start_year = QtWidgets.QLabel('Start year:') 
        self.combobox_start_year = QtWidgets.QSpinBox()    
        self.combobox_start_year.setRange(first_year, last_year-1)                 
        self.label_stop_year = QtWidgets.QLabel('Stop year:')   
        self.combobox_stop_year = QtWidgets.QSpinBox() 
        self.combobox_stop_year.setRange(first_year+1, last_year)                        
        self.qlist_widget = QtWidgets.QListWidget()        
        self.qlist_widget.addItems(self.names_vars)
        
        
        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.label_choose_var,0,0,1,1)                 
        layout.addWidget(self.button,0,1,1,1)         
        layout.addWidget(self.save_button,0,2,1,1)
        layout.addWidget(self.label_start_year,0,3,1,1)
        layout.addWidget(self.combobox_start_year,0,4,1,1)        
        layout.addWidget(self.label_stop_year,0,5,1,1)
        layout.addWidget(self.combobox_stop_year,0,6,1,1)                
                        
        layout.addWidget(self.qlist_widget,1,0,1,1)      
        layout.addWidget(self.canvas,1,1,1,6)    
                                    
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

        self.name =  str(self.qlist_widget.currentItem().text())
        var_ice_nonmasked = np.array(self.fh_ice.variables[self.name][:]).T 
        var_ice =  ma.masked_invalid (var_ice_nonmasked)
        var_water = np.array(self.fh_water.variables[self.name][:]).T 
        var_sediments = np.array(self.fh_sediments.variables[self.name][:]).T 
        data_units = self.fh_ice.variables[self.name].units

                    
        return var_ice,var_water,var_sediments,data_units
            
    def plot_3fig(self): 
       
        plt.clf() 
             
        self.fh_ice =  Dataset(self.ice_fname)  
        self.fh_water =  Dataset(self.water_fname)  
        self.fh_sediments =  Dataset(self.sediments_fname) 
                    
        self.time = self.fh_ice.variables['time']

        self.depth = self.fh_ice.variables['z'][:] 
        self.depth_faces = self.fh_ice.variables['z_faces'][:] 
           
        self.max_faces = np.max(self.depth_faces)
        
        self.min_ice = np.min(self.depth)
        self.max_ice = np.max(self.depth)
        
        self.depth_ice = (self.depth - self.max_ice)*-3
        self.depth_ice_faces = np.array((self.depth_faces - self.max_faces)*-3)
        
        self.depth_ice = np.array(self.depth_ice)
        
        self.min_ice = np.amin(self.depth_ice_faces)
        self.max_ice = np.amax(self.depth_ice_faces)
        
        self.depth_water = np.array(self.fh_water.variables['z_faces'][:]) 
        self.depth_sed = self.fh_sediments.variables['z_faces'][:] 
        
        self.min_water = np.amin(self.depth_water)
        self.max_water = np.amax(self.depth_water)
        
        self.min_sed = np.amin(self.depth_sed)
        self.max_sed = np.amax(self.depth_sed)
        
        self.time2 = self.fh_ice.variables['time'][:]
    
        self.time_units = self.fh_ice.variables['time'].units

        self.format_time = num2date(self.time2,units = self.time_units,calendar= 'standard')
         
               
        
        #########################
        # Values for time axis  #
        #########################
        
        
        start_year = self.combobox_start_year.value()
        stop_year = self.combobox_stop_year.value()
        
        to_start = datetime.datetime(start_year,1,1,12,0)
        to_stop= datetime.datetime(stop_year,1,1,12,0)
        #to_start = datetime.date(2014, 11, 4)
        
        #start = int(np.where(format_time == to_start)[0])
        
        
        start = date2index(to_start, self.time,#units = time_units,
                            calendar=None, select='nearest')
        stop = date2index(to_stop, self.time,#units = time_units,
                            calendar=None, select='nearest')


        data = self.read_var()
        #self.fh_ice.close()         
        var_ice = data[0]
        var_water = data[1]
        var_sed = data[2]
        data_units = data[3]
                                 
        X,Y = np.meshgrid(self.time2[start:stop],self.depth_ice_faces)
        X  = num2date(X,units = self.time_units) #format_time  
        start_f = num2date(self.time2[start],units = self.time_units) 
        stop_f = num2date(self.time2[stop],units = self.time_units) 
        #X = format_time
        
        X_water,Y_water = np.meshgrid(self.time2[start:stop],self.depth_water)
        X_water = num2date(X_water,units = self.time_units)   
        #X_water = format_time
        
        X_sed, Y_sed = np.meshgrid(self.time2[start:stop],self.depth_sed)
        X_sed = num2date(X_sed,units = self.time_units)   
        #X_sed = format_time
        self.fh_ice.close()
        self.fh_water.close()
        self.fh_sediments.close()          
        
        gs = gridspec.GridSpec(3, 1)
        gs.update(left=0.15, right= 0.97,top = 0.95,bottom = 0.06,
                           wspace=0.2,hspace=0.2)
      
        #add subplots
        ax0 = self.figure.add_subplot(gs[0]) # o2 ice 
        ax1 = self.figure.add_subplot(gs[1]) # o2 water
        ax2 = self.figure.add_subplot(gs[2]) # o2 sed

        # interpolate data to plot            
        
        #ax2.set_xlabel("Date", fontsize=14)
        
        #specify colormap
        #cmap = plt.cm.terrain #'plasma' #'terrain'
        cmap = plt.get_cmap('viridis') 
        min = ma.min(var_ice)
        max = ma.max(var_ice)
        #print (max,min)
        #var_levels = np.linspace(min,max,num = 20 )

        #plot 2d figures 
        #CS1 = ax0.contourf(X,Y, var_ice[:,start:stop],
        #                   cmap = cmap,levels = var_levels)
        #without interpolation 
        CS1 = ax0.pcolor(X,Y,var_ice[:,start:stop],cmap = cmap )#) 3,edgecolor = 'w',
                         #linewidth = 0.000005)
        
        ax0.set_title((self.name+' '+ str(data_units)))
        
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
        
        ax2.axhline(self.max_water, color='w', linestyle = '--',linewidth = 1 ) 

        from dateutil.relativedelta import relativedelta
        if (stop-start)>= 367:
            dt =  int((stop - start)/365) #number of years
            time_ticks = []
            for n in range(0,dt+1):
                time_ticks.append(
                    self.format_time[start]+relativedelta(years = n))
        
        
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
 
        ax1.set_ylim(self.max_water,self.min_water)
        ax2.set_ylim(self.max_sed,self.min_sed)  
        ax0.set_ylim(self.min_ice,self.max_ice)
        
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
    
    