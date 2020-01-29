import pyodbc

def connectWithDatabase():
    connPESensorsDatabase = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                           'Server=WPLSXSQL1;'
                                           'Database=sensmandb;'
                                           'uid=admuser;pwd=admu$er;'
                                           )
    return connPESensorsDatabase.cursor()

import pyodbc


def getInventoryNumber(inventoryNumber, cursor):
    cursor.execute("SELECT nr_zd FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    inventoryNumber = cursor.fetchone()[0]
    return inventoryNumber


def getType(inventoryNumber, cursor):
    cursor.execute("SELECT typ_id FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    type = cursor.fetchone()[0]
    return type


def getModel(inventoryNumber, cursor):
    cursor.execute("SELECT k_modelu FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    model = cursor.fetchone()[0]
    return model


def getSerialNumber(inventoryNumber, cursor):
    cursor.execute("SELECT n_seryjny FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    serialNumber = cursor.fetchone()[0]
    return serialNumber


def getProducent(inventoryNumber, cursor):
    cursor.execute("SELECT prod FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    producent = cursor.fetchone()[0]
    return producent


def getCalibrationPeriod(inventoryNumber, cursor):
    cursor.execute("SELECT okres_k FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    calibrationPeriod = cursor.fetchone()[0]
    return calibrationPeriod


def getCalibrationDate(inventoryNumber, cursor):
    cursor.execute("SELECT kolejna_k FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    calibrationDate = cursor.fetchone()[0]
    return calibrationDate


def getStatus(inventoryNumber, cursor):
    cursor.execute("SELECT status FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    status = cursor.fetchone()[0]
    return status


def getMinAnalogSignal(inventoryNumber, cursor):
    cursor.execute("SELECT syg_ana_min FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    minAnalogSignal = cursor.fetchone()[0]
    if minAnalogSignal is None:
        return ''
    else:
        return minAnalogSignal


def getMaxAnalogSignal(inventoryNumber, cursor):
    cursor.execute("SELECT syg_ana_max FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    maxAnalogSignal = cursor.fetchone()[0]
    if maxAnalogSignal is None:
        return ''
    else:
        return maxAnalogSignal


def getUnitAnalogSignal(inventoryNumber, cursor):
    cursor.execute("SELECT jednostka_ana FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    unitAnalogSignal = cursor.fetchone()[0]
    if unitAnalogSignal is None:
        return ''
    else:
        return unitAnalogSignal


def getMinMeasSignal(inventoryNumber, cursor):
    cursor.execute("SELECT syg_mierz_min FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    minMeasSignal = cursor.fetchone()[0]
    if minMeasSignal is None:
        return ''
    else:
        return minMeasSignal


def getMaxMeasSignal(inventoryNumber, cursor):
    cursor.execute("SELECT syg_mierz_max FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    maxMeasSignal = cursor.fetchone()[0]
    if maxMeasSignal is None:
        return ''
    else:
        return maxMeasSignal


def getUnitMeasSignal(inventoryNumber, cursor):
    cursor.execute("SELECT jednostka_mierz FROM Baza_czujniki WHERE nr_zd = '" + inventoryNumber + "'")
    unitMeasSignal = cursor.fetchone()[0]
    if unitMeasSignal is None:
        return ''
    else:
        return unitMeasSignal


#def addNewSensor(cursor, inventoryNumber, model, serialNumber, producent, calibrationPeriod, calibrationDate, status, minAnalogSignal, maxAnalogSignal, unitAnalogSignal, minMeasSignal, maxMeasSignal, unitMeasSignal, type):
#    query = "INSERT INTO Baza_czujniki (nr_zd, k_modelu, n_seryjny, prod, okres_k, kolejna_k, status, syg_ana_min, syg_ana_max, jednostka_ana, syg_mierz_min, syg_mierz_max, jednostka_mierz, typ_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
#    cursor.execute(query, (inventoryNumber, model, serialNumber, producent, calibrationPeriod, calibrationDate, status, minAnalogSignal, maxAnalogSignal, unitAnalogSignal, minMeasSignal, maxMeasSignal, unitMeasSignal, type))
#    cursor.commit()




