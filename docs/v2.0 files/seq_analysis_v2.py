from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QTableView, QTableWidgetItem, QTableWidget
from plot_fsa_v2 import *
from file_names import Ui_Form
from time_pts_align import Ui_Form2
import sys
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
from ui_begin_v2 import Ui_MainWindow


# Creates a pandas like dataframe for output of tables
class pandasModel(QAbstractTableModel):

    def __init__(self, data):  # Takes in a pandas df as data
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


class displayFileNames(QtWidgets.QWidget):
    def __init__(self, fsa_list):
        super().__init__()
        self.ui7 = Ui_Form()
        self.ui7.setupUi(self)
        self.ui7.textEdit.append(str(fsa_list))
        self.show()


class displayTimePts(QtWidgets.QWidget):
    def __init__(self, time_list):
        super().__init__()
        self.ui8 = Ui_Form2()
        self.ui8.setupUi(self)
        self.ui8.textBrowser.append(str(time_list))
        self.show()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tab1
        self.ui.browse_button.clicked.connect(self.getTxt)  # gets the .txt file with peak data
        self.ui.submit_button.clicked.connect(self.getTimeUnderscore)  # Gets time underscore
        self.ui.pushButton_10.clicked.connect(self.showAllPeaks)  # shows all the peaks (product + int std)
        self.ui.pushButton_12.clicked.connect(self.showAllIntStdPeaks)  # Shows all internal std peaks
        self.ui.pushButton_13.clicked.connect(self.showAllProductPeaks)  # Shows all non internal std peaks
        self.ui.pushButton_14.clicked.connect(self.getMinHeight)  # Gets the min height filters
        self.ui.pushButton_15.clicked.connect(
            self.showAllFilteredPeaks)  # Shows all product peaks with min height filter
        self.ui.pushButton_16.clicked.connect(
            self.showFilteredStd)  # Shows all internal std peaks with min height filter

        # Tab2
        self.ui.pushButton_19.clicked.connect(self.showDifferences)  # shows sorted ranges list
        self.ui.pushButton_20.clicked.connect(
            self.showDifferencesTable)  # shows all peaks with difference ranges column
        self.ui.pushButton_21.clicked.connect(self.getPolymersRanges)  # Gets the excel values and inputs into table
        self.ui.pushButton_2.clicked.connect(self.add_input_row)  # Adds a row for the input table
        self.ui.pushButton_24.clicked.connect(
            self.calcTableandFAVSB)  # Calculates the fractional area vs size before conc
        self.ui.pushButton_25.clicked.connect(self.showTableWithSize)  # Shows table with polymer sizes in column
        self.ui.pushButton_23.clicked.connect(
            self.showFracAreaSizeBefore)  # Shows fractional area vs size before conc fix
        self.ui.pushButton_32.clicked.connect(self.calcFracAreaSizeAfter)  # Calculates the frac area v size after conc
        self.ui.pushButton_36.clicked.connect(self.showFracAreaSizeAfter)  # Shows frac area v size afteer conc fix
        self.ui.pushButton_37.clicked.connect(self.saveTableAfterConc)  # Saves conc fixed table to directory
        self.ui.pushButton_38.clicked.connect(self.calcDeletePolymer)  # Calculates frac area v size after deletion
        self.ui.pushButton_39.clicked.connect(self.showDeletePolymer)  # Shows the frac area v size after deletion table
        self.ui.pushButton_40.clicked.connect(self.saveTableAfterDeletion)  # Path to save table after deleted  polymer
        self.ui.pushButton_41.clicked.connect(self.showPreliminaryGraph)  # Shows the prelimnary graph
        self.ui.pushButton_42.clicked.connect(
            self.showPreliminaryDeleteGraph)  # Shows the preliminary graph after polymer deletion

        # Tab3
        self.ui.pushButton.clicked.connect(self.getFSAFiles)  # Browse for .fsa files
        self.ui.pushButton_45.clicked.connect(self.time_underscore_plot)  # Submits the time underscore for .fsa plots
        self.ui.pushButton_56.clicked.connect(self.showFileNames)  # shows files aligning
        self.ui.pushButton_57.clicked.connect(self.showTimePts)  # Shows time points aligning
        self.ui.pushButton_58.clicked.connect(self.showPossibleDimensions)  # Shows possible dim of 2d plots
        self.ui.pushButton_67.clicked.connect(self.showAlignment)  # Shows 2d plot alignment
        self.ui.pushButton_65.clicked.connect(self.show3d)  # Shows 3d plots
        self.ui.pushButton_69.clicked.connect(self.show3dlog)  # Shows log(3d) plots
        self.ui.pushButton_68.clicked.connect(self.show2dscaled)  # Shows 2d scaled plots
        self.ui.pushButton_66.clicked.connect(self.show3dscaled)  # Shows 3d scaled plots
        self.ui.pushButton_70.clicked.connect(self.show3dlogscaled)  # shows log(3d) scaled plots

    # Functions gets the .txt raw output form the sequencer
    def getTxt(self):
        # global fileName
        # options = QtGui.QFileDialog.Options()
        # Opens the .txt raw output file
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.txt')
        if fileName != '':  # If the file found isn't empty
            self.previous_fileName = fileName
            # Gets the run description from the .txt file. Usually it's the second line of the file. First line is headers
            self.ui.name_txt_line_edit_fill.setText(fileName)
            file = open(fileName, 'r')
            file.readline()
            second_line = file.readline()
            split_second_line = second_line.split()
            txt_file_name = split_second_line[1]
            file.close()
            self.ui.sample_name_fill.setText(txt_file_name)
            self.txtfileName = fileName
        elif fileName == '' and self.ui.name_txt_line_edit_fill.text() != '':  # This corrects if the filname is entered, but user presses cancel
            self.ui.name_txt_line_edit_fill.setText(self.previous_fileName)
            self.txtfileName = self.previous_fileName

    # Have to error check in case not an integer
    def getTimeUnderscore(self):

        try:
            self.time_underscore = int(self.ui.time_line_edit_fill.text())
            self.df_all_peaks = filtered_data(self.txtfileName,
                                              self.time_underscore)
            self.df_all_int_std_peaks = int_std_all(self.df_all_peaks, self.ui.lineEdit.text().upper()
                                                    )  # Calculates all internal std. peaks
            self.ui.pushButton_10.setEnabled(True)  # enables show all peaks button before submitting data
            self.ui.pushButton_12.setEnabled(True)  # enables show all internal std. peak button
            self.ui.pushButton_13.setEnabled(True)  # enables show all non int std. peaks
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No time underscore, or dye does not match dye detected, please try again')
            error_dialog.exec_()

    # Shows all peaks
    def showAllPeaks(self):
        try:
            model = pandasModel(self.df_all_peaks)
            self.view = QTableView()
            self.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view.resizeColumnsToContents()
            self.view.setModel(model)
            self.view.setWindowTitle('All Peaks')
            self.view.resize(800, 600)
            # self.close()
            self.view.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No time underscore, or dye does not match dye detected, please try again')
            error_dialog.exec_()

    # Shows all internal std peaks after pressing button
    def showAllIntStdPeaks(self):
        try:
            model_all_int = pandasModel(self.df_all_int_std_peaks)
            self.view_int_std_all = QTableView()
            self.view_int_std_all.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_int_std_all.resizeColumnsToContents()
            self.view_int_std_all.setModel(model_all_int)
            self.view_int_std_all.setWindowTitle('All Internal Std. Peaks')
            self.view_int_std_all.resize(800, 600)
            self.view_int_std_all.show()

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No time underscore, or dye does not match dye detected, please try again')
            error_dialog.exec_()

    # Shows all non internal std peaks
    def showAllProductPeaks(self):
        try:
            prod_dye = self.ui.lineEdit_2.text().upper()
            model = pandasModel(self.df_all_peaks.loc[self.df_all_peaks['Dye'] == prod_dye])
            self.view = QTableView()
            self.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view.resizeColumnsToContents()
            self.view.setModel(model)
            self.view.setWindowTitle('All Peaks')
            self.view.resize(800, 600)
            # self.close()
            self.view.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No time underscore, or dye does not match dye detected, please try again')
            error_dialog.exec_()

    # Gets min height thresholds for internal std and product peaks
    def getMinHeight(self):
        try:
            self.min_height = int(self.ui.lineEdit_11.text())
            self.min_height_int_std = int(self.ui.lineEdit_10.text())
            # For use in another class

            self.df_all_filtered_peaks = all_peaks_filtered(self.df_all_peaks,
                                                            self.min_height, self.ui.lineEdit_2.text().upper())  # Creates table with all product peaks above min height
            self.df_global_peaks = all_peaks_filtered_global(self.df_all_peaks,
                                                             self.min_height)  # Creates table with all peaks above min height for use other methods
            self.df_int_std_filter = int_std_filtered(self.df_all_peaks,
                                                      self.min_height_int_std,self.ui.lineEdit.text().upper())  # Creates table with all int std. peaks
            self.df_differences_table = sample_distance(
                self.df_global_peaks, self.ui.lineEdit.text().upper(), self.ui.lineEdit_2.text().upper())  # Creates table with distances column added
            # Create difference list for table
            self.df_diff_ranges = self.df_differences_table['Diff'].tolist()
            self.df_diff_ranges.sort()
            self.df_diff_ranges_tab = pd.DataFrame(self.df_diff_ranges, columns=['Diff'])

            # Ungrey the selections for seeing each table
            self.ui.pushButton_15.setEnabled(True)
            self.ui.pushButton_16.setEnabled(True)
            self.ui.pushButton_19.setEnabled(True)
            self.ui.pushButton_20.setEnabled(True)
            self.ui.pushButton_24.setEnabled(True)


        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table, please check min height or other conditions')
            error_dialog.exec_()

    # shows all filtered peaks after pressing button
    def showAllFilteredPeaks(self):

        try:

            model_all_filtered = pandasModel(self.df_all_filtered_peaks)
            self.view_all_filtered = QTableView()
            self.view_all_filtered.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_all_filtered.resizeColumnsToContents()
            self.view_all_filtered.setModel(model_all_filtered)
            self.view_all_filtered.setWindowTitle('All Filtered Peaks')
            self.view_all_filtered.resize(800, 600)
            # self.close()
            self.view_all_filtered.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table, please check min height or other conditions')
            error_dialog.exec_()

    # Shows table with internal std peaks given min height filter
    def showFilteredStd(self):
        try:
            model_int_std_filter = pandasModel(self.df_int_std_filter)
            self.view_int_std_filter = QTableView()
            self.view_int_std_filter.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_int_std_filter.resizeColumnsToContents()
            self.view_int_std_filter.setModel(model_int_std_filter)
            self.view_int_std_filter.setWindowTitle('Filtered internal std. peaks')
            self.view_int_std_filter.resize(800, 600)
            # self.close()
            self.view_int_std_filter.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table, please check min height or other conditions')
            error_dialog.exec_()

    # Shows peak table with differences column
    def showDifferencesTable(self):
        try:
            # for table
            model = pandasModel(self.df_differences_table)
            self.view_diff = QTableView()
            self.view_diff.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_diff.resizeColumnsToContents()
            self.view_diff.setModel(model)
            self.view_diff.setWindowTitle('Differences Table')
            self.view_diff.resize(800, 600)
            # self.close
            self.view_diff.show()

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table. Please go back and reenter parameters')
            error_dialog.exec_()

    # Shows a column of all difference ranges
    def showDifferences(self):
        # try:
        # For ranges only, Removed repeated lines above
        model2 = pandasModel(self.df_diff_ranges_tab)
        self.view_diff2 = QTableView()
        self.view_diff2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.view_diff2.resizeColumnsToContents()
        self.view_diff2.setModel(model2)
        self.view_diff2.setWindowTitle('Differences')
        self.view_diff2.resize(300, 600)
        # self.close
        self.view_diff2.show()
        # except:
        #     error_dialog = QtWidgets.QErrorMessage()
        #     error_dialog.showMessage('Please press show differences ranges first')
        #     error_dialog.exec_()

    # ----------------------------------------------------------------------------------------------------------------
    # POLYMER BOUNDS STARTS HERE
    # ---------------------------------------------------------------------------------------------------------------

    # Gets the inputed polymer bounds
    def get_polymer_table(self):
        polymer_table = []
        # Need to error check for empty cell value
        for row in range(self.ui.tableWidget.rowCount()):
            if self.ui.tableWidget.item(row, 0) == None:
                break
            else:
                polymer_table.append([])
            for col in range(self.ui.tableWidget.columnCount()):
                polymer_table[row].append(self.ui.tableWidget.item(row, col).text())

        polymer_table = pd.DataFrame(polymer_table)
        polymer_table.columns = ["Polymer", "Low", "High"]  # sets the column names
        polymer_table[["Low", "High"]] = polymer_table[["Low", "High"]].apply(pd.to_numeric)
        self.polymer_table = polymer_table  # Creates instance to be used in other methods
        return self.polymer_table

    # Gets polymer ranges from excel file
    def getPolymersRanges(self):
        try:
            self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Excel file with difference ranges", "",
                                                                     "Excel Files (*.xlsx);;Excel 03 (*.xls)")
            if self.fileName:
                size_list = import_ranges(self.fileName)[0]
                lower_bounds = import_ranges(self.fileName)[1]
                upper_bounds = import_ranges(self.fileName)[2]
                df_table = pd.DataFrame({"Polymer": size_list, "Low": lower_bounds, "High": upper_bounds})
                if self.ui.tableWidget.rowCount() < len(size_list):
                    self.ui.tableWidget.setRowCount(len(size_list))
                dim = df_table.shape  # Gets dimensions of table
                for row in range(dim[0]):
                    for col in range(dim[-1]):
                        self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(df_table.iloc[row, col])))
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot import excel file. Please check input conditions are correct')
            error_dialog.exec_()

    # Adds a row to the input table
    def add_input_row(self):
        num_rows = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(num_rows + 1)

    # Calculates fractional area vs size before concentration fix
    def calcTableandFAVSB(self):
        global pre_fASB_test
        global zip_dict
        try:
            a = self.get_polymer_table()  # Gets data inputted into tableWidget
            polymer_list = a["Polymer"].tolist()
            low_bounds = a["Low"].tolist()
            upper_bounds = a["High"].tolist()
            combine_bounds = list(
                map(list, zip(low_bounds, upper_bounds)))  # Returns: [[low_bound,upper_bound],[low_bound,upper_bound]]
            self.tws = size(self.df_differences_table, polymer_list, combine_bounds)  # Table with size
            dp_col = self.tws['Data Point']
            size_col = self.tws['Size']
            zip_dict = dict(zip(dp_col, size_col))
            # print(zip_dict)
            pre_fASB_test = table(self.tws)
            self.time_list = pre_fASB_test.index.values.tolist()
            pre_fASB_test.insert(0, column='Time', value=self.time_list)
            # self.fASB = table(self.tws)
            self.fASB = pre_fASB_test
            self.ui.pushButton_23.setEnabled(True)
            self.ui.pushButton_25.setEnabled(True)
            self.ui.pushButton_32.setEnabled(True)
            # Enables buttons for scaled graphs
            self.ui.pushButton_68.setEnabled(True)  # 2d plotsscaled
            self.ui.pushButton_66.setEnabled(True)  # 3d plots scaled
            self.ui.pushButton_70.setEnabled(True)  # scaled log(3d)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Polymers or difference ranges entered incorrectly, please try again')
            error_dialog.exec_()

    # Show peaks with updated size button
    def showTableWithSize(self):
        try:
            model_tws = pandasModel(self.tws)
            self.view_tws = QTableView()
            self.view_tws.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_tws.resizeColumnsToContents()
            self.view_tws.setModel(model_tws)
            self.view_tws.setWindowTitle('Table with Polymer Size')
            self.view_tws.resize(1000, 600)
            self.view_tws.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Polymers or difference ranges entered incorrectly, please try again')
            error_dialog.exec_()

    # Show fractional area vs size before concentration fix button
    def showFracAreaSizeBefore(self):
        try:
            model_fASB = pandasModel(self.fASB)
            self.view_fASB = QTableView()
            self.view_fASB.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_fASB.resizeColumnsToContents()
            self.view_fASB.setModel(model_fASB)
            self.view_fASB.setWindowTitle('Frac v. size before conc. fix')
            self.view_fASB.resize(1000, 600)
            self.view_fASB.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Polymers or difference ranges entered incorrectly, please try again')
            error_dialog.exec_()

    # Calculates fractional area vs size after concentration fix
    def calcFracAreaSizeAfter(self):
        try:
            pre_fASB = table(self.tws)
            self.time_list = pre_fASB.index.values.tolist()
            pre_fASB.insert(0, column='Time', value=self.time_list)

            fASB2 = pre_fASB
            conc = self.ui.lineEdit_20.text()
            self.fasA = conc_fix(fASB2, float(conc))
            self.ui.pushButton_36.setEnabled(True)  # Enables the show conc and size v time button
            self.ui.pushButton_37.setEnabled(True)  # Enables the path to save table button
            self.ui.pushButton_41.setEnabled(True)  # Enables the show prelimnary conc and size vs time plot button

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Invalid concentration')
            error_dialog.exec_()

    # Shows fractional area vs size after concentration fix
    def showFracAreaSizeAfter(self):
        try:
            model_fasA = pandasModel(self.fasA)
            self.view_fasA = QTableView()
            self.view_fasA.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.view_fasA.resizeColumnsToContents()
            self.view_fasA.setModel(model_fasA)
            self.view_fasA.setWindowTitle('Frac v. size after conc. fix')
            self.view_fasA.resize(1200, 600)
            self.view_fasA.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table. Please check concentration or other conditions')
            error_dialog.exec_()

    # Saves .txt and excel files to directory
    def saveTableAfterConc(self):
        dirName = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory'))

        if dirName:
            half_table = kintek_export(self.fasA)
            full_table = self.fasA.iloc[:, 1:]
            half_table.to_csv(dirName + '/' + self.ui.lineEdit_21.text() + '.txt', sep='\t')
            full_table.to_csv(dirName + '/' + self.ui.lineEdit_21.text() + '.csv', sep=',')

    # Calculates the deleted polymer
    def calcDeletePolymer(self):
        global table_adel_before_conc_fix
        global flag
        try:

            #     pre_fASB = table(self.tws)
            #     self.time_list = pre_fASB.index.values.tolist()
            dp_col = self.tws['Data Point']
            size_col = self.tws['Size']
            zip_dict = dict(zip(dp_col, size_col))
            # print(zip_dict)
            pre_fASB = table(self.tws)
            self.time_list = pre_fASB.index.values.tolist()
            # pre_fASB.insert(0, column='Time', value=self.time_list)

            fASB2 = pre_fASB

            self.conc = self.ui.lineEdit_20.text()
            pre_fasA = conc_fix(fASB2, int(self.conc))  # After concentration fix

            fASB3 = pre_fasA  # After conc. fix just reinitialized

            fASB3.insert(0, column='Time', value=self.time_list)

            del_polymer = self.ui.lineEdit_22.text()
            del_polymer_list = del_polymer.split(',')
            del_polymer_list.sort(key=natural_keys)
            # print(del_polymer_list)
            # Deleted fractional area v size before conc. fix
            # fASB2.insert(0, column='Time', value=self.time_list)
            fASB2.reset_index(level=0, inplace=True)

            # print(fASB2)
            table_adel_before_conc_fix = deletePolymer(fASB2, del_polymer_list)
            # print(table_adel_before_conc_fix)
            table_adel = deletePolymer(pre_fasA, del_polymer_list)
            conc_inside = self.ui.lineEdit_20.text()
            pre_table_adel2 = conc_fix(table_adel, int(conc_inside))
            self.table_adel2 = pre_table_adel2
            self.ui.pushButton_42.setEnabled(True)  # Enable show preliminary graph after deletion button
            self.ui.pushButton_39.setEnabled(True)  # Enables show table after deletion button
            self.ui.pushButton_40.setEnabled(True)  # Enables path to save after deletion button
            flag = True

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Already deleted polymer or invalid polymer')
            error_dialog.exec_()

    # Saves table after deletion of polymer
    def saveTableAfterDeletion(self):
        dirName2 = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory'))
        if dirName2:
            half_table = kintek_export(self.table_adel2)
            full_table = self.table_adel2.iloc[:, 1:]
            half_table.to_csv(dirName2 + '/' + self.ui.lineEdit_23.text() + '.txt', sep='\t')
            full_table.to_csv(dirName2 + '/' + self.ui.lineEdit_23.text() + '.csv', sep=',')

    # Shows table after deletion of polymer
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
            self.view_adel.resize(1000, 600)
            self.view_adel.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show table. Please check deletion polymers')
            error_dialog.exec_()

    # Shows the prelimnary graph before deletion
    def showPreliminaryGraph(self):
        try:

            half_table = kintek_export(self.fasA.iloc[:, 1:])
            # time_values = half_table.index.tolist()
            # Create data sets with all the fractional areas. Only need to calculate one time for x value
            # for i in range(1,len(half_table)):
            time_values = half_table.index.tolist()
            y_values_list = []
            for i in range(len(half_table.columns)):
                y_values = half_table.iloc[:, i].values.tolist()
                plt.plot(time_values, y_values)
                # y_values_list.append(list(zip(time_values,y_values)))
            plt.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot graph, please calculate the frac area vs. size again')
            error_dialog.exec_()

    # Shows preliminary graph after deleted polymer
    def showPreliminaryDeleteGraph(self):
        try:

            half_table = kintek_export(self.table_adel2.iloc[:, 1:])
            # time_values = half_table.index.tolist()
            # Create data sets with all the fractional areas. Only need to calculate one time for x value
            # for i in range(1,len(half_table)):
            time_values = half_table.index.tolist()
            y_values_list = []
            for i in range(len(half_table.columns)):
                y_values = half_table.iloc[:, i].values.tolist()
                plt.plot(time_values, y_values)
            plt.show()
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot graph, please calculate the frac area vs. size again')
            error_dialog.exec_()

    # ---------------------------------------------------------------------------------------------------------------------
    # BEGINNING OF THIRD TAB
    # ----------------------------------------------------------------------------------------------------------------------

    def getFSAFiles(self):
        try:
            self.dirName = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory',
                                                                          options=QtWidgets.QFileDialog.DontUseNativeDialog))
            if self.dirName:
                self.ui.lineEdit_24.setText(self.dirName)
                # Gets the number of pts (for dimension purposes)
                self.fsaNamesList = getFSANamesListNotNum(self.dirName)
                self.num_pts = len(self.fsaNamesList)
                first_fsa = getFSANames(self.dirName)
                self.ui.lineEdit_25.setText(first_fsa)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Directory cannot detect any .fsa files, please try again')
            error_dialog.exec_()

    def time_underscore_plot(self):
        try:
            self.plot_time_underscore = int(self.ui.lineEdit_32.text())
            self.fsaNamesList_2 = getFSANamesList(self.dirName, self.plot_time_underscore)
            self.ui.label_50.setText(str(len(timePts(self.fsaNamesList_2, self.plot_time_underscore))))
            self.ui.pushButton_56.setEnabled(True)
            self.ui.pushButton_57.setEnabled(True)
            self.ui.pushButton_58.setEnabled(True)

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Time underscore not valid,please try again')
            error_dialog.exec_()

    # Shows the files aligning
    def showFileNames(self):
        try:
            self.fName = displayFileNames(getFSANamesList(self.dirName, self.plot_time_underscore))
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(
                'Cannot show time pts. please check the time underscore or folder with .fsa files.')
            error_dialog.exec_()

    # Shows time points
    def showTimePts(self):
        try:
            self.time_pt = displayTimePts(timePts(self.fsaNamesList, self.plot_time_underscore))
        # Write another method that gets the number of time pts.
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(
                'Cannot show time pts. please check the time underscore or folder with .fsa files.')
            error_dialog.exec_()

    # Shows possible dimensions of 2d plot
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

    # shows alignment of 2d plots
    def showAlignment(self):
        try:
            # Params for graph
            self.min_x = self.ui.lineEdit_41.text()
            self.max_x = self.ui.lineEdit_42.text()
            self.min_y = self.ui.lineEdit_43.text()
            self.max_y = self.ui.lineEdit_44.text()
            self.desired_row = self.ui.lineEdit_35.text()
            self.desired_col = self.ui.lineEdit_36.text()
            dirName = self.dirName
            plot_time_underscore = self.plot_time_underscore
            plot(dirName, plot_time_underscore, int(self.min_x), int(self.max_x), int(self.min_y), int(self.max_y),
                 int(self.desired_row), int(self.desired_col))


        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please check x/y ranges.')
            error_dialog.exec_()

    # Shows 3d graphs
    def show3d(self):
        try:
            # Params for graph
            self.min_x = self.ui.lineEdit_41.text()
            self.max_x = self.ui.lineEdit_42.text()
            self.min_y = self.ui.lineEdit_43.text()
            self.max_y = self.ui.lineEdit_44.text()
            dirName = self.dirName
            plot_time_underscore = self.plot_time_underscore
            plot3d(self.num_pts, self.fsaNamesList, plot_time_underscore, int(self.min_x), int(self.max_x),
                   int(self.min_y),
                   int(self.max_y), dirName)

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please check x/y ranges')
            error_dialog.exec_()

    # Shows log(3d) plots
    def show3dlog(self):
        try:
            self.min_x = self.ui.lineEdit_41.text()
            self.max_x = self.ui.lineEdit_42.text()
            self.min_y = self.ui.lineEdit_43.text()
            self.max_y = self.ui.lineEdit_44.text()
            dirName = self.dirName
            plot_time_underscore = self.plot_time_underscore
            plot3dlog(self.num_pts, self.fsaNamesList, plot_time_underscore, int(self.min_x), int(self.max_x),
                      int(self.min_y),
                      int(self.max_y), dirName)

        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please check x/y ranges')
            error_dialog.exec_()

    # Shows 2d scaled
    def show2dscaled(self):
        # try:
        self.min_x = self.ui.lineEdit_41.text()
        self.max_x = self.ui.lineEdit_42.text()
        self.min_y = self.ui.lineEdit_43.text()
        self.max_y = self.ui.lineEdit_44.text()
        self.desired_row = self.ui.lineEdit_35.text()
        self.desired_col = self.ui.lineEdit_36.text()
        dirName = self.dirName
        plot_time_underscore = self.plot_time_underscore
        try:
            if flag:
                plot2dScaled(dirName, plot_time_underscore, int(self.min_x), int(self.max_x), int(self.min_y)
                             , 1, int(self.desired_row), int(self.desired_col), zip_dict, pre_fASB_test)

        except NameError:
            plot2dScaled(self.dirName, self.plot_time_underscore, int(self.min_x), int(self.max_x), int(self.min_y)
                         , 1, int(self.desired_row), int(self.desired_col), zip_dict, pre_fASB_test)
        #
        # except:
        #     error_dialog = QtWidgets.QErrorMessage()
        #     error_dialog.showMessage('Cannot show alignment, please perform frac area v size first.')
        #     error_dialog.exec_()

    # Shows 3d scaled plots
    def show3dscaled(self):
        try:
            self.min_x = self.ui.lineEdit_41.text()
            self.max_x = self.ui.lineEdit_42.text()
            self.min_y = self.ui.lineEdit_43.text()
            self.max_y = self.ui.lineEdit_44.text()
            dirName = self.dirName
            plot_time_underscore = self.plot_time_underscore
            try:
                if flag:
                    plot3dScaled(self.num_pts, self.fsaNamesList, plot_time_underscore, int(self.min_x),
                                 int(self.max_x), int(self.min_y),
                                 1, dirName, zip_dict, pre_fASB_test)

            except NameError:
                plot3dScaled(self.num_pts, self.fsaNamesList, self.plot_time_underscore, int(self.min_x),
                             int(self.max_x),
                             int(self.min_y),
                             1, self.dirName, zip_dict, pre_fASB_test)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, if you want scaled 3d plot, then you have to go back'
                                     'and perform fractional area vs size')
            error_dialog.exec_()

    # Show log(3d) scaled
    def show3dlogscaled(self):
        try:
            self.min_x = self.ui.lineEdit_41.text()
            self.max_x = self.ui.lineEdit_42.text()
            self.min_y = self.ui.lineEdit_43.text()
            self.max_y = self.ui.lineEdit_44.text()
            dirName = self.dirName
            plot_time_underscore = self.plot_time_underscore
            try:
                if flag:
                    plot3dlogscaled(self.num_pts, self.fsaNamesList, plot_time_underscore, int(self.min_x),
                                    int(self.max_x),
                                    int(self.min_y),
                                    1, dirName, zip_dict, pre_fASB_test)

            except NameError:
                plot3dlogscaled(self.num_pts, self.fsaNamesList, self.plot_time_underscore, int(self.min_x),
                                int(self.max_x),
                                int(self.min_y),
                                1, self.dirName, zip_dict, pre_fASB_test)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Cannot show alignment, please perform frac area v size first.')
            error_dialog.exec_()


if __name__ == '__main__':
    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())

# NEED TO FIX SHOW TABLE DIFFERENCES FIRST. This prevents ranges list from showing w/o seeing full table first