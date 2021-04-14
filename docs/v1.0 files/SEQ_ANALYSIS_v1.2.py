from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QTableView, QLineEdit, QRadioButton, QComboBox, QMessageBox,QPushButton, QApplication,QCheckBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QAbstractTableModel, Qt, QSettings,QPoint
from skip_frac import Ui_MainWindow
from run_desc_2 import Ui_MainWindow2
from polymer_bounds import Ui_MainWindow3
from align_param import Ui_MainWindow5
from skip_align import Ui_MainWindow6
from plot_fsa import plot,divisors,getFSANames,timePts,getFSANamesList,plot3d,atoi,natural_keys,deletePolymer,import_ranges,import_sizes, kintek_export,plot3dScaled,getFSANamesListNotNum,plot2dScaled,plot3dlog
from plot_fsa import plot3dlogscaled
from file_names import Ui_Form
from time_pts_align import Ui_Form2

import matplotlib.pyplot as plt

import re
import sys
import pandas as pd
import numpy as np
import math
import os
from pathlib import Path


# Appending for multiple substrate multiple product problem
# Have the table with the difference ranges then let the user choose which difference ranges you want to pick

def filtered_data(name,time_underscore):
    # file_name = 'Burst on PThio DNA.txt'
    f = open(name, 'r')
    headers = ['Dye', 'Peak Number', 'Height', 'Time', 'Well', 'Area', 'Data Point']
    # data = pd.read_csv('Burst on PThio DNA.txt')
    f.readline()
    col_data = []
    count = 0
    # reads each line in the text file
    for test in f:
        # Splits column data based on header
        # Dye/Sample Peak,Sample File Name,Size, Height, Area,Data Point

        test_set = test.split()
        # Output: ['"B,1"', 'PT_100nM_0_TLD_4.2.19_1_2019-04-02_A05.fsa', '894', '11056', '2524']

        # print(test_set)
        # strips the underscore in long description
        desc_fix = test_set[1].split('_')
        # Output: ['PT', '100nM', '0', 'TLD', '4.2.19', '1', '2019-04-02', 'A05.fsa']

        # print(desc_fix)
        # removes long description name
        test_set.pop(1)
        # Output: ['"B,1"','894', '11056', '2524']
        # print(test_set)
        # print(test_set)

        # inserts time into test_set
        test_set.insert(2, desc_fix[time_underscore])

        # Output:['"B,1"', 'PT_100nM_0_TLD_4.2.19_1_2019-04-02_A05.fsa', '0', '894', '11056', '2524']

        # inserts Well number at the end of test_set
        test_set.insert(3, desc_fix[len(desc_fix) - 1])

        # Output: #['"B,1"', 'PT_100nM_0_TLD_4.2.19_1_2019-04-02_A05.fsa', '0', 'A05.fsa', '894', '11056', '2524']

        # print(test_set)

        # splits dye and peak number and puts them into separate columns
        dye_peak = test_set[0].strip('\"').replace(',', '')
        test_set.pop(0)
        i = 0
        # while i < len(dye_peak):
        #     test_set.insert(i, dye_peak[i])
        #     i += 1
        while i < 1:
            test_set.insert(i, dye_peak[i])
            i += 1

        test_set.insert(1, dye_peak[i:])
        # print(test_set)
        # adding all data to each column
        col_data.append(test_set)
        count += 1
    # pprint.pprint(col_data)
    df = pd.DataFrame(col_data, columns=headers)
    # print(col_data)

    # filters height above user input. Note that if filter height
    # is above internal standard height, then error will raise
    # have to add try/except block here for future use
    return df
    # df_int_all = df.loc[df['Dye'] == 'Y']
    # return df_int_all
    # print()
    # print("These are all the internal std. peaks\n")
    # print('---------------------------------------\n')
    # print(df_int_all)
    # print()
    #min_height = input("Please enter the minimum height (make sure bigger than int std desired): ")
    # while string_alpha_check(min_height):
    #     min_height = input("Not valid integer, please try again: ")

    # min_height = int(min_height)
    # df_hmin = df.loc[df['Height'].astype(int) > min_height]
    # return df_hmin


def int_std_all(df):
    df_int_all = df.loc[df['Dye'] == 'Y']
    return df_int_all

def all_peaks_filtered(df,min_height):
    df_hmin = df.loc[df['Height'].astype(int) > min_height]
    df_hmin_2 = df_hmin.loc[df_hmin['Dye'] == 'B']
    return df_hmin_2

def all_peaks_filtered_global(df,min_height):
    df_hmin = df.loc[df['Height'].astype(int) > min_height]
    return df_hmin
def int_std_filtered(df,min_height_int_std):
    df_int_std_filtered = df.loc[df['Height'].astype(int) > min_height_int_std]
    df_int_std_filtered_2 = df_int_std_filtered.loc[df_int_std_filtered['Dye'] == 'Y']
    return df_int_std_filtered_2

class pandasModel(QAbstractTableModel):

    def __init__(self, data): #Takes in a pandas df as data
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    # def setData(self, index, value, role=Qt.EditRole):
    #     if index.isValid():
    #         row = index.row()
    #         col = index.column()
    #         self._data.iloc[row][col] = float(value)
    #         self.dataChanged.emit(index, index, (Qt.DisplayRole,))
    #         return True
    #     return False

    # def flags(self, index):
    #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable



def closeProgram():
    sys.exit()


#Asks if you want to skip fractional area vs size. Yes goes straight to alignment
#No goes to fractional area vs. size
#Quit ends the program
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.setWindowTitle('Skip Frac vs. Size')
        self.show()
        self.ui.pushButton.clicked.connect(self.on_push_yes)
        # self.ui.hide()
        self.ui.pushButton_2.clicked.connect(self.on_push_no)
        #self.ui.pushButton_3.clicked.connect(closeProgram)


    def on_push_yes(self):
        self.param = alignParam()
    def on_push_no(self):
        self.close()
        self.RunDesc = RunDesc()
        #self.ui.close()
        # window_RunD = RunDesc()
        # window_RunD.show()


class RunDesc(QtWidgets.QMainWindow):
    def __init__(self):
        super(RunDesc,self).__init__()
        self.ui2 = Ui_MainWindow2()
        self.ui2.setupUi2(self)
        #self.setWindowTitle('Run Description')
        self.show()

        # self.df_all_peaks = filtered_data(fileName, time_underscore) #Calculates all the peaks in table
        # self.df_all_int_std_peaks = int_std_all(self.df_all_peaks) #Calculates all internal std. peaks

        #Gets the file run description from text file
        self.ui2.pushButton.clicked.connect(self.getTxt)
        #Gets the time underscore
        self.ui2.pushButton_2.clicked.connect(self.getTimeUnderscore) #Gets the time underscore
        self.ui2.pushButton_3.clicked.connect(self.pressBack) #Goes to the previous frame
        self.ui2.pushButton_8.clicked.connect(self.showAllPeaks) #Shows all the peaks before filtering
        self.ui2.pushButton_4.clicked.connect(self.showAllIntStdPeaks) #Shows all internal standard peaks
        self.ui2.pushButton_5.clicked.connect(self.getMinHeight) #Gets the minimum height filter
        self.ui2.pushButton_6.clicked.connect(self.showAllFilteredPeaks) #Shows all the filtered peaks
        self.ui2.pushButton_7.clicked.connect(self.showFilteredStd) #Shows all the filtered internal std. peaks
        self.ui2.pushButton_9.clicked.connect(self.showPolymerBounds) #Connected to the continue button
        self.ui2.pushButton_10.clicked.connect(closeProgram)
        #Makes these buttons grey before pushing the calculate peaks button
        self.ui2.pushButton_4.setEnabled(False)
        self.ui2.pushButton_8.setEnabled(False)
        self.ui2.pushButton_5.setEnabled(False)
        self.ui2.pushButton_6.setEnabled(False)
        self.ui2.pushButton_7.setEnabled(False)
        self.ui2.pushButton_11.setEnabled(False)
        self.ui2.pushButton_11.clicked.connect(self.showAllProductPeaks) #Shows all non int. std. peaks


#fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , '*.xlsm')

    #Goes back to the skip fractional area vs size window
    def pressBack(self):
        self.close()
        self.backFrac = MyWindow()

    #Functions gets the .txt raw output form the sequencer
    def getTxt(self):
        #global fileName
        #options = QtGui.QFileDialog.Options()
        #Opens the .txt raw output file
        global previous_fileName #Creates a global function for previous file name entered
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(),'*.txt')
        if fileName != '': #If the file found isn't empty
            previous_fileName = fileName
            #Gets the run description from the .txt file. Usually it's the second line of the file. First line is headers
            self.ui2.lineEdit_2.setText(fileName)
            file = open(fileName,'r')
            file.readline()
            second_line = file.readline()
            split_second_line = second_line.split()
            txt_file_name = split_second_line[1]
            file.close()
            self.ui2.RunDescLabel.setText(txt_file_name)
            self.txtfileName = fileName
        elif fileName == '' and self.ui2.lineEdit_2.text() != '': #This corrects if the filname is entered, but user presses cancel
            self.ui2.lineEdit_2.setText(previous_fileName)
            self.txtfileName = previous_fileName




    #Have to error check in case not an integer
    def getTimeUnderscore(self):
        global time_underscore

        try:
            time_underscore = int(self.ui2.lineEdit.text())
            pre_df_all_peaks = filtered_data(self.txtfileName, time_underscore) #In case someone tries again w/o closing program
            self.df_all_peaks = pre_df_all_peaks   # Calculates all the peaks in table


            pre_df_all_int_std_peaks = int_std_all(self.df_all_peaks) #In case someone tries again w/o closing program
            self.df_all_int_std_peaks =  pre_df_all_int_std_peaks # Calculates all internal std. peaks
            self.ui2.pushButton_4.setEnabled(True)
            self.ui2.pushButton_8.setEnabled(True)
            self.ui2.pushButton_5.setEnabled(True)
            self.ui2.pushButton_11.setEnabled(True)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No time underscore, please try again')
            error_dialog.exec_()

    def getMinHeight(self):
        global min_height
        global df_global_peaks
        try:
            min_height = int(self.ui2.lineEdit_3.text())
            min_height_int_std = int(self.ui2.lineEdit_4.text())
              # For use in another class

            pre_df_all_filtered_peaks =  all_peaks_filtered(self.df_all_peaks, min_height) #This makes a local table before
            #instantiting into the instance variable. This is in case someone doesn't want to quit the program
            #and runs another instance of the .txt files
            self.df_all_filtered_peaks = pre_df_all_filtered_peaks #Creates table with all peaks above min height



            df_global_peaks = all_peaks_filtered_global(self.df_all_peaks, min_height) #Creates global peaks above min height for use other methods


            pre_df_all_int_std_filter = int_std_filtered(self.df_all_peaks,min_height_int_std) #Local table in case someone runs
            #Another file w/o closing
            self.df_int_std_filter = pre_df_all_int_std_filter #Creates table with all int std. peaks

            #Ungrey the selections for seeing each table
            self.ui2.pushButton_6.setEnabled(True)
            self.ui2.pushButton_7.setEnabled(True)


        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table, please check min height or other conditions')
            error_dialog.exec_()



    def showAllPeaks(self):
        try:

            #self.df_all_peaks = filtered_data(fileName,time_underscore)
            #self.df_int_std_all = int_std_all(self.df_all_peaks)
            pre_df_all_peaks = self.df_all_peaks #Corrects for another instance of .txt peaks
            model = pandasModel(pre_df_all_peaks)
            self.view = QTableView()
            self.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view.resizeColumnsToContents()
            self.view.setModel(model)
            self.view.setWindowTitle('All Peaks')
            self.view.resize(800, 600)
            #self.close()
            self.view.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Time underscore not entered, or underscore is out of bounds')
            error_dialog.exec_()

    def showAllProductPeaks(self):
        try:
            #df_hmin_2 = df_hmin.loc[df_hmin['Dye'] == 'B']
            #self.df_all_peaks = filtered_data(fileName,time_underscore)
            #self.df_int_std_all = int_std_all(self.df_all_peaks)
            pre_df_all_peaks = self.df_all_peaks.loc[self.df_all_peaks['Dye'] == 'B'] #Corrects for another instance of .txt peaks
            model = pandasModel(pre_df_all_peaks)
            self.view = QTableView()
            self.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view.resizeColumnsToContents()
            self.view.setModel(model)
            self.view.setWindowTitle('All Peaks')
            self.view.resize(800, 600)
            #self.close()
            self.view.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Time underscore not entered, or underscore is out of bounds')
            error_dialog.exec_()


    def showAllIntStdPeaks(self):
        try:
            #self.df_all_int_std_peaks = int_std_all(self.df_all_peaks)
            pre_df_all_int_std_peaks = self.df_all_int_std_peaks #Corrects for another instance of the peaks
            model_all_int = pandasModel(pre_df_all_int_std_peaks)
            self.view_int_std_all = QTableView()
            self.view_int_std_all.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_int_std_all.resizeColumnsToContents()
            self.view_int_std_all.setModel(model_all_int)
            self.view_int_std_all.setWindowTitle('All Internal Std. Peaks')
            self.view_int_std_all.resize(800, 600)
            # self.close()
            self.view_int_std_all.show()

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Time underscore not entered, or underscore is out of bounds')
            error_dialog.exec_()


    def showAllFilteredPeaks(self):
        #global df_global_peaks #For use in another class
        try:
            # self.df_all_filtered_peaks = all_peaks_filtered(self.df_all_peaks,min_height)
            # df_global_peaks = all_peaks_filtered(self.df_all_filtered_peaks,min_height)
            pre_df_all_filtered_peaks = self.df_all_filtered_peaks #Fixes for altering to another instance of the peak
            model_all_filtered = pandasModel(pre_df_all_filtered_peaks)
            self.view_all_filtered = QTableView()
            self.view_all_filtered.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_all_filtered.resizeColumnsToContents()
            self.view_all_filtered.setModel(model_all_filtered)
            self.view_all_filtered.setWindowTitle('All Filtered Peaks')
            self.view_all_filtered.resize(800,600)
            #self.close()
            self.view_all_filtered.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table, please check min height or other conditions')
            error_dialog.exec_()


    def showFilteredStd(self):
        try:
            #self.df_int_std_filter = int_std_filtered(self.df_all_filtered_peaks)
            pre_df_int_std_filter = self.df_int_std_filter
            model_int_std_filter = pandasModel(pre_df_int_std_filter)
            self.view_int_std_filter = QTableView()
            self.view_int_std_filter.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_int_std_filter.resizeColumnsToContents()
            self.view_int_std_filter.setModel(model_int_std_filter)
            self.view_int_std_filter.setWindowTitle('Filtered internal std. peaks')
            self.view_int_std_filter.resize(800,600)
            #self.close()
            self.view_int_std_filter.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table, please check min height or other conditions')
            error_dialog.exec_()


    def showPolymerBounds(self):
        self.polymer = polymerBounds()
        #self.close()


def sample_distance(filtered_data):
    # gets peaks without internal standard
    df_no_int = filtered_data.loc[filtered_data['Dye'] == 'B']
    #print(df_no_int)

    # gets peaks with internal standard
    df_int_std = filtered_data.loc[filtered_data['Dye'] == 'Y']

    #Exports the internal standard data
    #export_int_std = df_int_std.to_csv('Export_data_int_std.csv',sep = ',')
    # print('These are the internal std. peaks after filtering')
    # print('------------------------------------------------')
    # print(df_int_std)
    # print()
    # makes list of int standard data points
    int_stdlist = df_int_std['Data Point'].tolist()

    # makes list of int standard time points
    int_stdtimelist = df_int_std['Time'].tolist()

    # makes list of sample data points
    sample_list = df_no_int['Data Point'].tolist()

    # makes list of sample time points
    sample_timelist = df_no_int['Time'].tolist()
    # print(sample_timelist)

    #zips the internal standard time points and data points into a dictionary
    # Ex: {1:2,3:4}
    int_std_dict = dict(zip(int_stdtimelist, int_stdlist))

    #zips the sample time points and data points into a nested list
    # Ex: [[1,2],[3,4]]
    sample_2d = [list(a) for a in zip(sample_timelist, sample_list)]

    #pprint.pprint(sample_2d)

    # if sample_2d[i][0] in int_std_dict:

    #Creates a column in the pandas dataframe for difference
    #(internal standard - sample) by using datapoint
    #For each time
    diff_list = []
    for i in range(len(sample_2d)):
        #Subtracts the internal std value by the sample datapoint
        #Method is inefficient, could probably use nested list
        # for the internal standards as well
        #diff = int(int_std_dict[sample_2d[i][0]]) - int(sample_2d[i][1])
        diff = round(float(int(int_std_dict[sample_2d[i][0]])/int(sample_2d[i][1])) * 100,2)
        diff_list.append(diff)

    #This is to prevent pandas SettingwithCopyWarning
    df_diff = df_no_int.copy()
    df_diff['Diff'] = diff_list

    # exports data with compared to internal standard
    #export_excel_difference = df_diff.to_csv('Export_data_intstd_Diff.csv',sep=',')

    #Returns a dataframe containing values with differences and
    #No intenal standard column
    return (df_diff)




#Gives table full of table with sizes

def size(df,length,ranges_list):
    # Asks user input for template size
    # original = int(input('Please enter the template size: '))
    # Adjusts the peak number in relation to template size

    # Polymer length list. Ex: [27mer,28mer,29mer]
    #length = []

    # Nested list for the ranges of the difference ranges for each polymer.
    # Ex: For 27mer: [[300,400]]. Where 300 is lower bound and 400 is upper bound
    #ranges_list = []

    # Creates a dictionary for polymer length and difference ranges
    # Ex: {27mer:[300,400],28mer"[450,500]}
    ranges_dict = {}

    # Loop appends each polymer as the key and the range list as the value
    for i in range(len(ranges_list)):
        ranges_dict[length[i]] = ranges_list[i]
    # print(ranges_dict)

    # Takes difference values to list
    diff_list = df['Diff'].astype(float).tolist()

    # Gets the keys of the dictionary which are the polymer sizes
    ranges_keys = list(ranges_dict.keys())
    # print(ranges_keys)
    final_length_list = []
    # print(diff_list)

    # Parses the differences (internal std - sample) and checks to see
    # If within a certain range. If it is, then it is appends the key(size)
    # to final_length_list
    for j in diff_list:
        for i in range(len(ranges_keys)):
            # Gets the value of ranges. Ex: [300,400]
            width = ranges_dict[ranges_keys[i]]
            # print(ranges_dict[ranges_keys[i]])

            # Takes lower bound
            low = width[0]
            # Takes upper bound
            high = width[-1]
            # If the difference is in between these bounds, then
            # append the size to the final_length_list
            if j >= low and j < high:
                final_length_list.append(ranges_keys[i])

    # print(final_length_list)
    # Creates a new column in the dataframe for the size of each sample run
    df["Size"] = final_length_list

    return df



 # Function that creates the table containing area values for each polymer
def table(df):
    #Creates sorted set with time values (unique values only)
    df_time = list(set(df['Time'].tolist()))
    df_time.sort()

    #Creates sorted set with size values (unique values only)
    df_size = list(set(df['Size'].tolist()))
    df_size.sort(key=natural_keys)

    #print(df_size)
    #n = pd.DataFrame(columns = df_size)
    # headings = df_size
    # headings.append('Total')
    # for i in range(len(df_size)-1):
    #     headings.append(str(df_size[i]) + '/' + headings[len(headings)-1-i])
    # n = pd.DataFrame(df_time,columns=['Time'])
    #  for i in range(len(headings)):
    #      n[headings[i]] = np.nan
    #n.set_index('Time',inplace=True)

    area_list = df['Area'].tolist()
    time_list = df['Time'].astype(float).tolist()
    # time_dict = {'time':time_list}

    #Creates dictionary where time and size are keys. Value is area
    size_list = df['Size'].tolist()

    #Creates tuple of time,size pairs
    #This tuple will eventually be the key values for the dictionary
    two_keys = list(zip(time_list,size_list))
    #print(two_keys)

    new_dict = {}

    #Creates new empty dataframe with time values as index
    n = pd.DataFrame()
    n.index.name = 'Time'

    for size in df_size:
        n[size] = ""
    #print(n)
    #Appends area to dictionary containing the time and size keys
    #Ex: {(0.05 sec,27mer),34000, (0.10 sec, 27mer), 20000}
    for i in range(len(two_keys)):
        new_dict[two_keys[i]] = area_list[i]

    #Parses the dictionary and creates a new column in the table
    #for area. Locates the time and size and inputs the area for that
    #those values into the dataframe
    for key in two_keys:
        time = key[0]
        size = key[1]
        n.loc[time,size] = int(new_dict[key])
    #     print(n)
    # print(new_dict)
    # print(len(new_dict))
    # print('This is the table for fractional area vs. size. Please analyze to see if you want to delete outliers.')
    # print('-----------------------------------------------------------------------------')
    # print(n)
    #
    # #Creates new columns containing the area of each polymer/total
    # remove_datapt_quest = input('Do you want to delete a polymer? If so, please enter ''y'', else enter in ''n'': ')
    # while remove_datapt_quest == 'y' or remove_datapt_quest == 'Y':
    #     remove_datapt = input('Please enter the polymer name you want to delete (ex: 24mer): ')
    #     del n[remove_datapt]
    #     remove_datapt_quest= input('Any more polymers you want to delete? Please enter y for yes and n for no: ')
    # #Creates new columns containing the area of each polymer/total
    # n['Total'] = n.sum(axis=1)
    # headers_list = n.columns.values.tolist()
    # for i in range(len(headers_list)-1):
    #     divide_name = headers_list[i] + '/' + headers_list[-1]
    #     n[divide_name] = n.iloc[:,i] / n.iloc[:,len(headers_list)-1]
    #
    #Sorts table by time and fill 'NaN' values with '0'
    n.sort_index(inplace=True)
    n = n.fillna(0)
    n['Total'] = n.sum(axis=1)
    headers_list = n.columns.values.tolist()
    #print(headers_list)
    for i in range(len(headers_list)-1):
        divide_name = headers_list[i] + '/' + headers_list[-1]
        n[divide_name] = round(n.iloc[:,i] / n.iloc[:,len(headers_list)-1],2)
    #n = n.fillna(0)
    # print('This is the table for fractional area vs. size. Please analyze to see if you want to delete outliers.')
    # print('-----------------------------------------------------------------------------')
    # print(n)

    # remove_datapt_quest = input('Do you want to delete a polymer? If so, please enter ''y'', else enter in ''n'': ')
    # while remove_datapt_quest == 'y' or remove_datapt_quest == 'Y':
    #     remove_datapt = input('Please enter the polymer name you want to delete (ex: 24mer): ')
    #     del n[remove_datapt]
    #     del n[remove_datapt + '/Total']
    #     headers_list.remove(remove_datapt)
    #     #headers_list.remove(remove_datapt + '/Total')
    #     n['Total'] = 0
    #     n['Total'] = n.iloc[:,:int(len(n.columns)/2)].sum(axis=1)
    #     remove_datapt_quest= input('Any more polymers you want to delete? Please enter y for yes and n for no: ')
    for i in range(len(headers_list)-1):
        divide_name = headers_list[i] + '/' + headers_list[-1]
        n[divide_name] = round(n.iloc[:,i] / n.iloc[:,len(headers_list)-1],3)
    #Sorts table by time and fill 'NaN' values with '0'
    n = n.fillna(0)

    #Exports non-concentration fixed data. Gives the fractional area for
    #Each polymer and the time points
    #export_before_conc = n.to_csv('Export_data_Before_concfix.csv',sep=',')
    return n



def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)',text)]



def conc_fix(df,conc):
    #conc = int(input("Please enter the concentration(nM): "))

    #Creates new columns containing polymer/total multiplied by concentration
    headers = df.columns.values.tolist()
    for head in headers:
        if '/Total' in head:
            df.loc[:,head] = df.loc[:,head] * conc
    df = df.fillna(0)
    df.sort_index(inplace=True)

    #csv_name = input("Please enter desired name of exported csv file: ")

    #Gets the time and concentration/total columns only
    col_length = df.shape[1]
    midpt = int((col_length)/2) + 1
    df1 = df.iloc[:,midpt:]
    # p = Path('Exported Data')
    # p.mkdir(exist_ok= True)

    #Exports .txt file of polymer/total
    # export_txt = df1.to_csv(os.getcwd() + '/' + str(p) + '/' + csv_name  +'.txt',sep='\t')
    # #Exports the data to excel sheet
    # export = df.to_csv(os.getcwd() + '/' + str(p) + '/' + csv_name  + '.csv',sep=',')
    return df



polymer_list = []
class polymerBounds(QtWidgets.QMainWindow):

    def __init__(self):
        super(polymerBounds,self).__init__()

        self.ui3 = Ui_MainWindow3()
        self.ui3.setupUi3(self)
        #self.setWindowTitle('Polymer Bounds')
        self.show()





        global df_differences_global
        try:
            #Calculates the filtered tables with differences in a separate column
            df_differences_global = sample_distance(df_global_peaks)
            self.df_differences = sample_distance(df_global_peaks)
            self.df_diff_ranges = self.df_differences['Diff'].tolist()
            self.df_diff_ranges.sort()
            self.df_diff_ranges_tab = pd.DataFrame(self.df_diff_ranges, columns=['Diff'])

            # Calculates the differences and just puts them into a column
            # self.df_differences2 = sample_distance(df_global_peaks)
            # self.df_diff_ranges2 = self.df_differences2['Diff'].tolist()
            # self.df_diff_ranges2.sort()
            # self.df_diff_ranges_tab = pd.DataFrame(self.df_diff_ranges, columns=['Diff'])
            #


        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table. Please enter min height')
            self.close()
            error_dialog.exec_()





        self.ui3.pushButton.clicked.connect(self.showDifferencesTable)
        self.ui3.pushButton_5.clicked.connect(self.showDifferences)
        self.ui3.pushButton_2.clicked.connect(self.getPolymerName)
        self.ui3.pushButton_3.clicked.connect(self.getDifferenceRanges)
        self.ui3.pushButton_7.clicked.connect(self.showTableWithSize)
        self.ui3.pushButton_4.clicked.connect(self.showFracAreaSizeBefore)
        self.ui3.pushButton_8.clicked.connect(self.goBack)
        self.ui3.pushButton_6.clicked.connect(self.showFracAreaSizeAfter)
        self.ui3.pushButton_9.clicked.connect(self.goalignParam)
        self.ui3.pushButton_11.clicked.connect(self.showDeletePolymer)
        self.ui3.pushButton_10.clicked.connect(closeProgram)
        self.ui3.pushButton_12.clicked.connect(self.saveTableAfterConc)
        self.ui3.pushButton_13.clicked.connect(self.saveTableAfterDeletion)
        self.ui3.pushButton_14.clicked.connect(self.getPolymersRanges)
        self.ui3.pushButton_15.clicked.connect(self.calcFracAreaSizeAfter)
        self.ui3.pushButton_16.clicked.connect(self.calcTableandFAVSB)
        self.ui3.pushButton_17.clicked.connect(self.calcDeletePolymer)
        self.ui3.pushButton_18.clicked.connect(self.showPreliminaryGraph)
        self.ui3.pushButton_19.clicked.connect(self.showPreliminaryDeleteGraph)
        self.ui3.pushButton_19.setEnabled(False)
        self.ui3.pushButton_9.setEnabled(False)



        # self.ui3.pushButton_3.clicked.connect(self.getLowerBound)
        # self.ui3.pushButton_4.clicked.connect(self.getUpperBound)
        #
        #self.ui3.label.setText(polymer_name)
        # self.ui3.label_5.setText(self.lower_bound)
        # self.ui3.label_5.setText(self.upper_bound)

        # self.df_all_peaks = filtered_data(fileName, time_underscore)
        # # self.df_int_std_all = int_std_all(self.df_all_peaks)
        # model = pandasModel(self.df_all_peaks)
        # self.view = QTableView()
        # self.view.setModel(model)
        # self.view.setWindowTitle('All Peaks')
        # self.view.resize(800, 600)
        # # self.close()
        # self.view.show()



    def showDifferencesTable(self):
        #global df_differences_global
        try:
            # df_differences_global = sample_distance(df_global_peaks)
            # self.df_differences = sample_distance(df_global_peaks)
            # self.df_diff_ranges = self.df_differences['Diff'].tolist()
            # self.df_diff_ranges.sort()
            # self.df_diff_ranges_tab = pd.DataFrame(self.df_diff_ranges,columns=['Diff'])


            #for table
            model = pandasModel(self.df_differences)
            self.view_diff = QTableView()
            self.view_diff.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_diff.resizeColumnsToContents()
            self.view_diff.setModel(model)
            self.view_diff.setWindowTitle('Differences Table')
            self.view_diff.resize(800,600)
            #self.close
            self.view_diff.show()

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table. Please go back and reenter parameters')
            error_dialog.exec_()


    def showDifferences(self):
        try:
            # self.df_differences2 = sample_distance(df_global_peaks)
            # self.df_diff_ranges2= self.df_differences2['Diff'].tolist()
            # self.df_diff_ranges2.sort()
            # self.df_diff_ranges_tab = pd.DataFrame(self.df_diff_ranges, columns=['Diff'])

            # For ranges only
            model2 = pandasModel(self.df_diff_ranges_tab)
            self.view_diff2 = QTableView()
            self.view_diff2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_diff2.resizeColumnsToContents()
            self.view_diff2.setModel(model2)
            self.view_diff2.setWindowTitle('Differences')
            self.view_diff2.resize(300, 600)
            # self.close
            self.view_diff2.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Please press show differences ranges first')
            error_dialog.exec_()

    def getPolymerName(self):
        global polymer_list
        try:
            polymer_name = self.ui3.lineEdit_2.text()
            polymer_list = polymer_name.split(',')
            names = ','.join(polymer_list)
            self.ui3.label.setText(names)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Invalid polymer names please try again')
            error_dialog.exec_()

        #print(polymer_list)
    def getDifferenceRanges(self):
        global diff_ranges_global
        global final_list
        try:
            diff_ranges_global = self.ui3.lineEdit.text()

            #changes the ranges from string type to float
            #ranges_list = "[110,111]:[111,113]"
            diff_ranges_global = diff_ranges_global.replace(" ","")
            a = diff_ranges_global.split(':') #Gives [[110,111],[111,113]] a list type
            final_list = []
            for x in a:
                new_x = x.strip('[]') #Gives 110,111
                num_list = new_x.split(',') #gives [
                for i in range(len(num_list)):
                    num_list[i] = float(num_list[i])
                final_list.append(num_list)

            diff_ranges = self.ui3.lineEdit.text()
            self.ui3.label_6.setText(diff_ranges)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Polymers or difference ranges entered incorrectly, please try again')
            error_dialog.exec_()


    def calcTableandFAVSB(self):
        global pre_fASB_test
        global zip_dict
        try:

            self.tws = size(df_differences_global, polymer_list, final_list) #Table with size
            dp_col = self.tws['Data Point']
            size_col = self.tws['Size']
            zip_dict = dict(zip(dp_col, size_col))
            #print(zip_dict)
            pre_fASB_test = table(self.tws)
            self.time_list = pre_fASB_test.index.values.tolist()
            pre_fASB_test.insert(0,column = 'Time', value = self.time_list)
            #self.fASB = table(self.tws)
            self.fASB = pre_fASB_test
            self.ui3.pushButton_9.setEnabled(True)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Polymers or difference ranges entered incorrectly, please try again')
            error_dialog.exec_()

    def showTableWithSize(self):
        #global tws

        try:
            # tws = size(df_differences_global, polymer_list, final_list)

            # print(dp_col)
            # print(size_col)

            model_tws = pandasModel(self.tws)
            self.view_tws = QTableView()
            self.view_tws.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_tws.resizeColumnsToContents()
            self.view_tws.setModel(model_tws)
            self.view_tws.setWindowTitle('Table with Polymer Size')
            self.view_tws.resize(1000, 600)
            # self.close()
            self.view_tws.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Polymers or difference ranges entered incorrectly, please try again')
            error_dialog.exec_()

    def showFracAreaSizeBefore(self):
        #global fASB
        try:
            # fASB = table(tws)
            model_fASB = pandasModel(self.fASB)
            self.view_fASB = QTableView()
            self.view_fASB.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_fASB.resizeColumnsToContents()
            self.view_fASB.setModel(model_fASB)
            self.view_fASB.setWindowTitle('Frac v. size before conc. fix')
            self.view_fASB.resize(1000,600)
            self.view_fASB.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Polymers or difference ranges entered incorrectly, please try again')
            error_dialog.exec_()




    def calcFracAreaSizeAfter(self):
        try:
            pre_fASB = table(self.tws)
            self.time_list = pre_fASB.index.values.tolist()
            pre_fASB.insert(0, column='Time', value=self.time_list)

            fASB2 = pre_fASB
            conc = self.ui3.lineEdit_3.text()
            #pre_fasA = conc_fix(fASB2, int(conc))
            self.fasA = conc_fix(fASB2,int(conc))
            # fASB3 = pre_fasA
            # fASB3.insert(0, column='Time', value=self.time_list)
            # self.fasA = fASB3
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Invalid concentration')
            error_dialog.exec_()

    def showFracAreaSizeAfter(self):
        #global fasA
        try:
            model_fasA = pandasModel(self.fasA)
            self.view_fasA = QTableView()
            self.view_fasA.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_fasA.resizeColumnsToContents()
            self.view_fasA.setModel(model_fasA)
            self.view_fasA.setWindowTitle('Frac v. size after conc. fix')
            self.view_fasA.resize(1200, 600)
            self.view_fasA.show()
            #self.view_fasA.close()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table. Please press show frav v area before, then click this button'
                                     'again')
            error_dialog.exec_()

    #Calculates the deleted polymer
    def calcDeletePolymer(self):
        global table_adel_before_conc_fix
        global flag
        try:

            #     pre_fASB = table(self.tws)
        #     self.time_list = pre_fASB.index.values.tolist()
            dp_col = self.tws['Data Point']
            size_col = self.tws['Size']
            zip_dict = dict(zip(dp_col, size_col))
            #print(zip_dict)
            pre_fASB = table(self.tws)
            self.time_list = pre_fASB.index.values.tolist()
            #pre_fASB.insert(0, column='Time', value=self.time_list)

            fASB2 = pre_fASB


            self.conc = self.ui3.lineEdit_3.text()
            pre_fasA = conc_fix(fASB2, int(self.conc)) #After concentration fix

            fASB3 = pre_fasA #After conc. fix just reinitialized

            fASB3.insert(0, column='Time', value=self.time_list)

            del_polymer = self.ui3.lineEdit_4.text()
            del_polymer_list = del_polymer.split(',')
            del_polymer_list.sort(key=natural_keys)
            #print(del_polymer_list)
            # Deleted fractional area v size before conc. fix
            #fASB2.insert(0, column='Time', value=self.time_list)
            fASB2.reset_index(level=0, inplace=True)

            #print(fASB2)
            table_adel_before_conc_fix = deletePolymer(fASB2, del_polymer_list)
           # print(table_adel_before_conc_fix)
            table_adel = deletePolymer(pre_fasA,del_polymer_list)
            conc_inside = self.ui3.lineEdit_3.text()
            pre_table_adel2 = conc_fix(table_adel,int(conc_inside))
            self.table_adel2 = pre_table_adel2
            self.ui3.pushButton_19.setEnabled(True)
            flag = True

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Already deleted polymer or invalid polymer')
            error_dialog.exec_()



    # def btnstate(self):
    #     if self.ui3.pushButton_17.isChecked():
    #         return True
    #     else:
    #         return False
    def showDeletePolymer(self):
        try:
            # del_polymer = self.ui3.lineEdit_4.text()
            # del_polymer_list = del_polymer.split(',')
            # del_polymer_list.sort(key=natural_keys)
            # table_adel = deletePolymer(self.fasA,del_polymer_list)

            model_adel = pandasModel(self.table_adel2)
            self.view_adel = QTableView()
            self.view_adel.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_adel.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.view_adel.resizeColumnsToContents()
            self.view_adel.resizeRowsToContents()
            self.view_adel.setModel(model_adel)
            self.view_adel.setWindowTitle('Frac v size after deletion')
            self.view_adel.resize(1000,600)
            self.view_adel.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table. Please press show frav v area before, then click this button'
                                     'again')
            error_dialog.exec_()

    #QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)"
    def getPolymersRanges(self):
        self.fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Excel file with difference ranges","", "Excel Files (*.xlsx);;Excel 03 (*.xls)")
        if self.fileName:
            size_list = import_sizes(self.fileName)
            ranges_list = import_ranges(self.fileName)
            self.ui3.lineEdit_2.setText(size_list)
            self.ui3.lineEdit.setText(ranges_list)


    def saveTableAfterConc(self):
        dirName = str(QtWidgets.QFileDialog.getExistingDirectory(self,'Select Directory'))

        if dirName:
            half_table = kintek_export(self.fasA)
            full_table = self.fasA.iloc[:,1:]
            half_table.to_csv(dirName + '/' + self.ui3.lineEdit_5.text() + '.txt', sep = '\t')
            full_table.to_csv(dirName + '/' + self.ui3.lineEdit_5.text() + '.csv', sep = ',')


    def saveTableAfterDeletion(self):
        dirName2 = str(QtWidgets.QFileDialog.getExistingDirectory(self,'Select Directory'))
        if dirName2:
            half_table = kintek_export(self.table_adel2)
            full_table = self.table_adel2.iloc[:,1:]
            half_table.to_csv(dirName2 + '/' + self.ui3.lineEdit_6.text() + '.txt', sep='\t')
            full_table.to_csv(dirName2 + '/' + self.ui3.lineEdit_6.text() + '.csv', sep=',')


    def showPreliminaryGraph(self):
        try:

            half_table = kintek_export(self.fasA.iloc[:,1:])
            #time_values = half_table.index.tolist()
            #Create data sets with all the fractional areas. Only need to calculate one time for x value
            #for i in range(1,len(half_table)):
            time_values = half_table.index.tolist()
            y_values_list = []
            for i in range(len(half_table.columns)):

                y_values = half_table.iloc[:,i].values.tolist()
                plt.plot(time_values,y_values)
                #y_values_list.append(list(zip(time_values,y_values)))

            #print(y_values_list)
            #[[(0.0, 0.0), (0.0025, 33.45), (0.004, 39.75), (0.006, 47.55), (0.008, 50.85), (0.01, 55.35), (0.012, 56.7), (0.015, 57.9)]]

            # for mix in y_values_list:
            #     for coor in mix:
            #         plt.scatter(coor[0],coor[1])

            plt.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot graph, please calculate the frac area vs. size again')
            error_dialog.exec_()
        # for x,y in zip(time_values,y_values_list):
        #     plt.scatter(x,y)
        # print(y_values)
        # print(time_values)

        #plt.scatter(time_values,y_values)

        #plt.show()


    def showPreliminaryDeleteGraph(self):
        try:

            half_table = kintek_export(self.table_adel2.iloc[:,1:])
            #time_values = half_table.index.tolist()
            #Create data sets with all the fractional areas. Only need to calculate one time for x value
            #for i in range(1,len(half_table)):
            time_values = half_table.index.tolist()
            y_values_list = []
            for i in range(len(half_table.columns)):

                y_values = half_table.iloc[:,i].values.tolist()
                plt.plot(time_values,y_values)
                #y_values_list.append(list(zip(time_values,y_values)))

            #print(y_values_list)
            #[[(0.0, 0.0), (0.0025, 33.45), (0.004, 39.75), (0.006, 47.55), (0.008, 50.85), (0.01, 55.35), (0.012, 56.7), (0.015, 57.9)]]

            # for mix in y_values_list:
            #     for coor in mix:
            #         plt.scatter(coor[0],coor[1])

            plt.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot graph, please calculate the frac area vs. size again')
            error_dialog.exec_()




    def goBack(self):
        self.close()
        #self.backDesc = RunDesc()
        #polymer_list.append(self.polymer_name)

    def goalignParam(self): #goes to the alignment parameters without asking for skipping alignment parameter popup
        #self.close()
        self.aP = alignParam()
        self.aP.ui5.pushButton_10.setEnabled(True)
        self.aP.ui5.pushButton_11.setEnabled(True)
        self.aP.ui5.pushButton_13.setEnabled(True)

    # def goToSkipAlign(self): Method to go to skip alignment
    #     self.close()
    #     self.skipAlign = skipAlign()

    #     self.ui3.label_5.setText(self.polymer_name)
    #
    # def getLowerBound(self):
    #     self.lower_bound = float(self.ui3.lineEdit_3.text())
    #     self.ui3.label_5.setText(self.lower_bound)
    #
    # def getUpperBound(self):
    #     self.upper_bound = float(self.ui3.lineEdit_4.text())
    #     self.ui3.label_5.setText(self.upper_bound)


# class skipAlign(QtWidgets.QMainWindow): Class popup for skip alignment
#     def __init__(self):
#         super().__init__()
#         self.ui4 = Ui_MainWindow6()
#         self.ui4.setupUi(self)
#         self.show()
#
#
#         self.ui4.pushButton.clicked.connect(self.closeProgram)
#         self.ui4.pushButton_2.clicked.connect(self.a_param)
#
#
#     def a_param(self):
#         self.close()
#         self.aP = alignParam()
#         self.aP.ui5.pushButton_10.setEnabled(True)
#         self.aP.ui5.pushButton_11.setEnabled(True)
#         self.aP.ui5.pushButton_13.setEnabled(True)
#
#     def closeProgram(self):
#         sys.exit(app.exec_())



class alignParam(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui5 = Ui_MainWindow5()
        self.ui5.setupUi5(self)
        self.show()
        self.plot_time_underscore = 0
        self.fsaNamesList = []
        self.num_pts = 0
        #Remember to change these values to an int

        self.ui5.pushButton.clicked.connect(self.getFSAFiles)
        self.ui5.pushButton_2.clicked.connect(self.getTimeUnderscore)
        self.ui5.pushButton_8.clicked.connect(self.showFileNames)
        self.ui5.pushButton_7.clicked.connect(self.showTimePts)
        self.ui5.pushButton_3.clicked.connect(self.showPossibleDimensions)
        self.ui5.pushButton_4.clicked.connect(self.showAlignment)
        self.ui5.pushButton_5.clicked.connect(self.show3d)
        self.ui5.pushButton_6.clicked.connect(closeProgram)
        self.ui5.pushButton_9.clicked.connect(self.goBack)
        self.ui5.pushButton_10.clicked.connect(self.show3dscaled)
        self.ui5.pushButton_11.clicked.connect(self.show2dscaled)
        self.ui5.pushButton_10.setEnabled(False)
        self.ui5.pushButton_11.setEnabled(False)
        self.ui5.pushButton_12.clicked.connect(self.show3dlog)
        self.ui5.pushButton_13.clicked.connect(self.show3dlogscaled)
        self.ui5.pushButton_13.setEnabled(False)

    def getFSAFiles(self):
        try:
            self.dirName = str(QtWidgets.QFileDialog.getExistingDirectory(self,'Select Directory',options = QtWidgets.QFileDialog.DontUseNativeDialog))
            if self.dirName:
                self.ui5.lineEdit.setText(self.dirName)
                #Gets the number of pts (for dimension purposes)
                self.fsaNamesList = getFSANamesListNotNum(self.dirName)
                self.num_pts = len(self.fsaNamesList)
                first_fsa = getFSANames(self.dirName)
                self.ui5.label_8.setText(first_fsa)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Directory cannot detect any .fsa files, please try again')
            error_dialog.exec_()



    def getTimeUnderscore(self):
        try:
            self.plot_time_underscore = int(self.ui5.lineEdit_2.text())
            self.fsaNamesList = getFSANamesList(self.dirName,self.plot_time_underscore)
            self.ui5.label_12.setText(str(len(timePts(self.fsaNamesList,self.plot_time_underscore))))

        #self.ui5.label_8.setText(str(plot_time_underscore))
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Time underscore not valid,please try again')
            error_dialog.exec_()

    def showFileNames(self):
        try:
            self.fName= displayFileNames(getFSANamesList(self.dirName,self.plot_time_underscore))
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show time pts. please check the time underscore or folder with .fsa files.')
            error_dialog.exec_()

    def showTimePts(self):
        try:
            self.time_pt = displayTimePts(timePts(self.fsaNamesList,self.plot_time_underscore))
        #Write another method that gets the number of time pts.
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show time pts. please check the time underscore or folder with .fsa files.')
            error_dialog.exec_()

    def showPossibleDimensions(self):
        try:
            dim_table = divisors(self.num_pts)
            model_dim = pandasModel(dim_table)
            self.view_dim = QTableView()
            self.view_dim.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_dim.resizeColumnsToContents()
            self.view_dim.setModel(model_dim)
            self.view_dim.resizeColumnsToContents()
            self.view_dim.setWindowTitle('Possible picture dimensions')
            self.view_dim.resize(600, 600)
            self.view_dim.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show possible dimensions, please check the .fsa files folder.')
            error_dialog.exec_()

    def showAlignment(self):
        try:

            min_x = self.ui5.lineEdit_3.text()
            max_x = self.ui5.lineEdit_4.text()
            min_y = self.ui5.lineEdit_5.text()
            max_y = self.ui5.lineEdit_6.text()
            desired_row = self.ui5.lineEdit_7.text()
            desired_col = self.ui5.lineEdit_8.text()
            dirName= self.dirName
            plot_time_underscore = self.plot_time_underscore
            #plot(self.dirName,self.plot_time_underscore,int(self.min_x),int(self.max_x),int(self.min_y),int(self.max_y),int(self.desired_row),int(self.desired_col))
            plot(dirName,plot_time_underscore,int(min_x),int(max_x),int(min_y),int(max_y),int(desired_row),int(desired_col))


        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please check x/y ranges.')
            error_dialog.exec_()

        #plot3d(length_dir,fsa_names_sorted,time_underscore,x_min,x_max,y_min,y_max,folder_fsa):
    def show3d(self):

        try:
            # num_pts = self.num_pts
            # fsaNamesList = self.fsaNamesList
            # plot_time_underscore = self.plot_time_underscore
            # min_x = self.min_x
            # max_x = self.max_x
            # min_y = self.min_y
            # max_y = self.max_y
            # dirName = self.dirName
            self.min_x = self.ui5.lineEdit_3.text()
            self.max_x = self.ui5.lineEdit_4.text()
            self.min_y = self.ui5.lineEdit_5.text()
            self.max_y = self.ui5.lineEdit_6.text()
            self.desired_row = self.ui5.lineEdit_7.text()
            self.desired_col = self.ui5.lineEdit_8.text()

            plot3d(self.num_pts,self.fsaNamesList,self.plot_time_underscore,int(self.min_x),int(self.max_x),int(self.min_y),
                 int(self.max_y),self.dirName)


            #plot3d(num_pts,fsaNamesList,plot_time_underscore,int(min_x),int(max_x),int(min_y),int(max_y),dirName)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please check x/y ranges')
            error_dialog.exec_()

    def show3dscaled(self):
        try:
            # num_pts = self.num_pts
            # fsaNamesList = self.fsaNamesList
            # plot_time_underscore = self.plot_time_underscore
            # min_x = self.min_x
            # max_x = self.max_x
            # min_y = self.min_y
            # max_y = self.max_y
            # dirName = self.dirName
            self.min_x = self.ui5.lineEdit_3.text()
            self.max_x = self.ui5.lineEdit_4.text()
            self.min_y = self.ui5.lineEdit_5.text()
            self.max_y = self.ui5.lineEdit_6.text()
            self.desired_row = self.ui5.lineEdit_7.text()
            self.desired_col = self.ui5.lineEdit_8.text()

            try:
                if flag:
                    plot3dScaled(self.num_pts, self.fsaNamesList, self.plot_time_underscore, int(self.min_x),
                                 int(self.max_x), int(self.min_y),
                                 1, self.dirName, zip_dict, pre_fASB_test)

            except NameError:
                plot3dScaled(self.num_pts, self.fsaNamesList, self.plot_time_underscore, int(self.min_x), int(self.max_x),
                             int(self.min_y),
                             1, self.dirName, zip_dict, pre_fASB_test)

            #plot3d(num_pts,fsaNamesList,plot_time_underscore,int(min_x),int(max_x),int(min_y),int(max_y),dirName)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, if you want scaled 3d plot, then you have to go back'
                                     'and perform fractional area vs size')
            error_dialog.exec_()

    def show2dscaled(self):
        try:

            min_x = self.ui5.lineEdit_3.text()
            max_x = self.ui5.lineEdit_4.text()
            min_y = self.ui5.lineEdit_5.text()
            max_y = self.ui5.lineEdit_6.text()
            desired_row = self.ui5.lineEdit_7.text()
            desired_col = self.ui5.lineEdit_8.text()
            dirName= self.dirName
            plot_time_underscore = self.plot_time_underscore
            #plot(self.dirName,self.plot_time_underscore,int(self.min_x),int(self.max_x),int(self.min_y),int(self.max_y),int(self.desired_row),int(self.desired_col))
            try:
                if flag:
                    plot2dScaled(dirName,plot_time_underscore,int(min_x),int(max_x),int(min_y),1,int(desired_row),int(desired_col), zip_dict, pre_fASB_test)

            except NameError:
                plot2dScaled(dirName,plot_time_underscore,int(min_x),int(max_x),int(min_y),1,int(desired_row),int(desired_col), zip_dict, pre_fASB_test)
            #plot(dirName,plot_time_underscore,int(min_x),int(max_x),int(min_y),int(max_y),int(desired_row),int(desired_col))


        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please perform frac area v size first.')
            error_dialog.exec_()

    def show3dlog(self):
        try:
            # num_pts = self.num_pts
            # fsaNamesList = self.fsaNamesList
            # plot_time_underscore = self.plot_time_underscore
            # min_x = self.min_x
            # max_x = self.max_x
            # min_y = self.min_y
            # max_y = self.max_y
            # dirName = self.dirName
            self.min_x = self.ui5.lineEdit_3.text()
            self.max_x = self.ui5.lineEdit_4.text()
            self.min_y = self.ui5.lineEdit_5.text()
            self.max_y = self.ui5.lineEdit_6.text()
            self.desired_row = self.ui5.lineEdit_7.text()
            self.desired_col = self.ui5.lineEdit_8.text()

            plot3dlog(self.num_pts,self.fsaNamesList,self.plot_time_underscore,int(self.min_x),int(self.max_x),int(self.min_y),
                 int(self.max_y),self.dirName)


            #plot3d(num_pts,fsaNamesList,plot_time_underscore,int(min_x),int(max_x),int(min_y),int(max_y),dirName)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please check x/y ranges')
            error_dialog.exec_()


    def show3dlogscaled(self):
        try:

            min_x = self.ui5.lineEdit_3.text()
            max_x = self.ui5.lineEdit_4.text()
            min_y = self.ui5.lineEdit_5.text()
            max_y = self.ui5.lineEdit_6.text()
            desired_row = self.ui5.lineEdit_7.text()
            desired_col = self.ui5.lineEdit_8.text()
            dirName = self.dirName
            plot_time_underscore = self.plot_time_underscore
            # plot(self.dirName,self.plot_time_underscore,int(self.min_x),int(self.max_x),int(self.min_y),int(self.max_y),int(self.desired_row),int(self.desired_col))
            try:
                if flag:
                    plot3dlogscaled(self.num_pts, self.fsaNamesList, self.plot_time_underscore, int(self.min_x), int(self.max_x),
                             int(self.min_y),
                             1, self.dirName, zip_dict, pre_fASB_test)

            except NameError:
                plot3dlogscaled(self.num_pts, self.fsaNamesList, self.plot_time_underscore, int(self.min_x), int(self.max_x),
                             int(self.min_y),
                             1, self.dirName, zip_dict, pre_fASB_test)
            # plot(dirName,plot_time_underscore,int(min_x),int(max_x),int(min_y),int(max_y),int(desired_row),int(desired_col))


        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please perform frac area v size first.')
            error_dialog.exec_()


    def goBack(self):
        self.close()



class displayFileNames(QtWidgets.QWidget):
    def __init__(self,fsa_list):
        super().__init__()
        self.ui7 = Ui_Form()
        self.ui7.setupUi(self)
        self.ui7.textEdit.append(str(fsa_list))
        # self.ui7.(str(fsa_list))
        #self.ui7.textEdit.append(str(fsa_list))
        self.show()

class displayTimePts(QtWidgets.QWidget):
    def __init__(self,time_list):
        super().__init__()
        self.ui8 = Ui_Form2()
        self.ui8.setupUi(self)
        self.ui8.textBrowser.append(str(time_list))
        self.show()
# class RunDesc(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(RunDesc,self).__init__()
#         self.ui2 = Ui_MainWindow2()
#         self.ui2.setupUi2(self)
#         self.setWindowTitle('Run Description')
#     #
#         self.ui2.pushButton.clicked.connect(self.gettxt)
#
#     def gettxt(self):
#         txtName = QtGui.QFileDialog.getOpenFileName(self, 'Single File', 'C:\\', '*.py')
#

if __name__ == '__main__':
    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = exception_hook
    #
    # appctxt = ApplicationContext()
    # window = QLabel()
    # image = QPixmap(appctxt.get_resource('image.jpg'))
    # window.setPixmap(image)
    # window.show()
    # sys.exit(appctxt.app.exec_())

    app = QtWidgets.QApplication(sys.argv)
    application = MyWindow()
    application.show()
    sys.exit(app.exec_())

