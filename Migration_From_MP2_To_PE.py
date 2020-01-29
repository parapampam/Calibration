import pyodbc
import os
import datetime
import PE_Database as PE
import MP2_Database as MP2


cursorMP2 = MP2.connectWithDatabase()
cursorPE = PE.connectWithDatabase()
sensorInventoryNumber = 'ZD7081'

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

def prepareInventoryNumber(inventoryNumber, cursor):
    return MP2.getInventoryNumber(inventoryNumber, cursor)


def prepareModel(inventoryNumber, cursor):
    return MP2.getModel(inventoryNumber, cursor)


def prepareSerialNumber(inventoryNumber, cursor):
    return MP2.getSerialNumber(inventoryNumber, cursor)


def prepareProducent(inventoryNumber, cursor):
    type = MP2.getType(inventoryNumber, cursor)
    producent = MP2.getProducent(inventoryNumber, cursor)
    model = MP2.getModel(inventoryNumber, cursor)
    # Czujnik ciśniena
    if type == '5' and 'STS ATM' in producent:
        return 'STS'
    # Waga
    elif type == '10':
        if 'Mettler Tole' in producent or 'METLER TOLED' in producent:
            return 'Mettler Toledo'
        else:
            return producent
    # Zestaw pomiarowy
    elif type == '11':
        if 'NI cDAQ' in model:
            return 'National Instruments'
        elif 'DEWE-43-A' in model:
            return 'DEWESoft'
        else:
            return producent
    # Oscyloskop
    elif type == '38':
        if 'ROHS' in producent:
            return 'Rohde&Schwarz'
        else:
            return producent
    else:
        return producent


def prepareCalibrationPeriod(inventoryNumber, cursor):
    return MP2.getCalibrationPeriod(inventoryNumber, cursor)


def prepareCalibrationDate(inventoryNumber, cursor):
    date = MP2.getCalibrationDate(inventoryNumber, cursor)
    if date == 'w kalibracji':
        return datetime.date.today()
    elif date == 'archiwum':
        return datetime.date.today()
    else:
        return datetime.date(int(date[3:]), int(date[:2]), daysInMonth[date[:2]])


def prepareStatus(inventoryNumber, cursor):
    date = MP2.getCalibrationDate(inventoryNumber, cursor)
    if date == 'w kalibracji':
        return 'wk'
    elif date == 'archiwum':
        return 'wn'
    else:
        return 'ns'


def prepareMinAnalogSignal(inventoryNumber, cursor):
    type = MP2.getType(inventoryNumber, cursor)
    range = MP2.getRange(inventoryNumber, cursor)
    if range is not None:
        if 'V' in range or 'mA' in range:
            return range.split('_')[0]
        # Moduł CANopen
        if 'V' in range or 'mA' in range and type == '39':
            return ''
        else:
            return ''
    else:
        return ''


def prepareMaxAnalogSignal(inventoryNumber, cursor):
    type = MP2.getType(inventoryNumber, cursor)
    range = MP2.getRange(inventoryNumber, cursor)
    if range is not None:
        # Moduł CANopen
        if type == '39':
            return ''
        elif 'mA' in range:
            return range.split('_')[1][:(len(range.split('_')[1]) - len('mA'))]
        elif 'V' in range:
            return range.split('_')[1][:(len(range.split('_')[1]) - len('V'))]
        else:
           return ''
    else:
        return ''


def prepareUnitAnalogSignal(inventoryNumber, cursor):
    type = MP2.getType(inventoryNumber, cursor)
    range = MP2.getRange(inventoryNumber, cursor)
    if range is not None:
        # Moduł CANopen
        if type == '39':
            return ''
        elif 'mA' in range:
            return range.split('_')[1][-len('mA'):]
        elif 'V' in range:
            return range.split('_')[1][-len('V')]
        else:
            return ''
    else:
        return ''


def prepareMinMeasSignal(inventoryNumber, cursor):
    type = MP2.getType(inventoryNumber, cursor)
    range = MP2.getRange(inventoryNumber, cursor)
    if range is not None:
        # Moduł CANopen(39)
        if type == '39':
            return range.split('_')[0]
        # Czujnik z sygnałem analogowym
        elif 'V' in range or 'mA' in range:
            return range.split('_')[2]
        # Piecyk(25), komora klimatyczna(28), komora temperaturowa(36), komora szokowa(37), komora solna(40)
        elif type == '25' or type == '28' or type == '36' or type == '37' or type == '40':
            return ''
        # Czujnik bez sygnału analogowego
        else:
            return range.split('_')[0]
    else:
        return ''


def prepareMaxMeasSignal(inventoryNumber, cursor):
    type = MP2.getType(inventoryNumber, cursor)
    range = MP2.getRange(inventoryNumber, cursor)
    if range is not None:
        if 'V' in range or 'mA' in range:
            # Czujnik drogi(3)
            if type == '3':
                if 'mm' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('mm'))]
            # Czujnik ciśnienia(5)
            if type == '5':
                if 'mbar a' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('mbar a'))]
                elif 'bar a' in range:
                    return range.split('_')[3][:(len(range.split('')[3]) - len('bar a'))]
                elif 'mbar' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('mbar'))]
                elif 'bar' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('bar'))]
            # Przepływomierz(6)
            if type == '6':
                if 'mln/min' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('mln/min'))]
                elif 'ln/min' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('ln/min'))]
                elif 'cm3n/min' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('cm3n/min'))]
            # Czujnik siły(7)
            if type == '7':
                if 'kN' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('kN'))]
                elif 'N' in range:
                    return range.split('_')[3][:(len(range.split('_')[3]) - len('N'))]
            # Moduł CANopen(39)
            if type == '39':
                if 'V' in range:
                    return range.split('_')[1][:(len(range.split('_')[1]) - len('V'))]
                elif 'mA' in range:
                    return range.split('_')[1][:(len(range.split('_')[1]) - len('mA'))]
        else:
            # Suwmiarka(4)
            if type == '4':
                if 'mm' in range:
                    return range.split('_')[1][:(len(range.split('_')[1]) - len('mm'))]
            # Waga(10)
            if type == '10':
                if 'kg' in range:
                    return range.split('_')[1][:(len(range.split('_')[1]) - len('kg'))]
                elif 'g' in range:
                    return range.split('_')[1][:(len(range.split('_')[1]) - len('g'))]
            # Głębokościomierz(14)
            if  type == '14':
                if 'mm' in range:
                    return range.split('_')[1][:(len(range.split('_')[1]) - len('mm'))]
            # Mikrometr(16)
                if type == '16':
                    if 'mm' in range:
                        return range.split('_')[1][:(len(range.split('_')[1]) - len('mm'))]
            # Wyokościomierz(19)
                if type == '19':
                    if 'mm' in range:
                        return range.split('_')[1][:(len(range.split('_')[1]) - len('mm'))]
    else:
        return ''


def prepareUnitMeasSignal(inventoryNumber, cursor):
    type = MP2.getType(inventoryNumber, cursor)
    range = MP2.getRange(inventoryNumber, cursor)
    if range is not None:
        if 'V' in range or 'mA' in range:
            # Czujnik drogi(3)
            if type == '3':
                if 'mm' in range:
                    return 'mm'
            # Czujnik ciśnienia(5)
            if type == '5':
                if 'mbar a' in range:
                    return 'mbar a'
                elif 'bar a' in range:
                    return 'bar a'
                elif 'mbar' in range:
                    return 'mbar'
                elif 'bar' in range:
                    return 'bar'
            # Przepływomierz(6)
            if type == '6':
                if 'mln/min' in range:
                    return 'mln/min'
                elif 'ln/min' in range:
                    return 'ln/min'
                elif 'cm3n/min' in range:
                    return 'cm3n/min'
            # Czujnik siły(7)
            if type == '7':
                if 'kN' in range:
                    return 'kN'
                elif 'N' in range:
                    return 'N'
            # Moduł CANopen(39)
            if type == '39':
                if 'V' in range:
                    return 'V'
                elif 'mA' in range:
                    return 'mA'
        else:
            # Suwmiarka(4)
            if type == '4':
                if 'mm' in range:
                    return range.split('_')[1][-(len('mm')):]
            # Waga(10)
            if type == '10':
                if 'kg' in range:
                    return range.split('_')[1][-(len('kg')):]
                elif 'g' in range:
                    return range.split('_')[1][-(len('g')):]
            # Głebokościomierz(14)
            if type == '14':
                if 'mm' in range:
                    return range.split('_')[1][-(len('mm')):]
            # Miktrometr(16)
            if type == '16':
                if 'mm' in range:
                    return range.split('_')[1][-(len('mm')):]
            # Wysokościomierz(19)
            if type == '19':
                if 'mm' in range:
                    return range.split('_')[1][:(len(range.split('_')[1]) - len('mm'))]
            # Piecyk(25)
            if type == '25':
                return range
            # Komora klimatyczna(28)
            if type == '28':
                return range
            # Komora temperaturowa(36)
            if type == '36':
                return range
            # Komora szokowa(37)
            if type == '37':
                return range
            # Komora solna(40)
            if type == '40':
                return range
    else:
        return ''


def prepareType(inventoryNumber, cursor):
    return MP2.getType(inventoryNumber, cursor)


sensor = {
    'inventoryNumber' : prepareInventoryNumber(sensorInventoryNumber, cursorMP2),
    'type' : prepareType(sensorInventoryNumber, cursorMP2),
    'model': prepareModel(sensorInventoryNumber, cursorMP2),
    'serialNumber' : prepareSerialNumber(sensorInventoryNumber, cursorMP2),
    'producent' : prepareProducent(sensorInventoryNumber, cursorMP2),
    'calibrationPeriod' : prepareCalibrationPeriod(sensorInventoryNumber, cursorMP2),
    'calibrationDate' : prepareCalibrationDate(sensorInventoryNumber, cursorMP2),
    'status': prepareStatus(sensorInventoryNumber, cursorMP2),
    'minAnalogSignal' : prepareMinAnalogSignal(sensorInventoryNumber, cursorMP2),
    'maxAnalogSignal' : prepareMaxAnalogSignal(sensorInventoryNumber, cursorMP2),
    'unitAnalogSignal' : prepareUnitAnalogSignal(sensorInventoryNumber, cursorMP2),
    'minMeasSignal' : prepareMinMeasSignal(sensorInventoryNumber, cursorMP2),
    'maxMeasSignal' : prepareMaxMeasSignal(sensorInventoryNumber, cursorMP2),
    'unitMeasSignal' : prepareUnitMeasSignal(sensorInventoryNumber, cursorMP2)
}


PE.addNewSensor(cursorPE, sensor['inventoryNumber'], sensor['model'], sensor['serialNumber'], sensor['producent'], sensor['calibrationPeriod'], sensor['calibrationDate'], sensor['status'], sensor['minAnalogSignal'], sensor['maxAnalogSignal'], sensor['unitAnalogSignal'], sensor['minMeasSignal'], sensor['maxAnalogSignal'], sensor['unitMeasSignal'], sensor['type'])

