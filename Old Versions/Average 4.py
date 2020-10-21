import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import xlsxwriter

conditions_list = []


def askConditions():
    while True:
        try:
            conditions = input("Please enter the conditions in your study, separated by commas (e.g. Controls, Patients).\n")
            conditions_split = [w.strip() for w in conditions.split(',')]
            global conditions_list
            conditions_list = list(map(str, conditions_split))
            break
        except:
            print("\nYour input is not recognized. Please try again.")
            conditions = input("\nPlease enter the conditions in your study, separated by commas (e.g. Controls, Patients).\n")
            conditions_split = conditions.split(",")
            conditions_list = list(map(str, conditions_split))


askConditions()

# Request user to input number of each condition in their experiment to process data appropriately
num_each_condition = []
for con in range(len(conditions_list)):
    while True:
        try:
            number_entered = int(input("How many subjects are in the condition '%s' in your experiment?\n" % conditions_list[con]))
            num_each_condition.append(number_entered)
            break
        except ValueError:
            print("Not a number! Try again.")
            continue

if all(subj == 0 for subj in num_each_condition):
    exit(1)


# class that allows iteration over all objects of a class
class IterSubject(type):
    def __iter__(cls):
        return iter(cls._allSubjects)


# class that defines a generic Subject
class Subject(metaclass=IterSubject):
    _allSubjects = []

    def __init__(self, subjectID):  # initializer (requires Subject ID as an argument when creating an object)
        self._allSubjects.append(self)
        self.subjectID = subjectID

    def setData(self, file):  # function to pass in name of text file and load data into array
        with open(file) as f:
            for i,l in enumerate(f):
                pass
            r = i+1
            c = f.readline()
            cs = [int(n) for n in c.split()]

        self.data = np.zeros(r,cs)

        self.data = np.loadtxt(file)
        backwards = str(file)[::-1]
        backwards = backwards.split('\\')
        forwards = backwards[0][::-1]
        forwards = forwards.split('.')
        self.name = forwards[0]

    def getData(self):  # function that return array
        return self.data

    def printData(self):  # function to print array
        print(self.data)

    def printID(self):  # function print Subject ID
        print(self.subjectID)

    def getName(self):
        return(self.name)

    def trimData(self, new_size_x, new_size_y):
        temp = np.copy(self.data)
        self.data = temp[:new_size_x,:new_size_y]


data_folder = Path(r"//utdfs01/UTD/Dept/BBSResearch/LabCLINT/SandBox/Python toolbox project")

subjects_of_each_condition = []
for each_condition in range(len(conditions_list)):
    subjects_of_each_condition.append([])
    #  list to store a specific group of instances of class Subject
    print("\nData entry for %s:" % conditions_list[each_condition])
    for x in range(
            num_each_condition[each_condition]):  # loop through number of Controls that user inputted and get data files for each Control subject
        file_Location = input(
            "\nPlease enter the path to the data file for Subject %s in '%s' in the folder 'Python toolbox project': \n"% ((str)(x + 1), conditions_list[each_condition]))  # request user to input path to data file; example can be found hard-coded below
        fileName = data_folder / file_Location  # compile full path of data file
        subjects_of_each_condition[each_condition].append(
            Subject("%s %s" % (conditions_list[each_condition], (str)(x + 1))))  # Create a new instance of class Subject and add it to Controls list
        while True:
            try:
                subjects_of_each_condition[each_condition][x].setData(fileName)  # read data from corresponding data file and store in array for that Control
                break
            except:
                print("\nFile not found in the specified path: %s" % fileName)
                file_Location = input(
                    "\nPlease try again. \n")  # request user to input path to data file; example can be found hard-coded below
                fileName = data_folder / file_Location  # compile full path of data file

# Control1 "Sample data/Controls/avv_045_restZT_data-sLorRoiLog.txt"
# Control2 "Sample data/Controls/cak_011_restZT_data-sLorRoiLog.txt"
# Control3 "Sample Data/Controls/nck_020_restZT_data-sLorRoiLog.txt"
# Control4 "Sample Data/Controls/oxs_036_restZT_data-sLorRoiLog.txt"
# Control5 "Sample Data/Controls/sew_023_restZT_data-sLorRoiLog.txt"
# Control6 "Sample Data/Controls/uxk_001_restZT_data-sLorRoiLog.txt"

# Patient1 "Sample data/Patients/ark_016_restZT_data-sLorRoiLog.txt"
# Patient2 "Sample data/Patients/ctc_007_restZT_data-sLorRoiLog.txt"
# Patient3 "Sample data/Patients/cxt_019_restZT_data-sLorRoiLog.txt"
# Patient4 "Sample data/Patients/kjs_037_restZT_data-sLorRoiLog.txt"
# Patient5 "Sample data/Patients/kxm_047_restZT_data-sLorRoiLog.txt"
# Patient6 "Sample data/Patients/mxn_002_restZT_data-sLorRoiLog.txt"
# Patient7 "Sample data/Patients/scj_009_restZT_data-sLorRoiLog.txt"

#Sample data/Controls/avv_045_restZT_data-sLorRoiLog.txt
#Sample data/Controls/cak_011_restZT_data-sLorRoiLog.txt
#Sample data/Patients/ark_016_restZT_data-sLorRoiLog.txt
#Sample data/Patients/ctc_007_restZT_data-sLorRoiLog.txt

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

#Making an excel file and sorting data
def export_to_excel():
    data_organized = []
    sheets = []
    for organized in range(len(conditions_list)):
        data_organized.append(xlsxwriter.Workbook("%s_Organized.xlsx" % conditions_list[organized]))
        sheets.append([])
    for number_of_freq in range(len(chosenFrequencies)):
        for each_condition in range(len(conditions_list)):
            sheets[each_condition].append(data_organized[each_condition].add_worksheet(str(chosenFrequencies[number_of_freq])))
            for row in range(num_each_condition[each_condition]):
                sheets[each_condition][number_of_freq].write(row+1, 0, subjects_of_each_condition[each_condition][row].getName())
                for column in range(np.size(subjects_of_each_condition[each_condition][row].getData(), 1)):
                    if row == 0:
                        sheets[each_condition][number_of_freq].write(row, column + 1,
                                                              'ROI %s' % str(column + 1))
                    sheets[each_condition][number_of_freq].write(row + 1, column + 1,
                                                              subjects_of_each_condition[each_condition][row].getData()[
                                                                  number_of_freq, column])
    for organized in range(len(conditions_list)):
        data_organized[organized].close()
    print("\nYour data has been organized for each condition. Each frequency band is its own sheet and the data is sorted into Subjects x ROIs. The files have been saved in the working directory.")

while True:
    try:
        export_to_excel()
        break
    except IndexError:
        chosenFrequencies = []
        print("\nYour data doesn't have this many frequencies. Please try again.")
        ask_for_frequencies()
        print(chosenFrequencies)
    except PermissionError:
        print("\nThe file you're attempting to create already exists and is currently in use. Please close it and try again.")
        exit(1)

#Making the graph
for each_condition in range(len(conditions_list)):
    for trim in range(num_each_condition[each_condition]):
        subjects_of_each_condition[each_condition][trim].trimData(len(chosenFrequencies), np.size(subjects_of_each_condition[each_condition][trim].getData(),1))

sumMatrices = []
for each_condition in range(len(conditions_list)):
    sumMatrices.append(np.zeros((len(chosenFrequencies), np.size(subjects_of_each_condition[each_condition][0].getData(),1))))
    for subjects in subjects_of_each_condition[each_condition]:
        sumMatrices[each_condition] += np.array(subjects.getData())
averageMatrices = []
for matrix in range(len(sumMatrices)):
    averageMatrices.append(sumMatrices[matrix] / num_each_condition[matrix])
    list(averageMatrices[matrix])
    averageMatrices[matrix].tolist()

width = 0.35

print_graphs = input("\nDo you want any of the data graphed? Enter Y for yes and N for no.\n")
valid_graph_inputs = {'Y', 'y', 'N', 'n'}
while print_graphs not in valid_graph_inputs:
    print_graphs = input("That is not a valid response. Please try again. Enter Y for yes and N for no.")

class graphNumbersExc(Exception):
    def __init__(self):
        Exception.__init__(self)

def makeGraphs():
    ROIs = input("\nPlease enter the numbers of the ROIs that you wanted graphed, in order, separated by commas.\n")
    ROIs_split = ROIs.split(",")
    while True:
        try:
            num_of_graphs = list(map(int, ROIs_split))
            break
        except:
            raise graphNumbersExc

    valid_num_of_graphs = True
    for each_condition in range(len(conditions_list)):
        if len(num_of_graphs) > np.size(subjects_of_each_condition[each_condition][0].getData(),1):
            valid_num_of_graphs = False

    if valid_num_of_graphs:
        for graphs in range(len(num_of_graphs)):
            plotMatrices = []
            for each_condition in range(len(conditions_list)):
                plotMatrices.append([0] * len(chosenFrequencies))
                for x in range(len(chosenFrequencies)):
                    plotMatrices[each_condition][x] = averageMatrices[each_condition][x, num_of_graphs[graphs]-1]
            y_pos = np.arange(0, len(conditions_list)*0.5*len(chosenFrequencies), len(conditions_list)*0.5)
            fig, ax = plt.subplots(figsize=(10, 7))
            plt.figure(graphs + 1)
            for plot in range(len(plotMatrices)):
                if plot == 0:
                    plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, label=chosenFrequencies[plot])
                else:
                    plt.bar([p + width*plot for p in y_pos], plotMatrices[plot], width, alpha=0.5, label=chosenFrequencies[plot])
            ax.set_xticks([p + (0.5 *(len(conditions_list)-1)) * width for p in y_pos])
            ax.set_xticklabels(chosenFrequencies)
            ax.set_ylabel('Average')
            ax.set_title('ROI %d' % num_of_graphs[graphs])
            maxY = 0
            for each_condition in range(len(conditions_list)):
                for x in range(len(chosenFrequencies)):
                    if plotMatrices[each_condition][x] > maxY:
                        maxY = plotMatrices[each_condition][x]
            plt.ylim([0, maxY+2])

            # Adding the legend and showing the plot
            plt.legend(conditions_list, loc='upper right')
            plt.savefig('ROI %d.png' % num_of_graphs[graphs])
        print("\nYour graphs have been created and saved successfully.")
    else:
        raise Exception


if print_graphs == 'Y' or print_graphs == 'y':
    while True:
        try:
            makeGraphs()
            break
        except graphNumbersExc:
            print("\nPlease enter only numbers, separated by commas. Try again.")
            num_of_graphs = []
        except (Exception, IndexError):
            num_of_graphs = []
            print("\nYou don't have this many ROIs in your data. Please try again.")