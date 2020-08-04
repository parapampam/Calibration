import Databases as Db
from tkinter import *

window = Tk()
window.title("Sprawdź kod obiektu ostatniego przyrządu pomiarowego w bazie danych MP2")

myLabel = Label(window, text=("\nKod obiektu ostatnio dodanego przyrządu pomiarowego to: \n\n"
                              + str(Db.MP2().get_last_leasurement_instrument()))
                + "\n")
myLabel.pack(padx=20)

window.mainloop()
