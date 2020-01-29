import pyodbc
import datetime

sensorToMigration = 'ZD7080'

sensor = {
    'inventoryNumber': '',
    'type': '',
    'model': '',
    'serialNumber': '',
    'producent': '',
    'calibrationPeriod': '',
    'calibrationDate': '',
    'status': 'wk',
    'minAnalogSignal': '',
    'maxAnalogSignal': '',
    'unitAnalogSignal': '',
    'minMeasSignal': '',
    'maxMeasSignal': '',
    'unitMeasSignal': ''
}

sensorType = {
    'Czujnik kata': '1',
    'Niezidentyfokowany': '2',
    'Czujnik drogi': '3',                           #dodany
    'Suwmiarka': '4',                               #dodany
    'Czujnik cisnienia': '5',                       #dodany
    'Przeplywomierz': '6',                          #dodany
    'Czujnik sily': '7',                            #dodany
    'Czujnik laserowy': '8',
    'Waga': '10',                                   #dodany
    'Zestaw pomiarowy': '11',                       #dodany
    'Glebokosciomierz': '14',                       #dodany
    'Mikrometr': '16',                              #dodany
    'Multimetr': '18',                              #dodany
    'Wysokosciomierz': '19',                        #dodany
    'Piecyk': '25',                                 #dodany
    'Komora klimatyczna': '28',                     #dodany
    'Komora temperaturowa': '36',                   #dodany
    'Komora szokowa': '37',                         #dodany
    'Oscyloskop': '38',                             #dodany
    'Modul CANopen': '39',                          #dodany
    'Komora solna': '40',                           #dodany
    'Przetwornik punktu rosy i temperatury': '41',  #dodany
    'Przetwornik wilgotnosci i temperatury': '42'   #dodany
}

daysInMonth = {
    '01': 31,
    '02': 28,
    '03': 31,
    '04': 30,
    '05': 31,
    '06': 30,
    '07': 31,
    '08': 31,
    '09': 30,
    '10': 31,
    '11': 30,
    '12': 31
}

def getInventoryNumberFromMP2(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    sensor['inventoryNumber'] = row[0]

def getTypeFromMP2(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.DESCRIPTION FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    sensor['type'] = sensorType[row[0]]

def getModelFromMP2(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.MODELNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    sensor['model'] = row[0]

def getSerialNumberFromMP2(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.SERIALNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    sensor['serialNumber'] = row[0]

def getProducentFromMP2(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.MANUFACTURER FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    # Czujnik ciśniena
    if sensor['type'] == '5' and 'STS ATM' in row[0]:
        sensor['producent'] = 'STS'
    # Waga
    elif sensor['type'] == '10':
        if 'Mettler Tole' in row[0] or 'METLER TOLED' in row[0]:
            sensor['producent'] = 'Mettler Toledo'
        else:
            sensor['producent'] = row[0]
    # Zestaw pomiarowy
    elif sensor['type'] == '11':
        if 'NI cDAQ' in sensor['model']:
            sensor['producent'] = 'National Instruments'
        elif 'DEWE-43-A' in sensor['model']:
            sensor['producent'] = 'DEWESoft'
        else:
            sensor['producent'] = row[0]
    # Oscyloskop
    elif sensor['type'] == '38':
        if 'ROHS' in row[0]:
            sensor['producent'] = 'Rohde&Schwarz'
        else:
            sensor['producent'] = row[0]
    else:
        sensor['producent'] = row[0]

def getCalibrationPeriod(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD7 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    sensor['calibrationPeriod'] = row[0][0]

def getCalibrationDateFromMP2(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    if row[0] == 'w kalibracji':
        sensor['calibrationDate'] = datetime.date.today()
        sensor['status'] = 'wk'
    elif row[0] == 'archiwum':
        sensor['calibrationDate'] = datetime.date.today()
        sensor['status'] = 'wn'
    else:
        sensor['calibrationDate'] = datetime.date(int(row[0][3:]), int(row[0][:2]), daysInMonth[row[0][:2]])
        sensor['status'] = 'ns'

def getMinAnalogSignal(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    if row[0] is not None:
        if 'V' in row[0] or 'mA' in row[0]:
            sensor['minAnalogSignal'] = row[0].split('_')[0]
        # Moduł CANopen
        if 'V' in row[0] or 'mA' in row[0] and sensor['type'] == '39':
            sensor['minAnalogSignal'] = ''
        else:
            sensor['minAnalogSignal'] = ''
    else:
        sensor['minAnalogSignal'] = ''


def getMaxAnalogSignal(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    if row[0] is not None:
        # Moduł CANopen
        if sensor['type'] == '39':
            sensor['maxAnalogSignal'] = ''
        elif 'mA' in row[0]:
            sensor['maxAnalogSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('mA'))]
        elif 'V' in row[0]:
            sensor['maxAnalogSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('V'))]
        else:
            sensor['maxAnalogSignal'] = ''
    else:
        sensor['maxAnalogSignal'] = ''

def getUnitAnalogSignal(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    if row[0] is not None:
        # Moduł CANopen
        if sensor['type'] == '39':
            sensor['maxAnalogSignal'] = ''
        elif 'mA' in row[0]:
            sensor['unitAnalogSignal'] = row[0].split('_')[1][-len('mA'):]
        elif 'V' in row[0]:
            sensor['unitAnalogSignal'] = row[0].split('_')[1][-len('V')]
        else:
            sensor['unitAnalogSignal'] = ''
    else:
        sensor['unitAnalogSignal'] = ''

def getMinMeasSignal(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    if row[0] is not None:
        # Moduł CANopen
        if sensor['type'] == '39':
            sensor['minMeasSignal'] = row[0].split('_')[0]
        # Czujnik z sygnałem analogowym
        elif 'V' in row[0] or 'mA' in row[0]:
            sensor['minMeasSignal'] = row[0].split('_')[2]
        # Piecyk
        elif sensor['type'] == '25':
            sensor['minMeasSignal'] = ''
        # Komora klimatyczna
        elif sensor['type'] == '28':
            sensor['minMeasSignal'] = ''
        # Komora temperaturowa
        elif sensor['type'] == '36':
            sensor['minMeasSignal'] = ''
        # Komora szokowa
        elif sensor['type'] == '37':
            sensor['minMeasSignal'] = ''
        # Komora solna
        elif sensor['type'] == '40':
            sensor['minMeasSignal'] == ''
        # Czujnik bez sygnału analogowego
        else:
            sensor['minMeasSignal'] = row[0].split('_')[0]
    else:
        sensor['minMeasSignal'] = ''

def getMaxMeasSignal(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    if row[0] is not None:
        if 'V' in row[0] or 'mA' in row[0]:
            # Czujnik drogi
            if sensor['type'] == '3':
                if 'mm' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('mm'))]
            # Czujnik ciśnienia
            if sensor['type'] == '5':
                if 'mbar a' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('mbar a'))]
                elif 'bar a' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('')[3]) - len('bar a'))]
                elif 'mbar' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('mbar'))]
                elif 'bar' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('bar'))]
            # Przepływomierz
            if sensor['type'] == '6':
                if 'mln/min' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('mln/min'))]
                elif 'ln/min' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('ln/min'))]
                elif 'cm3n/min' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('cm3n/min'))]
            # Czujnik siły
            if sensor['type'] == '7':
                if 'kN' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('kN'))]
                elif 'N' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[3][:(len(row[0].split('_')[3]) - len('N'))]
            # Moduł CANopen
            if sensor['type'] == '39':
                if 'V' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('V'))]
                elif 'mA' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('mA'))]
        else:
            # Suwmiarka
            if sensor['type'] == '4':
                if 'mm' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('mm'))]
            # Waga
            if sensor['type'] == '10':
                if 'kg' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('kg'))]
                elif 'g' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('g'))]
            # Głębokościomierz
            if sensor['type'] == '14':
                if 'mm' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('mm'))]
            # Mikrometr
            if sensor['type'] == '16':
                if 'mm' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('mm'))]
            # Wysokościomierz
            if sensor['type'] == '19':
                if 'mm' in row[0]:
                    sensor['maxMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('mm'))]
    else:
        sensor['maxMeasSignal'] = ''

def getUnitMeasSignal(sensorToMigration):
    cursorMP2.execute("SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + sensorToMigration + "'")
    row = cursorMP2.fetchone()
    if row[0] is not None:
        if 'V' in row[0] or 'mA' in row[0]:
            # Czujnik drogi
            if sensor['type'] == '3':
                if 'mm' in row[0]:
                    sensor['unitMeasSignal'] = 'mm'
            # Czujnik ciśnienia
            if sensor['type'] == '5':
                if 'mbar a' in row[0]:
                    sensor['unitMeasSignal'] = 'mbar a'
                elif 'bar a' in row[0]:
                    sensor['unitMeasSignal'] = 'bar a'
                elif 'mbar' in row[0]:
                    sensor['unitMeasSignal'] = 'mbar'
                elif 'bar' in row[0]:
                    sensor['unitMeasSignal'] = 'bar'
            # Przepływomierz
            if sensor['type'] == '6':
                if 'mln/min' in row[0]:
                    sensor['unitMeasSignal'] = 'mln/min'
                elif 'ln/min' in row[0]:
                    sensor['unitMeasSignal'] = 'ln/min'
                elif 'cm3n/min' in row[0]:
                    sensor['unitMeasSignal'] = 'cm3n/min'
            # Czujnik siły
            if sensor['type'] == '7':
                if 'kN' in row[0]:
                    sensor['unitMeasSignal'] = 'kN'
                elif 'N' in row[0]:
                    sensor['unitMeasSignal'] = 'N'
            # Moduł CANopen
            if sensor['type'] == '39':
                if 'V' in row[0]:
                    sensor['unitMeasSignal'] = 'V'
                elif 'mA' in row[0]:
                    sensor['unitMeasSignal'] = 'mA'
        else:
            # Suwmiarka
            if sensor['type'] == '4':
                if 'mm' in row[0]:
                    sensor['unitMeasSignal'] = row[0].split('_')[1][-(len('mm')):]
            # Waga
            if sensor['type'] == '10':
                if 'kg' in row[0]:
                    sensor['unitMeasSignal'] = row[0].split('_')[1][-(len('kg')):]
                elif 'g' in row[0]:
                    sensor['unitMeasSignal'] = row[0].split('_')[1][-(len('g')):]
            # Głebokościomierz
            if sensor['type'] == '14':
                if 'mm' in row[0]:
                    sensor['unitMeasSignal'] = row[0].split('_')[1][-(len('mm')):]
            # Miktrometr
            if sensor['type'] == '16':
                if 'mm' in row[0]:
                    sensor['unitMeasSignal'] = row[0].split('_')[1][-(len('mm')):]
            # Wysokościomierz
            if sensor['type'] == '19':
                if 'mm' in row[0]:
                    sensor['unitMeasSignal'] = row[0].split('_')[1][:(len(row[0].split('_')[1]) - len('mm'))]
            # Piecyk
            if sensor['type'] == '25':
                sensor['unitMeasSignal'] = row[0]
            # Komora klimatyczna
            if sensor['type'] == '28':
                sensor['unitMeasSignal'] = row[0]
            # Komora temperaturowa
            if sensor['type'] == '36':
                sensor['unitMeasSignal'] = row[0]
            # Komora szokowa
            if sensor['type'] == '37':
                sensor['unitMeasSignal'] = row[0]
            # Komora solna
            if sensor['type'] == '40':
                sensor['unitMeasSignal'] = row[0]
    else:
        sensor['unitMeasSignal'] = ''

connPESensorDatabase = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=WPLSXSQL1;'
                      'Database=sensmandb;'
                      'uid=admuser;pwd=admu$er;'
                      )

cursorPESensorDatabase = connPESensorDatabase.cursor()
cursorPESensorDatabase.execute("SELECT * FROM Baza_czujniki WHERE nr_zd = '" + sensorToMigration + "'")
row = cursorPESensorDatabase.fetchone()
print(row)



connMP2 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                       'Server=wplsxsql1;'
                       'Database=MP2_PRO;'
                       'uid=MP2_Read;pwd=Read_MP2;'
                       )

cursorMP2 = connMP2.cursor()
cursorMP2.execute("SELECT EQUIP.EQNUM, EQUIP.DESCRIPTION, EQUIP.MODELNUM, EQUIP.SERIALNUM, EQUIP.MANUFACTURER, "
                  "EQUIP.UD7, EQUIP.UD9, EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = 'ZD7007' ")
for row in cursorMP2:
    print(row)

getInventoryNumberFromMP2(sensorToMigration)
getTypeFromMP2(sensorToMigration)
getModelFromMP2(sensorToMigration)
getSerialNumberFromMP2(sensorToMigration)
getProducentFromMP2(sensorToMigration)
getCalibrationPeriod(sensorToMigration)
getCalibrationDateFromMP2(sensorToMigration)
getMinAnalogSignal(sensorToMigration)
getMaxAnalogSignal(sensorToMigration)
getUnitAnalogSignal(sensorToMigration)
getMinMeasSignal(sensorToMigration)
getMaxMeasSignal(sensorToMigration)
getUnitMeasSignal(sensorToMigration)


query = "INSERT INTO Baza_czujniki (nr_zd, k_modelu, n_seryjny, prod, okres_k, kolejna_k, status, syg_ana_min, syg_ana_max, jednostka_ana, syg_mierz_min, syg_mierz_max, jednostka_mierz, typ_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"


print(sensor)


#cursorPESensorDatabase.execute(query, (sensor['inventoryNumber'], sensor['model'], sensor['serialNumber'], sensor['producent'], sensor['calibrationPeriod'], sensor['calibrationDate'], sensor['status'], sensor['minAnalogSignal'], sensor['maxAnalogSignal'], sensor['unitAnalogSignal'], sensor['minMeasSignal'], sensor['maxMeasSignal'], sensor['unitMeasSignal'], sensor['type']))
#cursorPESensorDatabase.commit()
#connPESensorDatabase.close()
#connMP2.close()
