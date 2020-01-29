from tkinter import *
import PE_Database as PE
import MP2_Database as MP2

root = Tk()

# Creating a Label Widget
myLabel = Label(root, text=str(MP2.lastAddedSensorInMP2Database(MP2.connectWithDatabase())))
# Showing it onto the screen
myLabel.pack()

root.mainloop()