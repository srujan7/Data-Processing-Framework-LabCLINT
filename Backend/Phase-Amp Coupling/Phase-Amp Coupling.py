import numpy as np
import pandas as pd
import scipy as sp
import scipy.stats
import matplotlib.pyplot as plt
from pathlib import Path
import xlsxwriter
import sys
from os.path import dirname, join, abspath

sys.path.insert(0, abspath(join(dirname(__file__), '..') + "\Toolbox"))
import Toolbox

conditions_list = []
conditions_list = Toolbox.askConditions(conditions_list)

num_each_condition = []
num_each_condition = Toolbox.askNumEachC(conditions_list, num_each_condition)

subjects_of_each_condition = []

ROIs = []
chosenROIs = []

class PACSubject(Toolbox.Subject):
    def __init__(self, subjectID):
        self.name = None
        self.data = None
        self.data_degrees = None
        self.linear_correlations = None
        self.circular_correlations = None
        self.ROIs = []
        super(PACSubject, self).__init__(subjectID)

    def setData(self, fileList, rois):
        data = []
        num_rows = 0
        for file in fileList:
            with open(file) as f:
                data.append(np.genfromtxt(f))
                num_rows = data[0].shape[0]
                self.ROIs = rois
        subj_Data = np.concatenate(data)
        row_labels = []
        for r in range(num_rows):
            row_labels.append(r)

        idx = pd.MultiIndex.from_product([ROIs, row_labels], names=('ROI', 'Time'))
        data_list = pd.DataFrame(data=subj_Data, index=idx, columns=chosenFrequencies)
        self.data = data_list

        self.data_degrees = self.data.copy()
        self.data_degrees.iloc[:,1] = self.data_degrees.iloc[:,1]*(180/(np.pi))

        print(self.data)

        subject_name = str(fileList[0])
        subject_name = subject_name.split('\\')
        subject_name = subject_name[len(subject_name) - 1]
        subject_name = subject_name.split('_')
        self.name = subject_name[0] + '_' + subject_name[1] + '-' + subject_name[2]

    def getData(self):
        return self.data

    def getDataDegrees(self):
        return self.data_degrees

    def setLinearCorrelations(self, corrList):
        self.linear_correlations = pd.DataFrame(data=corrList, index=ROIs, columns=['Linear Correlation Coefficient'])

    def setCircularCorrelations(self, circCorrList):
        self.circular_correlations = pd.DataFrame(data=circCorrList, index=ROIs,
                                                  columns=['Circular Correlation Coefficient'])

    def getLinearCorrelations(self):
        return self.linear_correlations

    def getCircularCorrelations(self):
        return self.circular_correlations


data_folder = Path(r"C:\Users\vse160030\Documents\GitHub\Data-Reorganization-Lab-CLINT")

def ask_for_rois():
    print("\n")
    while True:
        try:
            numROIs = int(input("How many ROIs are present in your data? (Max: 84)\n"))
            if numROIs <= 84:
                break
        except ValueError:
            print("\nPlease enter an integer.")
            continue

        if numROIs > 84:
            print("\nThe number entered exceeds the maximum value allowed. Please try again.")
            continue

    # function to return chosen ROI, which can then be added to the chosenROIs list
    def ROIchoice(c):
        switcher = {
            "1L": 'Primary somatosensory cortex (Postcentral gyrus)',
            "2L": 'Primary somatosensory cortex (Postcentral gyrus)',
            "3L": 'Primary somatosensory cortex (Postcentral gyrus)',
            "4L": 'Primary motor cortex (Precentral gyrus)',
            "5L": 'Somatosensory association cortex',
            "6L": 'Premotor and supplementary motor cortex',
            "7L": 'Visuo-motor cortex',
            "8L": 'Frontal eye fields',
            "9L": 'Dorsolateral prefrontal cortex',
            "10L": 'Anterior prefrontal cortex',
            "11L": 'Orbitofrontal area',
            "13L": 'Insular Cortex',
            "17L": 'Primary visual cortex (V1)',
            "18L": 'Secondary visual cortex (V2)',
            "19L": 'Associative visual cortex (V3, V4, V5)',
            "20L": 'Inferior temporal gyrus',
            "21L": 'Middle temporal gyrus',
            "22L": 'Superior temporal gyrus',
            "23L": 'Ventral posterior cingulate cortex',
            "24L": 'Ventral anterior cingulate cortex',
            "25L": 'Subgenual area',
            "27L": 'Piriform cortex',
            "28L": 'Ventral entorhinal cortex',
            "29L": 'Retrosplenial cingulate cortex',
            "30L": 'Retrosplenial cerebral cortex',
            "31L": 'Dorsal posterior cingulate cortex',
            "32L": 'Dorsal anterior cingulate cortex',
            "33L": 'Cingulate cerebral cortex (Anterior cingulate gyrus)',
            "34L": 'Dorsal entorhinal cortex',
            "35L": 'Perirhinal cortex',
            "36L": 'Ectorhinal area (Temporal cerebral cortex)',
            "37L": 'Fusiform gyrus',
            "38L": 'Temporopolar area',
            "39L": 'Angular gyrus',
            "40L": 'Supramarginal gyrus',
            "41L": 'Auditory cortex',
            "42L": 'Auditory cortex',
            "43L": 'Primary gustatory cortex',
            "44L": 'Pars opercularis',
            "45L": 'Pars triangularis',
            "46L": 'Dorsolateral prefrontal cortex',
            "47L": 'Pars orbitalis',

            "1R": 'Primary somatosensory cortex (Postcentral gyrus)',
            "2R": 'Primary somatosensory cortex (Postcentral gyrus)',
            "3R": 'Primary somatosensory cortex (Postcentral gyrus)',
            "4R": 'Primary motor cortex (Precentral gyrus)',
            "5R": 'Somatosensory association cortex',
            "6R": 'Premotor and supplementary motor cortex',
            "7R": 'Visuo-motor cortex',
            "8R": 'Frontal eye fields',
            "9R": 'Dorsolateral prefrontal cortex',
            "10R": 'Anterior prefrontal cortex',
            "11R": 'Orbitofrontal area',
            "13R": 'Insular Cortex',
            "17R": 'Primary visual cortex (V1)',
            "18R": 'Secondary visual cortex (V2)',
            "19R": 'Associative visual cortex (V3, V4, V5)',
            "20R": 'Inferior temporal gyrus',
            "21R": 'Middle temporal gyrus',
            "22R": 'Superior temporal gyrus',
            "23R": 'Ventral posterior cingulate cortex',
            "24R": 'Ventral anterior cingulate cortex',
            "25R": 'Subgenual area',
            "27R": 'Piriform cortex',
            "28R": 'Ventral entorhinal cortex',
            "29R": 'Retrosplenial cingulate cortex',
            "30R": 'Retrosplenial cerebral cortex',
            "31R": 'Dorsal posterior cingulate cortex',
            "32R": 'Dorsal anterior cingulate cortex',
            "33R": 'Cingulate cerebral cortex (Anterior cingulate gyrus)',
            "34R": 'Dorsal entorhinal cortex',
            "35R": 'Perirhinal cortex',
            "36R": 'Ectorhinal area (Temporal cerebral cortex)',
            "37R": 'Fusiform gyrus',
            "38R": 'Temporopolar area',
            "39R": 'Angular gyrus',
            "40R": 'Supramarginal gyrus',
            "41R": 'Auditory cortex',
            "42R": 'Auditory cortex',
            "43R": 'Primary gustatory cortex',
            "44R": 'Pars opercularis',
            "45R": 'Pars triangularis',
            "46R": 'Dorsolateral prefrontal cortex',
            "47R": 'Pars orbitalis',
        }
        return switcher.get(c, 0)

    def inputROIs():
        choice = input("""\n
                            Left:
                            1L: Primary somatosensory cortex (Postcentral gyrus)
                            2L: Primary somatosensory cortex (Postcentral gyrus)
                            3L: Primary somatosensory cortex (Postcentral gyrus)
                            4L: Primary motor cortex (Precentral gyrus)
                            5L: Somatosensory association cortex
                            6L: Premotor and supplementary motor cortex
                            7L: Visuo-motor cortex
                            8L: Frontal eye fields
                            9L: Dorsolateral prefrontal cortex
                            10L: Anterior prefrontal cortex
                            11L: Orbitofrontal area
                            13L: Insular Cortex
                            17L: Primary visual cortex (V1)
                            18L: Secondary visual cortex (V2)
                            19L: Associative visual cortex (V3, V4, V5)
                            20L: Inferior temporal gyrus
                            21L: Middle temporal gyrus
                            22L: Superior temporal gyrus
                            23L: Ventral posterior cingulate cortex
                            24L: Ventral anterior cingulate cortex
                            25L: Subgenual area
                            27L: Piriform cortex
                            28L: Ventral entorhinal cortex
                            29L: Retrosplenial cingulate cortex
                            30L: Retrosplenial cerebral cortex
                            31L: Dorsal posterior cingulate cortex
                            32L: Dorsal anterior cingulate cortex
                            33L: Cingulate cerebral cortex (Anterior cingulate gyrus)
                            34L: Dorsal entorhinal cortex
                            35L: Perirhinal cortex
                            36L: Ectorhinal area (Temporal cerebral cortex)
                            37L: Fusiform gyrus
                            38L: Temporopolar area
                            39L: Angular gyrus
                            40L: Supramarginal gyrus
                            41L: Auditory cortex
                            42L: Auditory cortex
                            43L: Primary gustatory cortex
                            44L: Pars opercularis
                            45L: Pars triangularis
                            46L: Dorsolateral prefrontal cortex
                            47L: Pars orbitalis

                            Right:
                            1R: Primary somatosensory cortex (Postcentral gyrus)
                            2R: Primary somatosensory cortex (Postcentral gyrus)
                            3R: Primary somatosensory cortex (Postcentral gyrus)
                            4R: Primary motor cortex (Precentral gyrus)
                            5R: Somatosensory association cortex
                            6R: Premotor and supplementary motor cortex
                            7R: Visuo-motor cortex
                            8R: Frontal eye fields
                            9R: Dorsolateral prefrontal cortex
                            10R: Anterior prefrontal cortex
                            11R: Orbitofrontal area
                            13R: Insular Cortex
                            17R: Primary visual cortex (V1)
                            18R: Secondary visual cortex (V2)
                            19R: Associative visual cortex (V3, V4, V5)
                            20R: Inferior temporal gyrus
                            21R: Middle temporal gyrus
                            22R: Superior temporal gyrus
                            23R: Ventral posterior cingulate cortex
                            24R: Ventral anterior cingulate cortex
                            25R: Subgenual area
                            27R: Piriform cortex
                            28R: Ventral entorhinal cortex
                            29R: Retrosplenial cingulate cortex
                            30R: Retrosplenial cerebral cortex
                            31R: Dorsal posterior cingulate cortex
                            32R: Dorsal anterior cingulate cortex
                            33R: Cingulate cerebral cortex (Anterior cingulate gyrus)
                            34R: Dorsal entorhinal cortex
                            35R: Perirhinal cortex
                            36R: Ectorhinal area (Temporal cerebral cortex)
                            37R: Fusiform gyrus
                            38R: Temporopolar area
                            39R: Angular gyrus
                            40R: Supramarginal gyrus
                            41R: Auditory cortex
                            42R: Auditory cortex
                            43R: Primary gustatory cortex
                            44R: Pars opercularis
                            45R: Pars triangularis
                            46R: Dorsolateral prefrontal cortex
                            47R: Pars orbitalis"""
                       "\n\nPlease enter the ROIs: \n")
        return choice

    valid = True

    # list of all valid entries to query
    ROIsList = ['1L', '2L', '3L', '4L', '5L', '6L', '7L', '8L', '9L', '10L', '11L', '13L', '17L', '18L', '19L', '20L',
                '21L', '22L', '23L', '24L', '25L', '27L', '28L', '29L', '30L', '31L', '32L', '33L', '34L', '35L', '36L',
                '37L', '38L', '39L', '40L', '41L', '42L', '43L', '44L', '45L', '46L', '47L', '1R', '2R', '3R', '4R',
                '5R', '6R', '7R', '8R', '9R', '10R', '11R', '13R', '17R', '18R', '19R', '20R', '21R', '22R', '23R',
                '24R', '25R', '27R', '28R', '29R', '30R', '31R', '32R', '33R', '34R', '35R', '36R', '37R', '38R', '39R',
                '40R', '41R', '42R', '43R', '44R', '45R', '46R', '47R']

    print(
        "\nWhat ROIs are you evaluating in your data? Please enter the IDs of the ROIs from the list below. Enter all ROIs in one line, separated by a space (e.g. 1R 5L 3L 12R).")
    c = inputROIs().split()

    if len(c) != numROIs:
        valid = False

    # if input is invalid, continue requesting user to input valid ROIs until they do so
    while(not valid):
        print("\nYou have not entered the correct number of ROIs. Please try again.")
        c = []
        c.extend(inputROIs().split())
        if len(c) != numROIs:
            valid = False
        else:
            valid = True

    if valid:
        for cv in range(len(c)):
            if c[cv] in ROIsList:
                valid = True
            else:
                valid = False
                break

    while (not valid):
        print("\nYou have entered invalid ROIs. Please try again.")
        c = []
        c.extend(inputROIs().split())

        valid = True

        if len(c) != numROIs:
            valid = False

        while (not valid):
            print("\nYou have not entered the correct number of ROIs. Please try again.")
            c = []
            c.extend(inputROIs().split())
            if len(c) != numROIs:
                valid = False
            else:
                valid = True

        if valid:
            for cv in range(len(c)):
                if c[cv] in ROIsList:
                    valid = True
                else:
                    valid = False
                    break

    ROIs.extend(c)

    # add selected ROI names into chosenROIs list
    for roi in range(len(c)):
        chosenROIs.append(ROIchoice(c[roi]))

    print(chosenROIs)


ask_for_rois()
print("\nThese are the ROIs chosen, in order:", chosenROIs)

# list to hold the user's desired frequencies, in the order entered
chosenFrequencies = []


# function to take user input for frequency bands used in their experiment
def ask_for_frequencies():
    print(
        "\nWhat two frequency bands are you evaluating in your data? Please enter them in the order in which they are present in the input files. Enter all frequency bands in one line (e.g. BK).")

    # function to return chosen frequency band, which can then be added to the chosenFrequencies list
    def frequencyChoice(c):
        switcher = {
            "A": 'Delta',
            "a": 'Delta',
            "B": 'Theta',
            "b": 'Theta',
            "C": 'Alpha',
            "c": 'Alpha',
            "D": 'Alpha1',
            "d": 'Alpha1',
            "E": 'Alpha2',
            "e": 'Alpha2',
            "F": 'Alpha3',
            "f": 'Alpha3',
            "G": 'Beta',
            "g": 'Beta',
            "H": 'Beta1',
            "h": 'Beta1',
            "I": 'Beta2',
            "i": 'Beta2',
            "J": 'Beta3',
            "j": 'Beta3',
            "K": 'Gamma',
            "k": 'Gamma',
            "L": 'Low Gamma',
            "l": 'Low Gamma',
            "M": 'High Gamma',
            "m": 'High Gamma',
            "N": 'Mu',
            "n": 'Mu',
        }
        return switcher.get(c, 0)

    # variable to process input validation
    valid = True

    # function to display all frequency bands to user and request selection of desired bands
    def inputFreq():
        choice = input("""
                        A: Delta
                        B: Theta
                        C: Alpha
                        D: Alpha1
                        E: Alpha2
                        F: Alpha3
                        G: Beta
                        H: Beta1
                        I: Beta2
                        J: Beta3
                        K: Gamma
                        L: Low Gamma
                        M: High Gamma
                        N: Mu"""

                       "\n\n\nPlease enter your desired bands: \n")
        return choice

    # list of all valid entries to query
    frequencyList = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
                     'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n']

    # parse inputted frequencies into an itemized list and add each frequency band to chosenFrequencies list
    c = list(inputFreq())
    for cv in range(len(c)):
        if c[cv] in frequencyList:
            valid = True
        else:
            valid = False
            break
    if len(c) > 2:
        valid = False

    # if input is invalid, continue requesting user to input valid frequencies until they do so
    while (not valid):
        print("\nYou have entered invalid frequencies. Please try again.\n")
        c = list(inputFreq())
        for cv in range(len(c)):
            if c[cv] in frequencyList:
                valid = True
            else:
                valid = False
        if len(c) > 2:
            valid = False

    # add selected frequency band names into chosenFrequencies list
    for bands in range(len(c)):
        chosenFrequencies.append(frequencyChoice(c[bands]) + " amplitude")
        chosenFrequencies.append(frequencyChoice(c[bands]) + " phase")


# run the function to get frequencies from user
ask_for_frequencies()
print("\nThese are the frequency bands chosen, in order:", chosenFrequencies)


def dataFileEntry():
    for each_condition in range(len(conditions_list)):
        subjects_of_each_condition.append([])
        print("\nData entry for %s:" % conditions_list[each_condition])
        for x in range(
                num_each_condition[
                    each_condition]):
            fileNames = []
            for f in range(len(ROIs)):
                file_Location = input(
                    "\nPlease enter the path to the data file for '%s' for Subject %s of '%s' in the folder 'Data-Reorganization-Lab-CLINT': \n" % (chosenROIs[f],
                        (str)(x + 1), conditions_list[
                            each_condition]))
                fileFolder = data_folder / file_Location
                fileNames.append(fileFolder)

            subjects_of_each_condition[each_condition].append(
                PACSubject("%s %s" % (conditions_list[each_condition], (str)(
                    x + 1))))
            while True:
                try:
                    subjects_of_each_condition[each_condition][x].setData(
                        fileNames,
                        chosenROIs)
                    break
                except (FileNotFoundError, OSError):
                    print("\nOne or more of the files were not found in their specified paths." + "\nPlease try again. \n")
                    fileNames = []
                    for f in range(len(ROIs)):
                        file_Location = input(
                            "\nPlease enter the path to the data file for '%s' for Subject %s of '%s' in the folder 'Data-Reorganization-Lab-CLINT': \n" % (
                            chosenROIs[f],
                            (str)(x + 1), conditions_list[
                                each_condition]))
                        fileFolder = data_folder / file_Location
                        fileNames.append(fileFolder)


dataFileEntry()


#https://github.com/voytekresearch/tutorials/blob/master/Phase%20Amplitude%20Coupling%20Tutorial.ipynb
def circCorr(ang,line):
    n = len(ang)
    rxs = sp.stats.pearsonr(line,np.sin(ang))
    rxs = rxs[0]
    rxc = sp.stats.pearsonr(line,np.cos(ang))
    rxc = rxc[0]
    rcs = sp.stats.pearsonr(np.sin(ang),np.cos(ang))
    rcs = rcs[0]
    rho = np.sqrt((rxc**2 + rxs**2 - 2*rxc*rxs*rcs)/(1-rcs**2)) #r
    r_2 = rho**2 #r squared
    pval = 1- sp.stats.chi2.cdf(n*(rho**2),1)
    standard_error = np.sqrt((1-r_2)/(n-2))

    return rho, pval, r_2,standard_error


# Making an excel file and sorting data
def export_to_excel():
    data_organized = []
    data_organized_circ = []
    sheets = []
    sheets_circ = []
    corrList = []
    circCorrList = []
    for organized in range(len(conditions_list)):
        data_organized.append(xlsxwriter.Workbook("%s_Phase-Amp Coupling Linear Correlations.xlsx" % conditions_list[organized]))
        sheets.append([])
        data_organized_circ.append(xlsxwriter.Workbook("%s_Phase-Amp Coupling Circular Correlations.xlsx" % conditions_list[organized]))
        sheets_circ.append([])
    for each_condition in range(len(conditions_list)):
        sheets[each_condition].append(data_organized[each_condition].add_worksheet(str(conditions_list[each_condition])))
        sheets_circ[each_condition].append(data_organized_circ[each_condition].add_worksheet(str(conditions_list[each_condition])))
        subject_counter = 0
        for subject in range(num_each_condition[each_condition] + 1):
            if subject == 0:
                sheets[each_condition][0].write_row(0,1,ROIs)
                sheets_circ[each_condition][0].write_row(0,1,ROIs)
            else:
                sheets[each_condition][0].write(subject, 0, subjects_of_each_condition[each_condition][
                    subject_counter].getName())
                sheets_circ[each_condition][0].write(subject, 0, subjects_of_each_condition[each_condition][subject_counter].getName())
                for roi in range(len(ROIs)):
                    r,p = sp.stats.pearsonr(subjects_of_each_condition[each_condition][subject_counter].getData().loc[ROIs[roi],chosenFrequencies[1]],subjects_of_each_condition[each_condition][subject_counter].getData().loc[ROIs[roi],chosenFrequencies[2]])
                    corrList.append(r)
                    sheets[each_condition][0].write(subject, roi + 1, r)
                    w,x,y,z = circCorr(subjects_of_each_condition[each_condition][subject_counter].getData().loc[ROIs[roi],chosenFrequencies[1]],subjects_of_each_condition[each_condition][subject_counter].getData().loc[ROIs[roi],chosenFrequencies[2]])
                    circCorrList.append(w)
                    sheets_circ[each_condition][0].write(subject, roi + 1, w)
                subjects_of_each_condition[each_condition][subject_counter].setLinearCorrelations(corrList)
                subjects_of_each_condition[each_condition][subject_counter].setCircularCorrelations(circCorrList)
                corrList = []
                circCorrList = []
                subject_counter += 1

    for organized in range(len(conditions_list)):
        data_organized[organized].close()
        data_organized_circ[organized].close()
    print(
        "\nYour data has been organized for each condition and type of correlation. The data is sorted into Subjects x ROIs. The files have been saved in the working directory.")


while True:
    try:
        export_to_excel()
        break
    except (KeyError, IndexError):
        chosenFrequencies = []
        print("\nYour data doesn't have this many frequencies. Please try again.")
        ask_for_frequencies()
        print(chosenFrequencies)
    except PermissionError:
        print(
            "\nThe file you're attempting to create already exists and is currently in use. Please close it and try again.")
        exit(1)

averageMatrices = []
for each_condition in range(len(conditions_list)):
    idx = []
    for subject in range(num_each_condition[each_condition]):
        idx.append("Subject " + str(subject + 1))
    averageMatrices.append(pd.DataFrame(index=idx, columns=ROIs))
    for subject in range(num_each_condition[each_condition]):
        for roi in range(len(ROIs)):
            averageMatrices[each_condition].iloc[subject][roi] = \
            subjects_of_each_condition[each_condition][subject].getLinearCorrelations().iloc[0,0]

width = 0.35

class graphNumbersExc(Exception):
    def __init__(self):
        Exception.__init__(self)


print_graphs = input("\nDo you want the data graphed? Enter Y for yes and N for no.\n")
valid_graph_inputs = {'Y', 'y', 'N', 'n'}
while print_graphs not in valid_graph_inputs:
    print_graphs = input("That is not a valid response. Please try again. Enter Y for yes and N for no.")
which_graphs = input("\nEnter 1 to graph linear correlations. Enter 2 to graph circular correlations and export raw data. Enter 3 for both.\n")
valid_graphs = {'1','2','3'}
while which_graphs not in valid_graphs:
    which_graphs = input("That is not a valid response. Please try again.")

def makeGraphs():
    plotMatrices = []
    plotMatricesErrors = []
    for each_condition in range(len(conditions_list)):
        plotMatrices.append([0] * len(ROIs))
        plotMatricesErrors.append([0] * len(ROIs))
    for each_condition in range(len(conditions_list)):
        for roi in range(len(ROIs)):
                plotMatrices[each_condition][roi] = averageMatrices[each_condition][
                   str(ROIs[roi])].mean()
                plotMatricesErrors[each_condition][roi] = 2 * averageMatrices[each_condition][str(ROIs[roi])].sem()
    y_pos = np.arange(0, len(conditions_list) * 0.5 * len(ROIs), len(conditions_list) * 0.5)
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.figure(1)
    for plot in range(len(plotMatrices)):
        if plot == 0:
            plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, yerr=plotMatricesErrors[plot], capsize=10)
        else:
            plt.bar([p + width * plot for p in y_pos], plotMatrices[plot], width, alpha=0.5, yerr=plotMatricesErrors[plot], capsize=10)
    ax.set_xticks([p + (0.5 * (len(conditions_list) - 1)) * width for p in y_pos])
    ax.set_xticklabels(chosenROIs)
    ax.set_ylabel('Correlation Coefficient')
    ax.set_title('%s-%s Coupling' % (chosenFrequencies[1], chosenFrequencies[2]))
    maxY = 0
    for each_condition in range(len(conditions_list)):
        for roi in range(len(ROIs)):
            if abs(plotMatrices[each_condition][roi]) > maxY:
                maxY = abs(plotMatrices[each_condition][roi])
            if abs(plotMatrices[each_condition][roi]) + plotMatricesErrors[each_condition][roi] > maxY:
                maxY = abs(plotMatrices[each_condition][roi]) + plotMatricesErrors[each_condition][roi]
    plt.ylim([maxY * -1.25, maxY * 1.25])

    # Adding the legend and showing the plot
    plt.legend(conditions_list, loc='upper right')
    plt.savefig('Phase-Amplitude Coupling.png')

def makeCirclePlot():
    #bin_size = 5
    #bins = range(-180, 180 + bin_size, bin_size)
    #bins = np.dot(bins, 0.0174532925)

    num_bins = 72
    bin_size = (2*(np.pi))/num_bins
    bins = np.arange((-1*np.pi), np.pi + bin_size, bin_size)

    amps = []
    amps_mean = []
    # amps_errors = []
    subjects = []

    for roi in range(len(ROIs)):
        amps.append([])
        amps_mean.append([])
    for each_condition in range(len(conditions_list)):
        subjects.append([])
        for subject in range(num_each_condition[each_condition]):
            subjects[each_condition].append(subjects_of_each_condition[each_condition][subject].getName())
    for roi in range(len(ROIs)):
        for each_condition in range(len(conditions_list)):
            amps[roi].append(pd.DataFrame(index=bins, columns=subjects[each_condition]))
            amps[roi][each_condition].drop(amps[roi][each_condition].tail(1).index, inplace=True)
            amps_mean[roi].append(pd.DataFrame(index=bins,columns=['Average Amplitude']))
            amps_mean[roi][each_condition].drop(amps_mean[roi][each_condition].tail(1).index, inplace=True)
            #amps_errors.append(pd.DataFrame(index=bins,columns=['SEM']))
            #amps_errors[each_condition].drop(amps_errors[each_condition].tail(1).index, inplace=True)

    # filling phase bins with amplitudes
    for roi in range(len(ROIs)):
        for each_condition in range(len(conditions_list)):
            for subject in range(num_each_condition[each_condition]):
                for x in range(len(bins) - 1):
                    amps_above_lo_bound = np.where(subjects_of_each_condition[each_condition][subject].getData().loc['%s' % ROIs[roi]].iloc[:,1] >= bins[x])[0]
                    amps_below_hi_bound = np.where(subjects_of_each_condition[each_condition][subject].getData().loc['%s' % ROIs[roi]].iloc[:,1] < bins[x + 1])[0]
                    amps_below_hi_bound = set(amps_below_hi_bound)
                    amp_inds_in_this_bin = [amp_val for amp_val in amps_above_lo_bound if amp_val in amps_below_hi_bound]
                    amps_in_this_bin = subjects_of_each_condition[each_condition][subject].getData().loc['%s' % ROIs[roi]].iloc[amp_inds_in_this_bin,2]
                    amps[roi][each_condition].iloc[x,subject] = np.mean(amps_in_this_bin)

    bins = bins[:len(bins) - 1]

    for roi in range(len(ROIs)):
        for each_condition in range(len(conditions_list)):
            amps[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
            amps[roi][each_condition].rename_axis("Amplitude", axis="columns")
            amps_mean[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
            amps_mean[roi][each_condition].rename_axis("Amplitude", axis="columns")
            for b in range(len(bins)):
                amps_mean[roi][each_condition].iloc[b] = amps[roi][each_condition].iloc[b,:].mean()
            #amps_errors[each_condition].iloc[b] = amps[each_condition].iloc[b,:].sem()

    # normalizing to make the effect more clear
    for roi in range(len(ROIs)):
        for each_condition in range(len(conditions_list)):
            amps_mean[roi][each_condition].iloc[:] = ((amps_mean[roi][each_condition].iloc[:] - amps_mean[roi][each_condition].iloc[:].mean()) / amps_mean[roi][each_condition].iloc[:].std())
            #amps_errors[each_condition].iloc[:] = ((amps_errors[each_condition].iloc[:] - amps_errors[each_condition].iloc[:].mean()) / amps_errors[each_condition].iloc[:].std())

    # plotting figures
    for roi in range(len(ROIs)):
        for each_condition in range(len(conditions_list)):
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
            ax.bar(bins, amps_mean[roi][each_condition].iloc[:,0], width=bins[1] - bins[0], bottom=0.0)
            plt.title('Phase Amplitude Coupling')
            plt.savefig('Phase-Amplitude Coupling Circular_%s_BA %s.png' % (conditions_list[each_condition], ROIs[roi]))

    raw_data = []
    df_to_export = []
    for roi in range(len(ROIs)):
        df_to_export.append([])
        for each_condition in range(len(conditions_list)):
            df_to_export[roi].append(pd.concat([amps[roi][each_condition], amps_mean[roi][each_condition]], axis=1))
            df_to_export[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
            df_to_export[roi][each_condition].rename_axis("Amplitude", axis="columns")
    for each_condition in range(len(conditions_list)):
        raw_data.append(pd.ExcelWriter(("%s_Circular Graph Raw Data.xlsx" % conditions_list[each_condition]), engine='xlsxwriter'))
    for each_condition in range(len(conditions_list)):
        for roi in range(len(ROIs)):
            df_to_export[roi][each_condition].to_excel(raw_data[each_condition], sheet_name="BA %s" % ROIs[roi], index_label="Phase Range (Lower Bound)")
    for each_condition in range(len(conditions_list)):
        raw_data[each_condition].save()

    print("\nYour graphs have been created and saved successfully. The raw data has been exported to excel files.")

if print_graphs == 'Y' or print_graphs == 'y':
    if which_graphs == '1':
        makeGraphs()
    if which_graphs == '2':
        makeCirclePlot()
    if which_graphs == '3':
        makeGraphs()
        makeCirclePlot()