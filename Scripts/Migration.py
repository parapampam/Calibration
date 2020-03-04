import pyodbc
import os
import datetime
import Databases as Db
from tkinter import *

inventoryNumber = ""
pe = None
mp2 = None

def checkExistInDatabased(existInPE = True, existInMP2 = True ):
    if existInPE == True and existInMP2 == True:
        text = "Przyrząd pomiarowy jest już dodany do obydwu baz danych PE i MP2.\nNie można skopiować przyrządu pomiarowego" \
               " z bazy danych MP2 do bazy danych PE."
        bCopy.config(text="  Kopiuj przyrząd pomiarowy z bazy danych MP2 do bazy danych PE  ", state=DISABLED)
    elif existInPE == True and existInMP2 == False:
        text = "Przyrząd pomiarowy istnieje tylko w bazie danych PE.\nDo bazy danych MP2 może być tylko ręcznie."
        bCopy.config(text="  Kopiuj przyrząd pomiarowy z bazy danych MP2 do bazy danych PE  ", state=DISABLED)
    elif existInPE == False and existInMP2 == True:
        text = "Przyrząd pomiarowy istnieje tylko w bazie danych MP2.\nMożna go skopiować z bazy danych MP2 do bazy danych PE."
        bCopy.config(state=NORMAL, text="Kopiuj przyrząd pomiarowy " + inventoryNumber + " z bazy danych MP2 do bazy danych PE  ")
    else:
        text = "Przyrząd pomiarowy nie istnieje w żadnej z baz danych.\nDodaj najpierw przyrząd ręcznie do bazy danych MP2." \
               "\nA następnie skopiuj go do bazy danych PE za pomocą tego skryptu."
        bCopy.config(text="  Kopiuj przyrząd pomiarowy z bazy danych MP2 do bazy danych PE  ", state=DISABLED)
    lMeasurementInstrument.config(text=text)


def copyMeasurementInstrument(event):
    pe.addNewSensor(mp2.getModel(), mp2.getSerialNumber(), mp2.getProducent(), mp2.getCalibrationPeriod(),
                    mp2.getCalibrationDate(), "ns", mp2.getMinAnalogSignal(), mp2.getMaxAnalogSignal(),
                    mp2.getUnitAnalogSignal(), mp2.getMinMeasSignal(), mp2.getMaxMeasSignal(), mp2.getUnitMeasSignal(), mp2.getType())


def unitForCalibrationPeriod(calibrationPeriod):
    # Najdłuższy czasookres kalibracji to 3 lata.
    if calibrationPeriod == 1:
        return " rok"
    elif calibrationPeriod in range(2, 5):
        return " lata"
    else:
        return " lat"


def searchMeasurementInstrument(event):
    global inventoryNumber
    global pe
    global mp2
    inventoryNumber = eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:]
    pe = Db.PE(inventoryNumber)
    mp2 = Db.MP2(inventoryNumber)
    checkExistInDatabased(pe.measurementInstrumentInDatabase(), mp2.measurementInstrumentInDatabase())
    equelMeasurementInstrumentInBothDatabases(mp2)
    equelMeasurementInstrumentInBothDatabases(pe)

def equelMeasurementInstrumentInBothDatabases(x):
    if x.measurementInstrumentInDatabase():
        text = "xDatabase\n\nxType\nxInventoryNumber\nxModel\nxSerialNumber\nxProducent\nxCalibrationDate\nxCalibrationPeriod\n\n"
        text = text.replace("xDatabase",
                            "Informacje o przyrządzie pomiarowym\nw bazie danych " + str(x.__class__.__name__) + ": ")
        text = text.replace("xType", "Typ przyrządu pomiarowego: " + x.getType())
        text = text.replace("xInventoryNumber", "Numer inwentarzowy: " + x.getInventoryNumber())
        text = text.replace("xModel", "Kod modelu: " + x.getModel())
        text = text.replace("xSerialNumber", "Numer seryjny: " + x.getSerialNumber())
        text = text.replace("xProducent", "Producent: " + x.getProducent())
        if "naprawa" in x.getStatus() or "archiwum" in x.getStatus():
            text = text.replace("xCalibrationDate", "Data kalibracji: w archiwum ")
        else:
            text = text.replace("xCalibrationDate", "Data kalibracji: " + x.getCalibrationDate().strftime("%m.%Y"))
        text = text.replace("xCalibrationPeriod",
                            "Czasookres kalibracji: " + str(x.getCalibrationPeriod()) + unitForCalibrationPeriod(
                                int(x.getCalibrationPeriod())))
    else:
        text = "Informacje o przyrządzie pomiarowym\nw bazie danych " + str(x.__class__.__name__) + \
               ":\n\n\n\n\nNie istnieje\n\n\n\n\n"
    if str(x.__class__.__name__) == "MP2":
        lMeasurementInstrumentMP2.config(text=text)
    else:
        lMeasurementInstrumentPE.config(text=text)
print(inventoryNumber)
window = Tk()
window.title("Kopiowanie przyrządu pomiarowego z bazy danych MP2 do bazy danych PE")

lInformation = Label(window, text="\nWprowadź numer inwentarzowy przyrządu pomiarowego,\n  który chcesz skopiować"
                                  " z bazy danych MP2 do bazy danych PE: \n",
                     width=82, borderwidth=2, relief="groove")
lInformation.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

eInventoryNumber = Entry(window, width=35, borderwidth=2)
eInventoryNumber.insert(END, "Wprowadź TUTAJ numer inwentarzowy")
eInventoryNumber.grid(row=1, column=0, columnspan=2, pady=5)
eInventoryNumber.get()
eInventoryNumber.bind("<KeyRelease>", searchMeasurementInstrument)


lMeasurementInstrument = Label(window, text="\nTutaj pojawi się informacja po wyszukaniu czujnika\n",
                               width=82, height=3, borderwidth=2, relief="groove")
lMeasurementInstrument.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

lMeasurementInstrumentMP2 = Label(window, text="Informacje o przyrządzie pomiarowym\nw bazie danych MP2:"
                                               "\n\n\n\n\n...\n\n\n\n\n",
                                  width=50, borderwidth=2, relief="groove")
lMeasurementInstrumentMP2.grid(row=4, column=0, padx=0, pady=5)

lMeasurementInstrumentPE = Label(window, text="Informacje o przyrządzie pomiarowym\nw bazie danych PE:"
                                              "\n\n\n\n\n...\n\n\n\n\n",
                                 width=50, borderwidth=2, relief="groove")
lMeasurementInstrumentPE.grid(row=4, column=1, padx=0, pady=5)

bCopy = Button(window, text="  Kopiuj przyrząd pomiarowy z bazy danych MP2 do bazy danych PE  ")
bCopy.bind("<Button-1>", copyMeasurementInstrument)
bCopy.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
bCopy.config(state=DISABLED)

window.mainloop()
