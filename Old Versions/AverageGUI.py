from tkinter import *


class HomePage:

    def __init__(self, master):

        homeLabel = Label(master, text="Data Organization\n\n""What kind of data are you working with?\n")
        homeLabel.pack()

        frame = Frame(master)
        frame.pack()

        self.menubar = Menu(master)
        self.menubar.add_command(label="Home", command=self.GoHome(frame))
        self.menubar.add_command(label="Quit", command=frame.quit)

        master.config(menu=self.menubar)

        self.averageButton = Button(
            frame, text="Average", command=master.show_frame(AverageFrame)
        )
        self.averageButton.pack(side=LEFT)

        self.connectivityButton = Button(frame, text="Connectivity", command=self.connectivity)
        self.connectivityButton.pack(side=RIGHT)



    def connectivity(self):
        print("this is connectivity data")

    def average(self):
        AverageOrganization(root)

    def GoHome(self, frame):
        frame.tkraise()

class AverageOrganization:

    def __init__(self, master):

        average_window = Toplevel(master)

        self.menubar = Menu(master)
        self.menubar.add_command(label="Home", command=self.GoHome(average_window))
        self.menubar.add_command(label="Quit", command=average_window.quit)

        master.config(menu=self.menubar)

        condition_list = LabelFrame(average_window, text="Please enter the conditions in your study, separated by comma"
                                                         "s. (e.g. Controls, Patients, etc.)", padx=5, pady=5)
        condition_list.pack(padx=10, pady=10)

        condition_getter = Entry(condition_list)
        condition_getter.pack()

        condition_getter.focus_set()

        def AfterGettingList():
            list_of_conditions = condition_getter.get()
            split_clist = [w.strip() for w in list_of_conditions.split(',')]
            print(split_clist)

        submit_conditions = Button(average_window, text="Submit", width=10, command=AfterGettingList)
        submit_conditions.pack()

    def GoHome(self, frame):
        frame.tkraise()


root = Tk()

HomePage(root)

root.mainloop()
