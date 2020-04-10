import tkinter as tk
import Databases


def unitForCalibrationPeriod(calibrationPeriod):
    # Najdłuższy czasookres kalibracji to 3 lata.
    if calibrationPeriod == 1:
        return " rok"
    elif calibrationPeriod in range(2, 5):
        return " lata"
    else:
        return " lat"


class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Kopiowanie przyrządu pomiarowego z bazy danych MP2 do bazy danych PE")
        self.createWidgets()

    def createWidgets(self):
        self.lbl_Information = tk.Label(self.master, text="\nWprowadź numer inwentarzowy przyrządu pomiarowego,\n  "
                                                          "który chcesz skopiować z bazy danych MP2 do bazy danych PE: \n",
                                        width=82, borderwidth=2, relief="groove")
        self.lbl_Information.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.ent_InventoryNumber = tk.Entry(self.master, width=35, borderwidth=2)
        self.ent_InventoryNumber.insert(tk.END, "Wprowadź TUTAJ numer inwentarzowy")
        self.ent_InventoryNumber.grid(row=1, column=0, columnspan=2, pady=5)
        self.ent_InventoryNumber.get()
        self.ent_InventoryNumber.bind("<KeyRelease>", lambda x: self.searchMeasurementInstrument())

        self.lbl_MeasurementInstrument = tk.Label(self.master, text="\nTutaj pojawi się informacja po "
                                                                    "wyszukaniu czujnika\n",
                                                  width=82, height=3, borderwidth=2, relief="groove")
        self.lbl_MeasurementInstrument.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.lbl_MeasurementInstrumentMP2 = tk.Label(self.master, text="Informacje o przyrządzie pomiarowym\n"
                                                                       "w bazie danych MP2:\n\n\n\n\n\n...\n\n\n\n\n\n",
                                                     width=50, borderwidth=2, relief="groove")
        self.lbl_MeasurementInstrumentMP2.grid(row=4, column=0, padx=0, pady=5)

        self.lbl_MeasurementInstrumentPE = tk.Label(self.master, text="Informacje o przyrządzie pomiarowym\n"
                                                                      "w bazie danych PE:\n\n\n\n\n\n...\n\n\n\n\n\n",
                                                    width=50, borderwidth=2, relief="groove")
        self.lbl_MeasurementInstrumentPE.grid(row=4, column=1, padx=0, pady=5)

        self.btn_Copy = tk.Button(self.master, text="  Kopiuj przyrząd pomiarowy z bazy danych MP2 do bazy danych PE  ")
        self.btn_Copy.bind("<Button-1>", lambda x: self.copyMeasurementInstrument())
        self.btn_Copy.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.btn_Copy.config(state=tk.DISABLED)

    def searchMeasurementInstrument(self):
        pe = Databases.PE(self.ent_InventoryNumber.get().upper()[:2] + self.ent_InventoryNumber.get()[2:])
        mp2 = Databases.MP2(self.ent_InventoryNumber.get().upper()[:2] + self.ent_InventoryNumber.get()[2:])

        labelText = ""
        buttonState = tk.DISABLED
        if pe.measurementInstrumentInDatabase() is True and mp2.measurementInstrumentInDatabase() is True:
            labelText = "Przyrząd pomiarowy jest już dodany do obydwu baz danych PE i MP2.\nNie można" \
                        " skopiować przyrządu pomiarowego z bazy danych MP2 do bazy danych PE."
        elif pe.measurementInstrumentInDatabase() is True and mp2.measurementInstrumentInDatabase() is False:
            labelText = "Przyrząd pomiarowy istnieje tylko w bazie danych PE.\nDo bazy danych MP2 może być" \
                        " tylko ręcznie."
        elif pe.measurementInstrumentInDatabase() is False and mp2.measurementInstrumentInDatabase() is True:
            labelText = "Przyrząd pomiarowy istnieje tylko w bazie danych MP2.\nMożna go skopiować z bazy danych MP2" \
                        " do bazy danych PE."
            buttonState = tk.NORMAL
        else:
            labelText = "Przyrząd pomiarowy nie istnieje w żadnej z baz danych.\nDodaj najpierw przyrząd ręcznie" \
                        " do bazy danych MP2.\nA następnie skopiuj go do bazy danych PE za pomocą tego skryptu."
            buttonState = tk.DISABLED
        self.lbl_MeasurementInstrument.config(text=labelText)
        self.btn_Copy.config(state=buttonState)

        for i in [pe, mp2]:
            text = ""
            if i.measurementInstrumentInDatabase():
                text = "\nInformacje o przyrządzie pomiarowym\nw bazie danych {}\n\nTyp przyrządu pomiarowego: {}\n" \
                       "Numer inwentarzowy: {}\nKod modelu: {}\nNumer seryjny: {}\nProducent: {}\nData kalibracji: {}\n" \
                       "Czasookres kalibracji: {}\nStatus przyrządu: {}\n\n" \
                    .format(str(i.__class__.__name__), i.getType(), i.getInventoryNumber(), i.getModel(),
                            i.getSerialNumber(), i.getProducent(), i.getCalibrationDate().strftime("%m.%Y"),
                            str(i.getCalibrationPeriod()) + unitForCalibrationPeriod(int(i.getCalibrationPeriod())),
                            i.getStatus())
            else:
                text = "Informacje o przyrządzie pomiarowym\nw bazie danych " + str(i.__class__.__name__) + \
                       ":\n\n\n\n\n\n\nNie istnieje\n\n\n\n\n"
            if str(i.__class__.__name__) == "MP2":
                self.lbl_MeasurementInstrumentMP2.config(text=text)
            else:
                self.lbl_MeasurementInstrumentPE.config(text=text)

    def copyMeasurementInstrument(self):
        pe = Databases.PE(self.ent_InventoryNumber.get().upper()[:2] + self.ent_InventoryNumber.get()[2:])
        mp2 = Databases.MP2(self.ent_InventoryNumber.get().upper()[:2] + self.ent_InventoryNumber.get()[2:])
        pe.addNewSensor(mp2.getModel(), mp2.getSerialNumber(), mp2.getProducent(), mp2.getCalibrationPeriod(),
                        mp2.getCalibrationDate(), "ns", mp2.getMinAnalogSignal(), mp2.getMaxAnalogSignal(),
                        mp2.getUnitAnalogSignal(), mp2.getMinMeasSignal(), mp2.getMaxMeasSignal(),
                        mp2.getUnitMeasSignal(), mp2.getType())



window = tk.Tk()
app = Application(master=window)
app.mainloop()
