import pyodbc
import os
import datetime
import Databases as Db
from tkinter import *

inventoryNumber = ""
pe = None
mp2 = None

def unitForCalibrationPeriod(calibrationPeriod):
    # Najdłuższy czasookres kalibracji to 3 lata.
    if calibrationPeriod == 1:
        return " rok"
    elif calibrationPeriod in range(2, 5):
        return " lata"
    else:
        return " lat"

def copyMeasurementInstrument(event):
    pe.addNewSensor(mp2.getModel(), mp2.getSerialNumber(), mp2.getProducent(), mp2.getCalibrationPeriod(),
                    mp2.getCalibrationDate(), "ns", mp2.getMinAnalogSignal(), mp2.getMaxAnalogSignal(), mp2.getUnitAnalogSignal(),
                    mp2.getMinMeasSignal(), mp2.getMaxMeasSignal(), mp2.getUnitMeasSignal(), mp2.getType())

def checkExistInDatabased(existInPE = True, existInMP2 = True ):
    #inventoryNumber = eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:]
    if existInPE == True and existInMP2 == True:
        text = "Przyrząd pomiarowy jest już dodany do obydwu baz danych PE i MP2.\nNie można skopiować przyrządu pomiarowego" \
               " z bazy danych MP2 do bazy danych PE."
        bCopy.config(text=" Kopiuj przyrząd pomiarowy ", state=DISABLED)
    elif existInPE == True and existInMP2 == False:
        text = "Przyrząd pomiarowy istnieje tylko w bazie danych PE.\nDo bazy danych MP2 może być tylko ręcznie."
        bCopy.config(text=" Kopiuj przyrząd pomiarowy ", state=DISABLED)
    elif existInPE == False and existInMP2 == True:
        text = "Przyrząd pomiarowy istnieje tylko w bazie danych MP2.\nMożna go skopiować z bazy danych MP2 do bazy danych PE."
        bCopy.config(state=NORMAL, text="Kopiuj przyrząd pomiarowy " + inventoryNumber)
    else:
        text = "Przyrząd pomiarowy nie istnieje w żadnej z baz danych.\nDodaj najpierw przyrząd ręcznie do bazy danych MP2." \
               "\nA następnie skopiuj go do bazy danych PE za pomocą tego skryptu."
        bCopy.config(text=" Kopiuj przyrząd pomiarowy ", state=DISABLED)
    lMeasurementInstrument.config(text=text)



def searchMeasurementInstrument(event):
    inventoryNumber = eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:]
    pe = Db.PE(inventoryNumber)
    mp2 = Db.MP2(inventoryNumber)
    checkExistInDatabased(pe.measurementInstrumentInDatabase(), mp2.measurementInstrumentInDatabase())
    equelMeasurementInstrumentInBothDatabases(mp2, pe)


def equelMeasurementInstrumentInBothDatabases(mp2, pe):
    text = "Informacje o przyrządzie pomiarowym\nw bazie danych xDatabase:\n\nTyp przyrządu pomiarowego: xType\n" \
           "Numer inwentarzowy: xInventoryNumber\nModel: xModel\nNumer seryjny: xSerialNumber\nProducent: xProducent\n" \
           "Data kalibracji: xCalibrationDate\nCzasookres kalibracji: xCalibrationPeriod\n"

    if mp2.measurementInstrumentInDatabase() == True:
        textMP2 = text.replace("xDatabase", "MP2")
        textMP2 = textMP2.replace("xType", mp2.getType())
        textMP2 = textMP2.replace("xInventoryNumber", mp2.getInventoryNumber())
        textMP2 = textMP2.replace("xModel", mp2.getModel())
        textMP2 = textMP2.replace("xSerialNumber", mp2.getSerialNumber())
        textMP2 = textMP2.replace("xProducent", mp2.getProducent())
        textMP2 = textMP2.replace("xCalibrationDate", str(mp2.getCalibrationDate()))
        textMP2 = textMP2.replace("xCalibrationPeriod", mp2.getCalibrationPeriod() + unitForCalibrationPeriod(int(mp2.getCalibrationPeriod())))
        lMeasurementInstrumentMP2.config(text=textMP2)
    else:
        pass

    if pe.measurementInstrumentInDatabase() == True:
        textPE = text.replace("xDatabase", "PE")
        textPE = textPE.replace("xType", pe.getType())
        textPE = textPE.replace("xInventoryNumber", pe.getInventoryNumber())
        textPE = textPE.replace("xModel", pe.getModel())
        textPE = textPE.replace("xSerialNumber", pe.getSerialNumber())
        textPE = textPE.replace("xProducent", pe.getProducent())
        textPE = textPE.replace("xCalibrationDate", str(pe.getCalibrationDate()))
        textPE = textPE.replace("xCalibrationPeriod", str(pe.getCalibrationPeriod()) + str(unitForCalibrationPeriod(pe.getCalibrationPeriod())))
        lMeasurementInstrumentPE.config(text=textPE)
    else:
        pass


print(inventoryNumber)
window = Tk()
window.title("Kopiowanie przyrządu pomiarowego z bazy danych MP2 do bazy danych PE")

lInformation = Label(window, text="\nWprowadź numer inwentarzowy przyrządu pomiarowego,\n  który chcesz skopiować"
                                  " z bazy danych MP2 do bazy danych PE: \n",
                     width=72, borderwidth=2, relief="groove")
lInformation.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

eInventoryNumber = Entry(window, width=35, borderwidth=2)
eInventoryNumber.insert(END, "Wprowadź TUTAJ numer inwentarzowy")
eInventoryNumber.grid(row=1, column=0, columnspan=2, pady=5)
eInventoryNumber.get()
eInventoryNumber.bind("<KeyRelease>", searchMeasurementInstrument)


lMeasurementInstrument = Label(window, text="\nTutaj pojawi się informacja po wyszukaniu czujnika\n",
                               width=72, height=3, borderwidth=2, relief="groove")
lMeasurementInstrument.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

lMeasurementInstrumentMP2 = Label(window, text="Informacje o przyrządzie pomiarowym\nw bazie danych MP2:\n...",
                                  width=35, borderwidth=2, relief="groove")
lMeasurementInstrumentMP2.grid(row=4, column=0, padx=0, pady=5)

lMeasurementInstrumentPE = Label(window, text="Informacje o przyrządzie pomiarowym\nw bazie danych PE:\n...",
                                 width=35, borderwidth=2, relief="groove")
lMeasurementInstrumentPE.grid(row=4, column=1, padx=0, pady=5)

bCopy = Button(window, text=" Kopiuj przyrząd pomiarowy ")
bCopy.bind("<Button-1>", copyMeasurementInstrument)
bCopy.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
bCopy.config(state=DISABLED)

window.mainloop()
