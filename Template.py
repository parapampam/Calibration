import os
import datetime
import locale

# ustawienie czasu lokalnego
locale.setlocale(locale.LC_ALL, '')


class Template:
    def __init__(self, inventoryNumber=""):
        self.inventoryNumber = inventoryNumber


    def readTemplate(self, fileName=""):
        path = os.path.join("//wplcswroclaw12m/pdp/01_Team's/TQC_MTS/Kalibracje/FAQ/Program kalibracyjny/", fileName)
        if os.path.isfile(path):
            file = open(path)
            template = file.read()
            file.close()
            return template
        else:
            print("Taki plik nie istnieje!")

    def replaceInventoryNumber(self, text):
        return text.replace("xInventoryNumber", self.inventoryNumber)

    def replaceModel(self, text, model):
        return text.replace("xModel", model)

    def replaceSerialNumber(self, text, serialNumber):
        return text.replace("xSerialNumber", serialNumber)

    def replaceProducent(self, text, producent):
        return text.replace("xProducent", producent)

    def replaceCalibrationDate(self, text, date):
        return text.replace("xDate", date)

    def replaceType(self, text, type):
        return text.replace("xType", type)

    def replaceCalibrationRange(self, text, range):
        return text.replace("xCalibrationRange", range)




class Report(Template):
    def readCalibrationReportTemplate(self, type):
        fileName = ""
        if type == "Czujnik ciśnienia":
            fileName = "Calibration Report Pressure.txt"
        elif type == "Komora temperaturowa":
            fileName = "Calibration Report Temperature Chamber.txt"
        return super().readTemplate(fileName)

    def readMeasurementReportTemplate(self, type):
        fileName = ""
        if type == "Komora temperaturowa":
            fileName = "Measurement Report Chamber Temperature.txt"
        return super().readTemplate(fileName)

    def replaceInventoryNumber(self, text):
        return super().replaceInventoryNumber(text)

    def replaceCalibrationDate(self, text):
        date = str(datetime.date.today().strftime("%d %B %Y")) + " r."
        return super().replaceCalibrationDate(text, date)

    def replaceCertificateNumber(self, text):
        return text.replace("xCertificateNumber", str(self.inventoryNumber) + " / " + str(datetime.date.today().strftime("%m"))
                        + " / " + str(datetime.date.today().strftime("%Y")))

    def replaceCalibrationRange(self, text, minMeas, maxMeas, unitMeas):
        range = minMeas + " ... " + maxMeas + unitMeas
        return super().replaceCalibrationRange(text, range)

    def replacePointsInMeasurementTable(self, text, points, column):
        for i in range(0, 15):
            x = column + str(i) + " "
            y = str(round(float(points[i].get()), 2)) + " "
            text = text.replace(x, y)
        return text


class Label(Template):
    def readTemplate(self):
        fileName = ""
        if self.type == "Czujnik ciśnienia":
            fileName = "Label Pressure Sensor.txt"
        elif self.type == "Komora temperaturowa":
            fileName == "Label Temperature Chamber.txt"
        return super().readTemplate(fileName)

    def replaceInventoryNumber(self, text):
        return super().replaceInventoryNumber(text)
