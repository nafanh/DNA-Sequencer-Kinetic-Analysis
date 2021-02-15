import pandas as pd
import numpy as np
import re
import pprint
import matplotlib.pyplot as plt
import math
import os
from Bio import SeqIO
from collections import defaultdict
from Bio import SeqIO
from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pprint
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
from openpyxl import Workbook
from openpyxl import load_workbook
import pandas as pd
import numpy as np


def kintek_export(df):
    col_length = df.shape[1]
    midpt = int((col_length) / 2) + 1
    df1 = df.iloc[:, midpt:]
    # p = Path('Exported Data')
    # p.mkdir(exist_ok=True)

    return df1


filepath = "C:\\Users\\nhuan_000\PycharmProjects\dna seq\pthio\\burst_ranges.xlsx"


def import_ranges(filepath):
    # filepath = "C:\\Users\\nhuan_000\PycharmProjects\dna seq\pthio\\burst_ranges.xlsx"

    wb = load_workbook(filepath)
    ws = wb.active

    size = ws["A"]
    lower = ws["B"]
    upper = ws["C"]
    lower_bounds = []
    upper_bounds = []

    for i in range(1, len(lower)):
        lower_bounds.append(lower[i].value)

    for i in range(1, len(upper)):
        upper_bounds.append(upper[i].value)

    # print(lower_bounds)
    # print(upper_bounds)
    new_list = []
    # for i in range(len(lower_bounds)):
    #     name = '[' + str(lower_bounds[i]) + ':' + str(upper_bounds[i]) + ']'
    #     new_list.append(name)

    pre_list = list(map(list, zip(lower_bounds, upper_bounds)))
    pre_list = str(pre_list)
    new_list = pre_list.replace('],', ']:')
    new_list2 = new_list[1:-1]
    new_list3 = new_list2.replace(' ', '')
    return str(new_list3)


# print(import_ranges(filepath))
# print(type(import_ranges(filepath)))

def import_sizes(filePath):
    wb = load_workbook(filePath)
    ws = wb.active
    size = ws['A']
    polymer_list = ''
    for i in range(1, len(size)):
        if i == 1:
            polymer_list += str(size[i].value)
        else:
            polymer_list += ',' + str(size[i].value)
    return polymer_list


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


# if remove_datapt == None:
#     break
# while remove_datapt not in n.columns:
#     remove_datapt = sg.PopupGetText('Polymer not in table, please try again', title='Error')
#     if remove_datapt == None:
#         break
# del n[remove_datapt]
# del n[remove_datapt + '/Total']
# headers_list.remove(remove_datapt)
# # headers_list.remove(remove_datapt + '/Total')
# n['Total'] = 0
# n['Total'] = n.iloc[:, :int(len(n.columns) / 2)].sum(axis=1)
# # remove_datapt_quest= input('Any more polymers you want to delete? Please enter y for yes and n for no: ')
# remove_datapt_quest = sg.PopupGetText(
#     'Any more polymers you want to delete? Please enter y for yes and n for no: ', title='Additional Polymers')


# for i in range(len(headers_list) - 1):
#     divide_name = headers_list[i] + '/' + headers_list[-1]
#     n[divide_name] = n.iloc[:, i] / n.iloc[:, len(headers_list) - 1]
# # Sorts table by time and fill 'NaN' values with '0'
# n = n.fillna(0)
# n.sort_index(inplace=True)
#         n = n.fillna(0)
#         n['Total'] = n.sum(axis=1)
#         headers_list = n.columns.values.tolist()
#         #print(headers_list)
#         for i in range(len(headers_list)-1):
#             divide_name = headers_list[i] + '/' + headers_list[-1]
#             n[divide_name] = n.iloc[:,i] / n.iloc[:,len(headers_list)-1]
#         #n = n.fillna(0)
#         print('This is the table for fractional area vs. size. Please analyze to see if you want to delete outliers.')
#         print('-----------------------------------------------------------------------------')
#         print(n)
#
#         print(headers_list)
#         remove_datapt_quest = input('Do you want to delete a polymer? If so, please enter ''y'', else enter anything else: ')
#         while remove_datapt_quest == 'y' or remove_datapt_quest == 'Y':
#             remove_datapt = input('Please enter the polymer name you want to delete (ex: 24mer): ')
#             while 'mer' not in remove_datapt:
#                 remove_datapt = input('Not valid polymer name, please try again: ')
#             del n[remove_datapt]
#             del n[remove_datapt + '/Total']
#             headers_list.remove(remove_datapt)
#             print(headers_list)
#             print(n)
#             #headers_list.remove(remove_datapt + '/Total')
#             n['Total'] = 0
#             n['Total'] = n.iloc[:,:int(len(n.columns)/2)].sum(axis=1)
#             remove_datapt_quest= input('Any more polymers you want to delete? Please enter y for yes and n for no: ')
#         for i in range(len(headers_list)-1):
#             divide_name = headers_list[i] + '/' + headers_list[-1]
#             n[divide_name] = n.iloc[:,i] / n.iloc[:,len(headers_list)-1]
#         #Sorts table by time and fill 'NaN' values with '0'
#         n = n.fillna(0)
#
#         #Exports non-concentration fixed data. Gives the fractional area for
#         #Each polymer and the time points
#         #export_before_conc = n.to_csv('Export_data_Before_concfix.csv',sep=',')
#         return n
#


def deletePolymer(n, polymers):
    # Test set ['Time','27mer','28mer','Total','27mer/Total','28mer/Total']
    headers_list = n.columns.values.tolist()
    # print(headers_list)
    # print(headers_list) #['Time', '27mer', '28mer', 'Total', '27mer/Total', '28mer/Total']
    headers_list = headers_list[1:(len(headers_list) // 2) + 1]
    # print(headers_list) #['27mer', '28mer', 'Total']
    # print(headers_list) #Output: ['27mer','28mer','Total']
    for remove_datapt in polymers:
        del n[remove_datapt]
        del n[remove_datapt + '/Total']
        headers_list.remove(remove_datapt)
        # print(headers_list) #['28mer', 'Total']
        # Output: ['28mer','Total']
        # headers_list.remove(remove_datapt + '/Total')
        n['Total'] = 0
        n['Total'] = n.iloc[:, 1:int(len(n.columns) / 2) + 1].sum(axis=1)
        # print(n)

    # print(headers_list)
    # print(n)
    for i in range(len(headers_list) - 1):
        divide_name = headers_list[i] + '/' + headers_list[-1]  # last is always total ok
        n[divide_name] = n.loc[:, headers_list[i]] / n.loc[:, 'Total']
    # Sorts table by time and fill 'NaN' values with '0'
    # print(n)
    n = n.fillna(0)
    return n


# n = pd.DataFrame([[0,5,1,2,3,float(5/10),float(1/3),float(2/3)],[0.5,5,6,7,13,float(5/10),float(6/13),float(7/13)]],columns = ['Time','26mer','27mer','28mer','Total','26mer/Total','27mer/Total','28mer/Total'])
# #print(n)
# o = pd.DataFrame([[0,1,2,3,float(1/3),float(2/3)],[0.5,6,7,13,float(6/13),float(7/13)]],columns = ['Time','27mer','28mer','Total','27mer/Total','28mer/Total'])
# p = pd.DataFrame([[0,5,5,1,2,3,float(5/10),float(5/10),float(1/3),float(2/3)],[0.5,5,5,6,7,13,float(5/10),float(5/10),float(6/13),float(7/13)]],columns = ['Time','25mer','26mer','27mer','28mer','Total','25mer/Total','26mer/Total','27mer/Total','28mer/Total'])
#
#
# print(deletePolymer(n,['27mer']))
# print(deletePolymer(o,['27mer']))
# print(deletePolymer(p,['27mer']))

def plot3d(length_dir, fsa_names_sorted, time_underscore, x_min, x_max, y_min, y_max, folder_fsa):
    global x_std_max
    fig2 = plt.figure()
    ax2 = plt.axes(projection='3d')
    # Counter for subplot number
    subplot_num = 1
    # Creates a list for all the differences. Will take the largest difference to set the axes x min and x max (y min and y max for 3d scatter)
    diff_list = []
    # parses the directory for .fsa files
    for k in range(length_dir):
        if k == 0: # This gets the standard reference peak, just the first .fsa file in the directory
            # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
            first_dp_split = fsa_names_sorted[k].split('_')
            time = first_dp_split[time_underscore]
            standard = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
            s_abif_key = standard.annotations['abif_raw'].keys()
            s_trace = defaultdict(list)
            s_channels = ['DATA1', 'DATA3']
            for sc in s_channels:
                # s_trace['DATA1'] = y values
                s_trace[sc] = standard.annotations['abif_raw'][sc]
            x_values = np.asarray(s_trace['DATA1'])
            y_std_max = max(s_trace['DATA3'])  # Max y-value for the first graph (used as standard)
            x_std_max = s_trace['DATA3'].index(y_std_max)  # The x-value for the max y-value
            # print(x_values[x_min:x_max+1])

            z_values = x_values[x_min:x_max + 1]  # Makes 3D plot z-values the x-values of 2D plot
            x_values_time = [float(time)] * len(z_values)  # np array with as many time values as there are data points
            y_values = np.arange(x_min, x_max + 1)  # Y-values of 3d plot same as 2d plot
            ##    print(len(x_values))
            ##    print(len(y_values))
            ##    print(len(z_values))
            # x_values = np.arange(1,len(y_values)+1)
            ##
            ##
            sc_std = ax2.plot(x_values_time, y_values, z_values, alpha=0.7)
            continue

        subplot_num += 1
        name_split = fsa_names_sorted[k].split('_')
        time_peak = name_split[time_underscore]
        # opens up the FSA file
        record = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
        # Record returns a bunch of dictionaries. Use this line to get the dictionary
        # keys of abif_raw only
        abif_key = record.annotations['abif_raw'].keys()
        # Creates an empty list as the value in the dict
        trace = defaultdict(list)
        # DATA1 is where all the peak value is held, so only grab this dictionary key
        channels = ['DATA1', 'DATA3']
        # Parses the channels list and returns the values for each key in dictionary
        for c in channels:
            trace[c] = record.annotations['abif_raw'][c]
        # Xvalues for time pts
        x_values_non_std = np.asarray(trace['DATA1']) # The actual y-values from 2d plot
        # Numpy for y values (xvalues_non_std)

        # Get the max value data
        y_peak = max(trace['DATA3'])
        # Gets the x value of the max value
        x_peak = trace['DATA3'].index(y_peak)
        # Takes difference of reference x value and time point x value
        diff = x_peak - x_std_max
        diff_list.append(diff)
        # y_values_append_values = np.arange(x_max - diff, x_max)
        #print(diff)

        # X_values_non_std are really the y values on a 2d graph
        y_values_non_std = np.arange(x_min, x_max + 1) - diff # Diff removes the amount of data points +/- from the graph
        # print(y_values_non_std)
        # x_min_diff_first_x = np.where(y_values_non_std == x_min)
        # print(x_min_diff_first_x)
        # if x_min_diff_first_x[0].size != 0:
        #     x_min_diff_first_x_range = np.arange(x_min_diff_first_x[0])
        #     #print(x_min_diff_first_x_range)
        #     y_values_non_std = np.delete(y_values_non_std,x_min_diff_first_x_range)
        # print(y_values_non_std)
        # print(x_min_diff_first_x)
        # print(y_values_non_std)
        # x_min_diff_first_x_np = np.arange(x_min_diff_first_x)
        # np.delete(y_values_non_std,x_min_diff_first_x_np)
        z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)] # Data points corrected for shift.
        # Adds zero values
        x_values_time_non_std = [float(time_peak)] * len(y_values_non_std) # Makes list of time points with len =
        # data point length

        diff_range_list = np.arange(diff) # makes np array with length of difference, if negative then empty array

        # Removes the values less than x_min for positive differences
        y_values_non_std = np.delete(y_values_non_std, diff_range_list)
        #print(y_values_non_std)
        z_values_non_std = np.delete(z_values_non_std, diff_range_list)
        x_values_time_non_std = np.delete(x_values_time_non_std, diff_range_list)

        # print(diff)

        zero_list = [0] * diff
        # if diff > 0:

        # Positive differences, we will
        if diff > 0:
            y_values_append_values = np.arange(x_max - diff, x_max)
            # z_values_append_values = np.array(zero_list)
            z_values_append_values = np.array(x_values_non_std[x_max:x_max+diff]) # Appends RFU values greater than
            # x_max after shifting
            x_values_time_append_values = np.array([float(time_peak)] * diff)

            y_values_non_std = np.append(y_values_non_std, y_values_append_values)
            z_values_non_std = np.append(z_values_non_std, z_values_append_values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)
            # print(len(y_values_non_std))

        else:
            y_values_append_values = np.arange(x_min, x_min - diff + 1) # Subtracting by a negative number is addition
            x_range = x_max - x_min
            y_values_delete_values_end = [x for x in range(x_range + 1, x_range - diff + 2)] # from [end: end+diff]
            # print(y_values_delete_values_end)
            # appended to y_values
            y_values_delete_values_begin = [x for x in range(0, abs(diff) + 1)]
            # y_values_delete_values = np.arange(x_max,x_max - diff)
            z_values_append_values = np.array(zero_list) # Zero values for appending to beginning of z-values (RFU)
            x_values_time_append_values = np.array([float(time_peak)] * diff) # Time values to append)
            # print(x_values_time_append_values)

            y_values_non_std = np.insert(y_values_non_std, 0, y_values_append_values) # insert data point values at
            # beginning of numpy array
            y_values_non_std = np.delete(y_values_non_std, y_values_delete_values_end)
            z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)]
            x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)


            # print(b)
            # print(len(y_values_non_std))
            z_values_non_std = np.append(z_values_non_std, z_values_append_values) # Add zero values to beginning (
            # negative data point values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)
            # x_values_time_non_std = math.log(x_values_time_non_std)*100

        # x_values_time_non_std = np.log(x_values_time_non_std)
        # print(x_values_time_non_std)
        # else:
        #   y_values_append_values = np.arange(x_max + diff, x_max)

        # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
        # np.append(y_values_non_std,zero_list)

        # print(y_values_non_std)

        sc_non_std = ax2.plot(x_values_time_non_std, y_values_non_std, z_values_non_std, alpha=0.7)
    ax2.set_ylim(x_min, x_max)
    ax2.set_zlim(y_min, y_max)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Data Point')
    ax2.set_zlabel('RFU')
    # make the panes transparent
    # ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.set_facecolor('grey')
    # make the grid lines transparent
    # ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    # #Gets x values for vectorization purposes
    # array = np.arange(1,len(trace['DATA1'])+1)
    # #Subtracts difference from array (vectorization)
    # array -= diff

    plt.show()
    #plt.close()


def divisors(n):  # Gives output of a list of lists [[1,4],[2,2]]
    factors = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            factors.append([i, int(n / i)])

    rev_factors = []
    for i in range(len(factors)):
        rev_factors.append([factors[i][1], factors[i][0]])
    for x in rev_factors:
        if x not in factors: factors.append(x)
    dim_table = pd.DataFrame(factors, columns=['Num of Rows', 'Num of Cols'])
    dim_table.index.name = 'Possibility #'
    dim_table.index += 1
    return dim_table


def getFSANames(dir_name):
    fsa_names = [x for x in os.listdir(dir_name) if x.endswith('.fsa')]
    ex_name = fsa_names[0]
    return ex_name


def getFSANamesListNotNum(dir_name):
    fsa_names = [x for x in os.listdir(dir_name) if x.endswith('.fsa')]
    return fsa_names


def getFSANamesList(dir_name, time_underscore):
    fsa_names = [x for x in os.listdir(dir_name) if x.endswith('.fsa')]
    time_list = []
    # Adjusts to make the zero time point the first .fsa file in the directory
    for i in range(len(fsa_names)):
        name_list = fsa_names[i].split('_')
        time_value = name_list[time_underscore]
        if '.' not in time_value:
            time_list.append(int(time_value))
            continue
        time_list.append(float(time_value))
    # Sorts time_list
    time_list.sort()
    fsa_names_sorted = []

    for time in time_list:
        for ext_name in fsa_names:
            ext_name_split = ext_name.split('_')
            if ext_name_split[time_underscore] == str(time):
                fsa_names_sorted.append(ext_name)
            continue
    # print(fsa_names_sorted)
    return fsa_names_sorted


def timePts(fsa_names, time_underscore):
    time_list = []
    for i in range(len(fsa_names)):
        name_list = fsa_names[i].split('_')
        time_value = name_list[time_underscore]
        if '.' not in time_value:
            time_list.append(int(time_value))
            continue
        time_list.append(float(time_value))
    # Sorts time_list
    time_list.sort()

    return time_list


# Plots 2d alignment
def plot(dir_name, time_underscore, x_min, x_max, y_min, y_max, rows, cols):
    os.chdir(dir_name)
    fsa_names = [x for x in os.listdir(dir_name) if x.endswith('.fsa')]
    length_dir = len(fsa_names)
    time_underscore = int(time_underscore)
    time_list = []
    # Adjusts to make the zero time point the first .fsa file in the directory
    for i in range(len(fsa_names)):
        name_list = fsa_names[i].split('_')
        time_value = name_list[time_underscore]
        if '.' not in time_value:
            time_list.append(int(time_value))
            continue
        time_list.append(float(time_value))
    # Sorts time_list
    time_list.sort()

    fsa_names_sorted = []

    for time in time_list:
        for ext_name in fsa_names:
            ext_name_split = ext_name.split('_')
            if ext_name_split[time_underscore] == str(time):
                fsa_names_sorted.append(ext_name)
            continue

    # Creates figure, axis objects for subplot
    fig, ax = plt.subplots(rows, cols, sharex='all', sharey='all')
    axes_list = [item for sublist in ax for item in sublist]

    # Initialize variables for row and column
    i = 0
    j = 1
    count_1x = 0
    # Parses through each fsa file in the directory
    for k in range(length_dir):
        # n = str(os.getcwd()) + '/' + fsa_dir + '/' + length_dir_name[k]
        # Takes first time point as the standard reference peak
        if k == 0:
            first_dp_split = fsa_names_sorted[k].split('_')
            time = first_dp_split[time_underscore]
            standard = SeqIO.read(fsa_names_sorted[k], 'abi')
            s_abif_key = standard.annotations['abif_raw'].keys()
            s_trace = defaultdict(list)
            s_channels = ['DATA1', 'DATA3']
            for sc in s_channels:
                s_trace[sc] = standard.annotations['abif_raw'][sc]

            # y_val_data = np.asarray(s_trace['DATA3'])
            # print(len(y_val_data))
            y_std_max = max(s_trace['DATA3'])
            x_std_max = s_trace['DATA3'].index(y_std_max)
            # Outputs the graph for the standard peaks
            if rows == 1 or cols == 1:
                ax[count_1x].plot(s_trace['DATA1'], color='black')
                ax[count_1x].set_title('Time: ' + time, loc='right', fontsize=8)
                ax[count_1x].set_xlim(x_min, x_max)
                ax[count_1x].set_ylim(y_min, y_max)
                count_1x += 1

            else:
                ax[0, 0].plot(s_trace['DATA1'], color='black')
                ax[0, 0].set_title('Time: ' + time, loc='right', fontsize=8)
                ax[0, 0].set_xlim(x_min, x_max)
                ax[0, 0].set_ylim(y_min, y_max)
            continue

        # Resets the row once gets to end of row limit
        if j == cols:
            i += 1
            j = 0
        # Gets the time for peaks
        name_split = fsa_names_sorted[k].split('_')
        time_peak = name_split[time_underscore]

        # opens up the FSA file
        record = SeqIO.read(fsa_names_sorted[k], 'abi')
        # Record returns a bunch of dictionaries. Use this line to get the dictionary
        # keys of abif_raw only
        abif_key = record.annotations['abif_raw'].keys()
        # Creates an empty list as the value in the dict
        trace = defaultdict(list)
        # DATA1 is where all the peak value is held, so only grab this dictionary key
        channels = ['DATA1', 'DATA3']
        # Parses the channels list and returns the values for each key in dictionary
        for c in channels:
            trace[c] = record.annotations['abif_raw'][c]

        # Get the max value data
        y_peak = max(trace['DATA3'])
        # Gets the x value of the max value
        x_peak = trace['DATA3'].index(y_peak)
        # Takes difference of reference x value and time point x value
        diff = x_peak - x_std_max
        # print(diff)
        # Gets x values for vectorization purposes
        array = np.arange(1, len(trace['DATA1']) + 1)
        # Subtracts difference from array (vectorization)
        # if diff > 0:
        array -= diff
        # else:
        #     array += diff

        # print(trace['DATA1'])
        # np.append(array,zero_list)
        # Plots the chromatogram data
        ##    for i in range(2):
        ##        for j in range(4):
        ##            if i == 0 and j == 0:
        ##                continue
        if rows == 1:
            ax[count_1x].plot(array, trace['DATA1'], color='black')
            ax[count_1x].set_title('Time: ' + time_peak, loc='right', fontsize=8)
            ax[count_1x].set_xlim(x_min, x_max)
            ax[count_1x].set_ylim(y_min, y_max)
            count_1x += 1
        elif cols == 1:
            ax[count_1x].plot(array, trace['DATA1'], color='black')
            ax[count_1x].set_title('Time: ' + time_peak, loc='right', fontsize=8)
            ax[count_1x].set_xlim(x_min, x_max)
            ax[count_1x].set_ylim(y_min, y_max)
            count_1x += 1
        # Displays the peaks
        else:
            ax[i, j].plot(array, trace['DATA1'], color='black')
            ax[i, j].set_title('Time: ' + time_peak, loc='right', fontsize=8)
            ax[i, j].set_xlim(x_min, x_max)
            ax[i, j].set_ylim(y_min, y_max)
            j += 1
        # Increments column for subplot

    subplot_diff = (rows * cols) - length_dir
    if subplot_diff > 0:
        for i in range(length_dir, (rows * cols)):
            axes_list[i].remove()

    #    plt.plot(array,trace['DATA1'],color='black')
    # plt.xlim(2000,3000)
    #    plt.ylim(0,5000)
    fig.suptitle('Chromatogram Peaks')
    fig.text(0.04, 0.5, 'RFU', va='center', rotation='vertical')

    plt.show()
    #plt.close()


def plot2dScaled(dir_name, time_underscore, x_min, x_max, y_min, y_max, rows, cols, zip_dict, pre_fASB_test):
    os.chdir(dir_name)
    fsa_names = [x for x in os.listdir(dir_name) if x.endswith('.fsa')]
    length_dir = len(fsa_names)
    time_underscore = int(time_underscore)
    time_list = []
    # Adjusts to make the zero time point the first .fsa file in the directory
    for i in range(len(fsa_names)):
        name_list = fsa_names[i].split('_')
        time_value = name_list[time_underscore]
        if '.' not in time_value:
            time_list.append(int(time_value))
            continue
        time_list.append(float(time_value))
    # Sorts time_list
    time_list.sort()

    fsa_names_sorted = []

    for time in time_list:
        for ext_name in fsa_names:
            ext_name_split = ext_name.split('_')
            if ext_name_split[time_underscore] == str(time):
                fsa_names_sorted.append(ext_name)
            continue

    # Creates figure, axis objects for subplot
    fig, ax = plt.subplots(rows, cols, sharex='all', sharey='all')
    axes_list = [item for sublist in ax for item in sublist]

    # Initialize variables for row and column
    i = 0
    j = 1
    count_1x = 0
    # Parses through each fsa file in the directory
    for k in range(length_dir):
        # n = str(os.getcwd()) + '/' + fsa_dir + '/' + length_dir_name[k]
        # Takes first time point as the standard reference peak
        if k == 0:
            first_dp_split = fsa_names_sorted[k].split('_')
            time = first_dp_split[time_underscore]
            standard = SeqIO.read(fsa_names_sorted[k], 'abi')
            s_abif_key = standard.annotations['abif_raw'].keys()
            s_trace = defaultdict(list)
            s_channels = ['DATA1', 'DATA3']
            for sc in s_channels:
                s_trace[sc] = standard.annotations['abif_raw'][sc]

            # y_val_data = np.asarray(s_trace['DATA3'])
            # print(len(y_val_data))
            y_std_max = max(s_trace['DATA3'])
            x_std_max = s_trace['DATA3'].index(y_std_max)
            # Outputs the graph for the standard peaks
            y_std_maxdata1 = max(s_trace['DATA1'])
            x_std_maxdata1 = s_trace['DATA1'].index(y_std_maxdata1)
            size_with_xmax = zip_dict[str(x_std_maxdata1)]  # Gets the size of the xmax value
            size_with_xmax_total = size_with_xmax + '/' + 'Total'
            frac_row = pre_fASB_test.iloc[k, :]
            frac = frac_row.loc[size_with_xmax_total]
            # print(size_with_xmax_total)
            # print(frac)
            # print(y_std_maxdata1)
            factor1 = frac / y_std_maxdata1
            # print(factor1)
            # print(type(s_trace['DATA1']))
            if rows == 1 or cols == 1:
                ax[count_1x].plot(np.array(s_trace['DATA1']) * factor1, color='black')
                ax[count_1x].set_title('Time: ' + time, loc='right', fontsize=8)
                ax[count_1x].set_xlim(x_min, x_max)
                ax[count_1x].set_ylim(y_min, y_max)
                count_1x += 1
            else:
                ax[0, 0].plot(np.array(s_trace['DATA1']) * factor1, color='black')
                ax[0, 0].set_title('Time: ' + time, loc='right', fontsize=8)
                ax[0, 0].set_xlim(x_min, x_max)
                ax[0, 0].set_ylim(y_min, y_max)
            continue

        # Resets the row once gets to end of row limit
        if j == cols:
            i += 1
            j = 0
        # Gets the time for peaks
        name_split = fsa_names_sorted[k].split('_')
        time_peak = name_split[time_underscore]

        # opens up the FSA file
        record = SeqIO.read(fsa_names_sorted[k], 'abi')
        # Record returns a bunch of dictionaries. Use this line to get the dictionary
        # keys of abif_raw only
        abif_key = record.annotations['abif_raw'].keys()
        # Creates an empty list as the value in the dict
        trace = defaultdict(list)
        # DATA1 is where all the peak value is held, so only grab this dictionary key
        channels = ['DATA1', 'DATA3']
        # Parses the channels list and returns the values for each key in dictionary
        for c in channels:
            trace[c] = record.annotations['abif_raw'][c]

        # Get the max value data
        y_peak = max(trace['DATA3'])
        # Gets the x value of the max value
        x_peak = trace['DATA3'].index(y_peak)
        y_peak_data1 = max(trace['DATA1'])  # fractional area/max intenisty
        x_peak_data1 = trace['DATA1'].index(y_peak_data1)

        size_with_xmax_2 = zip_dict[str(x_peak_data1)]  # Gets the size of the xmax value
        size_with_xmax_total_2 = size_with_xmax_2 + '/' + 'Total'
        frac_row_2 = pre_fASB_test.iloc[k, :]
        frac2 = frac_row_2.loc[size_with_xmax_total_2]
        # print(frac2)
        factor2 = frac2 / y_peak_data1
        # print(size_with_xmax_total_2)
        # print(y_peak_data1)
        # print(factor2)
        # Takes difference of reference x value and time point x value
        diff = x_peak - x_std_max
        # print(diff)
        # Gets x values for vectorization purposes
        array = np.arange(1, len(trace['DATA1']) + 1)
        # Subtracts difference from array (vectorization)
        # if diff > 0:
        array -= diff
        # else:
        #     array += diff

        # print(trace['DATA1'])
        # np.append(array,zero_list)
        # Plots the chromatogram data
        ##    for i in range(2):
        ##        for j in range(4):
        ##            if i == 0 and j == 0:
        ##                continue
        if rows == 1:
            ax[count_1x].plot(array, np.array(trace['DATA1']) * factor2, color='black')
            ax[count_1x].set_title('Time: ' + time_peak, loc='right', fontsize=8)
            ax[count_1x].set_xlim(x_min, x_max)
            ax[count_1x].set_ylim(y_min, y_max)
            count_1x += 1
        elif cols == 1:
            ax[count_1x].plot(array, np.array(trace['DATA1']) * factor2, color='black')
            ax[count_1x].set_title('Time: ' + time_peak, loc='right', fontsize=8)
            ax[count_1x].set_xlim(x_min, x_max)
            ax[count_1x].set_ylim(y_min, y_max)
            count_1x += 1
        # Displays the peaks
        else:
            ax[i, j].plot(array, np.array(trace['DATA1']) * factor2, color='black')
            ax[i, j].set_title('Time: ' + time_peak, loc='right', fontsize=8)
            ax[i, j].set_xlim(x_min, x_max)
            ax[i, j].set_ylim(y_min, y_max)
            j += 1
        # Increments column for subplot

    #    plt.plot(array,trace['DATA1'],color='black')
    # plt.xlim(2000,3000)
    #    plt.ylim(0,5000)

    subplot_diff = (rows * cols) - length_dir
    if subplot_diff > 0:
        for i in range(length_dir, (rows * cols)):
            axes_list[i].remove()
    fig.suptitle('Chromatogram Peaks')
    fig.text(0.04, 0.5, 'Frac. Area', va='center', rotation='vertical')

    plt.show()
    #plt.close()


def plot3dScaled(length_dir, fsa_names_sorted, time_underscore, x_min, x_max, y_min, y_max, folder_fsa, zip_dict,
                 pre_fASB_test):  # fvs is a dataframe with the fractional area v size
    fig3 = plt.figure()
    ax3 = plt.axes(projection='3d')
    # Counter for subplot number
    subplot_num = 1
    # Creates a list for all the differences. Will take the largest difference to set the axes x min and x max (y min and y max for 3d scatter)
    diff_list = []
    # parses the directory for .fsa files
    for k in range(length_dir):
        if k == 0:
            # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
            first_dp_split = fsa_names_sorted[k].split('_')
            time = first_dp_split[time_underscore]
            standard = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
            s_abif_key = standard.annotations['abif_raw'].keys()
            s_trace = defaultdict(list)
            s_channels = ['DATA1', 'DATA3']
            for sc in s_channels:
                # s_trace['DATA1'] = y values
                s_trace[sc] = standard.annotations['abif_raw'][sc]
            x_values = np.asarray(s_trace['DATA1'])
            y_std_max = max(s_trace['DATA3'])
            x_std_max = s_trace['DATA3'].index(y_std_max)
            # print(x_values[x_min:x_max+1])

            y_std_maxdata1 = max(s_trace['DATA1'])
            x_std_maxdata1 = s_trace['DATA1'].index(y_std_maxdata1)
            size_with_xmax = zip_dict[str(x_std_maxdata1)]  # Gets the size of the xmax value
            size_with_xmax_total = size_with_xmax + '/' + 'Total'
            frac_row = pre_fASB_test.iloc[k, :]
            frac = frac_row.loc[size_with_xmax_total]
            # print(size_with_xmax_total)
            # print(frac)
            # print(y_std_maxdata1)
            factor1 = frac / y_std_maxdata1
            # print(factor1)

            # Gets a range for the max peak

            # Gets max y value for data1:
            y_std_peakdata1 = max(s_trace['DATA1']) / sum(s_trace['DATA1'])
            z_values = x_values[x_min:x_max + 1]
            x_values_time = [float(time)] * len(z_values)
            y_values = np.arange(x_min, x_max + 1)
            ##    print(len(x_values))
            ##    print(len(y_values))
            ##    print(len(z_values))
            # x_values = np.arange(1,len(y_values)+1)
            ##
            ##
            # print(type(z_values))
            scaled_z_values = z_values * (frac / y_std_maxdata1)
            # print(max(z_values))
            # print(max(scaled_z_values))
            # print(scaled_z_values)
            ax3.plot(x_values_time, y_values, scaled_z_values, alpha=0.7)
            continue

        subplot_num += 1
        name_split = fsa_names_sorted[k].split('_')
        time_peak = name_split[time_underscore]
        # opens up the FSA file
        record = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
        # Record returns a bunch of dictionaries. Use this line to get the dictionary
        # keys of abif_raw only
        abif_key = record.annotations['abif_raw'].keys()
        # Creates an empty list as the value in the dict
        trace = defaultdict(list)
        # DATA1 is where all the peak value is held, so only grab this dictionary key
        channels = ['DATA1', 'DATA3']
        # Parses the channels list and returns the values for each key in dictionary
        for c in channels:
            trace[c] = record.annotations['abif_raw'][c]
        # Xvalues for time pts
        x_values_non_std = np.asarray(trace['DATA1'])
        # Numpy for y values (xvalues_non_std)

        # Get the max value data
        y_peak = max(trace['DATA3'])
        # Gets the x value of the max value
        x_peak = trace['DATA3'].index(y_peak)

        # Gets the y-peak for Data1
        y_peak_data1 = max(trace['DATA1'])  # fractional area/max intenisty
        x_peak_data1 = trace['DATA1'].index(y_peak_data1)

        size_with_xmax_2 = zip_dict[str(x_peak_data1)]  # Gets the size of the xmax value
        size_with_xmax_total_2 = size_with_xmax_2 + '/' + 'Total'
        frac_row_2 = pre_fASB_test.iloc[k, :]
        frac2 = frac_row_2.loc[size_with_xmax_total_2]
        # print(frac2)
        factor2 = frac2 / y_peak_data1
        # print(size_with_xmax_total_2)
        # print(y_peak_data1)
        # print(factor2)

        # Takes difference of reference x value and time point x value
        diff = x_peak - x_std_max
        diff_list.append(diff)
        # y_values_append_values = np.arange(x_max - diff, x_max)
        # print(diff)

        # X_values_non_std are really the y values on a 2d graph
        y_values_non_std = np.arange(x_min, x_max + 1) - diff

        x_min_diff_first_x = np.where(y_values_non_std == x_min)
        # print(x_min_diff_first_x)
        # if x_min_diff_first_x[0].size != 0:
        #     x_min_diff_first_x_range = np.arange(x_min_diff_first_x[0])
        #     #print(x_min_diff_first_x_range)
        #     y_values_non_std = np.delete(y_values_non_std,x_min_diff_first_x_range)
        # print(y_values_non_std)
        # print(x_min_diff_first_x)
        # print(y_values_non_std)
        # x_min_diff_first_x_np = np.arange(x_min_diff_first_x)
        # np.delete(y_values_non_std,x_min_diff_first_x_np)
        z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)] # Z-values are the y-values on 2d graph
        x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)

        diff_range_list = np.arange(diff)

        # Removes the values less than x_min for positive differences
        y_values_non_std = np.delete(y_values_non_std, diff_range_list)
        z_values_non_std = np.delete(z_values_non_std, diff_range_list)
        x_values_time_non_std = np.delete(x_values_time_non_std, diff_range_list)

        scaled_z_values_non_std = z_values_non_std * (frac2 / y_peak_data1)
        # print(max(z_values_non_std))
        # print(max(scaled_z_values_non_std))

        # print(diff)

        zero_list = [0] * diff
        # if diff > 0:

        # Positive differences, we will
        if diff > 0:
            y_values_append_values = np.arange(x_max - diff, x_max)
            # z_values_append_values = np.array(zero_list)
            z_values_append_values = np.array(x_values_non_std[x_max:x_max + diff])
            x_values_time_append_values = np.array([float(time_peak)] * diff)

            y_values_non_std = np.append(y_values_non_std, y_values_append_values)
            z_values_non_std = np.append(z_values_non_std, z_values_append_values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)
            # print(len(y_values_non_std))

        else:
            y_values_append_values = np.arange(x_min, x_min - diff + 1)
            x_range = x_max - x_min
            y_values_delete_values_end = [x for x in range(x_range + 1, x_range - diff + 2)]
            y_values_delete_values_begin = [x for x in range(0, abs(diff) + 1)]
            # y_values_delete_values = np.arange(x_max,x_max - diff)

            z_values_append_values = np.array(zero_list)
            x_values_time_append_values = np.array([float(time_peak)] * diff)

            y_values_non_std = np.insert(y_values_non_std, 0, y_values_append_values)
            y_values_non_std = np.delete(y_values_non_std, y_values_delete_values_end)
            z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)]
            x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)
            # print(b)
            # print(len(y_values_non_std))
            z_values_non_std = np.append(z_values_non_std, z_values_append_values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)

        # else:
        #   y_values_append_values = np.arange(x_max + diff, x_max)

        # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
        # np.append(y_values_non_std,zero_list)

        # print(y_values_non_std)

        ax3.plot(x_values_time_non_std, y_values_non_std, z_values_non_std * (frac2 / y_peak_data1), alpha=0.7)
    ax3.set_ylim(x_min, x_max)
    ax3.set_zlim(y_min, y_max)
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Data Point')
    ax3.set_zlabel('Frac. Area')
    # make the panes transparent
    # ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.set_facecolor('grey')
    # make the grid lines transparent
    # ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    # #Gets x values for vectorization purposes
    # array = np.arange(1,len(trace['DATA1'])+1)
    # #Subtracts difference from array (vectorization)
    # array -= diff

    plt.show()
    #plt.close()


def plot3dlog(length_dir, fsa_names_sorted, time_underscore, x_min, x_max, y_min, y_max, folder_fsa):
    fig2 = plt.figure()
    ax2 = plt.axes(projection='3d')
    # Counter for subplot number
    subplot_num = 1
    # Creates a list for all the differences. Will take the largest difference to set the axes x min and x max (y min and y max for 3d scatter)
    diff_list = []
    # parses the directory for .fsa files
    for k in range(length_dir):
        if k == 0:
            # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
            first_dp_split = fsa_names_sorted[k].split('_')
            time = first_dp_split[time_underscore]
            standard = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
            s_abif_key = standard.annotations['abif_raw'].keys()
            s_trace = defaultdict(list)
            s_channels = ['DATA1', 'DATA3']
            for sc in s_channels:
                # s_trace['DATA1'] = y values
                s_trace[sc] = standard.annotations['abif_raw'][sc]
            x_values = np.asarray(s_trace['DATA1'])
            y_std_max = max(s_trace['DATA3'])
            x_std_max = s_trace['DATA3'].index(y_std_max)
            # print(x_values[x_min:x_max+1])

            z_values = x_values[x_min:x_max + 1]
            x_values_time = [float(time)] * len(z_values)
            y_values = np.arange(x_min, x_max + 1)
            ##    print(len(x_values))
            ##    print(len(y_values))
            ##    print(len(z_values))
            # x_values = np.arange(1,len(y_values)+1)
            ##
            ##
            sc_std = ax2.plot(np.log(x_values_time), y_values, z_values, alpha=0.7)
            continue

        subplot_num += 1
        name_split = fsa_names_sorted[k].split('_')
        time_peak = name_split[time_underscore]
        # opens up the FSA file
        record = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
        # Record returns a bunch of dictionaries. Use this line to get the dictionary
        # keys of abif_raw only
        abif_key = record.annotations['abif_raw'].keys()
        # Creates an empty list as the value in the dict
        trace = defaultdict(list)
        # DATA1 is where all the peak value is held, so only grab this dictionary key
        channels = ['DATA1', 'DATA3']
        # Parses the channels list and returns the values for each key in dictionary
        for c in channels:
            trace[c] = record.annotations['abif_raw'][c]
        # Xvalues for time pts
        x_values_non_std = np.asarray(trace['DATA1'])
        # Numpy for y values (xvalues_non_std)

        # Get the max value data
        y_peak = max(trace['DATA3'])
        # Gets the x value of the max value
        x_peak = trace['DATA3'].index(y_peak)
        # Takes difference of reference x value and time point x value
        diff = x_peak - x_std_max
        diff_list.append(diff)
        # y_values_append_values = np.arange(x_max - diff, x_max)
        # print(diff)

        # X_values_non_std are really the y values on a 2d graph
        y_values_non_std = np.arange(x_min, x_max + 1) - diff

        x_min_diff_first_x = np.where(y_values_non_std == x_min)
        # print(x_min_diff_first_x)
        # if x_min_diff_first_x[0].size != 0:
        #     x_min_diff_first_x_range = np.arange(x_min_diff_first_x[0])
        #     #print(x_min_diff_first_x_range)
        #     y_values_non_std = np.delete(y_values_non_std,x_min_diff_first_x_range)
        # print(y_values_non_std)
        # print(x_min_diff_first_x)
        # print(y_values_non_std)
        # x_min_diff_first_x_np = np.arange(x_min_diff_first_x)
        # np.delete(y_values_non_std,x_min_diff_first_x_np)
        z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)]
        x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)

        diff_range_list = np.arange(diff)

        # Removes the values less than x_min for positive differences
        y_values_non_std = np.delete(y_values_non_std, diff_range_list)
        z_values_non_std = np.delete(z_values_non_std, diff_range_list)
        x_values_time_non_std = np.delete(x_values_time_non_std, diff_range_list)

        # print(diff)

        zero_list = [0] * diff
        # if diff > 0:

        # Positive differences, we will
        if diff > 0:
            y_values_append_values = np.arange(x_max - diff, x_max)
            # z_values_append_values = np.array(zero_list)
            z_values_append_values = np.array(x_values_non_std[x_max:x_max + diff])
            x_values_time_append_values = np.array([float(time_peak)] * diff)

            y_values_non_std = np.append(y_values_non_std, y_values_append_values)
            z_values_non_std = np.append(z_values_non_std, z_values_append_values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)
            # print(len(y_values_non_std))

        else:
            y_values_append_values = np.arange(x_min, x_min - diff + 1)
            x_range = x_max - x_min
            y_values_delete_values_end = [x for x in range(x_range + 1, x_range - diff + 2)]
            y_values_delete_values_begin = [x for x in range(0, abs(diff) + 1)]
            # y_values_delete_values = np.arange(x_max,x_max - diff)

            z_values_append_values = np.array(zero_list)
            x_values_time_append_values = np.array([float(time_peak)] * diff)

            y_values_non_std = np.insert(y_values_non_std, 0, y_values_append_values)
            y_values_non_std = np.delete(y_values_non_std, y_values_delete_values_end)
            z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)]
            x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)
            # print(b)
            # print(len(y_values_non_std))
            z_values_non_std = np.append(z_values_non_std, z_values_append_values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)
            # x_values_time_non_std = math.log(x_values_time_non_std)*100

        # x_values_time_non_std = np.log(x_values_time_non_std)
        # print(x_values_time_non_std)
        # else:
        #   y_values_append_values = np.arange(x_max + diff, x_max)

        # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
        # np.append(y_values_non_std,zero_list)

        # print(y_values_non_std)

        sc_non_std = ax2.plot(np.log(x_values_time_non_std), y_values_non_std, z_values_non_std, alpha=0.7)
    ax2.set_ylim(x_min, x_max)
    ax2.set_zlim(y_min, y_max)
    ax2.set_xlabel('Log Time')
    ax2.set_ylabel('Data Point')
    ax2.set_zlabel('RFU')
    # make the panes transparent
    # ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.set_facecolor('grey')
    # make the grid lines transparent
    # ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    # #Gets x values for vectorization purposes
    # array = np.arange(1,len(trace['DATA1'])+1)
    # #Subtracts difference from array (vectorization)
    # array -= diff

    plt.show()
    #plt.close()


def plot3dlogscaled(length_dir, fsa_names_sorted, time_underscore, x_min, x_max, y_min, y_max, folder_fsa, zip_dict,
                    pre_fASB_test):
    fig3 = plt.figure()
    ax3 = plt.axes(projection='3d')
    # Counter for subplot number
    subplot_num = 1
    # Creates a list for all the differences. Will take the largest difference to set the axes x min and x max (y min and y max for 3d scatter)
    diff_list = []
    # parses the directory for .fsa files
    for k in range(length_dir):
        if k == 0:
            # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
            first_dp_split = fsa_names_sorted[k].split('_')
            time = first_dp_split[time_underscore]
            standard = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
            s_abif_key = standard.annotations['abif_raw'].keys()
            s_trace = defaultdict(list)
            s_channels = ['DATA1', 'DATA3']
            for sc in s_channels:
                # s_trace['DATA1'] = y values
                s_trace[sc] = standard.annotations['abif_raw'][sc]
            x_values = np.asarray(s_trace['DATA1'])
            y_std_max = max(s_trace['DATA3'])
            x_std_max = s_trace['DATA3'].index(y_std_max)
            # print(x_values[x_min:x_max+1])

            y_std_maxdata1 = max(s_trace['DATA1'])
            x_std_maxdata1 = s_trace['DATA1'].index(y_std_maxdata1)
            size_with_xmax = zip_dict[str(x_std_maxdata1)]  # Gets the size of the xmax value
            size_with_xmax_total = size_with_xmax + '/' + 'Total'
            frac_row = pre_fASB_test.iloc[k, :]
            frac = frac_row.loc[size_with_xmax_total]
            # print(size_with_xmax_total)
            # print(frac)
            # print(y_std_maxdata1)
            factor1 = frac / y_std_maxdata1
            # print(factor1)

            # Gets a range for the max peak

            # Gets max y value for data1:
            y_std_peakdata1 = max(s_trace['DATA1']) / sum(s_trace['DATA1'])
            z_values = x_values[x_min:x_max + 1]
            x_values_time = [float(time)] * len(z_values)
            y_values = np.arange(x_min, x_max + 1)
            ##    print(len(x_values))
            ##    print(len(y_values))
            ##    print(len(z_values))
            # x_values = np.arange(1,len(y_values)+1)
            ##
            ##
            # print(type(z_values))
            scaled_z_values = z_values * (frac / y_std_maxdata1)
            # print(max(z_values))
            # print(max(scaled_z_values))
            # print(scaled_z_values)
            ax3.plot(np.log(x_values_time), y_values, scaled_z_values, alpha=0.7)
            continue

        subplot_num += 1
        name_split = fsa_names_sorted[k].split('_')
        time_peak = name_split[time_underscore]
        # opens up the FSA file
        record = SeqIO.read(folder_fsa + '/' + fsa_names_sorted[k], 'abi')
        # Record returns a bunch of dictionaries. Use this line to get the dictionary
        # keys of abif_raw only
        abif_key = record.annotations['abif_raw'].keys()
        # Creates an empty list as the value in the dict
        trace = defaultdict(list)
        # DATA1 is where all the peak value is held, so only grab this dictionary key
        channels = ['DATA1', 'DATA3']
        # Parses the channels list and returns the values for each key in dictionary
        for c in channels:
            trace[c] = record.annotations['abif_raw'][c]
        # Xvalues for time pts
        x_values_non_std = np.asarray(trace['DATA1'])
        # Numpy for y values (xvalues_non_std)

        # Get the max value data
        y_peak = max(trace['DATA3'])
        # Gets the x value of the max value
        x_peak = trace['DATA3'].index(y_peak)

        # Gets the y-peak for Data1
        y_peak_data1 = max(trace['DATA1'])  # fractional area/max intenisty
        x_peak_data1 = trace['DATA1'].index(y_peak_data1)

        size_with_xmax_2 = zip_dict[str(x_peak_data1)]  # Gets the size of the xmax value
        size_with_xmax_total_2 = size_with_xmax_2 + '/' + 'Total'
        frac_row_2 = pre_fASB_test.iloc[k, :]
        frac2 = frac_row_2.loc[size_with_xmax_total_2]
        # print(frac2)
        factor2 = frac2 / y_peak_data1
        # print(size_with_xmax_total_2)
        # print(y_peak_data1)
        # print(factor2)

        # Takes difference of reference x value and time point x value
        diff = x_peak - x_std_max
        diff_list.append(diff)
        # y_values_append_values = np.arange(x_max - diff, x_max)
        # print(diff)

        # X_values_non_std are really the y values on a 2d graph
        y_values_non_std = np.arange(x_min, x_max + 1) - diff  # removes values data point values that are +/- the
        # difference. It's subtraction by difference because if positive, then remove data points in front

        x_min_diff_first_x = np.where(y_values_non_std == x_min)
        # print(x_min_diff_first_x)
        # if x_min_diff_first_x[0].size != 0:
        #     x_min_diff_first_x_range = np.arange(x_min_diff_first_x[0])
        #     #print(x_min_diff_first_x_range)
        #     y_values_non_std = np.delete(y_values_non_std,x_min_diff_first_x_range)
        # print(y_values_non_std)
        # print(x_min_diff_first_x)
        # print(y_values_non_std)
        # x_min_diff_first_x_np = np.arange(x_min_diff_first_x)
        # np.delete(y_values_non_std,x_min_diff_first_x_np)
        z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)]
        x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)

        diff_range_list = np.arange(diff)

        # Removes the values less than x_min for positive differences
        y_values_non_std = np.delete(y_values_non_std, diff_range_list)
        z_values_non_std = np.delete(z_values_non_std, diff_range_list)
        x_values_time_non_std = np.delete(x_values_time_non_std, diff_range_list)

        scaled_z_values_non_std = z_values_non_std * (frac2 / y_peak_data1)
        # print(max(z_values_non_std))
        # print(max(scaled_z_values_non_std))

        # print(diff)

        zero_list = [0] * diff
        # if diff > 0:

        # Positive differences, we will
        if diff > 0:
            y_values_append_values = np.arange(x_max - diff, x_max)
            # z_values_append_values = np.array(zero_list)
            z_values_append_values = np.array(x_values_non_std[x_max:x_max + diff])
            x_values_time_append_values = np.array([float(time_peak)] * diff)

            y_values_non_std = np.append(y_values_non_std, y_values_append_values)
            z_values_non_std = np.append(z_values_non_std, z_values_append_values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)
            # print(len(y_values_non_std))

        else:
            y_values_append_values = np.arange(x_min, x_min - diff + 1)
            x_range = x_max - x_min
            y_values_delete_values_end = [x for x in range(x_range + 1, x_range - diff + 2)]
            y_values_delete_values_begin = [x for x in range(0, abs(diff) + 1)]
            # y_values_delete_values = np.arange(x_max,x_max - diff)

            z_values_append_values = np.array(zero_list)
            x_values_time_append_values = np.array([float(time_peak)] * diff)

            y_values_non_std = np.insert(y_values_non_std, 0, y_values_append_values)
            y_values_non_std = np.delete(y_values_non_std, y_values_delete_values_end)
            z_values_non_std = x_values_non_std[x_min:x_min + len(y_values_non_std)]
            x_values_time_non_std = [float(time_peak)] * len(y_values_non_std)
            # print(b)
            # print(len(y_values_non_std))
            z_values_non_std = np.append(z_values_non_std, z_values_append_values)
            x_values_time_non_std = np.append(x_values_time_non_std, x_values_time_append_values)

        # else:
        #   y_values_append_values = np.arange(x_max + diff, x_max)

        # ax = fig.add_subplot(3,3,subplot_num,projection='3d')
        # np.append(y_values_non_std,zero_list)

        # print(y_values_non_std)

        ax3.plot(np.log(x_values_time_non_std), y_values_non_std, z_values_non_std * (frac2 / y_peak_data1), alpha=0.7)
    ax3.set_ylim(x_min, x_max)
    ax3.set_zlim(y_min, y_max)
    ax3.set_xlabel('Log Time')
    ax3.set_ylabel('Data Point')
    ax3.set_zlabel('Frac. Area')
    # make the panes transparent
    # ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax.set_facecolor('grey')
    # make the grid lines transparent
    # ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    # #Gets x values for vectorization purposes
    # array = np.arange(1,len(trace['DATA1'])+1)
    # #Subtracts difference from array (vectorization)
    # array -= diff

    plt.show()
    #plt.close()
