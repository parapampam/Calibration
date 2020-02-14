import pyodbc

class PE:
    def __init__(self, inventoryNumber):
        self.inventoryNumber = inventoryNumber

    def connectWithDatabase(self):
        connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                                   'Server=WPLSXSQL1;'
                                                   'Database=sensmandb;'
                                                   'uid=admuser;pwd=admu$er;'
                                                   )
        return connect.cursor()

    def getInventoryNumber(self, cursor):
        cursor.execute("SELECT nr_zd FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        try:
            self.inventoryNumber = cursor.fetchone()[0]
            return self.inventoryNumber
        except TypeError:
            return ""

    def getType(self, cursor):
        cursor.execute(
            "SELECT Btc.lo FROM Baza_typ_czujnika AS Btc JOIN Baza_czujniki AS Bc ON Bc.typ_id = Btc.id AND Bc.nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getModel(self, cursor):
        cursor.execute("SELECT k_modelu FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getSerialNumber(self, cursor):
        cursor.execute("SELECT n_seryjny FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getProducent(self, cursor):
        cursor.execute("SELECT prod FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getCalibrationPeriod(self, cursor):
        cursor.execute("SELECT okres_k FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getCalibrationDate(self, cursor):
        cursor.execute("SELECT kolejna_k FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getStatus(self, cursor):
        cursor.execute("SELECT status FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getMinAnalogSignal(self, cursor):
        cursor.execute("SELECT syg_ana_min FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getMaxAnalogSignal(self, cursor):
        cursor.execute("SELECT syg_ana_max FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getUnitAnalogSignal(self, cursor):
        cursor.execute("SELECT jednostka_ana FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getMinMeasSignal(self, cursor):
        cursor.execute("SELECT syg_mierz_min FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getMaxMeasSignal(self, cursor):
        cursor.execute("SELECT syg_mierz_max FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getUnitMeasSignal(self, cursor):
        cursor.execute("SELECT jednostka_mierz FROM Baza_czujniki WHERE nr_zd = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]


class MP2:

    def __init__(self, inventoryNumber):
        self.inventoryNumber = inventoryNumber

    def connectWithDatabase(self):
        connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                 'Server=wplsxsql1;'
                                 'Database=MP2_PRO;'
                                 'uid=MP2_Read;pwd=Read_MP2;'
                                 )
        return connect.cursor()

    def getInventoryNumber(self, cursor):
        cursor.execute("SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        try:
            self.inventoryNumber = cursor.fetchone()[0]
            return  self.inventoryNumber
        except TypeError:
            return ""

    def getType(self, cursor):
        sensorType = {
            "Czujnik cisnienia": "Czujnik ciśnienia",
            "Komora temperaturowa": "Komora temperaturowa"
        }
        cursor.execute("SELECT EQUIP.DESCRIPTION FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        return sensorType[cursor.fetchone()[0]]

    def getModel(self, cursor):
        cursor.execute("SELECT EQUIP.MODELNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getSerialNumber(self, cursor):
        cursor.execute("SELECT EQUIP.SERIALNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getProducent(self, cursor):
        cursor.execute("SELECT EQUIP.MANUFACTURER FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getCalibrationPeriod(self, cursor):
        cursor.execute("SELECT EQUIP.UD7 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0][0]

    def getCalibrationDate(self, cursor):
        cursor.execute("SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]

    def getRange(self, cursor):
        cursor.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + self.inventoryNumber + "'")
        return cursor.fetchone()[0]


