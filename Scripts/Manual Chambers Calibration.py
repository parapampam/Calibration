from tkinter import *
import Databases as Db
import Template


from random import seed, random

eSetTemperature = ["setTemperature1", "setTemperature2", "setTemperature3", "setTemperature4", "setTemperature5",
                   "setTemperature6", "setTemperature7", "setTemperature8", "setTemperature9", "setTemperature10",
                   "setTemperature11", "setTemperature12", "setTemperature13", "setTemperature14", "setTemperature15"]

eReadVaisalaTemperature = ["readVaisalaTemperature1", "readVaisalaTemperature2", "readVaisalaTemperature3",
                           "readVaisalaTemperature4", "readVaisalaTemperature5", "readVaisalaTemperature6",
                           "readVaisalaTemperature7", "readVaisalaTemperature8", "readVaisalaTemperature9",
                           "readVaisalaTemperature10", "readVaisalaTemperature11", "readVaisalaTemperature12",
                           "readVaisalaTemperature13", "readVaisalaTemperature14", "readVaisalaTemperature15"]

eReadChamberTemperature = ["readChamberTemperature1", "readChamberTemperature2", "readChamberTemperature3",
                           "readChamberTemperature4", "readChamberTemperature5", "readChamberTemperature6",
                           "readChamberTemperature7", "readChamberTemperature8", "readChamberTemperature9",
                           "readChamberTemperature10", "readChamberTemperature11", "readChamberTemperature12",
                           "readChamberTemperature13", "readChamberTemperature14", "readChamberTemperature15"]

eDifferenceTemperature = ["differenceTemperature1", "differenceTemperature2", "differenceTemperature3",
                          "differenceTemperature4", "differenceTemperature5", "differenceTemperature6",
                          "differenceTemperature7", "differenceTemperature8", "differenceTemperature9",
                          "differenceTemperature10", "differenceTemperature11", "differenceTemperature12",
                          "differenceTemperature13", "differenceTemperature14", "differenceTemperature15"]

eErrorTemperature = ["errorTemperature1", "errorTemperature2", "errorTemperature3", "errorTemperature4",
                     "errorTemperature5", "errorTemperatur6", "errorTemperature7", "errorTemperature8",
                     "errorTemperature9", "errorTemperature10", "errorTemperature11", "errorTemperature12",
                     "errorTemperature13", "errorTemperature14", "errorTemperature15"]


def searchChamber(event):
    text = ""
    varInventoryNumber.set(eInventoryNumber.get())
    pe = Db.PE(varInventoryNumber.get())
    if Db.PE.measurementInstrumentInDatabase(pe):
        chamberType = pe.getType()
        if "Komora temperaturowa" in chamberType:
            text = "To jest komora temperaturowa"
        elif "Komora klimatyczna" in chamberType:
            text = "To jest komora klimatyczna"
        elif "Komora solna" in chamberType:
            text = "To jest komora solna"
        elif "Komora szokowa" in chamberType:
            text = "To jest komora szokowa"
        elif "Piecyk" in chamberType:
            text = "To jest piecyk"
        else:
            text = "To nie jest komora"
    else:
        text = "Przyrząd pomiarowy o takim numerze inwentarzowym nie istnieje"
    lChamberInfo.config(text=text)


def calc(event):
    for i in range(len(eSetTemperature)):
        eDifferenceTemperature[i].config(state=NORMAL)
        eDifferenceTemperature[i].delete(0, END)
        eDifferenceTemperature[i].insert(0, round(float(eReadChamberTemperature[i].get())
                                                  - float(eReadVaisalaTemperature[i].get()), 2))
        eDifferenceTemperature[i].config(state=DISABLED)

    for i in range(len(eSetTemperature)):
        eErrorTemperature[i].config(state=NORMAL)
        eErrorTemperature[i].delete(0, END)
        eErrorTemperature[i].insert(0, round(float(eDifferenceTemperature[i].get())*100/((float(eSetTemperature[14].get())-float(eSetTemperature[0].get()))), 2))
        eErrorTemperature[i].config(state=DISABLED)



def randomAndRound(n):
    seed(n)
    return round(random(), 2)

def printReport(event):
    varInventoryNumber.set(eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:])
    pe = Db.PE(varInventoryNumber.get())
    report = Template.Report(pe.inventoryNumber)
    text = report.readCalibrationReportTemplate(pe.getType())
    text = report.replaceInventoryNumber(text)
    text = report.replaceModel(text, pe.getModel())
    text = report.replaceSerialNumber(text, pe.getSerialNumber())
    text = report.replaceProducent(text, pe.getProducent())
    text = report.replaceCalibrationDate(text)
    text = report.replaceCertificateNumber(text)
    text = report.replaceType(text, pe.getType())
    text = report.replaceCalibrationRange(text, eSetTemperature[0].get(), eSetTemperature[14].get(), "°C")
    #print(text)

    measurement = report.readMeasurementReportTemplate(pe.getType())
    measurement = report.replaceInventoryNumber(measurement)
    measurement = report.replacePointsInMeasurementTable(measurement, eReadVaisalaTemperature, "a")
    measurement = report.replacePointsInMeasurementTable(measurement, eReadChamberTemperature, "b")
    measurement = report.replacePointsInMeasurementTable(measurement, eDifferenceTemperature, "c")
    measurement = report.replacePointsInMeasurementTable(measurement, eErrorTemperature, "d")
    print(measurement)



window = Tk()
window.title("Ręczna kalibracja komór")

varInventoryNumber = StringVar()

lInformation = Label(window,
                     text="\nProgram przeznaczony do ręcznej kalibracji komór\nWprowadz numer inwentarzowy komory, którą chcesz kalibrować: \n")
lInformation.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

eInventoryNumber = Entry(window)
eInventoryNumber.grid(row=1, column=0, columnspan=5, padx=5, pady=5)
eInventoryNumber.get()
eInventoryNumber.bind("<KeyRelease>", searchChamber)

lChamberInfo = Label(window, text="")
lChamberInfo.grid(row=2, column=0, columnspan=5)

fSetTemperature = LabelFrame(window, text="Temperatura\nzadana\n[°C]", padx=5, pady=5)
fSetTemperature.grid(row=3, column=0)
for i in range(len(eSetTemperature)):
    if i in range(0, 3):
        x = -40
    elif i in range(3, 6):
        x = 40
    elif i in range(6, 9):
        x = 80
    elif i in range(9, 12):
        x = 110
    elif i in range(12, 16):
        x = 140
    else:
        x = -88
    eSetTemperature[i] = Entry(fSetTemperature, width=6)
    eSetTemperature[i].insert(END, x)
    eSetTemperature[i].pack(padx=2, pady=2)

fReadVaisalaTemperature = LabelFrame(window, text="Temperatura\nodczytana ze wzorca\n[°C]", padx=5, pady=5)
fReadVaisalaTemperature.grid(row=3, column=1)
for i in range(len(eReadVaisalaTemperature)):
    if i in range(0, 3):
        x = -40 + randomAndRound(10)
    elif i in range(3, 6):
        x = 40 + randomAndRound(4)
    elif i in range(6, 9):
        x = 80 + randomAndRound(3)
    elif i in range(9, 12):
        x = 110 + randomAndRound(4)
    elif i in range(12, 16):
        x = 138 + randomAndRound(5)
    else:
        x = -88
    eReadVaisalaTemperature[i] = Entry(fReadVaisalaTemperature, width=10)
    eReadVaisalaTemperature[i].insert(END, x)
    eReadVaisalaTemperature[i].pack(padx=2, pady=2)
    eReadVaisalaTemperature[i].get()

fReadChamberTemperature = LabelFrame(window, text="Temperatura\nodczytana z komory\n[°C]", padx=5, pady=5)
fReadChamberTemperature.grid(row=3, column=2)
for i in range(len(eReadChamberTemperature)):
    if i in range(0, 3):
        x = -40 + randomAndRound(500)
    elif i in range(3, 6):
        x = 40 + randomAndRound(400)
    elif i in range(6, 9):
        x = 80 + randomAndRound(200)
    elif i in range(9, 12):
        x = 110 + randomAndRound(300)
    elif i in range(12, 16):
        x = 142 + randomAndRound(100)
    else:
        x = -88
    eReadChamberTemperature[i] = Entry(fReadChamberTemperature, width=6)
    eReadChamberTemperature[i].insert(END, x)
    eReadChamberTemperature[i].pack(padx=2, pady=2)
    eReadChamberTemperature[i].get

fDifferenceTemperature = LabelFrame(window, text="Różnica\ntemperatur\n[°C]", padx=5, pady=5)
fDifferenceTemperature.grid(row=3, column=3)
for i in range(len(eDifferenceTemperature)):
    eDifferenceTemperature[i] = Entry(fDifferenceTemperature, width=6, state=DISABLED)
    eDifferenceTemperature[i].pack(padx=2, pady=2)

fErrorTemperature = LabelFrame(window, text="Błąd\npomiarowy\n[%]", padx=5, pady=5)
fErrorTemperature.grid(row=3, column=4)
for i in range(len(eErrorTemperature)):
    eErrorTemperature[i] = Entry(fErrorTemperature, width=6, state=DISABLED)
    eErrorTemperature[i].pack(padx=2, pady=2)

bCalculate = Button(window, text="Oblicz", padx=5, pady=5)
bCalculate.bind("<Button-1>", calc)
bCalculate.grid(row=4, column=0, columnspan=2)

bPrintReport = Button(window, text="Wydrukuj raport kalibracyjny", padx=5, pady=5)
bPrintReport.bind("<Button-1>", printReport)
bPrintReport.grid(row=4, column=3, columnspan=2)

window.mainloop()
