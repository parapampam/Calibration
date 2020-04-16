from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Separator


import Databases




class Application(Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.varStr_InventoryNumber = StringVar() #???

        self.ent_SetOne = ["setOne1", "setOne2", "setOne3", "setOne4", "setOne5", "setOne6", "setOne7", "setOne8",
                           "setOne9", "setOne10", "setOne11", "setOne12", "setOne13", "setOne14", "setOne15"]

        self.ent_SetTwo = ["setTwo1", "setTwo2", "setTwo3", "setTwo4", "setTwo5", "setTwo6", "setTwo7", "setTwo8",
                           "setTwo9", "setTwo10", "setTwo11", "setTwo12", "setTwo13", "setTwo14", "setTwo15"]

        self.ent_ReadVaisalaOne = ["readVaisalaOne1", "readVaisalaOne2", "readVaisalaOne3", "readVaisalaOne4",
                                   "readVaisalaOne5", "readVaisalaOne6", "readVaisalaOne7", "readVaisalaOne8",
                                   "readVaisalaOne9", "readVaisalaOne10", "readVaisalaOne11", "readVaisalaOne12",
                                   "readVaisalaOne13", "readVaisalaOne14", "readVaisalaOne15"]

        self.ent_ReadVaisalaTwo = ["readVaisalaTwo1", "readVaisalaTwo2", "readVaisalaTwo3", "readVaisalaTwo4",
                                   "readVaisalaTwo5", "readVaisalaTwo6", "readVaisalaTwo7", "readVaisalaTwo8",
                                   "readVaisalaTwo9", "readVaisalaTwo10", "readVaisalaTwo11", "readVaisalaTwo12",
                                   "readVaisalaTwo13", "readVaisalaTwo14", "readVaisalaTwo15"]

        self.ent_ReadChamberOne = ["readChamberOne1", "readChamberOne2", "readChamberOne3", "readChamberOne4",
                                   "readChamberOne5", "readChamberOne6", "readChamberOne7", "readChamberOne8",
                                   "readChamberOne9", "readChamberOne10", "readChamberOne11", "readChamberOne12",
                                   "readChamberOne13", "readChamberOne14", "readChamberOne15"]

        self.ent_ReadChamberTwo = ["readChamberTwo1", "readChamberTwo2", "readChamberTwo3", "readChamberTwo4",
                                   "readChamberTwo5", "readChamberTwo6", "readChamberTwo7", "readChamberTwo8",
                                   "readChamberTwo9", "readChamberTwo10", "readChamberTwo11", "readChamberTwo12",
                                   "readChamberTwo13", "readChamberTwo14", "readChamberTwo15"]

        self.ent_DifferenceOne = ["differenceOne1", "differenceOne2", "differenceOne3", "differenceOne4",
                                  "differenceOne5", "differenceOne6", "differenceOne7", "differenceOne8",
                                  "differenceOne9", "differenceOne10", "differenceOne11", "differenceOne12",
                                  "differenceOne13", "differenceOne14", "differenceOne15"]

        self.ent_DifferenceTwo = ["differenceTwo1", "differenceTwo2", "differenceTwo3", "differenceTwo4",
                                  "differenceTwo5", "differenceTwo6", "differenceTwo7", "differenceTwo8",
                                  "differenceTwo9", "differenceTwo10", "differenceTwo11", "differenceTwo12",
                                  "differenceTwo13", "differenceTwo14", "differenceTwo15"]

        self.ent_ErrorOne = ["errorOne1", "errorOne2", "errorOne3", "errorOne4", "errorOne5", "errorOne6", "errorOne7",
                             "errorOne8", "errorOne9", "errorOne10", "errorOne11", "errorOne12", "errorOne13",
                             "errorOne14", "errorOne15"]

        self.ent_ErrorTwo = ["errorOne1", "errorTwo2", "errorTwo3", "errorTwo4", "errorTwo5", "errorTwo6", "errorTwo7",
                             "errorTwo8", "errorTwo9", "errorTwo10", "errorTwo11", "errorTwo12", "errorTwo13",
                             "errorTwo14", "errorTwo15"]

        master.title("Ręczna kalibracja komór")
        self.fontStyle = Font(size=12)

        self.createFirstColumn()
        self.createSecondColumn()
        self.createThirdColumn()

        self.scrollbar = Scrollbar(self.master, orient=HORIZONTAL)
        self.scrollbar.grid(row=1, column=1, columnspan=2, sticky=N+S+W)
        self.scrollbar.config(command=self.master)


    def createFirstColumn(self):
        self.frm_FirstColumn = Frame(self.master)
        self.frm_FirstColumn.grid(row=0, column=0, padx=5, pady=5)

        self.lbl_ProgramInfo = Label(self.frm_FirstColumn, text="\nProgram przeznaczony do ręcznej kalibracji "
                                                                   "komór.\n\nWprowadź numer inwentarzowy komory,"
                                                                   "\nktórą chcesz kalibrować: \n",
                                        font=self.fontStyle, width=40)
        self.lbl_ProgramInfo.grid(row=0, column=0, pady=10, columnspan=2)

        self.sep_Line1 = Separator(self.frm_FirstColumn, orient="horizontal")
        self.sep_Line1.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.ent_InventoryNumber = Entry(self.frm_FirstColumn, font=self.fontStyle, width=35, borderwidth=2,
                                         justify=CENTER)
        self.ent_InventoryNumber.insert(END, "Wprowadź TUTAJ numer inwentarzowy")
        self.ent_InventoryNumber.grid(row=2, column=0, columnspan=2, padx=5, pady=20, ipadx=2, ipady=2)
        self.ent_InventoryNumber.bind("<KeyRelease>", lambda x: self.searchChamber())

        self.sep_Line2 = Separator(self.frm_FirstColumn, orient="horizontal")
        self.sep_Line2.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.lbl_ChamberInfo = Label(self.frm_FirstColumn, text="\nTutaj pojawi się informacja po wyszukaniu komory.\n",
                                     font=self.fontStyle, width=50, height=8)
        self.lbl_ChamberInfo.grid(row=4, column=0, columnspan=2, ipady=20)

        self.sep_Line3 = Separator(self.frm_FirstColumn, orient="horizontal")
        self.sep_Line3.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.btn_Calculate = Button(self.frm_FirstColumn, text="Oblicz", font=self.fontStyle)
        # self.btn_Calculate.bind("<Button-1>", calc)
        self.btn_Calculate.grid(row=6, column=0, padx=5, pady=20, ipadx=5, ipady=5)

        self.btn_PrintReport = Button(self.frm_FirstColumn, text="Wydrukuj raport kalibracyjny", font=self.fontStyle)
        # self.btn_PrintReport.bind("<Button-1>", printReport)
        self.btn_PrintReport.grid(row=6, column=1, padx=5, pady=20, ipadx=5, ipady=5)

    def createSecondColumn(self):
        self.frm_SecondColumn = Frame(self.master)
        self.frm_SecondColumn.grid(row=0, column=1, padx=5, pady=5)

        self.lblFrm_MeasurementTableOne = LabelFrame(self.frm_SecondColumn, text="", font=self.fontStyle)
        self.lblFrm_MeasurementTableOne.grid(row=0, column=0, padx=5, pady=5)

        self.lblFrm_SetOne = LabelFrame(self.lblFrm_MeasurementTableOne, text="", font=self.fontStyle)
        self.lblFrm_SetOne.grid(row=0, column=0, padx=5, pady=5)
        for i in range(len(self.ent_SetOne)):
            self.ent_SetOne[i] = Entry(self.lblFrm_SetOne, font=self.fontStyle, width=8)
            self.ent_SetOne[i].insert(END, " ")
            self.ent_SetOne[i].pack(padx=2, pady=2)
            self.ent_SetOne[i].config(state=DISABLED)

        self.lblFrm_ReadVaisalaOne = LabelFrame(self.lblFrm_MeasurementTableOne, text="",
                                                font=self.fontStyle)
        self.lblFrm_ReadVaisalaOne.grid(row=0, column=1, padx=5, pady=5)
        for i in range(len(self.ent_ReadVaisalaOne)):
            self.ent_ReadVaisalaOne[i] = Entry(self.lblFrm_ReadVaisalaOne, font=self.fontStyle, width=8)
            self.ent_ReadVaisalaOne[i].insert(END, " ")
            self.ent_ReadVaisalaOne[i].pack(padx=2, pady=2)
            self.ent_ReadVaisalaOne[i].config(state=DISABLED)

        self.lblFrm_ReadChamberOne = LabelFrame(self.lblFrm_MeasurementTableOne, text="",
                                                font=self.fontStyle)
        self.lblFrm_ReadChamberOne.grid(row=0, column=2, padx=5, pady=5)
        for i in range(len(self.ent_ReadChamberOne)):
            self.ent_ReadChamberOne[i] = Entry(self.lblFrm_ReadChamberOne, font=self.fontStyle, width=8)
            self.ent_ReadChamberOne[i].insert(END, " ")
            self.ent_ReadChamberOne[i].pack(padx=2, pady=2)
            self.ent_ReadChamberOne[i].config(state=DISABLED)

        self.lblFrm_DifferenceOne = LabelFrame(self.lblFrm_MeasurementTableOne, text="", font=self.fontStyle)
        self.lblFrm_DifferenceOne.grid(row=0, column=3, padx=5, pady=5)
        for i in range(len(self.ent_DifferenceOne)):
            self.ent_DifferenceOne[i] = Entry(self.lblFrm_DifferenceOne, font=self.fontStyle, width=8, state=DISABLED)
            self.ent_DifferenceOne[i].pack(padx=2, pady=2)

        self.lblFrm_ErrorOne = LabelFrame(self.lblFrm_MeasurementTableOne, text = "", font=self.fontStyle)
        self.lblFrm_ErrorOne.grid(row=0, column=4, padx=5, pady=5)
        for i in range(len(self.ent_DifferenceOne)):
            self.ent_ErrorOne[i] = Entry(self.lblFrm_ErrorOne, font=self.fontStyle, width=8, state=DISABLED)
            self.ent_ErrorOne[i].pack(padx=2, pady=2)

    def createThirdColumn(self):
        self.frm_ThirdColumn = Frame(self.master)
        self.frm_ThirdColumn.grid(row=0, column=2, padx=5, pady=5)

        self.lblFrm_MeasurementTableTwo = LabelFrame(self.frm_ThirdColumn, text="", font=self.fontStyle)
        self.lblFrm_MeasurementTableTwo.grid(row=0, column=0, padx=5, pady=5)

        self.lblFrm_SetTwo = LabelFrame(self.lblFrm_MeasurementTableTwo, text="", font=self.fontStyle)
        self.lblFrm_SetTwo.grid(row=0, column=0, padx=5, pady=5)
        for i in range(len(self.ent_SetTwo)):
            self.ent_SetTwo[i] = Entry(self.lblFrm_SetTwo, font=self.fontStyle, width=8)
            self.ent_SetTwo[i].insert(END, " ")
            self.ent_SetTwo[i].pack(padx=2, pady=2)
            self.ent_SetTwo[i].config(state=DISABLED)

        self.lblFrm_ReadVaisalaTwo = LabelFrame(self.lblFrm_MeasurementTableTwo, text="",
                                                font=self.fontStyle)
        self.lblFrm_ReadVaisalaTwo.grid(row=0, column=1, padx=5, pady=5)
        for i in range(len(self.ent_ReadVaisalaTwo)):
            self.ent_ReadVaisalaTwo[i] = Entry(self.lblFrm_ReadVaisalaTwo, font=self.fontStyle, width=8)
            self.ent_ReadVaisalaTwo[i].insert(END, " ")
            self.ent_ReadVaisalaTwo[i].pack(padx=2, pady=2)
            self.ent_ReadVaisalaTwo[i].config(state=DISABLED)

        self.lblFrm_ReadChamberTwo = LabelFrame(self.lblFrm_MeasurementTableTwo, text="",
                                                font=self.fontStyle)
        self.lblFrm_ReadChamberTwo.grid(row=0, column=2, padx=5, pady=5)
        for i in range(len(self.ent_ReadChamberTwo)):
            self.ent_ReadChamberTwo[i] = Entry(self.lblFrm_ReadChamberTwo, font=self.fontStyle, width=8)
            self.ent_ReadChamberTwo[i].insert(END, " ")
            self.ent_ReadChamberTwo[i].pack(padx=2, pady=2)
            self.ent_ReadChamberTwo[i].config(state=DISABLED)

        self.lblFrm_DifferenceTwo = LabelFrame(self.lblFrm_MeasurementTableTwo, text="", font=self.fontStyle)
        self.lblFrm_DifferenceTwo.grid(row=0, column=3, padx=5, pady=5)
        for i in range(len(self.ent_DifferenceTwo)):
            self.ent_DifferenceTwo[i] = Entry(self.lblFrm_DifferenceTwo, font=self.fontStyle, width=8, state=DISABLED)
            self.ent_DifferenceTwo[i].pack(padx=2, pady=2)

        self.lblFrm_ErrorTwo = LabelFrame(self.lblFrm_MeasurementTableTwo, text="", font=self.fontStyle)
        self.lblFrm_ErrorTwo.grid(row=0, column=4, padx=5, pady=5)
        for i in range(len(self.ent_DifferenceTwo)):
            self.ent_ErrorTwo[i] = Entry(self.lblFrm_ErrorTwo, font=self.fontStyle, width=8, state=DISABLED)
            self.ent_ErrorTwo[i].pack(padx=2, pady=2)

    def searchChamber(self):
        pe = Databases.PE(self.ent_InventoryNumber.get().upper()[:2] + self.ent_InventoryNumber.get()[2:])

        lbl_ChamberInfoText = ""
        btn_CalculateStatus = DISABLED
        btn_PrintReportStatus = DISABLED

        lblFrm_MeasurementTableOneText = ""
        lblFrm_SetOneText = ""
        lblFrm_ReadVaisalaOneText = ""
        lblFrm_ReadChamberOneText = ""
        lblFrm_DifferenceOneText = ""
        lblFrm_ErrorOneText = ""

        lblFrm_MeasurementTableTwoText = ""
        lblFrm_SetTwoText = ""
        lblFrm_ReadVaisalaTwoText = ""
        lblFrm_ReadChamberTwoText = ""
        lblFrm_DifferenceTwoText = ""
        lblFrm_ErrorTwoText = ""

        if pe.measurementInstrumentInDatabase() is True:
            if pe.getType() in ["Komora temperaturowa", "Komora klimatyczna"]:
                lbl_ChamberInfoText = "\n\n{}\n\nNazwa komory: {}\nNumer inwentarzowy: {}\nModel: {}\nNumer seryjny: {}" \
                                      "\nProducent: {}\nData kalibracji: {}\n"\
                    .format(pe.getType(), pe.getUnitMeasSignal(), pe.getInventoryNumber(), pe.getModel(),
                            pe.getSerialNumber(), pe.getProducent(), pe.getCalibrationDate().strftime("%m.%Y"))

                if pe.getType() == "Komora temperaturowa":
                    lblFrm_MeasurementTableOneText = "Pomiary temperatury dla komory temperaturowej"
                    lblFrm_SetOneText = "Temperatura\nzadana\n[°C]"
                    lblFrm_ReadVaisalaOneText = "Temperatura\nodczytana ze wzorca\n[°C]"
                    lblFrm_ReadChamberOneText = "Temperatura\nodczytana z komory\n[°C]"
                    lblFrm_DifferenceOneText = "Różnica\ntemperatur\n[°C]"
                    lblFrm_ErrorOneText = "Błąd\npomiaru\n[%]"
                    lblFrm_MeasurementTableTwoText = ""
                    lblFrm_SetTwoText = ""
                    lblFrm_ReadVaisalaTwoText = ""
                    lblFrm_ReadChamberTwoText = ""
                    lblFrm_DifferenceTwoText = ""
                    lblFrm_ErrorTwoText = ""

                if pe.getType() == "Komora klimatyczna":
                    lblFrm_MeasurementTableOneText = "Pomiary temperatury dla komory klimatycznej"
                    lblFrm_SetOneText = "Temperatura\nzadana\n[°C]"
                    lblFrm_ReadVaisalaOneText = "Temperatura\nodczytana ze wzorca\n[°C]"
                    lblFrm_ReadChamberOneText = "Temperatura\nodczytana z komory\n[°C]"
                    lblFrm_DifferenceOneText = "Różnica\ntemperatur\n[°C]"
                    lblFrm_ErrorOneText = "Błąd\npomiaru\n[%]"
                    print(lambda x: self.defaultSetValues(pe.getType())[0])
                    lblFrm_MeasurementTableTwoText = "Pomiar wilgotności dla komory klimatycznej"
                    lblFrm_SetTwoText = "Wilgotność\nzadana\n[RH%]"
                    lblFrm_ReadVaisalaTwoText = "Wilgotność\nodczytana ze wzorca\n[RH%]"
                    lblFrm_ReadChamberTwoText = "Wilgotność\nodczytana z komory\n[RH%]"
                    lblFrm_DifferenceTwoText = "Różnica\nwilgotności\n[RH%]"
                    lblFrm_ErrorTwoText = "Błąd\npomiaru\n[%]"

            else:
                lbl_ChamberInfoText = "To nie jest komora"

        else:
            lbl_ChamberInfoText = "Taki przyrząd nie istnieje"

        self.lbl_ChamberInfo.config(text=lbl_ChamberInfoText)
        self.lblFrm_MeasurementTableOne.config(text=lblFrm_MeasurementTableOneText)
        self.lblFrm_SetOne.config(text=lblFrm_SetOneText)
        self.lblFrm_ReadVaisalaOne.config(text=lblFrm_ReadVaisalaOneText)
        self.lblFrm_ReadChamberOne.config(text=lblFrm_ReadChamberOneText)
        self.lblFrm_DifferenceOne.config(text=lblFrm_DifferenceOneText)
        self.lblFrm_ErrorOne.config(text=lblFrm_ErrorOneText)

        self.lblFrm_MeasurementTableTwo.config(text=lblFrm_MeasurementTableTwoText)
        self.lblFrm_SetTwo.config(text=lblFrm_SetTwoText)
        self.lblFrm_ReadVaisalaTwo.config(text=lblFrm_ReadVaisalaTwoText)
        self.lblFrm_ReadChamberTwo.config(text=lblFrm_ReadChamberTwoText)
        self.lblFrm_DifferenceTwo.config(text=lblFrm_DifferenceTwoText)
        self.lblFrm_ErrorTwo.config(text=lblFrm_ErrorTwoText)



    def defaultSetValues(type):
        defaultSetTemperatureForTemperatureChamber = []
        defaultSetTemperatureForClimateChamber = []
        defaultSetHumidityForClimateChamber = []
        if type == "Komora temperaturowa":
            defaultSetTemperatureForTemperatureChamber = [-40, -40, -40, 40, 40, 40, 80, 80, 80, 110, 110, 110, 140,
                                                          140, 140]
        elif type == "Komora klimatyczna":
            defaultSetTemperatureForClimateChamber = [-40, -40, -40, 40, 40, 40, 80, 80, 80, 110, 110, 110, 140,
                                                      140, 140]
            defaultSetHumidityForClimateChamber = [20, 20, 20, 40, 40, 40, 60, 60, 60, 80, 80, 80, 95, 95, 95]
        return defaultSetTemperatureForTemperatureChamber, defaultSetTemperatureForClimateChamber, \
               defaultSetHumidityForClimateChamber



#
# def calc(event):
#     print("oblicz")
#     print(eSetOne[0].get())
#     # for i in range(len(eSet)):
#     #     eDifferenceTemperature[i].config(state=NORMAL)
#     #     eDifferenceTemperature[i].delete(0, END)
#     #     eDifferenceTemperature[i].insert(0, round(float(eReadChamberTemperature[i].get())
#     #                                               - float(eReadVaisala[i].get()), 2))
#     #     eDifferenceTemperature[i].config(state=DISABLED)
#     #
#     # for i in range(len(eSet)):
#     #     eErrorTemperature[i].config(state=NORMAL)
#     #     eErrorTemperature[i].delete(0, END)
#     #     eErrorTemperature[i].insert(0, round(
#     #         float(eDifferenceTemperature[i].get()) * 100 / ((float(eSet[14].get()) - float(eSet[0].get()))), 2))
#     #     eErrorTemperature[i].config(state=DISABLED)
#
#
# def printReport(event):
#     varInventoryNumber.set(eInventoryNumber.get().upper()[:2] + eInventoryNumber.get()[2:])
#     pe = Db.PE(varInventoryNumber.get())
#     report = Template.Report(pe.inventoryNumber)
#     text = report.readCalibrationReportTemplate(pe.getType())
#     text = report.replaceInventoryNumber(text)
#     text = report.replaceModel(text, pe.getModel())
#     text = report.replaceSerialNumber(text, pe.getSerialNumber())
#     text = report.replaceProducent(text, pe.getProducent())
#     text = report.replaceCalibrationDate(text)
#     text = report.replaceCertificateNumber(text)
#     text = report.replaceType(text, pe.getType())
#     text = report.replaceCalibrationRange(text, eSet[0].get(), eSet[14].get(), "°C")
#     print(text)
#
#     measurement = report.readMeasurementReportTemplate(pe.getType())
#     measurement = report.replaceInventoryNumber(measurement)
#     measurement = report.replacePointsInMeasurementTable(measurement, eReadVaisala, "a")
#     measurement = report.replacePointsInMeasurementTable(measurement, eReadChamberTemperature, "b")
#     measurement = report.replacePointsInMeasurementTable(measurement, eDifferenceTemperature, "c")
#     measurement = report.replacePointsInMeasurementTable(measurement, eErrorTemperature, "d")
#     # print(measurement)
#
#
# for i in range(4):
#     print(str(i))
#
window = Tk()
app = Application(master=window)
app.mainloop()
