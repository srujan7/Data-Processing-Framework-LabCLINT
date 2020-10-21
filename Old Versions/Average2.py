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
            print("Not an integer! Try again.")
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
#Controls = []  # list to store a specific group of instances of class Subject
    print("\nData entry for %s:" % conditions_list[each_condition])
    for x in range(
            num_each_condition[each_condition]):  # loop through number of Controls that user inputted and get data files for each Control subject
        file_Location = input(
            "\nPlease enter the path to the data file for Subject %s in '%s' in the folder 'Python toolbox project': \n" % ((str)(x + 1),conditions_list[each_condition]))  # request user to input path to data file; example can be found hard-coded below
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

#Patients = []  # list to store a specific group of instances of class Subject
#print("\nData entry for Patients:")
#for p in range(
        #num_Patients):  # loop through number of Controls that user inputted and get data files for each Control subject
    #file_Location = input(
        #"\nPlease enter the path of the data file for Patient %s in the folder 'Python toolbox project': \n" %
        #(str)(p + 1))  # request user to input path to data file; example can be found hard-coded below
    #fileName = data_folder / file_Location  # compile full path of data file
    #Patients.append(
        #Subject("Patient %s" % (str)(p + 1)))  # Create a new instance of class Subject and add it to Controls list
    #while True:
        #try:
            #Patients[p].setData(fileName)  # read data from corresponding data file and store in array for that Control
            #break
        #except:
            #print("\nFile not found in the specified path: %s" % fileName)
            #file_Location = input(
                #"\nPlease try again. \n")  # request user to input path to data file; example can be found hard-coded below
            #fileName = data_folder / file_Location  # compile full path of data file

# Control1 = Subject("Control 1")
# fileName = data_folder / r"Sample data/Controls/avv_045_restZT_data-sLorRoiLog.txt" #specify file path here
# Control1.setData(fileName)

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

    # while t != "P" and t != "p":
    # choice = input("""
    # A: Delta
    # B: Theta
    # C: Alpha
    # D: Alpha1
    # E: Alpha2
    # F: Alpha3
    # H: Beta
    # I: Beta1
    # J: Beta2
    # K: Beta3
    # L: Gamma
    # M: Low Gamma
    # N: High Gamma
    # O: Mu
    # P: Stop

    # Please enter your choice: \n""")
    # if choice == "A" or choice == "a":
    # frequency.append(1)
    # if choice == "B" or choice == "b":
    # frequency.append(2)
    # if choice == "C" or choice == "c":
    # frequency.append(3)
    # if choice == "D" or choice == "d":
    # frequency.append(4)
    # if choice == "E" or choice == "e":
    # frequency.append(5)
    # if choice == "F" or choice == "f":
    # frequency.append(6)
    # if choice == "G" or choice == "g":
    # frequency.append(7)
    # if choice == "H" or choice == "h":
    # frequency.append(8)
    # if choice == "X" or choice == "x":
    # t = "X" #Stop asking what frequency they're using.
    # print(frequency)
    # print(frequency[0])


# run the function to get frequencies from user
ask_for_frequencies()
print("\nThese are the frequency bands chosen, in order:", chosenFrequencies)

#Making an excel file and sorting data
def export_to_excel():
    controls_organized = xlsxwriter.Workbook("Controls_Organized.xlsx")
    patients_organized = xlsxwriter.Workbook("Patients_Organized.xlsx")
    sheets_controls = []
    sheets_patients = []
    for number_of_freq in range(len(chosenFrequencies)):
        sheets_controls.append(controls_organized.add_worksheet(str(chosenFrequencies[number_of_freq])))
        sheets_patients.append(patients_organized.add_worksheet(str(chosenFrequencies[number_of_freq])))
        for row_controls in range(num_Controls):
            sheets_controls[number_of_freq].write(row_controls+1, 0, Controls[row_controls].getName())
            for column_controls in range(np.size(Controls[row_controls].getData(), 1)):
                if row_controls == 0:
                    sheets_controls[number_of_freq].write(row_controls, column_controls+1, 'ROI %s' % str(column_controls+1))
                sheets_controls[number_of_freq].write(row_controls+1, column_controls+1, Controls[row_controls].getData()[number_of_freq, column_controls])
        for row_patients in range(num_Patients):
            for column_patients in range(np.size(Patients[row_patients].getData(), 1)):
                sheets_patients[number_of_freq].write(row_patients, column_patients, Patients[row_patients].getData()[number_of_freq, column_patients])
    controls_organized.close()
    patients_organized.close()
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
for trim_c in range(
        num_Controls):
    Controls[trim_c].trimData(len(chosenFrequencies), np.size(Controls[0].getData(),1))

for trim_p in range(
        num_Patients):
    Patients[trim_p].trimData(len(chosenFrequencies), np.size(Patients[0].getData(),1))

sumMatrixControls = np.zeros((len(chosenFrequencies), np.size(Controls[0].getData(),1)))
sumMatrixPatients = np.zeros((len(chosenFrequencies), np.size(Patients[0].getData(),1)))
for x in Controls:
    sumMatrixControls += np.array(x.getData())
for y in Patients:
    sumMatrixPatients += np.array(y.getData())

# averageMatrix = ((np.array(Control1.data)) + (np.array(Control2.data)) + (np.array(Control3.data)) + (np.array(Control4.data)) + (np.array(Control5.data)) + (np.array(Control6.data)))/num_Controls
averageMatrixControls = sumMatrixControls / num_Controls  # create an average of all the matrices read from text files
averageMatrixPatients = sumMatrixPatients / num_Patients  # create an average of all the matrices read from text files

list(averageMatrixControls)
averageMatrixControls.tolist()
#print("\nAverage Matrix Controls: \n", averageMatrixControls)

list(averageMatrixPatients)
averageMatrixPatients.tolist()
#print("\nAverage Matrix Patients: \n", averageMatrixPatients)

gap = 0.4

print_graphs = input("\nDo you want any of the data graphed? Enter Y for yes and N for no.\n")
valid_graph_inputs = {'Y', 'y', 'N', 'n'}
while print_graphs not in valid_graph_inputs:
    print_graphs = input("That is not a valid response. Please try again. Enter Y for yes and N for no.")

if print_graphs == 'Y' or print_graphs == 'y':
    ROIs = input("\nPlease enter the numbers of the ROIs that you wanted graphed, in order, separated by commas.\n")
    ROIs_split = ROIs.split(",")
    num_of_graphs = list(map(int, ROIs_split))

    def makeGraphs():
        if(len(num_of_graphs) <= np.size(Controls[0].getData(),1)):
            for graphs in range(len(num_of_graphs)):
                plotMatrixControls = [0] * len(chosenFrequencies)
                plotMatrixPatients = [0] * len(chosenFrequencies)
                for x in range(len(chosenFrequencies)):
                    plotMatrixControls[x] = averageMatrixControls[x, num_of_graphs[graphs]-1]
                    plotMatrixPatients[x] = averageMatrixPatients[x, num_of_graphs[graphs]-1]
                y_pos = np.arange(len(chosenFrequencies))
                plt.figure(graphs + 1)
                plt.bar(y_pos, plotMatrixControls, align='center', alpha=0.5, width=0.4)
                plt.bar(y_pos + gap, plotMatrixPatients, align='center', alpha=0.5, width=0.4)
                plt.xticks(y_pos + (gap / 2), chosenFrequencies)
                plt.ylabel('Average')
                plt.title('ROI %d' % num_of_graphs[graphs])
                plt.savefig('ROI %d.png' % num_of_graphs[graphs])
            print("\nYour graphs have been created and saved successfully.")
        else:
            raise Exception

    while True:
        try:
            makeGraphs()
            break
        except (Exception, IndexError):
            num_of_graphs = []
            print("\nYou don't have this many ROIs in your data. Please try again.")
            ROIs = input("\nPlease enter the numbers of the ROIs that you wanted graphed, in order, separated by commas.\n")
            ROIs_split = ROIs.split(",")
            num_of_graphs = list(map(int, ROIs_split))
