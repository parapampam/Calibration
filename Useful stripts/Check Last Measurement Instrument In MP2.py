import pyodbc
import Databases as Db
from tkinter import *

window = Tk()
window.title("Sprawdź kod obiektu ostatniego przyrządu pomiarowego w bazie danych MP2")

myLabel = Label(window, text=("\nKod obiektu ostatnio dodanego przyrzyądzu pomiarowego to: \n\n"
                              + str(Db.MP2.getLastMeasurementInstrumentInDatabase(Db.MP2())))
                + "\n")
myLabel.pack(padx=20)

window.mainloop()
