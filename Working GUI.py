import tkinter as tk
from tkinter import filedialog as fd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import pandas as pd
from pathlib import Path
import sys
from os.path import dirname, join, abspath, os
import scipy as sp
import scipy.stats

sys.path.insert(0, abspath(join(dirname(__file__), '.') + "\Toolbox"))
import Toolbox

LARGE_FONT = ("Verdana", 12)
ROIs = []
numROIs = 0
connections = []

class ConSubject(Toolbox.Subject):
    def __init__(self, subjectID):
        self.name = None
        self.data = None
        self.orgData = None
        self.Frequencies = []
        super(ConSubject, self).__init__(subjectID)

    def setData(self, file):
        #Frequencies = []

        with open(file) as f:
            subj_Data = np.genfromtxt(f, skip_header=14)
            num_of_freq = 0
            for line in range(0, len(subj_Data), 84):
                num_of_freq += 1
                self.Frequencies.append('Frequency ' + str(num_of_freq))
        idx = pd.MultiIndex.from_product([self.Frequencies, ROIs], names=('Frequencies', 'ROIs'))
        data_list = pd.DataFrame(data=subj_Data, index=idx, columns=ROIs)
        self.data = data_list
        # print(self.data)

        subject_name = str(file)
        subject_name = subject_name.split('\\')
        subject_name = subject_name[-1]
        subject_name = subject_name.split('_')
        self.name = subject_name[0] + '_' + subject_name[1]

    def organizeData(self):
        toDF = []
        mask = []
        for x in range(len(ROIs)):
            for t in range(x+1):
                mask.append(True)
            for f in range(len(ROIs)-(x+1)):
                mask.append(False)
        indices_to_delete = np.where(mask)
        for number_of_freq in range(len(self.Frequencies)):
            flat = self.data.loc[(self.Frequencies[number_of_freq]), :].values
            flattened = flat.flatten()
            sorted = np.delete(flattened, indices_to_delete)
            toDF.append(sorted)
            # freq_loc = 'Frequency ' + str(number_of_freq + 1)
                #ROI_loc_row = ROIs[row + 1]
                #ROI_loc_col = ROIs[row + 2]
                # print(subjects_of_each_condition[each_condition][ra].getData().loc[(freq_loc, ROI_loc_row), ROI_loc_col::])
                #self.orgData.append(self.data.loc[(self.Frequencies[number_of_freq], ROI_loc_row), ROI_loc_col::])

        #row_index = pd.MultiIndex.from_product([self.Frequencies, ROIs], names=('Frequencies', 'ROIs'))
        self.orgData = pd.DataFrame(data=toDF, index=self.Frequencies, columns=connections)
        #print(self.orgData)
    def getOrgData(self):
        return self.orgData


class ConSubject2(Toolbox.Subject):
    def __init__(self, subjectID):
        self.name = None
        self.data = None
        self.orgData = None
        self.Frequencies = []
        super(ConSubject2, self).__init__(subjectID)

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
        self.name = subject_name[0] #+ '_' + subject_name[1]

    def organizeData(self):
        toDF = []
        mask = []
        for x in range(len(ROIs)):
            for t in range(x+1):
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
        #print(self.orgData)

    def getOrgData(self):
        return self.orgData


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
        data_list = pd.DataFrame(data=subj_Data, index=idx, columns=self.chosenFrequencies)
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


def circCorr(ang, line):
    n = len(ang)
    rxs = sp.stats.pearsonr(line, np.sin(ang))
    rxs = rxs[0]
    rxc = sp.stats.pearsonr(line, np.cos(ang))
    rxc = rxc[0]
    rcs = sp.stats.pearsonr(np.sin(ang), np.cos(ang))
    rcs = rcs[0]
    rho = np.sqrt((rxc**2 + rxs**2 - 2*rxc*rxs*rcs)/(1-rcs**2))
    r_2 = rho**2
    pval = 1 - sp.stats.chi2.cdf(n*(rho**2), 1)
    standard_error = np.sqrt((1-r_2)/(n-2))

    return rho, pval, r_2, standard_error


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, AveragePage, FunctionalPage, EffectiveConnectivity, PhaseAmp):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=3)
        label2 = tk.Label(self, text="What kind of data are you working with?", font=LARGE_FONT)
        label2.grid(row=1, column=0, columnspan=3)

        self.menubar = tk.Menu(controller)
        self.menubar.add_command(label="Home", command=lambda: controller.show_frame(HomePage))
        self.menubar.add_command(label="Quit", command=quit)

        controller.config(menu=self.menubar)

        button = tk.Button(self, text="Average ROIs", font=LARGE_FONT,
                           command=lambda: controller.show_frame(AveragePage))
        button.grid(column=0, row=2)
        functionalButton = tk.Button(self, text="Functional Connectivity", font=LARGE_FONT,
                                     command=lambda: controller.show_frame(FunctionalPage))
        functionalButton.grid(column=1, row=2)

        effectiveButton = tk.Button(self, text="Effective Connectivity", font=LARGE_FONT,
                                    command=lambda: controller.show_frame(EffectiveConnectivity))
        effectiveButton.grid(column=0, row=3)

        phaseButton = tk.Button(self, text="Phase-Amp Coupling", font=LARGE_FONT,
                                command=lambda: controller.show_frame(PhaseAmp))
        phaseButton.grid(column=1, row=3)


class AveragePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.averageDataLabel = tk.Label(self, text="Average Data", font=LARGE_FONT)
        self.averageDataLabel.grid(row=0, column=0)
        self.howManyConditionsLabel = tk.Label(self, text="How many conditions are in your study?")
        self.howManyConditionsLabel.grid(row=1, column=0)
        self.getNumberOfConditions = tk.Entry(self)
        self.getNumberOfConditions.grid(row=2, column=0)
        self.submitNumConButton = tk.Button(self, text="Submit", command=lambda: self.GetNumberConditions(controller))
        self.submitNumConButton.grid(row=2, column=1)
        self.numberConditions = 0

    def GetNumberConditions(self, parent):
        self.submitNumConButton.grid_remove()
        try:
            self.numberConditions = int(self.getNumberOfConditions.get())
            if self.numberConditions == 1:
                correctLabel = tk.Label(self, text=str(self.numberConditions) + " Condition. Is this correct?")
                yesButton = tk.Button(self, text="Yes", command=lambda: self.AveragePartTwo(correctLabel, yesButton,
                                                                                            noButton, parent),
                                      height=2, width=10)
                noButton = tk.Button(self, text="No", command=lambda: self.reset(correctLabel, yesButton, noButton),
                                     height=2, width=10)
                correctLabel.grid(row=3, column=0)
                yesButton.grid(row=3, column=1)
                noButton.grid(row=3, column=2)
                menubar = tk.Menu(parent)
                menubar.add_command(label="Home", command=lambda: self.goHome(correctLabel, yesButton,
                                                                              noButton, parent))
                menubar.add_command(label="Quit", command=quit)

                parent.config(menu=menubar)
            elif self.numberConditions <= 0:
                retryLabel = tk.Label(self, text="You need at least 1 condition, please re-enter the number of "
                                                 "conditions.")
                continueButton = tk.Button(self, text="Continue", command=lambda: self.reset1(retryLabel,
                                                                                              continueButton),
                                           height=2, width=10)
                retryLabel.grid(row=3, column=0)
                continueButton.grid(row=3, column=1)
                menubar = tk.Menu(parent)
                menubar.add_command(label="Home", command=lambda: self.goHome2(retryLabel, continueButton, parent))
                menubar.add_command(label="Quit", command=quit)

                parent.config(menu=menubar)
            else:
                correctLabel = tk.Label(self, text=str(self.numberConditions) + " Conditions. Is this correct?")
                yesButton = tk.Button(self, text="Yes", command=lambda: self.AveragePartTwo(correctLabel, yesButton,
                                                                                            noButton, parent),
                                      height=2, width=10)
                noButton = tk.Button(self, text="No", command=lambda: self.reset(correctLabel, yesButton, noButton),
                                     height=2, width=10)
                correctLabel.grid(row=3, column=0)
                yesButton.grid(row=3, column=1)
                noButton.grid(row=3, column=2)
                menubar = tk.Menu(parent)
                menubar.add_command(label="Home", command=lambda: self.goHome(correctLabel, yesButton, noButton,
                                                                              parent))
                menubar.add_command(label="Quit", command=quit)

                parent.config(menu=menubar)
        except:
            retryLabel = tk.Label(self, text="You must enter an integer number")
            continueButton = tk.Button(self, text="Continue", command=lambda: self.reset1(retryLabel, continueButton),
                                       height=2, width=10)
            retryLabel.grid(row=3, column=0)
            continueButton.grid(row=3, column=1)
            menubar = tk.Menu(parent)
            menubar.add_command(label="Home", command=lambda: self.goHome2(retryLabel, continueButton, parent))
            menubar.add_command(label="Quit", command=quit)

            parent.config(menu=menubar)

    def reset(self, label, but, but2):
        label.grid_forget()
        but.grid_forget()
        but2.grid_forget()
        self.getNumberOfConditions.delete(0, 'end')
        self.submitNumConButton.grid()

    def reset1(self, label, but):
        label.grid_forget()
        but.grid_forget()
        self.getNumberOfConditions.delete(0, 'end')
        self.submitNumConButton.grid()

    def AveragePartTwo(self, label, but, but2, parent):
        menubar = tk.Menu(parent)
        label.grid_forget()
        but.grid_forget()
        but2.grid_forget()
        self.getNumberOfConditions.grid_forget()
        self.howManyConditionsLabel.grid_forget()
        self.submitNumConButton.grid_forget()
        nameOfConditionsLabel = tk.Label(self, text="Please enter the names of the condition(s) in your study:")
        nameOfConditionsLabel.grid(row=1, column=0)
        blankLabel = tk.Label(self, text=" ")
        blankLabel.grid(row=0, column=1)
        getConditionNamesList = []
        for x in range(0, self.numberConditions):
            getConditionNames = tk.Entry(self)
            getConditionNames.insert(0, "Condition " + str(x+1))
            getConditionNames.grid(row=x+2, column=0)
            getConditionNamesList.append(getConditionNames)
        conditionNameSubmitButton = tk.Button(text="Submit", command=lambda: self.AveragePartThree(
            nameOfConditionsLabel, conditionNameSubmitButton, getConditionNamesList, blankLabel, parent), height=2,
                                              width=10)
        conditionNameSubmitButton.grid(row=2, column=0)
        menubar.add_command(label="Home", command=lambda: self.goHome3(nameOfConditionsLabel, getConditionNames,
                                                                       parent))
        menubar.add_command(label="Quit", command=quit)
        parent.config(menu=menubar)

    def AveragePartThree(self, label, button, entryList, blank, parent):
        self.listOfConditions = []
        self.averageDataLabel.grid_forget()
        blank.grid_forget()
        label.grid_forget()
        button.grid_forget()
        menubar = tk.Menu(parent)
        subjectsInConditionLabel = tk.Label(text="How many subjects are in each condition?")
        subjectsInConditionLabel.grid(row=0)
        subjectsInConditionList = []
        conditionLabelList = []
        for ent in entryList:
            self.listOfConditions.append(ent.get())
            ent.grid_forget()
        for x in range(0, len(entryList)):
            getConditionNumber = tk.Entry()
            getConditionNumber.grid(row=x+1, column=1)
            subjectsInConditionList.append(getConditionNumber)
            conditionLabel = tk.Label(text=self.listOfConditions[x]+":")
            conditionLabel.grid(row=x+1, column=0)
            conditionLabelList.append(conditionLabel)
        continueToFourButton = tk.Button(text="Submit", command=lambda: self.
                                         AveragePartFour(subjectsInConditionLabel, continueToFourButton,
                                                         subjectsInConditionList, conditionLabelList, parent))
        continueToFourButton.grid()
        #menubar.add_command(label="Home", command=lambda: self.goHome(subjectsInConditionLabel, conditionNameLabel,
                                                                      #subjectsInCondition, parent))
        menubar.add_command(label="Quit", command=quit)
        parent.config(menu=menubar)

    def AveragePartFour(self, label1, submitButton, entryList, labelList, parent):
        #File location
        label1.grid_forget()
        submitButton.grid_forget()
        self.numberOfSubjectsList = []
        for ent in entryList:
            self.numberOfSubjectsList.append(ent.get())
            ent.grid_forget()
        for lab in labelList:
            lab.grid_forget()
        lookForLocationLabel = tk.Label(text="Please select the location of your subjects' data files")
        lookForLocationLabel.grid_location(0, 0)
        lookForLocationLabel.grid(row=0, column=0)
        browseButton = tk.Button(text="Browse", command=lambda: self.getSubjectFiles(lookForLocationLabel, browseButton,
                                                                                     parent))
        browseButton.grid()
        menubar = tk.Menu(parent)
        menubar.add_command(label="Quit", command=quit)
        parent.config(menu=menubar)

    def getSubjectFiles(self, label, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.subjectsInEachCondition = []
        for each_condition in range(len(self.listOfConditions)):
            self.subjectsInEachCondition.append([])
            fileSelectLabel = tk.Label(text='Please select all of the subjects\' files in the condition "' +
                                            self.listOfConditions[each_condition] + '" by control clicking')
            fileSelectLabel.grid(row=0, column=0)
            fileLocation = fd.askopenfilenames(parent=parent, title="Select the files in the condition " +
                                                                    self.listOfConditions[each_condition])
            self.fileLocationList = list(fileLocation)
            for x in range(int(self.numberOfSubjectsList[each_condition])):
                self.subjectsInEachCondition[each_condition].append(Toolbox.Subject("%s %s" % (self.listOfConditions[
                                                                                           each_condition], str(x+1))))
                self.subjectsInEachCondition[each_condition][x].setData(self.fileLocationList[x])
                fileSelectLabel.grid_forget()
        buttone = tk.Button(text="Continue", command=lambda: self.getFrequencies(buttone))
        buttone.grid(row=0, column=0)

    def getFrequencies(self, button):
        button.grid_forget()
        getFrequenciesLabel = tk.Label(text="Which frequency bands are you evaluating in your data?")
        getFrequenciesLabel.grid(column=0, row=0)
        getFrequenciesListBox = tk.Listbox(selectmode="multiple", height=14)
        getFrequenciesListBox.insert(1, "Delta")
        getFrequenciesListBox.insert(2, "Theta")
        getFrequenciesListBox.insert(3, "Alpha")
        getFrequenciesListBox.insert(4, "Alpha1")
        getFrequenciesListBox.insert(5, "Alpha2")
        getFrequenciesListBox.insert(6, "Alpha3")
        getFrequenciesListBox.insert(7, "Beta")
        getFrequenciesListBox.insert(8, "Beta1")
        getFrequenciesListBox.insert(9, "Beta2")
        getFrequenciesListBox.insert(10, "Beta3")
        getFrequenciesListBox.insert(11, "Gamma")
        getFrequenciesListBox.insert(12, "Low Gamma")
        getFrequenciesListBox.insert(13, "High Gamma")
        getFrequenciesListBox.insert(14, "Mu")
        getFrequenciesListBox.grid()
        continueButton = tk.Button(text="Continue", command=lambda: self.organizeAndExport(getFrequenciesLabel,
                                                                                           getFrequenciesListBox,
                                                                                           continueButton))
        continueButton.grid()

    def organizeAndExport(self, label, listBox, button1):
        label.grid_forget()
        button1.grid_forget()
        indexNumbers = listBox.curselection()
        self.frequencyList = []
        for x in range(0, len(indexNumbers)):
            self.frequencyList.append(listBox.get(indexNumbers[x]))
        listBox.grid_forget()
        data_organized = []
        sheets = []
        for organized in range(len(self.listOfConditions)):
            data_organized.append(xlsxwriter.Workbook("%s_Organized.xlsx" % self.listOfConditions[organized]))
            sheets.append([])
        for number_of_freq in range(len(self.frequencyList)):
            for each_condition in range(len(self.listOfConditions)):
                sheets[each_condition].append(data_organized[each_condition].add_worksheet(str(self.frequencyList
                                                                                               [number_of_freq])))
                for row in range(int(self.numberOfSubjectsList[each_condition])):
                    sheets[each_condition][number_of_freq].write(row+1, 0, self.subjectsInEachCondition[each_condition][
                        row].getName())
                    for column in range(np.size(self.subjectsInEachCondition[each_condition][row].getData(), 1)):
                        if row == 0:
                            sheets[each_condition][number_of_freq].write(row, column + 1, 'ROI %s' % str(column + 1))
                        sheets[each_condition][number_of_freq].write(row + 1, column + 1, self.subjectsInEachCondition[
                            each_condition][row].getData()[number_of_freq, column])
        for organized in range(len(self.listOfConditions)):
            data_organized[organized].close()
        finishedLabel = tk.Label(text="Your data has been organized for each condition. Each frequency band is its own "
                                      "\nsheet and the data is sorted into Subjects x ROIs. The files have been saved i"
                                      "n\nthe working directory.")
        finishedLabel.grid(row=0, column=0)
        makeGraphsButton = tk.Button(text="Continue", command=lambda: self.askToGraph(finishedLabel, makeGraphsButton))
        makeGraphsButton.grid()

    def askToGraph(self, label, button):
        label.grid_forget()
        button.grid_forget()
        askIfGraph = tk.Label(text="Would you like your data graphed?")
        askIfGraph.grid(row=0, column=0)
        yesGraphButton = tk.Button(text="Yes", command=lambda: self.getROIs(askIfGraph, yesGraphButton,
                                                                               noGraphButton))
        yesGraphButton.grid(row=1, column=0)
        noGraphButton = tk.Button(text="No")
        noGraphButton.grid(row=1, column=1)

    def getROIs(self, label, button1, button2):
        label.grid_forget()
        button1.grid_forget()
        button2.grid_forget()
        askNumberROIs = tk.Label(text="Please enter the number of ROIs that you want graphed, in order, separated by co"
                                      "mmas")
        askNumberROIs.grid(row=0, column=0)
        ROIEntry = tk.Entry()
        ROIEntry.grid(row=1, column=0)
        submitROIsButton = tk.Button(text="Submit", command=lambda: self.makeGraphs(askNumberROIs, ROIEntry,
                                                                                    submitROIsButton))
        submitROIsButton.grid(row=1, column=1)

    def makeGraphs(self, label, entry, button):
        label.grid_forget()
        ROIs = entry.get()
        entry.grid_forget()
        button.grid_forget()
        for each_condition in range(len(self.listOfConditions)):
            for trim in range(int(self.numberOfSubjectsList[each_condition])):
                self.subjectsInEachCondition[each_condition][trim].trimData(len(self.frequencyList), np.size(
                    self.subjectsInEachCondition[each_condition][trim].getData(), 1))
        sumMatrices = []
        for each_condition in range(len(self.listOfConditions)):
            sumMatrices.append(np.zeros((len(self.frequencyList), np.size(self.subjectsInEachCondition[
                                                                                     each_condition][0].getData(), 1))))
            for subjects in self.subjectsInEachCondition[each_condition]:
                sumMatrices[each_condition] += np.array(subjects.getData())
        averageMatrices = []
        for matrix in range(len(sumMatrices)):
            averageMatrices.append(sumMatrices[matrix] / int(self.numberOfSubjectsList[matrix]))
            list(averageMatrices[matrix])
            averageMatrices[matrix].tolist()
        width = 0.35
        ROIs_split = ROIs.split(",")
        num_of_graphs = list(map(int, ROIs_split))
        valid_num_of_graphs = True
        for each_condition in range(len(self.listOfConditions)):
            if len(num_of_graphs) > np.size(self.subjectsInEachCondition[each_condition][0].getData(), 1):
                valid_num_of_graphs = False
        if valid_num_of_graphs:
            for graphs in range(len(num_of_graphs)):
                plotMatrices = []
                for each_condition in range(len(self.listOfConditions)):
                    plotMatrices.append([0] * len(self.frequencyList))
                    for x in range(len(self.frequencyList)):
                        plotMatrices[each_condition][x] = averageMatrices[each_condition][x, num_of_graphs[graphs]-1]
                y_pos = np.arange(0, len(self.listOfConditions)*0.5*len(self.frequencyList), len(
                    self.listOfConditions)*0.5)
                fig, ax = plt.subplots(figsize=(10, 7))
                plt.figure(graphs + 1)
                for plot in range(len(plotMatrices)):
                    if plot == 0:
                        plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, label=self.frequencyList[plot])
                    else:
                        plt.bar([p + width*plot for p in y_pos], plotMatrices[plot], width, alpha=0.5, label=self.
                                frequencyList[plot])
                ax.set_xticks([p + (0.5 * (len(self.listOfConditions)-1)) * width for p in y_pos])
                ax.set_xticklabels(self.frequencyList)
                ax.set_ylabel("Average")
                ax.set_title("ROI %d" % num_of_graphs[graphs])
                maxY = 0
                for each_condition in range(len(self.listOfConditions)):
                    for x in range(len(self.frequencyList)):
                        if plotMatrices[each_condition][x] > maxY:
                            maxY = plotMatrices[each_condition][x]
                plt.ylim([0, maxY+2])
                plt.legend(self.listOfConditions, loc='upper right')
                plt.savefig('ROI %d.png' % num_of_graphs[graphs])
            graphsPrintedLabel = tk.Label(text="Your graphs have been created and saved successfully")
            graphsPrintedLabel.grid(column=0, row=0)
            finishButton = tk.Button(text="Finish", command=lambda: quit())
            finishButton.grid()

    def goHome(self, label, but, but2, parent):
        label.grid_remove()
        but.grid_remove()
        but2.grid_remove()
        self.getNumberOfConditions.delete(0, 'end')
        parent.show_frame(HomePage)
        self.submitNumConButton.grid()

    def goHome2(self, label, but, parent):
        label.grid_remove()
        but.grid_remove()
        self.getNumberOfConditions.delete(0, 'end')
        parent.show_frame(HomePage)
        self.submitNumConButton.grid()

    def goHome3(self, label, entry, parent):
        label.grid_forget()
        entry.grid_forget()
        self.howManyConditionsLabel.grid(row=1, column=0)
        self.getNumberOfConditions.grid(row=2, column=0)
        self.submitNumConButton.grid(row=2, column=1)
        parent.show_frame(HomePage)

class FunctionalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.FunctionalDataLabel = tk.Label(self, text="Functional Connectivity", font=LARGE_FONT)
        self.FunctionalDataLabel.grid(row=0, column=0, columnspan=3)
        howManyConditionsLabel = tk.Label(self, text="How many conditions are in your study?")
        howManyConditionsLabel.grid(row=1, column=0)
        getNumberOfConditions = tk.Entry(self)
        getNumberOfConditions.grid(row=2, column=0)
        submitButton = tk.Button(self, text="Submit", command=lambda: self.getConditionNames(howManyConditionsLabel,
                                                                                             getNumberOfConditions,
                                                                                             submitButton, parent))
        submitButton.grid(row=2, column=1)
        self.numberConditions = 0

    def getConditionNames(self, label, entry, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.numberConditions = int(entry.get())
        entry.grid_forget()
        getConditionListLabel = tk.Label(self, text="Please enter the names of the condition(s) in your study:")
        getConditionListLabel.grid(row=1, column=0)
        getConditionNamesList = []
        for x in range(0, self.numberConditions):
            getConditionNames = tk.Entry(self)
            getConditionNames.insert(0, "Condition " + str(x+1))
            getConditionNames.grid(row=x+2, column=0)
            getConditionNamesList.append(getConditionNames)
        submitButton = tk.Button(text="Submit", command=lambda: self.FunctionalPartThree(getConditionListLabel,
                                                                                         submitButton,
                                                                                         getConditionNamesList, parent),
                                 height=2, width=10)
        submitButton.grid(row=2, column=0)

    def FunctionalPartThree(self, label, button, entryList, parent):
        self.conditions_list = []
        label.grid_forget()
        button.grid_forget()
        for ent in entryList:
            self.conditions_list.append(ent.get())
            ent.grid_forget()
        subjectsInConditionLabel = tk.Label(text="How many subjects are in each condition?")
        subjectsInConditionLabel.grid(row=0, column=0)
        subjectsInConditionList = []
        conditionLabelList = []
        for x in range(0, len(entryList)):
            conditionLabel = tk.Label(text=self.conditions_list[x]+":")
            conditionLabel.grid(row=x+1, column=0)
            getSubjectNumber = tk.Entry()
            getSubjectNumber.grid(row=x+1, column=1)
            subjectsInConditionList.append(getSubjectNumber)
            conditionLabelList.append(conditionLabel)
        continueButton = tk.Button(text="Submit", command=lambda: self.FunctionalPartFour(
            subjectsInConditionLabel, continueButton, subjectsInConditionList, conditionLabelList, parent))
        continueButton.grid()

    def FunctionalPartFour(self, label, button, entryList, labelList, parent):
        label.grid_forget()
        button.grid_forget()
        self.num_each_condition = []
        for ent in entryList:
            self.num_each_condition.append(ent.get())
            ent.grid_forget()
        for lab in labelList:
            lab.grid_forget()
        howManyROIsLabel = tk.Label(text="How many ROIs are present in your data? (Max: 84)")
        howManyROIsLabel.grid(row=0, column=0)
        getNumROIs = tk.Entry()
        getNumROIs.grid(row=1, column=0)
        submitButton = tk.Button(text="Submit", command=lambda: self.FunctionalPartFive(howManyROIsLabel, getNumROIs,
                                                                                        submitButton, parent))
        submitButton.grid(row=1, column=1)

    def FunctionalPartFive(self, label, entry, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.numROIs = int(entry.get())
        entry.grid_forget()
        pickROIsLabel = tk.Label(text="Please choose all of the ROIs in your data:")
        pickROIsLabel.grid(column=0, row=0, columnspan=2)
        leftLabel = tk.Label(text="Left sided ROIs")
        leftLabel.grid(row=1, column=0)
        rightLabel = tk.Label(text="Right sided ROIs")
        rightLabel.grid(row=1, column=1)
        getROIsListBoxLeft = tk.Listbox(selectmode="extended", width=45, exportselection=0)
        getROIsListBoxLeft.insert(1, "1L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(2, "2L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(3, "3L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(4, "4L. Primary motor cortex")
        getROIsListBoxLeft.insert(5, "5L. Somatosensory association cortex")
        getROIsListBoxLeft.insert(6, "6L. Premotor and supplementary motor cortex")
        getROIsListBoxLeft.insert(7, "7L. Visuo-motor cortex")
        getROIsListBoxLeft.insert(8, "8L. Frontal eye fields")
        getROIsListBoxLeft.insert(9, "9L. Dorsolateral prefrontal cortex")
        getROIsListBoxLeft.insert(10, "10L. Anterior prefrontal cortex")
        getROIsListBoxLeft.insert(11, "11L. Orbitofrontal area")
        getROIsListBoxLeft.insert(12, "13L. Insular Cortex")
        getROIsListBoxLeft.insert(13, "17L. Primary visual cortex (V1)")
        getROIsListBoxLeft.insert(14, "18L. Secondary visual cortex (V2)")
        getROIsListBoxLeft.insert(15, "19L. Associative visual cortex (V3, V4, V5)")
        getROIsListBoxLeft.insert(16, "20L. Inferior temporal gyrus")
        getROIsListBoxLeft.insert(17, "21L. Middle temporal gyrus")
        getROIsListBoxLeft.insert(18, "22L. Superior temporal gyrus")
        getROIsListBoxLeft.insert(19, "23L. Ventral posterior cingulate cortex")
        getROIsListBoxLeft.insert(20, "24L. Ventral anterior cingulate cortex")
        getROIsListBoxLeft.insert(21, "25L. Subgenual area")
        getROIsListBoxLeft.insert(22, "27L. Piriform cortex")
        getROIsListBoxLeft.insert(23, "28L. Ventral entorhinal cortex")
        getROIsListBoxLeft.insert(24, "29L. Retrosplenial cingulate cortex")
        getROIsListBoxLeft.insert(25, "30L. Retrosplenial cerebral cortex")
        getROIsListBoxLeft.insert(26, "31L. Dorsal posterior cingulate cortex")
        getROIsListBoxLeft.insert(27, "32L. Dorsal anterior cingulate cortex")
        getROIsListBoxLeft.insert(28, "33L. Cingulate cerebral cortex")
        getROIsListBoxLeft.insert(29, "34L. Dorsal entorhinal cortex")
        getROIsListBoxLeft.insert(30, "35L. Perirhinal cortex")
        getROIsListBoxLeft.insert(31, "36L. Ectorhinal area (Temporal cerebral cortex)")
        getROIsListBoxLeft.insert(32, "37L. Fusiform gyrus")
        getROIsListBoxLeft.insert(33, "38L. Temporopolar area")
        getROIsListBoxLeft.insert(34, "39L. Angular gyrus")
        getROIsListBoxLeft.insert(35, "40L. Supramarginal gyrus")
        getROIsListBoxLeft.insert(36, "41L. Auditory cortex")
        getROIsListBoxLeft.insert(37, "42L. Auditory cortex")
        getROIsListBoxLeft.insert(38, "43L. Primary gustatory cortex")
        getROIsListBoxLeft.insert(39, "44L. Pars opercularis")
        getROIsListBoxLeft.insert(40, "45L. Pars tiangularis")
        getROIsListBoxLeft.insert(41, "46L. Dorsolateral prefrontal cortex")
        getROIsListBoxLeft.insert(42, "47L. Pars orbitalis")
        getROIsListBoxLeft.grid(row=2, column=0)
        getROIsListBoxRight = tk.Listbox(selectmode="extended", width=45, exportselection=0)
        getROIsListBoxRight.insert(43, "1R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(44, "2R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(45, "3R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(46, "4R. Primary motor cortex")
        getROIsListBoxRight.insert(47, "5R. Somatosensory association cortex")
        getROIsListBoxRight.insert(48, "6R. Premotor and supplementary motor cortex")
        getROIsListBoxRight.insert(49, "7R. Visuo-motor cortex")
        getROIsListBoxRight.insert(50, "8R. Frontal eye fields")
        getROIsListBoxRight.insert(51, "9R. Dorsolateral prefrontal cortex")
        getROIsListBoxRight.insert(52, "10R. Anterior prefrontal cortex")
        getROIsListBoxRight.insert(53, "11R. Orbitofrontal area")
        getROIsListBoxRight.insert(54, "13R. Insular Cortex")
        getROIsListBoxRight.insert(55, "17R. Primary visual cortex (V1)")
        getROIsListBoxRight.insert(56, "18R. Secondary visual cortex (V2)")
        getROIsListBoxRight.insert(57, "19R. Associative visual cortex (V3, V4, V5)")
        getROIsListBoxRight.insert(58, "20R. Inferior temporal gyrus")
        getROIsListBoxRight.insert(59, "21R. Middle temporal gyrus")
        getROIsListBoxRight.insert(60, "22R. Superior temporal gyrus")
        getROIsListBoxRight.insert(61, "23R. Ventral posterior cingulate cortex")
        getROIsListBoxRight.insert(62, "24R. Ventral anterior cingulate cortex")
        getROIsListBoxRight.insert(63, "25R. Subgenual area")
        getROIsListBoxRight.insert(64, "27R. Piriform cortex")
        getROIsListBoxRight.insert(65, "28R. Ventral entorhinal cortex")
        getROIsListBoxRight.insert(66, "29R. Retrosplenial cingulate cortex")
        getROIsListBoxRight.insert(67, "30R. Retrosplenial cerebral cortex")
        getROIsListBoxRight.insert(68, "31R. Dorsal posterior cingulate cortex")
        getROIsListBoxRight.insert(69, "32R. Dorsal anterior cingulate cortex")
        getROIsListBoxRight.insert(70, "33R. Cingulate cerebral cortex")
        getROIsListBoxRight.insert(71, "34R. Dorsal entorhinal cortex")
        getROIsListBoxRight.insert(72, "35R. Perirhinal cortex")
        getROIsListBoxRight.insert(73, "36R. Ectorhinal area (Temporal cerebral cortex)")
        getROIsListBoxRight.insert(74, "37R. Fusiform gyrus")
        getROIsListBoxRight.insert(75, "38R. Temporopolar area")
        getROIsListBoxRight.insert(76, "39R. Angular gyrus")
        getROIsListBoxRight.insert(77, "40R. Supramarginal gyrus")
        getROIsListBoxRight.insert(78, "41R. Auditory cortex")
        getROIsListBoxRight.insert(79, "42R. Auditory cortex")
        getROIsListBoxRight.insert(80, "43R. Primary gustatory cortex")
        getROIsListBoxRight.insert(81, "44R. Pars opercularis")
        getROIsListBoxRight.insert(82, "45R. Pars tiangularis")
        getROIsListBoxRight.insert(83, "46R. Dorsolateral prefrontal cortex")
        getROIsListBoxRight.insert(84, "47R. Pars orbitalis")
        getROIsListBoxRight.grid(row=2, column=1)
        submitButton = tk.Button(text="Submit", command=lambda: self.FunctionalPartSix(
            pickROIsLabel, leftLabel, rightLabel, submitButton, getROIsListBoxLeft, getROIsListBoxRight, parent))
        submitButton.grid(row=3, column=0, columnspan=2)
        #Choose from a list of the ROIs, line 105 in "connectivity" file

    def FunctionalPartSix(self, label1, label2, label3, button, leftBox, rightBox, parent):
        label1.grid_forget()
        label2.grid_forget()
        label3.grid_forget()
        button.grid_forget()
        totalROIsL = ['1L', '2L', '3L', '4L', '5L', '6L', '7L', '8L', '9L', '10L', '11L', '13L', '17L', '18L', '19L',
                      '20L', '21L', '22L', '23L', '24L', '25L', '27L', '28L', '29L', '30L', '31L', '32L', '33L', '34L',
                      '35L', '36L', '37L', '38L','39L', '40L', '41L', '42L', '43L', '44L', '45L', '46L', '47L']
        totalROIsR = ['1R', '2R', '3R', '4R', '5R', '6R', '7R', '8R','9R', '10R', '11R', '13R', '17R', '18R', '19R',
                      '20R','21R', '22R', '23R', '24R', '25R', '27R', '28R', '29R', '30R', '31R', '32R', '33R', '34R',
                      '35R','36R', '37R', '38R', '39R', '40R', '41R', '42R', '43R', '44R', '45R', '46R', '47R']
        indexNumbersLeft = leftBox.curselection()
        indexNumbersRight = rightBox.curselection()
        for x in range(0, len(indexNumbersLeft)):
            ROIs.append(totalROIsL[indexNumbersLeft[x]])
        for x in range(0, len(indexNumbersRight)):
            ROIs.append(totalROIsR[indexNumbersRight[x]])
        leftBox.grid_forget()
        rightBox.grid_forget()
        for first in range(len(ROIs)):
            for second in range(first + 1, len(ROIs)):
                connections.append(str(ROIs[first]) + '-' + str(ROIs[second]))
        frequenciesLabel = tk.Label(text="Which frequency bands are you evaluating in your data? Select all that apply")
        frequenciesLabel.grid(row=0, column=0)
        getFrequenciesListBox = tk.Listbox(selectmode="multiple", height=14)
        getFrequenciesListBox.insert(1, "Delta")
        getFrequenciesListBox.insert(2, "Theta")
        getFrequenciesListBox.insert(3, "Alpha")
        getFrequenciesListBox.insert(4, "Alpha1")
        getFrequenciesListBox.insert(5, "Alpha2")
        getFrequenciesListBox.insert(6, "Alpha3")
        getFrequenciesListBox.insert(7, "Beta")
        getFrequenciesListBox.insert(8, "Beta1")
        getFrequenciesListBox.insert(9, "Beta2")
        getFrequenciesListBox.insert(10, "Beta3")
        getFrequenciesListBox.insert(11, "Gamma")
        getFrequenciesListBox.insert(12, "Low Gamma")
        getFrequenciesListBox.insert(13, "High Gamma")
        getFrequenciesListBox.insert(14, "Mu")
        getFrequenciesListBox.grid(row=1, column=0)
        submitButton = tk.Button(text="Submit", command=lambda: self.FunctionalPartSeven(frequenciesLabel,
                                                                                         getFrequenciesListBox,
                                                                                         submitButton, parent))
        submitButton.grid(row=2, column=0)

    def FunctionalPartSeven(self, label, listbox, button, parent):
        label.grid_forget()
        button.grid_forget()
        indexNumbers = listbox.curselection()
        self.chosenFrequencies = []
        self.subjects_of_each_condition = []
        for x in range(0, len(indexNumbers)):
            self.chosenFrequencies.append(listbox.get(indexNumbers[x]))
        listbox.grid_forget()
        self.fileLocationList = []
        for each_condition in range(len(self.conditions_list)):
            self.subjects_of_each_condition.append([])
            fileSelectLabel = tk.Label(text='Please select all of the subjects\' files in the condition "' +
                                       self.conditions_list[each_condition] + '" by control clicking')
            fileSelectLabel.grid(row=0, column=0)
            fileLocation = fd.askopenfilenames(parent=parent, title="Select the files in the condition " +
                                               self.conditions_list[each_condition])
            self.fileLocationList.extend(list(fileLocation))
            for x in range(int(self.num_each_condition[each_condition])):
                self.subjects_of_each_condition[each_condition].append(ConSubject("%s %s" % (self.conditions_list[
                    each_condition], str(x+1))))
                self.subjects_of_each_condition[each_condition][x].setData(self.fileLocationList[x], self.chosenFrequencies)
                fileSelectLabel.grid_forget()
        continueButton = tk.Button(text="Next", command=lambda: self.FunctionalPartEight(continueButton, parent))
        continueButton.grid(row=0, column=0)

    def FunctionalPartEight(self, button, parent):
        button.grid_forget()
        for each_condition in range(len(self.conditions_list)):
            for ra in range(int(self.num_each_condition[each_condition])):
                self.subjects_of_each_condition[each_condition][ra].organizeData()
        data_organized = []
        sheets = []
        for organized in range(len(self.conditions_list)):
            data_organized.append(xlsxwriter.Workbook("%s_Organized_Conn.xlsx" % self.conditions_list[organized]))
            sheets.append([])
        for number_of_freq in range(len(self.chosenFrequencies)):
            for each_condition in range(len(self.conditions_list)):
                sheets[each_condition].append(data_organized[each_condition].add_worksheet(str(self.chosenFrequencies[
                                                                                                   number_of_freq])))
                subject_counter = 0
                for subject in range(int(self.num_each_condition[each_condition])+1):
                    if subject == 0:
                        sheets[each_condition][number_of_freq].write_row(0, 1, connections)
                    else:
                        sheets[each_condition][number_of_freq].write(subject, 0, self.subjects_of_each_condition[
                            each_condition][subject_counter].getName())
                        sheets[each_condition][number_of_freq].write_row(subject, 1, self.subjects_of_each_condition[
                            each_condition][subject_counter].getOrgData().iloc[number_of_freq])
                        subject_counter += 1
        for organized in range(len(self.conditions_list)):
            data_organized[organized].close()
        finishedLabel = tk.Label(parent, text="Your data has been organized for each condition.\nEach frequency band ha"
                                              "s its own sheet and\nthe data is sorted into Subjects x ROIs.\nThe files"
                                              " have been saved in the working directory.")
        finishedLabel.grid(row=1, column=0)
        nextButton = tk.Button(text="Next", command=lambda: self.FunctionalPartNine(finishedLabel, nextButton, parent))
        nextButton.grid(row=1, column=0)

    def FunctionalPartNine(self, label, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.averageMatrices = []
        for each_condition in range(len(self.conditions_list)):
            self.averageMatrices.append([])
            for matrix in range(len(self.chosenFrequencies)):
                idx = []
                for subject in range(int(self.num_each_condition[each_condition])):
                    idx.append("Subject " + str(subject+1))
                self.averageMatrices[each_condition].append(pd.DataFrame(index=idx, columns=connections))
                for subject in range(int(self.num_each_condition[each_condition])):
                    self.averageMatrices[each_condition][matrix].iloc[subject] = self.subjects_of_each_condition[
                        each_condition][subject].getOrgData().iloc[matrix]
        graphLabel = tk.Label(text="Do you want any of the data graphed?")
        graphLabel.grid(row=0, column=0, columnspan=2)
        yesButton = tk.Button(text="Yes", command=lambda: self.FunctionalPartTenYes(graphLabel, yesButton, noButton,
                                                                                    parent))
        yesButton.grid(row=1, column=0)
        noButton = tk.Button(text="No", command=lambda: quit())
        noButton.grid(row=1, column=1)

    def FunctionalPartTenYes(self, label, yes, no, parent):
        label.grid_forget()
        yes.grid_forget()
        no.grid_forget()
        ROIsLabel = tk.Label(text="Please enter the ROI connections that you want graphed, separated by spaces.\nEx: 1L"
                                  "-1R 2L-3L")
        ROIsLabel.grid(column=0, row=0, columnspan=2)
        getROInum = tk.Entry()
        getROInum.grid(row=1, column=0)
        nextButton = tk.Button(text="Next", command=lambda: self.FunctionalPartEleven(ROIsLabel, getROInum, nextButton,
                                                                                      parent))
        nextButton.grid(row=1, column=1)

    def FunctionalPartEleven(self, label, entry, button, parent):
        label.grid_forget()
        button.grid_forget()
        ROIs_split = entry.get().split()
        num_of_graphs = list(map(str, ROIs_split))
        width = 0.35
        for graphs in range(len(num_of_graphs)):
            plotMatrices = []
            for each_condition in range(len(self.conditions_list)):
                plotMatrices.append([0] * len(self.chosenFrequencies))
                for x in range(len(self.chosenFrequencies)):
                    plotMatrices[each_condition][x] = self.averageMatrices[each_condition][x][str(num_of_graphs[
                                                                                                      graphs])].mean()
            y_pos = np.arange(0, len(self.conditions_list) * 0.5 * len(self.chosenFrequencies), len(
                self.conditions_list) * 0.5)
            fig, ax = plt.subplots(figsize=(10, 7))
            plt.figure(graphs+1)
            for plot in range(len(plotMatrices)):
                if plot == 0:
                    plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, label=self.chosenFrequencies[plot])
                else:
                    plt.bar([p + width * plot for p in y_pos], plotMatrices[plot], width, alpha=0.5,
                            label=self.chosenFrequencies[plot])
            ax.set_xticks([p+ (0.5 * (len(self.conditions_list) - 1)) * width for p in y_pos])
            ax.set_xticklabels(self.chosenFrequencies)
            ax.set_ylabel('Connectivity')
            ax.set_title('ROIs %s' % num_of_graphs[graphs])
            maxY = 0
            for each_condition in range(len(self.conditions_list)):
                for x in range(len(self.chosenFrequencies)):
                    if plotMatrices[each_condition][x] > maxY:
                        maxY = plotMatrices[each_condition][x]
            plt.ylim([0, maxY + 2])
            plt.legend(self.conditions_list, loc='upper right')
            plt.savefig('ROIs %s.png' % num_of_graphs[graphs])
        finalLabel = tk.Label(text="Your graphs have been created and saved successfully.")
        finalLabel.grid(column=0, row=0)
        finishButton = tk.Button(text="Finish", command=quit())
        finishButton.grid(column=0, row=1)


class EffectiveConnectivity(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.EffectiveDataLabel = tk.Label(self, text="Effective Connectivity", font=LARGE_FONT)
        self.EffectiveDataLabel.grid(row=0, column=0, columnspan=3)
        howManyConditionsLabel = tk.Label(self, text="How many conditions are in your study?")
        howManyConditionsLabel.grid(row=1, column=0)
        getNumberOfConditions = tk.Entry(self)
        getNumberOfConditions.grid(row=2, column=0)
        submitButton = tk.Button(self, text="Submit", command=lambda: self.getConditionNames(howManyConditionsLabel,
                                                                                             getNumberOfConditions,
                                                                                             submitButton, parent))
        submitButton.grid(row=2, column=1)

    def getConditionNames(self, label, entry, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.numberConditions = int(entry.get())
        entry.grid_forget()
        getConditionListLabel = tk.Label(self, text="Please enter the names of the condition(s) in your study:")
        getConditionListLabel.grid(row=1, column=0)
        getConditionNamesList = []
        for x in range(0, self.numberConditions):
            getConditionNames = tk.Entry(self)
            getConditionNames.insert(0, "Condition " + str(x+1))
            getConditionNames.grid(row=x+2, column=0)
            getConditionNamesList.append(getConditionNames)
        submitButton = tk.Button(text="Submit", command=lambda: self.EffectivePartThree(getConditionListLabel,
                                                                                        submitButton,
                                                                                        getConditionNamesList, parent),
                                 height=2, width=10)
        submitButton.grid(row=2, column=0)

    def EffectivePartThree(self, label, button, entryList, parent):
        self.conditions_list = []
        label.grid_forget()
        button.grid_forget()
        for ent in entryList:
            self.conditions_list.append(ent.get())
            ent.grid_forget()
        subjectsInConditionLabel = tk.Label(text="How many subjects are in each condition?")
        subjectsInConditionLabel.grid(row=0, column=0)
        subjectsInConditionList = []
        conditionLabelList = []
        for x in range(0, len(entryList)):
            conditionLabel = tk.Label(text=self.conditions_list[x]+":")
            conditionLabel.grid(row=x+1, column=0)
            getSubjectNumber = tk.Entry()
            getSubjectNumber.grid(row=x+1, column=1)
            subjectsInConditionList.append(getSubjectNumber)
            conditionLabelList.append(conditionLabel)
        continueButton = tk.Button(text="Submit", command=lambda: self.EffectivePartFour(
            subjectsInConditionLabel, continueButton, subjectsInConditionList, conditionLabelList, parent))
        continueButton.grid()

    def EffectivePartFour(self, label, button, entryList, labelList, parent):
        label.grid_forget()
        button.grid_forget()
        self.num_each_condition = []
        for ent in entryList:
            self.num_each_condition.append(ent.get())
            ent.grid_forget()
        for lab in labelList:
            lab.grid_forget()
        howManyROIsLabel = tk.Label(text="How many ROIs are present in your data? (Max: 84)")
        howManyROIsLabel.grid(row=0, column=0)
        getNumROIs = tk.Entry()
        getNumROIs.grid(row=1, column=0)
        submitButton = tk.Button(text="Submit", command=lambda: self.EffectivePartFive(howManyROIsLabel, getNumROIs,
                                                                                       submitButton, parent))
        submitButton.grid(row=1, column=1)

    def EffectivePartFive(self, label, entry, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.numROIs = int(entry.get())
        entry.grid_forget()
        pickROIsLabel = tk.Label(text="Please choose all of the ROIs in your data:")
        pickROIsLabel.grid(column=0, row=0, columnspan=2)
        leftLabel = tk.Label(text="Left sided ROIs")
        leftLabel.grid(row=1, column=0)
        rightLabel = tk.Label(text="Right sided ROIs")
        rightLabel.grid(row=1, column=1)
        getROIsListBoxLeft = tk.Listbox(selectmode="extended", width=45, exportselection=0)
        getROIsListBoxLeft.insert(1, "1L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(2, "2L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(3, "3L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(4, "4L. Primary motor cortex")
        getROIsListBoxLeft.insert(5, "5L. Somatosensory association cortex")
        getROIsListBoxLeft.insert(6, "6L. Premotor and supplementary motor cortex")
        getROIsListBoxLeft.insert(7, "7L. Visuo-motor cortex")
        getROIsListBoxLeft.insert(8, "8L. Frontal eye fields")
        getROIsListBoxLeft.insert(9, "9L. Dorsolateral prefrontal cortex")
        getROIsListBoxLeft.insert(10, "10L. Anterior prefrontal cortex")
        getROIsListBoxLeft.insert(11, "11L. Orbitofrontal area")
        getROIsListBoxLeft.insert(12, "13L. Insular Cortex")
        getROIsListBoxLeft.insert(13, "17L. Primary visual cortex (V1)")
        getROIsListBoxLeft.insert(14, "18L. Secondary visual cortex (V2)")
        getROIsListBoxLeft.insert(15, "19L. Associative visual cortex (V3, V4, V5)")
        getROIsListBoxLeft.insert(16, "20L. Inferior temporal gyrus")
        getROIsListBoxLeft.insert(17, "21L. Middle temporal gyrus")
        getROIsListBoxLeft.insert(18, "22L. Superior temporal gyrus")
        getROIsListBoxLeft.insert(19, "23L. Ventral posterior cingulate cortex")
        getROIsListBoxLeft.insert(20, "24L. Ventral anterior cingulate cortex")
        getROIsListBoxLeft.insert(21, "25L. Subgenual area")
        getROIsListBoxLeft.insert(22, "27L. Piriform cortex")
        getROIsListBoxLeft.insert(23, "28L. Ventral entorhinal cortex")
        getROIsListBoxLeft.insert(24, "29L. Retrosplenial cingulate cortex")
        getROIsListBoxLeft.insert(25, "30L. Retrosplenial cerebral cortex")
        getROIsListBoxLeft.insert(26, "31L. Dorsal posterior cingulate cortex")
        getROIsListBoxLeft.insert(27, "32L. Dorsal anterior cingulate cortex")
        getROIsListBoxLeft.insert(28, "33L. Cingulate cerebral cortex")
        getROIsListBoxLeft.insert(29, "34L. Dorsal entorhinal cortex")
        getROIsListBoxLeft.insert(30, "35L. Perirhinal cortex")
        getROIsListBoxLeft.insert(31, "36L. Ectorhinal area (Temporal cerebral cortex)")
        getROIsListBoxLeft.insert(32, "37L. Fusiform gyrus")
        getROIsListBoxLeft.insert(33, "38L. Temporopolar area")
        getROIsListBoxLeft.insert(34, "39L. Angular gyrus")
        getROIsListBoxLeft.insert(35, "40L. Supramarginal gyrus")
        getROIsListBoxLeft.insert(36, "41L. Auditory cortex")
        getROIsListBoxLeft.insert(37, "42L. Auditory cortex")
        getROIsListBoxLeft.insert(38, "43L. Primary gustatory cortex")
        getROIsListBoxLeft.insert(39, "44L. Pars opercularis")
        getROIsListBoxLeft.insert(40, "45L. Pars tiangularis")
        getROIsListBoxLeft.insert(41, "46L. Dorsolateral prefrontal cortex")
        getROIsListBoxLeft.insert(42, "47L. Pars orbitalis")
        getROIsListBoxLeft.grid(row=2, column=0)
        getROIsListBoxRight = tk.Listbox(selectmode="extended", width=45, exportselection=0)
        getROIsListBoxRight.insert(43, "1R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(44, "2R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(45, "3R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(46, "4R. Primary motor cortex")
        getROIsListBoxRight.insert(47, "5R. Somatosensory association cortex")
        getROIsListBoxRight.insert(48, "6R. Premotor and supplementary motor cortex")
        getROIsListBoxRight.insert(49, "7R. Visuo-motor cortex")
        getROIsListBoxRight.insert(50, "8R. Frontal eye fields")
        getROIsListBoxRight.insert(51, "9R. Dorsolateral prefrontal cortex")
        getROIsListBoxRight.insert(52, "10R. Anterior prefrontal cortex")
        getROIsListBoxRight.insert(53, "11R. Orbitofrontal area")
        getROIsListBoxRight.insert(54, "13R. Insular Cortex")
        getROIsListBoxRight.insert(55, "17R. Primary visual cortex (V1)")
        getROIsListBoxRight.insert(56, "18R. Secondary visual cortex (V2)")
        getROIsListBoxRight.insert(57, "19R. Associative visual cortex (V3, V4, V5)")
        getROIsListBoxRight.insert(58, "20R. Inferior temporal gyrus")
        getROIsListBoxRight.insert(59, "21R. Middle temporal gyrus")
        getROIsListBoxRight.insert(60, "22R. Superior temporal gyrus")
        getROIsListBoxRight.insert(61, "23R. Ventral posterior cingulate cortex")
        getROIsListBoxRight.insert(62, "24R. Ventral anterior cingulate cortex")
        getROIsListBoxRight.insert(63, "25R. Subgenual area")
        getROIsListBoxRight.insert(64, "27R. Piriform cortex")
        getROIsListBoxRight.insert(65, "28R. Ventral entorhinal cortex")
        getROIsListBoxRight.insert(66, "29R. Retrosplenial cingulate cortex")
        getROIsListBoxRight.insert(67, "30R. Retrosplenial cerebral cortex")
        getROIsListBoxRight.insert(68, "31R. Dorsal posterior cingulate cortex")
        getROIsListBoxRight.insert(69, "32R. Dorsal anterior cingulate cortex")
        getROIsListBoxRight.insert(70, "33R. Cingulate cerebral cortex")
        getROIsListBoxRight.insert(71, "34R. Dorsal entorhinal cortex")
        getROIsListBoxRight.insert(72, "35R. Perirhinal cortex")
        getROIsListBoxRight.insert(73, "36R. Ectorhinal area (Temporal cerebral cortex)")
        getROIsListBoxRight.insert(74, "37R. Fusiform gyrus")
        getROIsListBoxRight.insert(75, "38R. Temporopolar area")
        getROIsListBoxRight.insert(76, "39R. Angular gyrus")
        getROIsListBoxRight.insert(77, "40R. Supramarginal gyrus")
        getROIsListBoxRight.insert(78, "41R. Auditory cortex")
        getROIsListBoxRight.insert(79, "42R. Auditory cortex")
        getROIsListBoxRight.insert(80, "43R. Primary gustatory cortex")
        getROIsListBoxRight.insert(81, "44R. Pars opercularis")
        getROIsListBoxRight.insert(82, "45R. Pars tiangularis")
        getROIsListBoxRight.insert(83, "46R. Dorsolateral prefrontal cortex")
        getROIsListBoxRight.insert(84, "47R. Pars orbitalis")
        getROIsListBoxRight.grid(row=2, column=1)
        submitButton = tk.Button(text="Submit", command=lambda: self.EffectivePartSix(
            pickROIsLabel, leftLabel, rightLabel, submitButton, getROIsListBoxLeft, getROIsListBoxRight, parent))
        submitButton.grid(row=3, column=0, columnspan=2)

    def EffectivePartSix(self, label1, label2, label3, button, leftBox, rightBox, parent):
        label1.grid_forget()
        label2.grid_forget()
        label3.grid_forget()
        button.grid_forget()
        totalROIsL = ['1L', '2L', '3L', '4L', '5L', '6L', '7L', '8L', '9L', '10L', '11L', '13L', '17L', '18L', '19L',
                      '20L', '21L', '22L', '23L', '24L', '25L', '27L', '28L', '29L', '30L', '31L', '32L', '33L', '34L',
                      '35L', '36L', '37L', '38L', '39L', '40L', '41L', '42L', '43L', '44L', '45L', '46L', '47L']
        totalROIsR = ['1R', '2R', '3R', '4R', '5R', '6R', '7R', '8R', '9R', '10R', '11R', '13R', '17R', '18R', '19R',
                      '20R', '21R', '22R', '23R', '24R', '25R', '27R', '28R', '29R', '30R', '31R', '32R', '33R', '34R',
                      '35R', '36R', '37R', '38R', '39R', '40R', '41R', '42R', '43R', '44R', '45R', '46R', '47R']
        indexNumbersLeft = leftBox.curselection()
        indexNumbersRight = rightBox.curselection()
        for x in range(0, len(indexNumbersLeft)):
            ROIs.append(totalROIsL[indexNumbersLeft[x]])
        for x in range(0, len(indexNumbersRight)):
            ROIs.append(totalROIsR[indexNumbersRight[x]])
        leftBox.grid_forget()
        rightBox.grid_forget()
        for first in range(len(ROIs)):
            for second in range(first + 1, len(ROIs)):
                connections.append(str(ROIs[first]) + '-' + str(ROIs[second]))
        frequenciesLabel = tk.Label(text="Which frequency bands are you evaluating in your data? Select all that apply")
        frequenciesLabel.grid(row=0, column=0)
        getFrequenciesListBox = tk.Listbox(selectmode="multiple", height=14)
        getFrequenciesListBox.insert(1, "Delta")
        getFrequenciesListBox.insert(2, "Theta")
        getFrequenciesListBox.insert(3, "Alpha")
        getFrequenciesListBox.insert(4, "Alpha1")
        getFrequenciesListBox.insert(5, "Alpha2")
        getFrequenciesListBox.insert(6, "Alpha3")
        getFrequenciesListBox.insert(7, "Beta")
        getFrequenciesListBox.insert(8, "Beta1")
        getFrequenciesListBox.insert(9, "Beta2")

        getFrequenciesListBox.insert(10, "Beta3")
        getFrequenciesListBox.insert(11, "Gamma")
        getFrequenciesListBox.insert(12, "Low Gamma")
        getFrequenciesListBox.insert(13, "High Gamma")
        getFrequenciesListBox.insert(14, "Mu")
        getFrequenciesListBox.grid(row=1, column=0)
        submitButton = tk.Button(text="Submit", command=lambda: self.EffectivePartSeven(frequenciesLabel,
                                                                                         getFrequenciesListBox,
                                                                                         submitButton, parent))
        submitButton.grid(row=2, column=0)

    def EffectivePartSeven(self, label, listbox, button, parent):
        label.grid_forget()
        button.grid_forget()
        indexNumbers = listbox.curselection()
        self.chosenFrequencies = []
        self.subjects_of_each_condition = []
        for x in range(0, len(indexNumbers)):
            self.chosenFrequencies.append(listbox.get(indexNumbers[x]))
        listbox.grid_forget()
        self.fileLocationList = []
        for each_condition in range(len(self.conditions_list)):
            self.subjects_of_each_condition.append([])
            for x in range(int(self.num_each_condition[each_condition])):
                for f in range((len(self.chosenFrequencies))):
                    fileSelectLabel = tk.Label(text='Please select all of the subjects\' files in the condition "' +
                                                    self.conditions_list[each_condition] + '" for the frequency "' +
                                                    self.chosenFrequencies[f] + '" by control clicking')
                    fileSelectLabel.grid(row=0, column=0)
                    fileLocation = fd.askopenfilenames(parent=parent, title='Select the files in the condition ' +
                                                                            self.conditions_list[each_condition])
                    self.fileLocationList.extend(list(fileLocation))
                self.subjects_of_each_condition[each_condition].append(ConSubject2("%s %s" % (self.conditions_list[each_condition], str(x+1))))
                self.subjects_of_each_condition[each_condition][x].setData(self.fileLocationList,
                                                                           self.chosenFrequencies)
        continueButton = tk.Button(text="Next", command=lambda: self.EffectivePartEight(continueButton, parent))
        continueButton.grid(row=0, column=0)

    def EffectivePartEight(self, button, parent):
        button.grid_forget()
        for each_condition in range(len(self.conditions_list)):
            for ra in range(self.num_each_condition[each_condition]):
                self.subjects_of_each_condition[each_condition][ra].organizeData()
        data_organized = []
        sheets = []
        for organized in range(len(self.conditions_list)):
            data_organized.append(xlsxwriter.Workbook("%s_Organized_EffecConn.xlsx" % self.conditions_list[organized]))
            sheets.append([])
        for number_of_freq in range(len(self.chosenFrequencies)):
            for each_condition in range(len(self.conditions_list)):
                sheets[each_condition].append(data_organized[each_condition].add_worksheet(str(self.chosenFrequencies
                                                                                               [number_of_freq])))
                subject_counter = 0
                for subject in range(self.num_each_condition[each_condition] + 1):
                    if subject == 0:
                        sheets[each_condition][number_of_freq].write_row(0, 1, connections)
                    else:
                        sheets[each_condition][number_of_freq].write(
                            subject, 0, self.subjects_of_each_condition[each_condition][subject_counter].getName())
                        sheets[each_condition][number_of_freq].write_row(subject, 1, self.subjects_of_each_condition[
                            each_condition][subject_counter].getOrgData().iloc[number_of_freq])
                        subject_counter += 1
        for organized in range(len(self.conditions_list)):
            data_organized[organized].close()
        excelledLabel = tk.Label(text="Your data has been organized for each condition. Each frequency band is its own sheet and the data is sorted into Subjects x ROIs. The files have been saved in the working directory.")
        excelledLabel.grid(row=0, column=0)
        continueButton = tk.Button(text="Continue", command=lambda: self.EffectivePartNine(excelledLabel,
                                                                                           continueButton, parent))

    def EffectivePartNine(self, label, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.averageMatrices = []
        for each_condition in range(len(self.conditions_list)):
            self.averageMatrices.append([])
            for matrix in range(len(self.chosenFrequencies)):
                idx = []
                for subject in range(self.num_each_condition[each_condition]):
                    idx.append("Subjcet " + str(subject + 1))
                self.averageMatrices[each_condition].append(pd.DataFrame(index=idx, columns=connections))
                for subject in range(self.num_each_condition[each_condition]):
                    self.averageMatrices[each_condition][matrix].iloc[subject] = \
                    self.subjects_of_each_condition[each_condition][subject].getOrgdata().iloc[matrix]
        printQuestion = tk.Label(text="Would you like any of the data graphed?")
        printQuestion.grid(row=0, column=0, columnspan=2)
        yesButton = tk.Button(text="Yes", command=lambda: self.EffectivePartTenYes(printQuestion, noButton, yesButton,
                                                                                   parent))
        yesButton.grid(row=1, column=0)
        noButton = tk.Button(text="No", command=lambda: self.EffectivePartTenNo(label, noButton, yesButton, parent))
        noButton.grid(row=1, column=1)

    def EffectivePartTenNo(self, label, nbutton, ybutton, parent):
        label.grid_forget()
        nbutton.grid_forget()
        ybutton.grid_forget()
        quit()

    def EffectivePartTenYes(self, label, nbutton, ybutton, parent):
        label.grid_forget()
        nbutton.grid_forget()
        ybutton.grid_forget()
        askRois = tk.Label(text="Please enter the ROI connections that you wanted graphed, separated by spaces."
                           " Ex: 1L-1R 2L-3L")
        askRois.grid(row=0, column=0, columnspan=2)
        roiEntry = tk.Entry()
        roiEntry.grid(row=1, column=0)
        nextButton = tk.Button(text="Next", command=lambda: self.EffectivePartEleven(askRois, roiEntry, nextButton,
                                                                                     parent))
        nextButton.grid(row=1, column=1)

    def EffectivePartEleven(self, label, entry, button, parent):
        label.grid_forget()
        button.grid_forget()
        ROIs_split = entry.get().split()
        num_of_graphs = list(map(str, ROIs_split))
        width = 0.35
        for graphs in range(len(num_of_graphs)):
            plotMatrices = []
            for each_condition in range(len(self.conditions_list)):
                plotMatrices.append([0] * len(self.chosenFrequencies))
                for x in range(len(self.chosenFrequencies)):
                    plotMatrices[each_condition][x] = self.averageMatrices[each_condition][x][
                        str(num_of_graphs[graphs])].mean()
            y_pos = np.arange(0, len(self.conditions_list) * 0.5 * len(self.chosenFrequencies), len(self.conditions_list)
                              * 0.5)
            fig, ax = plt.subplots(figsize=(10, 7))
            plt.figure(graphs + 1)
            for plot in range(len(plotMatrices)):
                if plot == 0:
                    plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, label=self.chosenFrequencies[plot])
                else:
                    plt.bar([p + width * plot for p in y_pos], plotMatrices[plot], width, alpha=0.5,
                            label=self.chosenFrequencies[plot])
            ax.set_xticks([p + (0.5 * (len(self.conditions_list) -1))* width for p in y_pos])
            ax.setxticksLabels(self.chosenFrequencies)
            ax.setyLabel('Connectivity')
            ax.set_title('ROIs %s' % num_of_graphs[graphs])
            maxY = 0
            for each_condition in range(len(self.conditions_list)):
                for x in range(len(self.chosenFrequencies)):
                    if plotMatrices[each_condition][x] > maxY:
                        maxY = plotMatrices[each_condition][x]
            if maxY < 2:
                plt.ylim([0, maxY * 2])
            else:
                plt.ylim([0, maxY + 2])
            plt.legend(self.conditions_list, loc='upper right')
            plt.savefig('EffecConn ROIs %s.png' % num_of_graphs[graphs])
        finishedLabel = tk.Label(text="Your graphs have been created and saved successfully.")
        finishedLabel.grid(row=0, column=0)
        finishButton = tk.Button(text="Finish and Close", command=lambda: quit())
        finishButton.grid(row=1, column=0)


class PhaseAmp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        numConditions = tk.Label(self, text="How many conditions are in your study?")
        numConditions.grid(row=1, column=0)
        self.PhaseAmpLabel = tk.Label(self, text="Phase Amplitude Coupling", font=LARGE_FONT)
        self.PhaseAmpLabel.grid(row=0, column=0, columnspan=3)
        getNumConditions = tk.Entry(self)
        getNumConditions.grid(row=2, column=0)
        submitButton = tk.Button(self, text="Submit", command=lambda: self.getConditionNames(numConditions,
                                                                                             getNumConditions,
                                                                                             submitButton, parent))
        submitButton.grid(row=2, column=1)


    def getConditionNames(self, label, entry, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.numberConditions = int(entry.get())
        entry.grid_forget()
        conditionList = tk.Label(self, text="Please enter the names of the condition(s) in your study:")
        conditionList.grid(row=1, column=0)
        conditionNames = []
        for x in range(0, self.numberConditions):
            getConditionNames = tk.Entry(self)
            getConditionNames.insert(0, "Condition " + str(x+1))
            getConditionNames.grid(row=x+2, column=0)
            conditionNames.append(getConditionNames)
        submitButton = tk.Button(text="Submit", command=lambda: self.getNumSubjects(submitButton,
                                                                                    conditionNames, conditionList,
                                                                                    parent))
        submitButton.grid(row=2, column=0)

    def getNumSubjects(self, button, entryList, label, parent):
        self.conditions_list = []
        label.grid_forget()
        button.grid_forget()
        for ent in entryList:
            self.conditions_list.append(ent.get())
            ent.grid_forget()
        subjectsInConditionLabel = tk.Label(text="How many subjects are in each condition?")
        subjectsInConditionLabel.grid(row=0, column=0)
        subjectsInConditionList = []
        conditionLabelList = []
        for x in range(0, len(entryList)):
            conditionLabel = tk.Label(text=self.conditions_list[x]+":")
            conditionLabel.grid(row=x+1, column=0)
            getSubjectNumber = tk.Entry()
            getSubjectNumber.grid(row=x+1, column=1)
            subjectsInConditionList.append(getSubjectNumber)
            conditionLabelList.append(conditionLabel)
        submitButton = tk.Button(text="Submit", command=lambda: self.getNumROIs(subjectsInConditionLabel,
                                                                                subjectsInConditionList, submitButton,
                                                                                conditionLabelList, parent))
        submitButton.grid()

    def getNumROIs(self, label, entryList, button, labelList, parent):
        label.grid_forget()
        button.grid_forget()
        self.num_each_condition = []
        for ent in entryList:
            self.num_each_condition.append(ent.get())
            ent.grid_forget()
        for lab in labelList:
            lab.grid_forget()
        askNumRois = tk.Label(text="How many ROIs are present in your data? (Max: 84)")
        askNumRois.grid(row=1, column=0)
        numRoisEntry = tk.Entry()
        numRoisEntry.grid(row=2, column=0)
        submitButton = tk.Button(text="Continue", command=lambda: self.getConditionNames(askNumRois, numRoisEntry,
                                                                                         submitButton, parent))
        submitButton.grid(row=2, column=1)

    def PhaseAmpPartTwo(self, label, entry, button, parent):
        label.grid_forget()
        self.numROIs = entry.get()
        entry.grid_forget()
        button.grid_forget()
        pickROIsLabel = tk.Label(text="Please choose all of the ROIs in your data:")
        pickROIsLabel.grid(column=0, row=0, columnspan=2)
        leftLabel = tk.Label(text="Left sided ROIs")
        leftLabel.grid(row=1, column=0)
        rightLabel = tk.Label(text="Right sided ROIs")
        rightLabel.grid(row=1, column=1)
        getROIsListBoxLeft = tk.Listbox(selectmode="extended", width=45, exportselection=0)
        getROIsListBoxLeft.insert(1, "1L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(2, "2L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(3, "3L. Primary somatosensory cortex")
        getROIsListBoxLeft.insert(4, "4L. Primary motor cortex")
        getROIsListBoxLeft.insert(5, "5L. Somatosensory association cortex")
        getROIsListBoxLeft.insert(6, "6L. Premotor and supplementary motor cortex")
        getROIsListBoxLeft.insert(7, "7L. Visuo-motor cortex")
        getROIsListBoxLeft.insert(8, "8L. Frontal eye fields")
        getROIsListBoxLeft.insert(9, "9L. Dorsolateral prefrontal cortex")
        getROIsListBoxLeft.insert(10, "10L. Anterior prefrontal cortex")
        getROIsListBoxLeft.insert(11, "11L. Orbitofrontal area")
        getROIsListBoxLeft.insert(12, "13L. Insular Cortex")
        getROIsListBoxLeft.insert(13, "17L. Primary visual cortex (V1)")
        getROIsListBoxLeft.insert(14, "18L. Secondary visual cortex (V2)")
        getROIsListBoxLeft.insert(15, "19L. Associative visual cortex (V3, V4, V5)")
        getROIsListBoxLeft.insert(16, "20L. Inferior temporal gyrus")
        getROIsListBoxLeft.insert(17, "21L. Middle temporal gyrus")
        getROIsListBoxLeft.insert(18, "22L. Superior temporal gyrus")
        getROIsListBoxLeft.insert(19, "23L. Ventral posterior cingulate cortex")
        getROIsListBoxLeft.insert(20, "24L. Ventral anterior cingulate cortex")
        getROIsListBoxLeft.insert(21, "25L. Subgenual area")
        getROIsListBoxLeft.insert(22, "27L. Piriform cortex")
        getROIsListBoxLeft.insert(23, "28L. Ventral entorhinal cortex")
        getROIsListBoxLeft.insert(24, "29L. Retrosplenial cingulate cortex")
        getROIsListBoxLeft.insert(25, "30L. Retrosplenial cerebral cortex")
        getROIsListBoxLeft.insert(26, "31L. Dorsal posterior cingulate cortex")
        getROIsListBoxLeft.insert(27, "32L. Dorsal anterior cingulate cortex")
        getROIsListBoxLeft.insert(28, "33L. Cingulate cerebral cortex")
        getROIsListBoxLeft.insert(29, "34L. Dorsal entorhinal cortex")
        getROIsListBoxLeft.insert(30, "35L. Perirhinal cortex")
        getROIsListBoxLeft.insert(31, "36L. Ectorhinal area (Temporal cerebral cortex)")
        getROIsListBoxLeft.insert(32, "37L. Fusiform gyrus")
        getROIsListBoxLeft.insert(33, "38L. Temporopolar area")
        getROIsListBoxLeft.insert(34, "39L. Angular gyrus")
        getROIsListBoxLeft.insert(35, "40L. Supramarginal gyrus")
        getROIsListBoxLeft.insert(36, "41L. Auditory cortex")
        getROIsListBoxLeft.insert(37, "42L. Auditory cortex")
        getROIsListBoxLeft.insert(38, "43L. Primary gustatory cortex")
        getROIsListBoxLeft.insert(39, "44L. Pars opercularis")
        getROIsListBoxLeft.insert(40, "45L. Pars tiangularis")
        getROIsListBoxLeft.insert(41, "46L. Dorsolateral prefrontal cortex")
        getROIsListBoxLeft.insert(42, "47L. Pars orbitalis")
        getROIsListBoxLeft.grid(row=2, column=0)
        getROIsListBoxRight = tk.Listbox(selectmode="extended", width=45, exportselection=0)
        getROIsListBoxRight.insert(43, "1R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(44, "2R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(45, "3R. Primary somatosensory cortex")
        getROIsListBoxRight.insert(46, "4R. Primary motor cortex")
        getROIsListBoxRight.insert(47, "5R. Somatosensory association cortex")
        getROIsListBoxRight.insert(48, "6R. Premotor and supplementary motor cortex")
        getROIsListBoxRight.insert(49, "7R. Visuo-motor cortex")
        getROIsListBoxRight.insert(50, "8R. Frontal eye fields")
        getROIsListBoxRight.insert(51, "9R. Dorsolateral prefrontal cortex")
        getROIsListBoxRight.insert(52, "10R. Anterior prefrontal cortex")
        getROIsListBoxRight.insert(53, "11R. Orbitofrontal area")
        getROIsListBoxRight.insert(54, "13R. Insular Cortex")
        getROIsListBoxRight.insert(55, "17R. Primary visual cortex (V1)")
        getROIsListBoxRight.insert(56, "18R. Secondary visual cortex (V2)")
        getROIsListBoxRight.insert(57, "19R. Associative visual cortex (V3, V4, V5)")
        getROIsListBoxRight.insert(58, "20R. Inferior temporal gyrus")
        getROIsListBoxRight.insert(59, "21R. Middle temporal gyrus")
        getROIsListBoxRight.insert(60, "22R. Superior temporal gyrus")
        getROIsListBoxRight.insert(61, "23R. Ventral posterior cingulate cortex")
        getROIsListBoxRight.insert(62, "24R. Ventral anterior cingulate cortex")
        getROIsListBoxRight.insert(63, "25R. Subgenual area")
        getROIsListBoxRight.insert(64, "27R. Piriform cortex")
        getROIsListBoxRight.insert(65, "28R. Ventral entorhinal cortex")
        getROIsListBoxRight.insert(66, "29R. Retrosplenial cingulate cortex")
        getROIsListBoxRight.insert(67, "30R. Retrosplenial cerebral cortex")
        getROIsListBoxRight.insert(68, "31R. Dorsal posterior cingulate cortex")
        getROIsListBoxRight.insert(69, "32R. Dorsal anterior cingulate cortex")
        getROIsListBoxRight.insert(70, "33R. Cingulate cerebral cortex")
        getROIsListBoxRight.insert(71, "34R. Dorsal entorhinal cortex")
        getROIsListBoxRight.insert(72, "35R. Perirhinal cortex")
        getROIsListBoxRight.insert(73, "36R. Ectorhinal area (Temporal cerebral cortex)")
        getROIsListBoxRight.insert(74, "37R. Fusiform gyrus")
        getROIsListBoxRight.insert(75, "38R. Temporopolar area")
        getROIsListBoxRight.insert(76, "39R. Angular gyrus")
        getROIsListBoxRight.insert(77, "40R. Supramarginal gyrus")
        getROIsListBoxRight.insert(78, "41R. Auditory cortex")
        getROIsListBoxRight.insert(79, "42R. Auditory cortex")
        getROIsListBoxRight.insert(80, "43R. Primary gustatory cortex")
        getROIsListBoxRight.insert(81, "44R. Pars opercularis")
        getROIsListBoxRight.insert(82, "45R. Pars tiangularis")
        getROIsListBoxRight.insert(83, "46R. Dorsolateral prefrontal cortex")
        getROIsListBoxRight.insert(84, "47R. Pars orbitalis")
        getROIsListBoxRight.grid(row=2, column=1)
        submitButton = tk.Button(text="Submit", command=lambda: self.PhaseAmpPartThree(
        pickROIsLabel, leftLabel, rightLabel, submitButton, getROIsListBoxLeft, getROIsListBoxRight, parent))
        submitButton.grid(row=3, column=0, columnspan=2)

    def PhaseAmpPartThree(self, label1, label2, label3, button, leftBox, rightBox, parent):
        label1.grid_forget()
        label2.grid_forget()
        label3.grid_forget()
        button.grid_forget()
        totalROIsL = ['1L', '2L', '3L', '4L', '5L', '6L', '7L', '8L', '9L', '10L', '11L', '13L', '17L', '18L', '19L',
                      '20L', '21L', '22L', '23L', '24L', '25L', '27L', '28L', '29L', '30L', '31L', '32L', '33L', '34L',
                      '35L', '36L', '37L', '38L', '39L', '40L', '41L', '42L', '43L', '44L', '45L', '46L', '47L']
        totalROIsR = ['1R', '2R', '3R', '4R', '5R', '6R', '7R', '8R', '9R', '10R', '11R', '13R', '17R', '18R', '19R',
                      '20R', '21R', '22R', '23R', '24R', '25R', '27R', '28R', '29R', '30R', '31R', '32R', '33R', '34R',
                      '35R', '36R', '37R', '38R', '39R', '40R', '41R', '42R', '43R', '44R', '45R', '46R', '47R']
        indexNumbersLeft = leftBox.curselection()
        indexNumbersRight = rightBox.curselection()
        for x in range(0, len(indexNumbersLeft)):
            ROIs.append(totalROIsL[indexNumbersLeft[x]])
        for x in range(0, len(indexNumbersRight)):
            ROIs.append(totalROIsR[indexNumbersRight[x]])
        leftBox.grid_forget()
        rightBox.grid_forget()
        for first in range(len(ROIs)):
            for second in range(first + 1, len(ROIs)):
                connections.append(str(ROIs[first]) + '-' + str(ROIs[second]))
        self.chosenROIs = ROIs
        frequenciesLabel = tk.Listbox(selectmode="multiple", height=14)
        getFrequenciesListBox = tk.Listbox(selectmode="multiple", height=14)
        getFrequenciesListBox.insert(1, "Delta")
        getFrequenciesListBox.insert(2, "Theta")
        getFrequenciesListBox.insert(3, "Alpha")
        getFrequenciesListBox.insert(4, "Alpha1")
        getFrequenciesListBox.insert(5, "Alpha2")
        getFrequenciesListBox.insert(6, "Alpha3")
        getFrequenciesListBox.insert(7, "Beta")
        getFrequenciesListBox.insert(8, "Beta1")
        getFrequenciesListBox.insert(9, "Beta2")
        getFrequenciesListBox.insert(10, "Beta3")
        getFrequenciesListBox.insert(11, "Gamma")
        getFrequenciesListBox.insert(12, "Low Gamma")
        getFrequenciesListBox.insert(13, "High Gamma")
        getFrequenciesListBox.insert(14, "Mu")
        getFrequenciesListBox.grid(row=1, column=0)
        submitButton = tk.Button(text="Submit", command=lambda: self.PhaseAmpPartFour(frequenciesLabel,
                                                                                      getFrequenciesListBox,
                                                                                      submitButton, parent))
        submitButton.grid(row=2, column=0)

    def PhaseAmpPartFour(self, label, listbox, button, parent):
        label.grid_forget()
        button.grid_forget()
        indexNumbers = listbox.curselection()
        self.chosenFrequencies = []
        self.subjects_of_each_condition = []
        for x in range(0, len(indexNumbers)):
            self.chosenFrequencies.append(listbox.get(indexNumbers[x]))
        listbox.grid_forget()
        self.fileLocationList = []
        for each_condition in range(len(self.conditions_list)):
            self.subjects_of_each_condition.append([])
            for x in range(int(self.num_each_condition[each_condition])):
                for f in range((len(self.chosenFrequencies))):
                    fileSelectLabel = tk.Label(text='Please select all of the subjects\' files in the condition "' +
                                               self.conditions_list[each_condition] + '" for the frequency "' +
                                               self.chosenFrequencies[f] + '" by control clicking')
                    fileSelectLabel.grid(row=0, column=0)
                    fileLocation = fd.askopenfilenames(parent=parent, title='Select the files in the condition ' +
                                                                            self.conditions_list[each_condition])
                    self.fileLocationList.extend(list(fileLocation))
                self.subjects_of_each_condition[each_condition].append(PACSubject("%s %s" %
                                                                                  (self.conditions_list[each_condition],
                                                                                   (str)(x+1))))
                self.subjects_of_each_condition[each_condition][x].setData(self.fileLocationList,
                                                                           self.chosenROIs)
        continueButton = tk.Button(text="Next", command=lambda: self.PhaseAmpPartFive(continueButton, parent))
        continueButton.grid(row=0, column=0)

    def PhaseAmpPartFive(self, button, parent):
        button.grid_forget()
        data_organized = []
        data_organized_circ = []
        sheets = []
        sheets_circ = []
        corrList = []
        circCorrList = []
        for organized in range(len(self.conditions_list)):
            data_organized.append(xlsxwriter.Workbook("%s_Phase-Amp Coupling Linear Correlations.xlsx" %
                                                      self.conditions_list[organized]))
            sheets.append([])
            data_organized_circ.append(xlsxwriter.Workbook("%s_Phase-Amp Coupling Circular Correlations.xlsx" %
                                                           self.conditions_list[organized]))
            sheets_circ.append([])
        for each_condition in range(len(self.conditions_list)):
            sheets[each_condition].append(data_organized[each_condition].add_worksheet(str(self.conditions_list
                                                                                           [each_condition])))
            subject_counter = 0
            for subject in range(self.num_each_condition[each_condition] + 1):
                if subject == 0:
                    sheets[each_condition][0].write_row(0, 1, ROIs)
                    sheets_circ[each_condition][0].write_row(0, 1, ROIs)
                else:
                    sheets[each_condition][0].write(subject, 0, self.subjects_of_each_condition[each_condition][
                        subject_counter].getName())
                    sheets_circ[each_condition][0].write(subject, 0, self.subjects_of_each_condition[
                        each_condition][subject_counter].getName())
                    for roi in range(len(ROIs)):
                        r, p = sp.stats.pearsonr(self.subjects_of_each_condition[each_condition][
                                                     subject_counter].getData().loc[ROIs[roi],
                                                                                    self.chosenFrequencies[1]],
                                                 self.subjects_of_each_condition[each_condition][
                                                     subject_counter].getData().loc[ROIs[roi],
                        self.chosenFrequencies[2]])
                        corrList.append(r)
                        sheets[each_condition][0].write(subject, roi + 1, r)
                        w, x, y, z = circCorr(self.subjects_of_each_condition[each_condition][subject_counter].getData().loc[ROIs[roi], self.chosenFrequencies[1]], self.subjects_of_each_condition[each_condition][subject_counter].getData().loc[ROIs[roi], self.chosenFrequencies[2]])
                        circCorrList.append(w)
                        sheets_circ[each_condition][0].write(subject, roi + 1, w)
                    self.subjects_of_each_condition[each_condition][subject_counter].setLinearCorrelations(corrList)
                    self.subjects_of_each_condition[each_condition][subject_counter].setCircularCorrelations(circCorrList)
                    corrList = []
                    circCorrList = []
                    subject_counter += 1

        for organized in range(len(self.conditions_list)):
            data_organized[organized].close()
            data_organized_circ[organized].close()
        exportedLabel = tk.Label(text="Your data has been organized for each condition and type of correlation. The dat"
                                      "a is sorted into Subjects x ROIs. The files have been saved in the working direc"
                                      "tory.")
        exportedLabel.grid(row=0, column=0)
        continueButton = tk.Button(text="Continue", command=lambda: self.PhaseAmpPartSix(exportedLabel, continueButton,
                                                                                         parent))

    def PhaseAmpPartSix(self, label, button, parent):
        label.grid_forget()
        button.grid_forget()
        self.averageMatrices = []
        for each_condition in range(len(self.conditions_list)):
            idx = []
            for subject in range(self.num_each_condition[each_condition]):
                idx.append("Subject " + str(subject + 1))
            self.averageMatrices.append(pd.DataFrame(index=idx, columns=ROIs))
            for subject in range(self.num_each_condition[each_condition]):
                for roi in range(len(ROIs)):
                    self.averageMatrices[each_condition].iloc[subject][roi] = \
                    self.subjects_of_each_condition[each_condition][subject].getLinearCorrelations().iloc[0, 0]
        graphLabel = tk.Label(text="Do you want the data graphed? (Clicking no will quit the program)")
        graphLabel.grid(row=0, column=0, columnspan=2)
        yesButton = tk.Button(text="Yes", command=lambda: self.PhaseAmpPartSeven(graphLabel, yesButton, noButton, parent))
        yesButton.grid(row=1, column=0)
        noButton = tk.Button(text="No", command=lambda: quit)
        noButton.grid(row=1, column=2)

    def PhaseAmpPartSeven(self, label, yesbutton, nobutton, parent):
        label.grid_forget()
        yesbutton.grid_forget()
        nobutton.grid_forget()
        graphType = tk.Label(text="What do you want to graph?")
        graphType.grid(row=0, column=0, columnspan=3)
        linCorr = tk.Button(text="Linear Correlations", command=lambda: self.linearCorrelations(graphType, linCorr,
                                                                                                circuCorr, both, parent))
        linCorr.grid(row=1, column=0)
        circuCorr = tk.Button(text="Circular Correlations\n and export raw data",
                              command=lambda: self.circularCorrelations(graphType, linCorr, circuCorr, both, parent))
        circuCorr.grid(row=1, column=1)
        both = tk.Button(text="Both", command=lambda: self.bothCorrelations(graphType, linCorr, circuCorr, both,
                                                                            parent))
        both.grid(row=1, column=3)

    def linearCorrelations(self, label, but1, but2, but3):
        label.grid_forget()
        but1.grid_forget()
        but2.grid_forget()
        but3.grid_forget()
        plotMatrices = []
        plotMatricesErrors = []
        width = 0.35
        for each_condition in range(len(self.conditions_list)):
            plotMatrices.append([0] * len(ROIs))
            plotMatricesErrors.append([0]* len(ROIs))
        for each_condition in range(len(self.conditions_list)):
            for roi in range(len(ROIs)):
                plotMatrices[each_condition][roi] = self.averageMatrices[each_condition][
                    str(ROIs[roi])].mean()
                plotMatricesErrors[each_condition][roi] = 2 * self.averageMatrices[each_condition][
                    str(ROIs[roi])].sem()
        y_pos = np.arange(0, len(self.conditions_list) * 0.5 * len(ROIs), len(self.conditions_list) * 0.5)
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.figure(1)
        for plot in range(len(plotMatrices)):
            if plot == 0:
                plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, yerr=plotMatricesErrors[plot],
                        capsize=10)
            else:
                plt.bar([p + width * plot for p in y_pos], plotMatrices[plot], width, alpha=0.5,
                        yerr=plotMatricesErrors[plot], capsize=10)
        ax.set_xticks([p + (0.5 * (len(self.conditions_list) - 1)) * width for p in y_pos])
        ax.set_xticklabels(self.chosenROIs)
        ax.set_ylabel('Correlation Coefficient')
        ax.set_title('%s-%s Coupling' % (self.chosenFrequencies[1], self.chosenFrequencies[2]))
        maxY = 0
        for each_condition in range(len(self.conditions_list)):
            for roi in range(len(ROIs)):
                if abs(plotMatrices[each_condition][roi]) > maxY:
                    maxY = abs(plotMatrices[each_condition][roi])
                if abs(plotMatrices[each_condition][roi]) + plotMatricesErrors[each_condition][roi] > maxY:
                    maxY = abs(plotMatrices[each_condition][roi]) + plotMatricesErrors[each_condition][roi]
        plt.ylim([maxY * -1.25, maxY * 1.25])
        plt.legend(self.conditions_list, loc='upper right')
        plt.savefig('Phase-Amplitude Coupling.png')

    def circularCorrelations(self, label, but1, but2, but3, parent):
        label.grid_forget()
        but1.grid_forget()
        but2.grid_forget()
        but3.grid_forget()
        num_bins = 72
        bin_size = (2*(np.pi))/num_bins
        bins = np.arange((-1*np.pi), np.pi + bin_size, bin_size)

        amps = []
        amps_mean = []
        subjects = []

        for roi in range(len(ROIs)):
            amps.append([])
            amps_mean.append([])
        for each_condition in range(len(self.conditions_list)):
            subjects.append([])
            for subject in range(self.num_each_condition[each_condition]):
                subjects[each_condition].append(self.subjects_of_each_condition[each_condition][subject].getName())
        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                amps[roi].append(pd.DataFrame(index=bins, columns=subjects[each_condition]))
                amps[roi][each_condition].drop(amps[roi][each_condition].tail(1).index, inplace=True)
                amps_mean[roi].append(pd.DataFrame(index=bins, columns=['Average Amplitude']))
                amps_mean[roi][each_condition].drop(amps_mean[roi][each_condition].tail(1).index, inplace=True)
        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                for subject in range(self.num_each_condition[each_condition]):
                    for x in range(len(bins) - 1):
                        amps_above_lo_bound = np.where(self.subjects_of_each_condition[each_condition][subject].
                                                       getData().loc['%s' % ROIs[roi]].iloc[:, 1] >= bins[x])[0]
                        amps_below_hi_bound = np.where(self.subjects_of_each_condition[each_condition][
                                                           subject].getData().loc['%s' % ROIs[roi]].iloc[:, 1] < bins[
                            x+1])[0]
                        amps_below_hi_bound = set(amps_below_hi_bound)
                        amp_inds_in_this_bin = [amp_val for amp_val in amps_above_lo_bound if amp_val in
                                                 amps_below_hi_bound]
                        amps_in_this_bin = self.subjects_of_each_condition[each_condition][subject].getData().loc[
                            '%s' % ROIs[roi]].iloc[amp_inds_in_this_bin, 2]
                        amps[roi][each_condition].iloc[x, subject] = np.mean(amps_in_this_bin)
        bins = bins[:len(bins) - 1]

        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                amps[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
                amps[roi][each_condition].rename_axis("Amplitude", axis="columns")
                amps_mean[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
                amps_mean[roi][each_condition].rename_axis("Amplitude", axis="columns")
                for b in range(len(bins)):
                    amps_mean[roi][each_condition].iloc[b] = amps[roi][each_condition].iloc[b, :].mean()

        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                amps_mean[roi][each_condition].iloc[:] = ((amps_mean[roi][each_condition].iloc[:] -
                                                           amps_mean[roi][each_condition].iloc[:].mean()) / amps_mean[
                                                                roi][each_condition].iloc[:].std())

        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                fig = plt.figure(figsize=(8, 8))
                ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
                ax.bar(bins, amps_mean[roi][each_condition].iloc[:, 0], width=bins[1] - bins[0], bottom=0.0)
                plt.title("Phase Amplitude Coupling")
                plt.savefig('Phase-Amplitude Coupling Circular_%s_BA %s.png' % (self.conditions_list[each_condition],
                                                                                ROIs[roi]))

        raw_data = []
        df_to_export = []
        for roi in range(len(ROIs)):
            df_to_export.append([])
            for each_condition in range(len(self.conditions_list)):
                df_to_export[roi].append(pd.concat([amps[roi][each_condition], amps_mean[roi][each_condition]], axis=1))
                df_to_export[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
                df_to_export[roi][each_condition].rename_axis("Amplitude", axis="columns")
        for each_condition in range(len(self.conditions_list)):
            raw_data.append(pd.ExcelWriter(("%s_Circular Graph Raw Data.xlsx" % self.conditions_list[each_condition]),
                                           engine='xlsxwriter'))
        for each_condition in range(len(self.conditions_list)):
            for roi in range(len(ROIs)):
                df_to_export[roi][each_condition].to_excel(raw_data[each_condition], sheet_name="BA %s" % ROIs[roi],
                                                           index_label="Phase Range (Lower Bound)")
        for each_condition in range(len(self.conditions_list)):
            raw_data[each_condition].save()

    def bothCorrelations(self, label, but1, but2, but3, parent):
        label.grid_forget()
        but1.grid_forget()
        but2.grid_forget()
        but3.grid_forget()
        plotMatrices = []
        plotMatricesErrors = []
        width = 0.35
        for each_condition in range(len(self.conditions_list)):
            plotMatrices.append([0] * len(ROIs))
            plotMatricesErrors.append([0] * len(ROIs))
        for each_condition in range(len(self.conditions_list)):
            for roi in range(len(ROIs)):
                plotMatrices[each_condition][roi] = self.averageMatrices[each_condition][
                    str(ROIs[roi])].mean()
                plotMatricesErrors[each_condition][roi] = 2 * self.averageMatrices[each_condition][
                    str(ROIs[roi])].sem()
        y_pos = np.arange(0, len(self.conditions_list) * 0.5 * len(ROIs), len(self.conditions_list) * 0.5)
        fig, ax = plt.subplots(figsize=(10, 7))
        plt.figure(1)
        for plot in range(len(plotMatrices)):
            if plot == 0:
                plt.bar(y_pos, plotMatrices[plot], width, alpha=0.5, yerr=plotMatricesErrors[plot],
                        capsize=10)
            else:
                plt.bar([p + width * plot for p in y_pos], plotMatrices[plot], width, alpha=0.5,
                        yerr=plotMatricesErrors[plot], capsize=10)
        ax.set_xticks([p + (0.5 * (len(self.conditions_list) - 1)) * width for p in y_pos])
        ax.set_xticklabels(self.chosenROIs)
        ax.set_ylabel('Correlation Coefficient')
        ax.set_title('%s-%s Coupling' % (self.chosenFrequencies[1], self.chosenFrequencies[2]))
        maxY = 0
        for each_condition in range(len(self.conditions_list)):
            for roi in range(len(ROIs)):
                if abs(plotMatrices[each_condition][roi]) > maxY:
                    maxY = abs(plotMatrices[each_condition][roi])
                if abs(plotMatrices[each_condition][roi]) + plotMatricesErrors[each_condition][roi] > maxY:
                    maxY = abs(plotMatrices[each_condition][roi]) + plotMatricesErrors[each_condition][roi]
        plt.ylim([maxY * -1.25, maxY * 1.25])
        plt.legend(self.conditions_list, loc='upper right')
        plt.savefig('Phase-Amplitude Coupling.png')

        num_bins = 72
        bin_size = (2 * (np.pi)) / num_bins
        bins = np.arange((-1 * np.pi), np.pi + bin_size, bin_size)

        amps = []
        amps_mean = []
        subjects = []

        for roi in range(len(ROIs)):
            amps.append([])
            amps_mean.append([])
        for each_condition in range(len(self.conditions_list)):
            subjects.append([])
            for subject in range(self.num_each_condition[each_condition]):
                subjects[each_condition].append(self.subjects_of_each_condition[each_condition][subject].getName())
        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                amps[roi].append(pd.DataFrame(index=bins, columns=subjects[each_condition]))
                amps[roi][each_condition].drop(amps[roi][each_condition].tail(1).index, inplace=True)
                amps_mean[roi].append(pd.DataFrame(index=bins, columns=['Average Amplitude']))
                amps_mean[roi][each_condition].drop(amps_mean[roi][each_condition].tail(1).index, inplace=True)
        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                for subject in range(self.num_each_condition[each_condition]):
                    for x in range(len(bins) - 1):
                        amps_above_lo_bound = np.where(self.subjects_of_each_condition[each_condition][subject].
                                                       getData().loc['%s' % ROIs[roi]].iloc[:, 1] >= bins[x])[0]
                        amps_below_hi_bound = np.where(self.subjects_of_each_condition[each_condition][
                                                           subject].getData().loc['%s' % ROIs[roi]].iloc[:, 1] < bins[
                                                           x + 1])[0]
                        amps_below_hi_bound = set(amps_below_hi_bound)
                        amp_inds_in_this_bin = [amp_val for amp_val in amps_above_lo_bound if amp_val in
                                                amps_below_hi_bound]
                        amps_in_this_bin = self.subjects_of_each_condition[each_condition][subject].getData().loc[
                            '%s' % ROIs[roi]].iloc[amp_inds_in_this_bin, 2]
                        amps[roi][each_condition].iloc[x, subject] = np.mean(amps_in_this_bin)
        bins = bins[:len(bins) - 1]

        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                amps[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
                amps[roi][each_condition].rename_axis("Amplitude", axis="columns")
                amps_mean[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
                amps_mean[roi][each_condition].rename_axis("Amplitude", axis="columns")
                for b in range(len(bins)):
                    amps_mean[roi][each_condition].iloc[b] = amps[roi][each_condition].iloc[b, :].mean()

        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                amps_mean[roi][each_condition].iloc[:] = ((amps_mean[roi][each_condition].iloc[:] -
                                                           amps_mean[roi][each_condition].iloc[:].mean()) / amps_mean[
                                                                                                                roi][
                                                                                                                each_condition].iloc[
                                                                                                            :].std())

        for roi in range(len(ROIs)):
            for each_condition in range(len(self.conditions_list)):
                fig = plt.figure(figsize=(8, 8))
                ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
                ax.bar(bins, amps_mean[roi][each_condition].iloc[:, 0], width=bins[1] - bins[0], bottom=0.0)
                plt.title("Phase Amplitude Coupling")
                plt.savefig('Phase-Amplitude Coupling Circular_%s_BA %s.png' % (self.conditions_list[each_condition],
                                                                                ROIs[roi]))

        raw_data = []
        df_to_export = []
        for roi in range(len(ROIs)):
            df_to_export.append([])
            for each_condition in range(len(self.conditions_list)):
                df_to_export[roi].append(pd.concat([amps[roi][each_condition], amps_mean[roi][each_condition]], axis=1))
                df_to_export[roi][each_condition].rename_axis("Phase Range (Lower Bound)")
                df_to_export[roi][each_condition].rename_axis("Amplitude", axis="columns")
        for each_condition in range(len(self.conditions_list)):
            raw_data.append(pd.ExcelWriter(("%s_Circular Graph Raw Data.xlsx" % self.conditions_list[each_condition]),
                                           engine='xlsxwriter'))
        for each_condition in range(len(self.conditions_list)):
            for roi in range(len(ROIs)):
                df_to_export[roi][each_condition].to_excel(raw_data[each_condition], sheet_name="BA %s" % ROIs[roi],
                                                           index_label="Phase Range (Lower Bound)")
        for each_condition in range(len(self.conditions_list)):
            raw_data[each_condition].save()

        finished = tk.Label(text="Your graphs have been created and saved successfully. The raw data has been exported "
                                 "to excel files.")
        finished.grid(row=0, column=0)
        endButton = tk.Button(text="Quit", command=lambda: quit)
        endButton.grid(row=1, column=0)


app = Application()
app.mainloop()
