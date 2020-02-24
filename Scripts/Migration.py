import pyodbc
import os
import datetime
import Databases as Db
from tkinter import *


def copyMeasurementInstrument(event):
    print("rozocznij kopiowanie")

def checkExistInDatabased(existInPE = True, existInMP2 = True ):
    inventoryNumber = eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:]
    if existInPE == True and existInMP2 == True:
        text = "Przyrząd pomiarowy jest już dodany do obydwu baz danych: PE i MP2.\nNie można skopiować przyrządu pomiarowego" \
               " z bazy danych MP2 do bazy danych PE."
    elif existInPE == True and existInMP2 == False:
        text = "Przyrząd pomiarowy istnieje tylko w bazie danych PE.\nDo bazy danych MP2 może być tylko ręcznie."
    elif existInPE == False and existInMP2 == True:
        text = "Przyrząd pomiarowy istnieje tylko w bazie danych MP2.\nMożna go skopiować z bazy danych MP2 do bazy danych PE."
        bCopy = Button(window, text="Kopiuj przyrząd pomiarowy " + inventoryNumber + "\n z bazy danych MP2 do bazy danych PE")
        bCopy.bind("<Return>", copyMeasurementInstrument)
        bCopy.bind("<Button-1>", copyMeasurementInstrument)
        bCopy.grid(row=3, column=0, padx=10, pady=10)
    else:
        text = "Przyrząd pomiarowy nie istnieje w żadnej z baz danych.\nDodaj najpierw przyrząd ręcznie do bazy danych MP2." \
               "\nA następnie skopiuj go do bazy danych PE za pomocą tego skryptu."
    lMeasurementInstrument = Label(window, text=text)
    lMeasurementInstrument.grid(row=2, column=0, padx=10, pady=10)


def searchMeasurementInstrument(event):
    inventoryNumber = eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:]
    pe = Db.PE(inventoryNumber)
    mp2 = Db.MP2(inventoryNumber)
    checkExistInDatabased(pe.measurementInstrumentInDatabase(), mp2.measurementInstrumentInDatabase())



window = Tk()
window.title("Kopiowanie przyrządu pomiarowego z bazy danych MP2 do bazy danych PE")
lInformation = Label(window, text="\nWprowadź numer inwentarzowy przyrządu pomiarowego,\nktóry chcesz skopiować"
                                  " z bazy danych MP2 do bazy danych PE:")

lInformation.pack()
lInformation.grid(row=0, column=0, padx=10, pady=5)

eInventoryNumber = Entry(window, width=10, borderwidth=2)
eInventoryNumber.bind("<Return>", searchMeasurementInstrument)
eInventoryNumber.grid(row=1, column=0, pady=5)
eInventoryNumber.get()

window.mainloop()
