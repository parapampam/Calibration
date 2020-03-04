import pyodbc
import datetime


sensorType = {
    "Czujnik drogi": {"MP2": "Czujnik drogi", "PE": 3},
    "Suwmiarka": {"MP2": "Suwmiarka", "PE": 4},
    "Czujnik cisnienia": {"MP2": "Czujnik ciśnienia", "PE": 5},
    "Przeplywomierz": {"MP2": "Przepływomierz", "PE": 6},
    "Czujnik sily": {"MP2": "Czujnik siły", "PE": 7},
    "Waga": {"MP2": "Waga", "PE": 10},
    "Zestaw pomiarowy": {"MP2": "Zestaw pomiarowy", "PE": 11},
    "Klucz dynamometryczny": {"MP2": "Klucz dynamometryczny", "PE": 12},
    "Glebokosciomierz": {"MP2": "Głębokościomierz", "PE": 14},
    "Mikrometr": {"MP2": "Mikrometr", "PE": 16},
    "Wysokosciomierz": {"MP2": "Wysokościomierz", "PE": 19},
    "Piecyk": {"MP2": "Piecyk", "PE": 25},
    "Komora klimatyczna": {"MP2": "Komora klimatyczna", "PE": 28},
    "Komora temperaturowa": {"MP2": "Komora temperaturowa", "PE": 36},
    "Komora szokowa": {"MP2": "Komora szokowa", "PE": 37},
    "Komora solna": {"MP2": "Komora solna", "PE": 40}
}

daysInMonth = {
            "01": 31,
            "02": 28,
            "03": 31,
            "04": 30,
            "05": 31,
            "06": 30,
            "07": 31,
            "08": 31,
            "09": 30,
            "10": 31,
            "11": 30,
            "12": 31
        }


class Database:
    def __init__(self, inventoryNumber = ""):
        self.inventoryNumber = inventoryNumber

    def connectWithDatabase(self):
        pass

    def get(self, query = ""):
        cursor = self.connectWithDatabase()
        cursor.execute(query)
        return cursor.fetchone()[0]

    def getKey(self, type):
        global sensorType
        for key in sensorType.keys():
            for search, value in sensorType[key].items():
                if type == value:
                    return key
                else:
                    pass

class PE(Database):
    def connectWithDatabase(self):
        connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                                   'Server=WPLSXSQL1;'
                                                   'Database=sensmandb;'
                                                   'uid=admuser;pwd=admu$er;'
                                                   )
        return connect.cursor()

    def measurementInstrumentInDatabase(self):
        try:
            if self.getInventoryNumber():
                exist = True
            else:
                exist =  False
        except TypeError:
            exist = False
        return exist

    def getInventoryNumber(self):
        query = "SELECT nr_zd FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getType(self):
        query = "SELECT Btc.lo FROM Baza_typ_czujnika AS Btc JOIN Baza_czujniki AS Bc ON Bc.typ_id = Btc.id AND Bc.nr_zd = '"\
                + self.inventoryNumber + "'"
        return super().get(query)

    def getModel(self):
        query = "SELECT k_modelu FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getSerialNumber(self):
        query = "SELECT n_seryjny FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getProducent(self):
        query = "SELECT prod FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getCalibrationPeriod(self):
        query = "SELECT okres_k FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getCalibrationDate(self):
        query = "SELECT kolejna_k FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getStatus(self):
        status = {
            "wk": "kalibracja wewnętrzna",
            "zk": "kalibracja zewnętrzna",
            "wp": "wypożyczony",
            "ns": "wolny",
            "wn": "naprawa",
            "od": "do odbioru",
            "nn": "do ustawienia"
        }
        query = "SELECT status FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return status[super().get(query)]

    def getMinAnalogSignal(self):
        query = "SELECT syg_ana_min FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        minAnalogSignal = super().get(query)
        if minAnalogSignal % 1 == 0:
            return int(minAnalogSignal)
        else:
            return minAnalogSignal

    def getMaxAnalogSignal(self):
        query = "SELECT syg_ana_max FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        maxAnalogSignal = super().get(query)
        if maxAnalogSignal % 1 == 0:
            return int(maxAnalogSignal)
        else:
            return maxAnalogSignal

    def getUnitAnalogSignal(self):
        query = "SELECT jednostka_ana FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getMinMeasSignal(self):
        query = "SELECT syg_mierz_min FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        minMeasSignal = super().get(query)
        if minMeasSignal % 1 == 0:
            return int(minMeasSignal)
        else:
            return minMeasSignal

    def getMaxMeasSignal(self):
        query = "SELECT syg_mierz_max FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        maxMeasSignal = super().get(query)
        if maxMeasSignal % 1 == 0:
            return int(maxMeasSignal)
        else:
            return maxMeasSignal

    def getUnitMeasSignal(self):
        query = "SELECT jednostka_mierz FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'"
        return super().get(query)


    def addNewSensor(self, model, serialNumber, producent, calibrationPeriod, calibrationDate,
                     status, minAnalogSignal, maxAnalogSignal, unitAnalogSignal, minMeasSignal, maxMeasSignal,
                     unitMeasSignal, type):
        global sensorType
        print(self.inventoryNumber, model, serialNumber, producent, calibrationPeriod, calibrationDate,
                     status, minAnalogSignal, maxAnalogSignal, unitAnalogSignal, minMeasSignal, maxMeasSignal,
                     unitMeasSignal, type)
        print(sensorType[super().getKey(type)]["PE"])
        cursor = self.connectWithDatabase()
        query = "INSERT INTO Baza_czujniki (nr_zd, k_modelu, n_seryjny, prod, okres_k, kolejna_k, status, syg_ana_min, syg_ana_max, jednostka_ana, syg_mierz_min, syg_mierz_max, jednostka_mierz, typ_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (self.inventoryNumber, model, serialNumber, producent, calibrationPeriod, calibrationDate, status, minAnalogSignal, maxAnalogSignal, unitAnalogSignal, minMeasSignal, maxMeasSignal, unitMeasSignal, sensorType[super().getKey(type)]["PE"]))
        cursor.commit()


class MP2(Database):

    def connectWithDatabase(self):
        connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                 'Server=wplsxsql1;'
                                 'Database=MP2_PRO;'
                                 'uid=MP2_Read;pwd=Read_MP2;'
                                 )
        return connect.cursor()

    def getLastMeasurementInstrumentInDatabase(self):
        query = "SELECT EQUIP.EQNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.EQNUM LIKE 'LP[_]%' ORDER BY EQUIP.EQNUM DESC"
        cursor = self.connectWithDatabase()
        cursor.execute(query)
        return cursor.fetchone()[0]


    def measurementInstrumentInDatabase(self):
        try:
            if self.getInventoryNumber():
                exist = True
            else:
                exist = False
        except TypeError:
            exist = False
        return exist

    def getInventoryNumber(self):
        query = "SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getType(self):
        global sensorType
        query = "SELECT EQUIP.DESCRIPTION FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        return sensorType[super().get(query)]["MP2"]

    def getModel(self):
        query = "SELECT EQUIP.MODELNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getSerialNumber(self):
        query = "SELECT EQUIP.SERIALNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getProducent(self):
        query = "SELECT EQUIP.MANUFACTURER FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        return super().get(query)

    def getCalibrationPeriod(self):
        query = "SELECT EQUIP.UD7 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        return super().get(query).split(" ")[0]

    def getCalibrationDate(self):
        global daysInMonth
        query = "SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        calibrationDate = super().get(query)
        if "w kalibracji" in calibrationDate:
            calibrationDate = datetime.date.today()
        elif "archiwum" in calibrationDate:
            calibrationDate =  datetime.date.today()
        else:
            calibrationDate = datetime.date(int(calibrationDate[3:]), int(calibrationDate[:2]), daysInMonth[calibrationDate[:2]])
        return calibrationDate

    def getStatus(self):
        global daysInMonth
        query = "SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        status = super().get(query)
        if "w kalibracji" in status:
            status = "w kalibracji"
        elif "archiwum" in status:
            status = "w archiwum"
        elif datetime.date(int(status[3:]), int(status[:2]), daysInMonth[status[:2]]) > datetime.date.today():
            status = "aktualna kalibracja"
        else:
            status = "przeterminowana kalibracja"
        return status

    def getMinAnalogSignal(self):
        query = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        minAnalogSignal = super().get(query)
        if "V" in minAnalogSignal or "mA" in minAnalogSignal:
            minAnalogSignal = minAnalogSignal.split("_")[0]
        else:
            minAnalogSignal = ""
        return minAnalogSignal

    def getMaxAnalogSignal(self):
        query = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        maxAnalogSignal = super().get(query)
        if "V" in maxAnalogSignal or "mA" in maxAnalogSignal:
            maxAnalogSignal = maxAnalogSignal.split("_")[1]
            maxAnalogSignal = maxAnalogSignal[:(len(maxAnalogSignal) - self.countNumberLetters(maxAnalogSignal))]
        else:
            maxAnalogSignal = ""
        return maxAnalogSignal

    def getUnitAnalogSignal(self):
        query = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        unitAnalogSignal = super().get(query)
        if "V" in unitAnalogSignal or "mA" in unitAnalogSignal:
            unitAnalogSignal = unitAnalogSignal.split("_")[1]
            unitAnalogSignal = unitAnalogSignal[-self.countNumberLetters(unitAnalogSignal):]
        else:
            unitAnalogSignal = ""
        return unitAnalogSignal

    def getMinMeasSignal(self):
        query = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        minMeasSignal = super().get(query)
        if "V" in minMeasSignal or "mA" in minMeasSignal:
            minMeasSignal = minMeasSignal.split("_")[2]
        elif "_" in minMeasSignal:
            minMeasSignal = minMeasSignal.split("_")[0]
        else:
            minMeasSignal = ""
        return minMeasSignal

    def getMaxMeasSignal(self):
        query = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        maxMeasSignal = super().get(query)
        if "V" in maxMeasSignal or "mA" in maxMeasSignal:
            maxMeasSignal = maxMeasSignal.split("_")[3]
            maxMeasSignal = maxMeasSignal[:len(maxMeasSignal) - self.countNumberLetters(maxMeasSignal)]
        elif "_" in maxMeasSignal:
            maxMeasSignal = maxMeasSignal.split("_")[1]
            maxMeasSignal = maxMeasSignal[:len(maxMeasSignal) - self.countNumberLetters(maxMeasSignal)]
        else:
            maxMeasSignal = ""
        return maxMeasSignal

    def getUnitMeasSignal(self):
        query = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'"
        unitMeasSignal = super().get(query)
        if "V" in unitMeasSignal or "mA" in unitMeasSignal:
            unitMeasSignal = unitMeasSignal.split("_")[3]
            unitMeasSignal = unitMeasSignal[-self.countNumberLetters(unitMeasSignal):]
        elif "_" in unitMeasSignal:
            unitMeasSignal = unitMeasSignal.split("_")[1]
            unitMeasSignal = unitMeasSignal[-self.countNumberLetters(unitMeasSignal):]
        return unitMeasSignal

    def countNumberLetters(self, string):
        count = 0
        for char in string:
            if char.isalpha():
                count = count + 1
        return count

