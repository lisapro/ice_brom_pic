'''
Created on 28. jun. 2017

@author: ELP
'''
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)
import os
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from netCDF4 import Dataset,num2date,date2num,date2index
import numpy as np
import matplotlib
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

import sys
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure(figsize=(8.3 ,5), dpi=100,
                        facecolor='None',edgecolor='None')        
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self)    
        directory =  self.load_work_directory() 
        
        self.ice_fname = os.path.abspath(os.path.join(directory,'ice.nc')) 
        self.water_fname = os.path.join(directory,'water.nc')
        #self.sediments_fname = os.path.join(directory,'sediments.nc')
        self.ice_fname_base = os.path.abspath(os.path.join(directory,
                                'baseline\ice.nc')) 
        self.water_fname_base = os.path.join(directory,
                                'baseline\water.nc')
        #self.sediments_fname_base = os.path.join(directory,'sediments_base.nc')        
        self.fh_ice =  Dataset(self.ice_fname)   
        try:
            self.time = self.fh_ice.variables['time'][:]
            units = self.fh_ice.variables['time'].units     
        except KeyError: 
            self.time = self.fh_ice.variables['ocean_time'][:]
            units = self.fh_ice.variables['ocean_time'].units                    
        self.format_time = num2date(self.time,units = units,
                                    calendar= 'standard')   
            
        first_year = self.format_time[0].year
        last_year = self.format_time[-1].year
        
        self.fontsize = 12
        
        
        self.names_vars = [] 
        for names,vars in self.fh_ice.variables.items():
            self.names_vars.append(names)
            
                     
        self.names_vars =  sorted(self.names_vars, key=lambda s: s.lower())  
               
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
        
        #self.plot_3fig()
        #self.canvas.draw()
        
        
        self.button = QtWidgets.QPushButton('Plot')
        self.save_button = QtWidgets.QPushButton('Plot and Save_pdf')
        #self.label_choose_var = QtWidgets.QLabel('Choose variable:')
        
        self.change_title = QtWidgets.QLineEdit()
        self.symbols = QtWidgets.QLineEdit('Symbols: # \ $ / & % {} ^ *')
        self.checkbox_title = QtWidgets.QCheckBox('Change title ')
        
        self.label_start_year = QtWidgets.QLabel('Start year:') 
        self.combobox_start_year = QtWidgets.QSpinBox()    
        self.combobox_start_year.setRange(first_year, last_year-1)                 
        self.label_stop_year = QtWidgets.QLabel('Stop year:')   
        self.combobox_stop_year = QtWidgets.QSpinBox() 
        self.combobox_stop_year.setRange(first_year+1, last_year)                        
        self.qlist_widget = QtWidgets.QListWidget()        
        self.qlist_widget.addItems(self.names_vars)


        self.table_button = QtWidgets.QPushButton('Values(table)')       
        
        layout = QtWidgets.QGridLayout()

        #layout.addWidget(self.label_choose_var,0,0,1,1)
        layout.addWidget(self.checkbox_title,0,0,1,1)
        layout.addWidget(self.symbols,0,2,1,1)
         
        layout.addWidget(self.change_title,0,1,1,1)
                         
        layout.addWidget(self.button,0,3,1,1)         
        layout.addWidget(self.save_button,0,4,1,1)
        layout.addWidget(self.label_start_year,0,5,1,1)
        layout.addWidget(self.combobox_start_year,0,6,1,1)        
        layout.addWidget(self.label_stop_year,0,7,1,1)
        layout.addWidget(self.combobox_stop_year,0,8,1,1)                

        layout.addWidget(self.table_button,1,0,1,1)                
        layout.addWidget(self.qlist_widget,2,0,1,1)      
        layout.addWidget(self.canvas,2,1,1,8)    
        layout.addWidget(self.toolbar,1,1,1,1)                           
        self.setLayout(layout)        
        self.button.released.connect(self.call_show_3fig)  
        self.save_button.released.connect(self.call_save_3fig) 
        self.table_button.released.connect(self.table)    
          
    def load_work_directory(self):
        #directory = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        #directory = askdirectory()
        return askdirectory() #directory #ask_filename
    
    def call_show_3fig(self):
        #print ('in show 3 fig')
        self.action = 'showfigure'
        self.plot_3fig()
     
    def call_save_3fig(self):
        self.action = 'savepdf'
        self.plot_3fig()
        
    def read_var(self):

        self.name =  str(self.qlist_widget.currentItem().text())

        self.long_name = str(self.fh_ice.variables[str(self.name)].long_name)
        
        self.setWindowTitle(str(self.long_name)) 

        var_ice =  ma.masked_invalid (
            np.array(self.fh_ice.variables[self.name][0:1095]).T )
        var_ice_base = ma.masked_invalid (
            np.array(self.fh_ice_base.variables[self.name][0:1095]).T )
        
        var_ice_dif = var_ice-var_ice_base
        
        var_water = ma.masked_invalid (np.array(
            self.fh_water.variables[self.name][0:1095][:]).T)
        
        var_water_base = ma.masked_invalid (np.array(
            self.fh_water_base.variables[self.name][0:1095][:]).T)    
            
        var_water_dif = var_water - var_water_base         
        #var_sediments = np.array(
        #    self.fh_sediments.variables[self.name][:]).T 
           
        data_units = self.fh_ice.variables[self.name].units
        if len(self.change_title.text()) < 1: 
            self.change_title.setText('changes in'+self.name+' '+ data_units)                    
        return var_ice_dif,var_water_dif,var_water_dif,data_units

    def save_to_dir(self,dir_name):
        script_dir = os.path.abspath(os.path.dirname(__file__))
        dir_to_save = os.path.abspath(os.path.join(script_dir,dir_name))
            
        if not os.path.isdir(dir_to_save):
            os.makedirs(dir_to_save)
        filename = '{}\ice_brom_exp_diff_{}.png'.format(dir_to_save,self.name)       
        #plt.savefig(results_dir+title+'.png')
        plt.savefig(filename, format='png', dpi=300, transparent=True)


            
    def plot_3fig(self): 
       
        plt.clf() 
             
        self.fh_ice =  Dataset(self.ice_fname)  
        self.fh_ice_base = Dataset(self.ice_fname_base) 
        self.fh_water =  Dataset(self.water_fname)  
        self.fh_water_base =  Dataset(self.water_fname_base)        
        #self.fh_sediments =  Dataset(self.sediments_fname) 
                    
        self.depth = self.fh_ice.variables['z'][:] 
        self.depth_faces = self.fh_ice.variables['z_faces'][:] 
           
        self.max_faces = np.max(self.depth_faces)
        
        self.min_ice = np.min(self.depth)
        self.max_ice = np.max(self.depth)
        
        ice_res = 6
        self.depth_ice = (self.depth - self.max_ice)*-ice_res
        self.depth_ice_faces = np.array((self.depth_faces - self.max_faces)*-ice_res)
        
        self.depth_ice = np.array(self.depth_ice)
        
        self.min_ice = np.amin(self.depth_ice_faces)
        self.max_ice = np.amax(self.depth_ice_faces)
        
        self.depth_water = np.array(self.fh_water.variables['z_faces'][:])
        #self.depth_sed = self.fh_sediments.variables['z_faces'][:] 
        
        self.min_water = 60 #np.amin(self.depth_water)
        self.max_water = np.amax(self.depth_water)
        
        #self.min_sed = np.amin(self.depth_sed)
        #self.max_sed = np.amax(self.depth_sed)
         
        try:
            self.time = self.fh_ice.variables['time']      
            self.time2 = self.fh_ice.variables['time'][:]
            self.time_units = self.fh_ice.variables['time'].units
        except KeyError:
            self.time = self.fh_ice.variables['ocean_time']   
            self.time2 = self.fh_ice.variables['ocean_time'][:]            
            self.time_units = self.fh_ice.variables['ocean_time'].units
        self.format_time = num2date(self.time2,units = self.time_units,calendar= 'standard')
         
        #########################
        # Values for time axis  #
        #########################
                
        start_year = self.combobox_start_year.value()
        stop_year = self.combobox_stop_year.value()
        #assert start_year < stop_year
        to_start = datetime.datetime(start_year,1,1,12,0)
        to_stop= datetime.datetime(stop_year,1,1,12,0)
        
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
        
        #X_sed, Y_sed = np.meshgrid(self.time2[start:stop],self.depth_sed)
        #X_sed = num2date(X_sed,units = self.time_units)   
        #X_sed = format_time
        self.fh_ice.close()
        self.fh_water.close()
        #self.fh_sediments.close()          
        
        gs = gridspec.GridSpec(2, 1,height_ratios=[1, 1])
        gs.update(left=0.09, right= 0.98,top = 0.931,bottom = 0.07,
                           wspace=0.2,hspace=0.1)
      
        #add subplots
        ax0 = self.figure.add_subplot(gs[0]) # o2 ice 
        ax1 = self.figure.add_subplot(gs[1]) # o2 water
                  
        cmap = plt.get_cmap('viridis') #('Blues_r')
        #cmap_water = cmap #plt.get_cmap('RdBu_r') 
        min = ma.min(var_water)
        max = ma.max(var_water)
       
        #var_levels = np.linspace(min,max,num = 20 )

        #plot 2d figures 
        #CS1 = ax0.contourf(X,Y, var_ice[:,start:stop],
        #                   cmap = cmap,levels = var_levels)
        #without interpolation 
        vvmin = -10 
        vvmax = 10
        normalize = matplotlib.colors.Normalize(vmin=vvmin, vmax=vvmax)
        normalize = None
        CS1 = ax0.pcolormesh(X,Y,var_ice[:,start:stop],
                         norm = normalize,cmap = cmap )#) 3,edgecolor = 'w',
                         #linewidth = 0.000005)
                        
        if self.checkbox_title.isChecked() == True:
            title = self.change_title.text()
            ax0.set_title(title)
        else:                 
            ax0.set_title(self.long_name+' ['+ str(data_units)+']')
            
        import matplotlib.ticker as ticker

        def fmt(x, pos):
            a, b = '{:.2e}'.format(x).split('e')
            b = int(b)
            return r'${} \times 10^{{{}}}$'.format(a, b)
        
        CS4 = ax1.pcolormesh(X_water,Y_water,var_water[:,start:stop],norm = normalize,
                          cmap = cmap) #,edgecolor = 'w',
                         # linewidth = 0.000005)
        
        ### Time ticks ### 
        from dateutil.relativedelta import relativedelta
        if (stop-start)>= 367:
            dt =  int((stop - start)/365) #number of years
            time_ticks = []
            for n in range(0,dt+1):
                time_ticks.append(
                    self.format_time[start]+relativedelta(years = n))
        
        
        def add_colorbar(CS,axis,ma1):

            if ma1 > 10000 or ma1 < 0.001:
                cb = plt.colorbar(CS,ax = axis,pad=0.02,
                     aspect = 7) #,format=ticker.FuncFormatter(fmt)) 
            else: 
                cb = plt.colorbar(CS,ax = axis,pad=0.02,
                     aspect = 7)                     
            return cb
        
        ma1 = ma.max(var_ice[:,start:stop])
        cb0 = add_colorbar(CS1,ax0,ma1)
        cb1 = add_colorbar(CS4,ax1,ma1)
        #cb2 = add_colorbar(CS7,ax2)
        
        #letters = ['(a)','(b)','(c)']
        labels = ["Ice thickness (cm)", "Depth (m)","Depth \n(m)" ]
        n = 0
        
        for axis in (ax0,ax1): 
            try:
                axis.set_xticks(time_ticks)
            except: NameError
            axis.yaxis.set_label_coords(-0.065, 0.5)
            #axis.text(-0.21, 0.9, letters[n], transform=axis.transAxes , 
            #        size= self.fontsize) #, weight='bold')
            axis.set_ylabel(labels[n], fontsize = self.fontsize)
              
            n=n+1
            #plt.tick_params(axis='both', which='major', labelsize= self.fontsize) 
            
         
        ax1.set_ylim(self.max_water,self.min_water)
        #ax2.set_ylim(self.max_sed,self.min_sed)  
        ax0.set_ylim(self.min_ice,250) #self.max_ice
        
        # hide horizontal axis labels 
        ax0.set_xticklabels([])    
        #ax1.set_xticklabels([]) 
  
        #plt.yticks(fontsize=self.fontsize, rotation=90) 
        #ax.yaxis.label.set_size(16) 
        #plt.rcParams.update({'font.size': 14})
           
        if (stop-start)>= 365*6:
            ax1.xaxis.set_major_formatter(
                mdates.DateFormatter('%Y')) 
            #ticks = np.arange(time[start:stop],time[start:stop],50)
        elif (stop-start) > 367 and (stop-start) < 365*6:
            ax1.xaxis.set_major_formatter(
                mdates.DateFormatter('%m/%Y'))   
        else : 
            ax1.xaxis.set_major_formatter(
                mdates.DateFormatter('%b'))
                               
        if self.action == 'showfigure' : 
            self.canvas.draw()                
        elif self.action == 'savepdf' :
            self.canvas.draw()
            self.save_to_dir('Results')
    

    def table(self):

        self.fh_ice =  Dataset(self.ice_fname)  
        self.fh_water =  Dataset(self.water_fname)  
        #self.fh_sediments =  Dataset(self.sediments_fname)   
        data = self.read_var()
        self.depth_water = np.array(self.fh_water.variables['z_faces'][:])        
        #self.fh_ice.close()         
        #var_ice = data[0]
        var_water = data[1].T
        #var_sed = data[2]
        data_units = data[3]
        
        #data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}
        #table = MyTable(self, data, 5, 3)
        #table.show()
        
        self.tableWidget = QTableWidget() 
        
        #self.tableWidget.setItem(var_water, QTableWidgetItem("Cell (1,1)"))
        lenx = var_water.shape[0]
        leny = var_water.shape[1]
        
        self.tableWidget.setColumnCount(lenx) 
        self.tableWidget.setRowCount(leny+1)        
        for column in range(lenx):
            self.tableWidget.setHorizontalHeaderItem(
                column, QTableWidgetItem(str(self.format_time[column].date())))
        
        
        for row in range(leny):
            self.tableWidget.setVerticalHeaderItem(
                row, QTableWidgetItem(str(self.depth_water[row])))            
            
        #self.tableWidget.setHorizontalHeaderLabels(QString(self.time))

        for row in range(leny):
            for column in range(lenx):
                self.tableWidget.setItem(row,column, #row,column!
                    QTableWidgetItem(
                        str(var_water[column,row]))) #column,row!
        
        self.tableWidget.show()
        #print (var_water)       
        #pass                    
        #plt.savefig('ice_brom_{}.png'.format(name),transparent = True)
        #plt.savefig('ice_brom_{}.pdf'.format(name), format='pdf')
    
        # Save in a vector format 
        #plt.savefig('ice_brom_{}.eps'.format(name), format='eps')

                    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("plastique")
    main = Window()
    #main.showDialog()
    main.setStyleSheet("background-color:#dceaed;")
    main.show()
    
    sys.exit(app.exec_())    
    
    