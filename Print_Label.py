# Czujnik ciśnienia - dodane
# Komora temperaturowa - w trakcie
# Komora klimatyczna  - w trakcie
# Czujnik drogi - w trakcie

import pyodbc
import socket
import os
import PE_Database as PE
import MP2_Database as MP2
from tkinter import *


sensorInventoryNumber = "ZD5224"
cursorPE = PE.connectWithDatabase()
pathToSchemeLabel = "//wplcswroclaw12m/pdp/01_Team's/TQC_MTS/Kalibracje/FAQ/Program kalibracyjny/"
pathToPrintLabel = r"D:\xInventoryNumber.txt"


def checkSensorIsExist(inventoryNumber, cursor):
    if PE.getInventoryNumber(inventoryNumber, cursor) is None:
        return False
    else:
        return True


def preperePathToLabelSheme(inventoryNumber, cursor, path):
    type = PE.getType(inventoryNumber, cursor)
    producent = PE.getProducent(inventoryNumber, cursor)
    if type == "Czujnik ciśnienia":
        return os.path.join(path, "Label Pressure Sensor.txt")
    elif type == "Czujnik drogi":
        return os.path.join(path, "Label Distance Sensor.txt")
    elif type == "Komora temperaturowa":
        return os.path.join(path, "Label Temperature Chamber.txt")
    elif type == "Komora klimatyczna":
        return os.path.join(path, "Label Climate Chamber.txt")
    elif type == "Czujnik siły":
        return os.path.join(path, "Label Force Sensor.txt")
    elif type == "Zestaw pomiarowy":
        if producent == "DEWEsoft":
            return os.path.join(path, "Label DEWEsoft Measurement Set.txt")
        else:
            return os.path.join(path, "Label Measurement Set.txt")


def openLabelSheme(path):
    if os.path.isfile(path):
        file = open(path)
        label = file.read()
        file.close()
        return label
    else:
        print("Taki plik nie istnieje!")


def replaceInventoryNumber(label, inventoryNumber):
    if "xInventoryNumber" in label:
        return label.replace("xInventoryNumber", inventoryNumber)
    else:
        return label


def replaceModel(label, inventoryNumber, cursor):
    model = PE.getModel(inventoryNumber, cursor)
    if "xModel" in label:
        return label.replace("xModel", model)
    else:
        return label


def replaceSerialNumber(label, inventoryNumber, cursor):
    serialNumber = PE.getSerialNumber(inventoryNumber, cursor)
    if "xSerialNumber" in label:
        return label.replace("xSerialNumber", serialNumber)
    else:
        return label


def replaceCalibrationDate(label, inventoryNumber, cursor):
    calibrationDate = PE.getCalibrationDate(inventoryNumber, cursor)
    if "CalibrationDate" in label:
        return label.replace("xCalibrationDate", calibrationDate.strftime("%m.%Y"))
    else:
         return label


def replaceCalibrationPlace(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    unitMeasSignal = PE.getUnitMeasSignal(inventoryNumber, cursor)
    maxMeasSignal = PE.getMaxMeasSignal(inventoryNumber, cursor)
    if "xCalibrationPlace" in label:
        if type == "Czujnik ciśnienia":
            if "bar a" is unitMeasSignal or "mbar a" is unitMeasSignal:
                return label.replace("xCalibrationPlace", "External")
            else:
                if maxMeasSignal > 35:
                    return label.replace("xCalibrationPlace", "External")
                else:
                    return label.replace("xCalibrationPlace", "Internal")
        else:
            return label.replace("xCalibrationPlace", "Internal")
    else:
        return label


def replaceMinAnalogSignal(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    minAnalogSignal = PE.getMinAnalogSignal(inventoryNumber, cursor)
    if "xMinAnalogSignal" in label:
        if type == "Czujnik ciśnienia":
            if minAnalogSignal % 1 == 0:
                return label.replace("xMinAnalogSignal", str(int(minAnalogSignal)))
            else:
                return label.replace("xMinAnalogSignal", int(minAnalogSignal))
        else:
            return label
    else:
        return label


def replaceMaxAnalogSignal(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    maxAnalogSignal = PE.getMaxAnalogSignal(inventoryNumber, cursor)
    if "xMaxAnalogSignal" in label:
        if type == "Czujnik ciśnienia":
            if maxAnalogSignal % 1 == 0:
                return label.replace("xMaxAnalogSignal", str(int(maxAnalogSignal)))
            else:
                return label.replace("xMaxAnalogSignal", int(maxAnalogSignal))
        else:
            return label
    else:
        return label


def replaceUnitAnalogSignal(label, inventoryNumber, cursor):
    unitAnalogSignal = PE.getUnitAnalogSignal(inventoryNumber, cursor)
    if "xUnitAnalogSignal" in label:
        if unitAnalogSignal == "":
            return label
        else:
            return label.replace("xUnitAnalogSignal", unitAnalogSignal)
    else:
        return label


def replaceMinMeasSignal(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    minMeasSignal = PE.getMinMeasSignal(inventoryNumber, cursor)
    if "xMinMeasSignal" in label:
        if type == "Czujnik ciśnienia":
            if minMeasSignal % 1 == 0:
                return label.replace("xMinMeasSignal", str(int(minMeasSignal)))
            else:
                return label.replace("xMinMeasSignal", int(minMeasSignal))
        else:
            return label
    else:
        return label


def replaceMaxMeasSignal(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    maxMeasSignal = PE.getMaxMeasSignal(inventoryNumber, cursor)
    if "xMaxMeasSignal" in label:
        if type == "Czujnik ciśnienia":
            if maxMeasSignal % 1 == 0:
                return label.replace("xMaxMeasSignal", str(int(maxMeasSignal)))
            else:
                return label.replace("xMaxMeasSignal", int(maxMeasSignal))
        else:
            return label
    else:
        return label


def replaceUnitMeasSignal(label, inventoryNumber, cursor):
    unitMeasSignal = PE.getUnitMeasSignal(inventoryNumber, cursor)
    if "xUnitMeasSignal" in label:
        if unitMeasSignal == "":
            return label
        else:
            return label.replace("xUnitMeasSignal", unitMeasSignal)
    else:
        return label


def replaceSqueezeRange(label):
    if "xSqueezeRange" in label:
        a = label.splitlines()
        count = 0
        for char in a:
            if "xSqueezeRange" in char:
                break
            count = count + 1
        if 1 <= len(a[count].split(';')[1]) <= 15:
            return label.replace("xSqueezeRange", "q100")
        elif 16 <= len(a[count].split(';')[1]) <= 20:
            return label.replace("xSqueezeRange", "q80")
        else:
            return label.replace("xSqueezeRange", "q60")
    else:
        return label


def replaceOperator(label):
    if "xOperator" in label:
        return label.replace("xOperator", os.getlogin()[0] + os.getlogin().lower()[1:])
    else:
        return label


def replaceSqueezeOperator(label):
    if "xSqueezeOperator" in label:
        lengthOperator = len(os.getlogin())
        if 1 <= lengthOperator <= 15:
            return label.replace("xSqueezeOperator", "q100")
        elif 16 <= lengthOperator <= 20:
            return label.replace("xSqueezeOperator", "q80")
        else:
            return label.replace("xSqueezeOperator", "q60")
    else:
        return label


def replaceClass(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    unitMeasSignal = PE.getUnitMeasSignal(inventoryNumber, cursor)
    maxMeasSignal = PE.getMaxMeasSignal(inventoryNumber, cursor)
    if "xClass" in label:
        if type == "Czujnik ciśnienia":
            if "bar a" is unitMeasSignal or "mbar a" is unitMeasSignal:
                return label.replace("xClass", '')
            else:
                if maxMeasSignal > 35:
                    return label.replace("xClass", "")
                else:
                    return label.replace("xClass", "")
        else:
            return label
    else:
        return label


def replaceErrorValue(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    unitMeasSignal = PE.getUnitMeasSignal(inventoryNumber, cursor)
    maxMeasSignal = PE.getMaxMeasSignal(inventoryNumber, cursor)
    if "xErrorValue" in label:
        if type == "Czujnik ciśnienia":
            if "bar a" is unitMeasSignal or "mbar a" is unitMeasSignal:
                return label.replace("xErrorValue", '')
            else:
                if maxMeasSignal > 35:
                    return label.replace("xErrorValue", "")
                else:
                    return label.replace("xErrorValue", "")
        else:
            return label.replace("xErrorValue", "")
    else:
        return label


def replaceSqueezeClass(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    unitMeasSignal = PE.getUnitMeasSignal(inventoryNumber, cursor)
    maxMeasSignal = PE.getMaxMeasSignal(inventoryNumber, cursor)
    if "xSqueezeClass" in label:
        if type == "Czujnik ciśnienia":
            if "bar a" is unitMeasSignal or "mbar a" is unitMeasSignal:
                return label.replace("xSqueezeClass", "q0")
            else:
                if maxMeasSignal > 35:
                    return label.replace("xSqueezeClass", "q0")
                else:
                    return label.replace("xSqueezeClass", "q0")
        else:
            return label
    else:
        return label


def replaceName(label, inventoryNumber, cursor):
    type = PE.getType(inventoryNumber, cursor)
    unitMeasSignal = PE.getUnitMeasSignal(inventoryNumber, cursor)
    if "xName" in label:
        if type == "Komora temperaturowa":
            return label.replace("xName", unitMeasSignal)
        elif type == "Komora klimatyczna":
            return label.replace("xName", unitMeasSignal)
    else:
        return label


def deleteLinesWitchQ0(label):
    a = label.splitlines()
    count = 0
    for char in a:
        if "q0" in char:
            a[count] = ""
        count = count + 1
    return '\n'.join(a)


def writeLabelToFile(label, inventoryNumber, path):
    path = path.replace("xInventoryNumber", inventoryNumber)
    file = open(path, "w+")
    file.write(label)
    file.close()


def printLabel(label, inventoryNumber):
    cmd = r"cmd /k copy /b D:\xInventoryNumber.txt \\xHost\Mach4"
    cmd = cmd.replace("xHost", socket.gethostname())
    cmd = cmd.replace("xInventoryNumber", inventoryNumber)
    os.system(cmd)


def removeFile(inventoryNumber, path):
    file = path.replace("xInventoryNumber", inventoryNumber)
    os.remove(file)


if checkSensorIsExist(sensorInventoryNumber, cursorPE):
    labelScheme = openLabelSheme(preperePathToLabelSheme(sensorInventoryNumber, cursorPE, pathToSchemeLabel))
    print(labelScheme)
    labelScheme = replaceInventoryNumber(labelScheme, sensorInventoryNumber)
    labelScheme = replaceModel(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceSerialNumber(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceCalibrationDate(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceCalibrationPlace(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceMinAnalogSignal(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceMaxAnalogSignal(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceUnitAnalogSignal(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceMinMeasSignal(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceMaxMeasSignal(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceUnitMeasSignal(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceOperator(labelScheme)
    labelScheme = replaceSqueezeOperator(labelScheme)
    labelScheme = replaceSqueezeRange(labelScheme)
    labelScheme = replaceClass(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceErrorValue(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceSqueezeClass(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = replaceName(labelScheme, sensorInventoryNumber, cursorPE)
    labelScheme = deleteLinesWitchQ0(labelScheme)
    writeLabelToFile(labelScheme, sensorInventoryNumber, pathToPrintLabel)
    #printLabel(labelScheme, sensorInventoryNumber)
    #removeFile(sensorInventoryNumber, pathToPrintLabel)
else:
    print("Nie ma takiego czujnika w bazie danych PE")

root = Tk()
root.title("Wydruk etykiet kalibracyjnych")

l = Label(root, text="\n Wprowadź numer inwentarzowy przyrządu pomiarowego,\n dla którego chcesz wydrukować etykietę kalibracyjną: ")
l.grid(row=0, column=0, padx=10, pady=5)

eInventoryNumber = Entry(root, width=35, borderwidth=2)
eInventoryNumber.grid(row=1, column=0, pady=5)
eInventoryNumber.get()


# Szablon tekstu po wyszukaniu:
# UŻYJ ETYKIETY %s !!!
# Wydrukuj etykietę kalibracyjną dla %s
# Numer inwentarzowy: %s
# Model: %s
# Numer seryjny: %s
# Producent: %s
# %s
#
#UŻYJ ETYKIETY %s !!!


def searchSensor():
    text = "UŻYJ ETYKIETY xSize !!! \n\n Wydrukuj etykietę kalibracyjną dla xType \n Numer inwentarzowy: xInventoryNumber \n" \
           " Model: xModel \n Numer seryjny: xSerialNumber \n Producent: xProducent \n\n " \
           " UŻYJ ETYKIETY xSize !!! \n"
    inventoryNumber = eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:]
    if PE.getInventoryNumber(inventoryNumber, cursorPE) is not None:
        type = PE.getType(inventoryNumber, cursorPE)
        if type == "Czujnik ciśnienia":
            text = text.replace("xSize", "20x20")
            text = text.replace("xType", "czujnika ciśnienia")
            text = text.replace("xInventoryNumber", inventoryNumber)
            text = text.replace("xModel", PE.getModel(inventoryNumber, cursorPE))
            text = text.replace("xSerialNumber", PE.getSerialNumber(inventoryNumber, cursorPE))
            text = text.replace("xProducent", PE.getProducent(inventoryNumber, cursorPE))

    else:
        text = "Taki czujnik nie istnieje"
    fSensorDescription = LabelFrame(root, text= "Opis przyrz przyrządu pomiarowego: ")
    fSensorDescription.grid(row=3, column=0,)
    bPrint = Button(fSensorDescription, text=text)
    bPrint.pack()

bFind = Button(root, text="Znajdź wprowadzony przyrząd pomiarowy", command=searchSensor)
bFind.grid(row=2, column=0, pady=5)


root.mainloop()