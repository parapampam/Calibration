import pyodbc

def connectWithPESensorsDatabase():
    connPESensorsDatabase = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                           'Server=WPLSXSQL1;'
                                           'Database=sensmandb;'
                                           'uid=admuser;pwd=admu$er;'
                                           )
    return connPESensorsDatabase.cursor()


def connectWithMP2Database():
    connMP2 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                             'Server=wplsxsql1;'
                             'Database=MP2_PRO;'
                             'uid=MP2_Read;pwd=Read_MP2;'
                             )

    return connMP2.cursor()


def lastAddedSensorInMP2Database(cursor):
    cursor.execute("SELECT EQUIP.EQNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.EQNUM LIKE 'LP[_]%' ORDER BY EQUIP.EQNUM DESC")
    return cursor.fetchone()[0]

