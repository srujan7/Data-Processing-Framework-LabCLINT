import numpy as np
from pathlib import Path

def askConditions(conditions_list):
    while True:
        try:
            conditions = input("Please enter the conditions in your study, separated by commas (e.g. Controls, Patients).\n")
            conditions_split = [w.strip() for w in conditions.split(',')]
            conditions_list
            conditions_list = list(map(str, conditions_split))
            break
        except:
            print("\nYour input is not recognized. Please try again.")
            conditions = input("\nPlease enter the conditions in your study, separated by commas (e.g. Controls, Patients).\n")
            conditions_split = conditions.split(",")
            conditions_list = list(map(str, conditions_split))

    return conditions_list

def askNumEachC(conditions_list, num_each_condition):
    # Request user to input number of each condition in their experiment to process data appropriately
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

    return num_each_condition


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
        backwards = str(file)[::-1]
        backwards = backwards.split('\\')
        forwards = backwards[0][::-1]
        forwards = forwards.split('.')
        self.name = forwards[0]

        with open(file) as f:
            for i,l in enumerate(f):
                pass
            r = i+1

        self.data = np.zeros(r,[])
        self.data = np.loadtxt(file)
        print(self.data)

        f.close()

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
