import numpy as np
import pandas as pd
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

connections = []


class ConSubject(Toolbox.Subject):
    def __init__(self, subjectID):
        self.name = None
        self.data = None
        self.orgData = None
        self.Frequencies = []
        super(ConSubject, self).__init__(subjectID)

    def setData(self, fileList, freq):
        data = []
        for file in fileList:
            with open(file) as f:
                data.append(np.genfromtxt(f))
                self.Frequencies = freq
        subj_Data = np.concatenate(data)
        idx = pd.MultiIndex.from_product([self.Frequencies, ROIs], names=('Frequencies', 'ROIs'))
        data_list = pd.DataFrame(data=subj_Data, index=idx, columns=ROIs)
        self.data = data_list

        subject_name = str(fileList[0])
        subject_name = subject_name.split('\\')
        subject_name = subject_name[-1]
        subject_name = subject_name.split('_')
        self.name = subject_name[0]

    def organizeData(self):
        toDF = []
        mask = []
        for x in range(len(ROIs)):
            for t in range(len(ROIs)):
                if t == x:
                    mask.append(True)
                else:
                    mask.append(False)
        indices_to_delete = np.where(mask)
        for number_of_freq in range(len(self.Frequencies)):
            flat = self.data.loc[(self.Frequencies[number_of_freq]), :].values
            flattened = flat.flatten()
            sorted = np.delete(flattened, indices_to_delete)
            toDF.append(sorted)
        self.orgData = pd.DataFrame(data=toDF, index=self.Frequencies, columns=connections)
        print(self.orgData)

    def getOrgData(self):
        return self.orgData


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
        "\nWhat ROIs are you evaluating in your data? Please enter the IDs of the ROIs, for one dimension, from the list below in the order in which they are present in the input files. Enter all ROIs in one line, separated by a space (e.g. 1R 5L 3L 12R).")
    c = inputROIs().split()

    for cv in range(len(c)):
        if c[cv] in ROIsList:
            valid = True
        else:
            valid = False
            break

    # if input is invalid, continue requesting user to input valid ROIs until they do so
    while (not valid):
        print("\nYou have entered invalid ROIs. Please try again.")
        c = []
        c.extend(inputROIs().split())
        for cv in range(len(c)):
            if c[cv] in ROIsList:
                valid = True
            else:
                valid = False

    ROIs.extend(c)


ask_for_rois()

for first in range(len(ROIs)):
    for second in range(len(ROIs)):
        if first == second:
            continue
        connections.append(str(ROIs[first]) + '-' + str(ROIs[second]))

# list to hold the user's desired frequencies, in the order entered
chosenFrequencies = []


# function to take user input for frequency bands used in their experiment
def ask_for_frequencies():
    print(
        "\nWhat frequency bands are you evaluating in your data? Please enter them in the order in which they are present in the input files. Enter all frequency bands in one line (e.g. ABCGK).")

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

    # if input is invalid, continue requesting user to input valid frequencies until they do so
    while (not valid):
        print("\nYou have entered invalid frequencies. Please try again.\n")
        c = list(inputFreq())
        for cv in range(len(c)):
            if c[cv] in frequencyList:
                valid = True
            else:
                valid = False

    # add selected frequency band names into chosenFrequencies list
    for bands in range(len(c)):
        chosenFrequencies.append(frequencyChoice(c[bands]))


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
            for f in range(len(chosenFrequencies)):
                file_Location = input(
                    "\nPlease enter the path to the data file for '%s' for Subject %s of '%s' in the folder 'Data-Reorganization-Lab-CLINT': \n" % (chosenFrequencies[f],
                        (str)(x + 1), conditions_list[
                            each_condition]))  # request user to input path to data folder
                fileFolder = data_folder / file_Location  # compile full path of data folder
                fileNames.append(fileFolder)

            subjects_of_each_condition[each_condition].append(
                ConSubject("%s %s" % (conditions_list[each_condition], (str)(
                    x + 1))))
            while True:
                try:
                    subjects_of_each_condition[each_condition][x].setData(
                        fileNames,
                        chosenFrequencies)
                    break
                except (FileNotFoundError, OSError):
                    print("\nFile not found in the specified path.")
                    print("\nPlease try again.\n")
                    for x in range(
                            num_each_condition[
                                each_condition]):
                        fileNames = []
                        for f in range(len(chosenFrequencies)):
                            file_Location = input(
                                "\nPlease enter the path to the data file for '%s' for Subject %s of '%s' in the folder 'Data-Reorganization-Lab-CLINT': \n" % (
                                chosenFrequencies[f],
                                (str)(x + 1), conditions_list[
                                    each_condition]))  # request user to input path to data folder
                            fileFolder = data_folder / file_Location  # compile full path of data folder
                            fileNames.append(fileFolder)


dataFileEntry()

for each_condition in range(len(conditions_list)):
    for ra in range(num_each_condition[each_condition]):
        subjects_of_each_condition[each_condition][ra].organizeData()


# Making an excel file and sorting data
def export_to_excel():
    data_organized = []
    sheets = []
    for organized in range(len(conditions_list)):
        data_organized.append(xlsxwriter.Workbook("%s_Organized_EffecConn.xlsx" % conditions_list[organized]))
        sheets.append([])
    for number_of_freq in range(len(chosenFrequencies)):
        for each_condition in range(len(conditions_list)):
            sheets[each_condition].append(
                data_organized[each_condition].add_worksheet(str(chosenFrequencies[number_of_freq])))
            subject_counter = 0
            for subject in range(num_each_condition[each_condition] + 1):
                if subject == 0:
                    sheets[each_condition][number_of_freq].write_row(0, 1, connections)
                else:
                    sheets[each_condition][number_of_freq].write(subject, 0, subjects_of_each_condition[each_condition][
                        subject_counter].getName())
                    sheets[each_condition][number_of_freq].write_row(subject, 1,
                                                                     subjects_of_each_condition[each_condition][
                                                                         subject_counter].getOrgData().iloc[
                                                                         number_of_freq])
                    subject_counter += 1
    for organized in range(len(conditions_list)):
        data_organized[organized].close()
    print(
        "\nYour data has been organized for each condition. Each frequency band is its own sheet and the data is sorted into Subjects x ROIs. The files have been saved in the working directory.")


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
    averageMatrices.append([])
    for matrix in range(len(chosenFrequencies)):
        idx = []
        for subject in range(num_each_condition[each_condition]):
            idx.append("Subject " + str(subject + 1))
        averageMatrices[each_condition].append(pd.DataFrame(index=idx, columns=connections))
        for subject in range(num_each_condition[each_condition]):
            averageMatrices[each_condition][matrix].iloc[subject] = \
            subjects_of_each_condition[each_condition][subject].getOrgData().iloc[matrix]

width = 0.35

print_graphs = input("\nDo you want any of the data graphed? Enter Y for yes and N for no.\n")
valid_graph_inputs = {'Y', 'y', 'N', 'n'}
while print_graphs not in valid_graph_inputs:
    print_graphs = input("That is not a valid response. Please try again. Enter Y for yes and N for no.")


class graphNumbersExc(Exception):
    def __init__(self):
        Exception.__init__(self)


def makeGraphs():
    ROIs = input("\nPlease enter the ROI connections that you wanted graphed, separated by spaces. Ex: 1L-1R 2L-3L\n")
    ROIs_split = ROIs.split()
    num_of_graphs = list(map(str, ROIs_split))

    while True:
        try:
            num_of_graphs = list(map(str, ROIs_split))
            break
        except:
            raise graphNumbersExc

    valid_num_of_graphs = True
    for each_condition in range(len(conditions_list)):
        if len(num_of_graphs) > len(subjects_of_each_condition[each_condition][0].getOrgData().columns):
            valid_num_of_graphs = False

    if valid_num_of_graphs:
        for graphs in range(len(num_of_graphs)):
            plotMatrices = []
            for each_condition in range(len(conditions_list)):
                plotMatrices.append([0] * len(chosenFrequencies))
                for x in range(len(chosenFrequencies)):
                    plotMatrices[each_condition][x] = averageMatrices[each_condition][x][
                        str(num_of_graphs[graphs])].mean()
            y_pos = np.arange(0, len(conditions_list) * 0.5 * len(chosenFrequencies), len(conditions_list) * 0.5)
            fig, ax = plt.subplots(figsize=(10, 7))
            plt.figure(graphs + 1)
            for plot in range(len(plotMatrices)):
                if plot == 0:
                    plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, label=chosenFrequencies[plot])
                else:
                    plt.bar([p + width * plot for p in y_pos], plotMatrices[plot], width, alpha=0.5,
                            label=chosenFrequencies[plot])
            ax.set_xticks([p + (0.5 * (len(conditions_list) - 1)) * width for p in y_pos])
            ax.set_xticklabels(chosenFrequencies)
            ax.set_ylabel('Connectivity')
            ax.set_title('ROIs %s' % num_of_graphs[graphs])
            maxY = 0
            for each_condition in range(len(conditions_list)):
                for x in range(len(chosenFrequencies)):
                    if plotMatrices[each_condition][x] > maxY:
                        maxY = plotMatrices[each_condition][x]
            if maxY < 2:
                plt.ylim([0, maxY * 2])
            else:
                plt.ylim([0, maxY + 2])

            # Adding the legend and showing the plot
            plt.legend(conditions_list, loc='upper right')
            plt.savefig('EffecConn ROIs %s.png' % num_of_graphs[graphs])
        print("\nYour graphs have been created and saved successfully.")
    else:
        raise Exception


if print_graphs == 'Y' or print_graphs == 'y':
    while True:
        try:
            makeGraphs()
            break
        except graphNumbersExc:
            print("\nPlease enter only connections of ROI IDs, separated by commas. Try again.")
            num_of_graphs = []
        except IndexError:
            num_of_graphs = []
            print("\nYou don't have this many ROIs in your data. Please try again.")