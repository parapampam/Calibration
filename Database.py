import pyodbc

def connectWithPESensorsDatabase():
    connPESensorsDatabase = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                           'Server=WPLSXSQL1;'
                                           'Database=sensmandb;'
                                           'uid=admuser;pwd=admu$er;'
                                           )
    cursor = connPESensorsDatabase.cursor()
    return cursor