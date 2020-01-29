import pyodbc

sensorType = {
    'Czujnik kata': '1',
    'Niezidentyfokowany': '2',
    'Czujnik drogi': '3',
    'Suwmiarka': '4',
    'Czujnik cisnienia': '5',
    'Przeplywomierz': '6',
    'Czujnik sily': '7',
    'Czujnik laserowy': '8',
    'Waga': '10',
    'Zestaw pomiarowy': '11',
    'Glebokosciomierz': '14',
    'Mikrometr': '16',
    'Multimetr': '18',
    'Wysokosciomierz': '19',
    'Piecyk': '25',
    'Komora klimatyczna': '28',
    'Komora temperaturowa': '36',
    'Komora szokowa': '37',
    'Oscyloskop': '38',
    'Modul CANopen': '39',
    'Komora solna': '40',
    'Przetwornik punktu rosy i temperatury': '41',
    'Przetwornik wilgotnosci i temperatury': '42'
}


def connectWithDatabase():
    connMP2 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                             'Server=wplsxsql1;'
                             'Database=MP2_PRO;'
                             'uid=MP2_Read;pwd=Read_MP2;'
                             )

    return connMP2.cursor()


def lastAddedSensorInMP2Database(cursor):
    cursor.execute("SELECT EQUIP.EQNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.EQNUM LIKE 'LP[_]%' ORDER BY EQUIP.EQNUM DESC")
    return cursor.fetchone()[0]


def getInventoryNumber(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return cursor.fetchone()[0]


def getType(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.DESCRIPTION FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return sensorType[cursor.fetchone()[0]]


def getModel(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.MODELNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return cursor.fetchone()[0]


def getSerialNumber(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.SERIALNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return cursor.fetchone()[0]


def getProducent(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.MANUFACTURER FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return cursor.fetchone()[0]


def getCalibrationPeriod(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.UD7 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return cursor.fetchone()[0][0]


def getCalibrationDate(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return cursor.fetchone()[0]


def getRange(inventoryNumber, cursor):
    cursor.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + inventoryNumber + "'")
    return cursor.fetchone()[0]
