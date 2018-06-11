'''
Created on 28. jun. 2017

@author: ELP
'''
import os
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
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
from matplotlib import rc
font = {'size' : 14}
rc('font', **font)
import sys
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure(figsize=(11, 8.25), dpi=100,
                        facecolor='None',edgecolor='None')        
        self.canvas = FigureCanvas(self.figure)         
        directory =  self.load_work_directory() 
        
        self.ice_fname = os.path.abspath(os.path.join(directory,'ice.nc')) 
        self.water_fname = os.path.join(directory,'water.nc')
        self.sediments_fname = os.path.join(directory,'sediments.nc')
        
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
        
        self.fontsize = 14
        
        
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
        try:
            self.name =  str(self.qlist_widget.currentItem().text())
        except AttributeError:   
            messagebox = QtWidgets.QMessageBox.about(self, "Retry",
                                             'Choose variable,please') 
            return None      
          
        self.long_name = str(self.fh_water.variables[str(self.name)].long_name)
        self.setWindowTitle(str(self.long_name)) 

        var_water = np.array(
            self.fh_water.variables[self.name][:]).T 
        var_sediments = np.array(
            self.fh_sediments.variables[self.name][:]).T 
                        
        data_units = self.fh_water.variables[self.name].units
        if len(self.change_title.text()) < 1: 
            self.change_title.setText(self.name+' '+ data_units)                    
        return var_water,var_sediments,data_units

    def save_to_dir(self,dir_name):
        #dir_name = 'Results'
        script_dir = os.path.abspath(os.path.dirname(__file__))
        dir_to_save = os.path.abspath(os.path.join(script_dir,dir_name))
            
        if not os.path.isdir(dir_to_save):
            os.makedirs(dir_to_save)
        filename = '{}\ice_brom_{}.pdf'.format(dir_to_save,self.name)       
        plt.savefig(filename, format='pdf',transparent = True)
        #plt.savefig(filename, format='pdf', dpi=300,transparent = True)

    def plot_3fig(self): 
       
        plt.clf() 
             

        self.fh_water =  Dataset(self.water_fname)  
        self.fh_sediments =  Dataset(self.sediments_fname) 
        
        self.depth_water = np.array(self.fh_water.variables['z_faces'][:])
        self.depth_sed = self.fh_sediments.variables['z_faces'][:] 
        
        self.min_water = np.amin(self.depth_water)
        self.max_water = np.amax(self.depth_water)
        
        self.min_sed = np.amin(self.depth_sed)
        self.max_sed = np.amax(self.depth_sed)
        
        try:
            self.time = self.fh_water.variables['time']      
            self.time2 = self.fh_water.variables['time'][:]
            self.time_units = self.fh_water.variables['time'].units
        except KeyError:
            self.time = self.fh_water.variables['ocean_time']   
            self.time2 = self.fh_water.variables['ocean_time'][:]     
            self.time_units = self.fh_water.variables['ocean_time'].units       
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
        
        var_water = data[0]
        var_sed = data[1]
        data_units = data[2]
        
        start_f = num2date(self.time2[start],units = self.time_units) 
        stop_f = num2date(self.time2[stop],units = self.time_units)    
                                             
        X_water,Y_water = np.meshgrid(self.time2[start:stop],self.depth_water)
        X_water = num2date(X_water,units = self.time_units)   
        
        X_sed, Y_sed = np.meshgrid(self.time2[start:stop],self.depth_sed)
        X_sed = num2date(X_sed,units = self.time_units)   

        self.fh_water.close()
        self.fh_sediments.close()          
        
        gs = gridspec.GridSpec(2, 1)
        gs.update(left=0.09, right= 1,top = 0.95,bottom = 0.06,
                           wspace=0.1,hspace=0.05)
      
        ax1 = self.figure.add_subplot(gs[0]) # water
        ax2 = self.figure.add_subplot(gs[1]) # sed
        
        #specify colormap
        #cmap = plt.cm.terrain #'plasma' #'terrain'        
        cmap = plt.get_cmap('viridis') 
        cmap_water = plt.get_cmap('CMRmap') 
        
        #min = ma.min(var_water)
        #max = ma.max(var_water)
        #var_levels = np.linspace(min,max,num = 20 )

        #plot 2d figures 
        #without interpolation 
       
        CS4 = ax1.pcolor(X_water,Y_water,var_water[:,start:stop],
                          cmap = cmap_water)
        CS7 = ax2.pcolor(X_sed,Y_sed,var_sed[:,start:stop], cmap = cmap_water)  
                      
        if self.checkbox_title.isChecked() == True:
            title = self.change_title.text()
            ax1.set_title(title)
        else:                 
            ax1.set_title(self.long_name+' ['+ str(data_units)+']')

        import matplotlib.ticker as ticker

        def fmt(x, pos):
            a, b = '{:.2e}'.format(x).split('e')
            b = int(b)
            return r'${} \times 10^{{{}}}$'.format(a, b)
        
        # interpolate data to plot 
        #CS1 = ax0.contourf(X,Y, var_ice[:,start:stop],
        #                   cmap = cmap,levels = var_levels)        
        #CS4 = ax1.contourf(X_water,Y_water, var_water[:,start:stop],
        #                   cmap = cmap) 
        #CS7 = ax2.contourf(X_sed,Y_sed, var_sed[:,start:stop],
        #                   cmap = cmap)    
       
        ax2.axhline(self.max_water, color='w', linestyle = '--',linewidth = 1 ) 
        ax2.annotate('  Sediment Water Interface',
                    xy =(start_f,self.max_water),
                    xytext=(start_f,self.max_water-0.01),color = 'w')
         
        #ax2.axhline(self.max_water, color='k', linestyle = '--',linewidth = 1 ) 
        #print (start_f,self.max_water)
        #ax2.annotate('Sediment Water Interface',
        #            xy =(start_f,self.max_water),
        #            xytext=(start_f,self.max_water-0.01),color = 'k')       
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
                     aspect = 7,shrink = 0.9,format=ticker.FuncFormatter(fmt)) 
            else: 
                cb = plt.colorbar(CS,ax = axis,pad=0.01,
                     aspect = 7,shrink = 0.9) 
            return cb
        
        ma1 = ma.max(var_water[:,start:stop])        
        cb1 = add_colorbar(CS4,ax1,ma1)
        cb2 = add_colorbar(CS7,ax2,ma1)
        
        #letters = ['(a)','(b)','(c)']
        labels = ["Depth m","Depth m" ]
        
        n = 0
        for axis in (ax1,ax2): 
            try:
                axis.set_xticks(time_ticks)
            except: NameError
            axis.yaxis.set_label_coords(-0.08, 0.5)
            #axis.text(-0.21, 0.9, letters[n], transform=axis.transAxes , 
            #        size= self.fontsize) #, weight='bold')
            axis.set_ylabel(labels[n], fontsize = self.fontsize)
              
            n=n+1
            #plt.tick_params(axis='both', which='major', labelsize= self.fontsize) 
            
         
        ax1.set_ylim(self.max_water,self.min_water)
        ax2.set_ylim(self.max_sed,self.min_sed)  #
       
        # hide horizontal axis labels 
 
        ax1.set_xticklabels([]) 
  
        #plt.yticks(fontsize=self.fontsize, rotation=90) 
        #ax.yaxis.label.set_size(16) 
        #plt.rcParams.update({'font.size': 14})
        if (stop-start) > 367 and (stop-start) < 365:
            ax2.xaxis.set_major_formatter(
                mdates.DateFormatter("%b '%y"))            
        elif (stop-start)>= 365*6:
            #ax5.xaxis.set_major_formatter(
            #     mdates.DateFormatter("%b '%y")) 
            ax2.xaxis.set_major_formatter(
                mdates.DateFormatter('%Y')) 
            #ticks = np.arange(time[start:stop],time[start:stop],50)

            #ax2.xaxis.set_major_formatter(
            #    mdates.DateFormatter('%m/%Y'))   
        else : 
            ax2.xaxis.set_major_formatter(
                mdates.DateFormatter('%b'))
                               
        if self.action == 'showfigure' : 
            self.canvas.draw()                
        elif self.action == 'savepdf' :
            self.canvas.draw()
            self.save_to_dir('Results')
    

    def table(self):

        self.fh_water =  Dataset(self.water_fname)  
        self.fh_sediments =  Dataset(self.sediments_fname)   
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
        #plt.savefig('ice_brom_{}.'.format(name),transparent = True)
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
    
    