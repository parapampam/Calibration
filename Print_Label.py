# Czujniki ciśnienia - dodane

import pyodbc
import os

import PE_Database as PE
import MP2_Database as MP2


sensorInventoryNumber = 'ZD7081'
cursorPE = PE.connectWithDatabase()
pathToLabel = "//wplcswroclaw12m/pdp/01_Team's/TQC_MTS/Kalibracje/FAQ/Program kalibracyjny/"

sensor = {'inventoryNumber': PE.getInventoryNumber(sensorInventoryNumber, cursorPE),
          'type': PE.getType(sensorInventoryNumber, cursorPE),
          'model': PE.getModel(sensorInventoryNumber, cursorPE),
          'serialNumber': PE.getSerialNumber(sensorInventoryNumber, cursorPE),
          'producent': PE.getProducent(sensorInventoryNumber, cursorPE),
          'calibrationPeriod': PE.getCalibrationPeriod(sensorInventoryNumber, cursorPE),
          'calibrationDate': PE.getCalibrationDate(sensorInventoryNumber, cursorPE),
          'status': PE.getStatus(sensorInventoryNumber, cursorPE),
          'minAnalogSignal': PE.getMinAnalogSignal(sensorInventoryNumber, cursorPE),
          'maxAnalogSignal': PE.getMaxAnalogSignal(sensorInventoryNumber, cursorPE),
          'unitAnalogSignal': PE.getUnitAnalogSignal(sensorInventoryNumber, cursorPE),
          'minMeasSignal': PE.getMinMeasSignal(sensorInventoryNumber, cursorPE),
          'maxMeasSignal': PE.getMaxMeasSignal(sensorInventoryNumber, cursorPE),
          'unitMeasSignal': PE.getUnitMeasSignal(sensorInventoryNumber, cursorPE)
          }


def preperePathToLabelSheme():
    # Czujnik ciśnienia
    if sensor['type'] == 5:
        return os.path.join(pathToLabel, 'Label Pressure Sensor.txt')
    # Czujnik siły
    elif sensor['type'] == 7:
        return os.path.join(pathToLabel, 'Label Force Sensor.txt')
    # Zestaw pomiarowy
    elif sensor['type'] == 11:
        # DEWESoft
        if "DEWEsoft" is sensor['producent']:
            return os.path.join(pathToLabel, 'Label DEWEsoft Measurement Set.txt')
        # Reszta zestawów pomiarowych
        else:
            return os.path.join(pathToLabel, 'Label Measurement Set.txt')


def openLabelSheme(path):
    if os.path.isfile(path):
        file = open(path)
        label = file.read()
        file.close()
        return label


def replaceInventoryNumber(label):
    if "xInventoryNumber" in label:
        return label.replace("xInventoryNumber", sensor['inventoryNumber'])
    else:
        return label


def replaceModel(label):
    if "xModel" in label:
        return label.replace("xModel", sensor['model'])
    else:
        return label


def replaceSerialNumber(label):
    if "xSerialNumber" in label:
        return label.replace("xSerialNumber", sensor['serialNumber'])
    else:
        return label


def replaceCalibrationDate(label):
    if "CalibrationDate" in label:
        return label.replace("xCalibrationDate", sensor['calibrationDate'].strftime("%m.%Y"))
    else:
         return label


def replaceCalibrationPlace(label):
    if "xCalibrationPlace" in label:
        # Czujnik ciśnienia(5)
        if sensor['type'] == 5:
            # jendostka
            if "bar a" is sensor['unitMeasSignal'] or "mbar a" is sensor['unitMeasSignal']:
                return label.replace("xCalibrationPlace", "External")
            else:
                # zakres
                if sensor['maxMeasSignal'] > 35:
                    return label.replace("xCalibrationPlace", "External")
                else:
                    return label.replace("xCalibrationPlace", "Internal")
        else:
            return label.replace("xCalibrationPlace", "Internal")
    else:
        return label


def replaceMinAnalogSignal(label):
    if "xMinAnalogSignal" in label:
        # Czujnik ciśnienia
        if sensor['type'] == 5:
            if sensor['minAnalogSignal'] % 1 == 0:
                return label.replace("xMinAnalogSignal", str(int(sensor['minAnalogSignal'])))
            else:
                return label.replace("xMinAnalogSignal", int(sensor['minAnalogSignal']))
        else:
            return label
    else:
        return label


def replaceMaxAnalogSignal(label):
    if "xMaxAnalogSignal" in label:
        # Czujnik ciśnienia
        if sensor['type'] == 5:
            if sensor['maxAnalogSignal'] % 1 == 0:
                return label.replace("xMaxAnalogSignal", str(int(sensor['maxAnalogSignal'])))
            else:
                return label.replace("xMaxAnalogSignal", int(sensor['maxAnalogSignal']))
        else:
            return label
    else:
        return label


def replaceUnitAnalogSignal(label):
    if "xUnitAnalogSignal" in label:
        if sensor['unitAnalogSignal'] == '':
            return label
        else:
            return label.replace("xUnitAnalogSignal", sensor['unitAnalogSignal'])
    else:
        return label


def replaceMinMeasSignal(label):
    if "xMinMeasSignal" in label:
        # Czujnik ciśnienia(5)
        if sensor['type'] == 5:
            if sensor['minMeasSignal'] % 1 == 0:
                return label.replace("xMinMeasSignal", str(int(sensor['minMeasSignal'])))
            else:
                return label.replace("xMinMeasSignal", int(sensor['minMeasSignal']))
        else:
            return label
    else:
        return label


def replaceMaxMeasSignal(label):
    if "xMaxMeasSignal" in label:
        # Czujnik ciśnienia(5)
        if sensor['type'] == 5:
            if sensor['maxMeasSignal'] == 5:
                return label.replace("xMaxMeasSignal", str(int(sensor['maxMeasSignal'])))
            else:
                return label.replace("xMaxMeasSignal", str(int(sensor['maxMeasSignal'])))
        else:
            return label
    else:
        return label


def replaceUnitMeasSignal(label):
    if "xUnitMeasSignal" in label:
        if sensor['unitMeasSignal'] == '':
            return label
        else:
            return label.replace("xUnitMeasSignal", sensor['unitMeasSignal'])
    else:
        return label


def replaceSqueezeRange(label):
    if "xSqueezeRange" in label:
        a = label.splitlines()
        count = 0
        for char in a:
            if "xSqueezeRange" in char:
                break
            count = count + 1
        if 1 <= len(a[count].split(';')[1]) <= 15:
            return label.replace("xSqueezeRange", "q100")
        elif 16 <= len(a[count].split(';')[1]) <= 20:
            return label.replace("xSqueezeRange", "q80")
        else:
            return label.replace("xSqueezeRange", "q60")
    else:
        return label


def replaceOperator(label):
    if "xOperator" in label:
        return label.replace("xOperator", os.getlogin()[0] + os.getlogin().lower()[1:])
    else:
        return label


def replaceSqueezeOperator(label):
    if "xSqueezeOperator" in label:
        lengthOperator = len(os.getlogin())
        if 1 <= lengthOperator <= 15:
            return label.replace("xSqueezeOperator", "q100")
        elif 16 <= lengthOperator <= 20:
            return label.replace("xSqueezeOperator", "q80")
        else:
            return label.replace("xSqueezeOperator", "q60")
    else:
        return label


def replaceClass(label):
    if "xClass" in label:
        # Czujnik ciśnienia
        if sensor['type'] == 5:
            # jendostka
            if "bar a" is sensor['unitMeasSignal'] or "mbar a" is sensor['unitMeasSignal']:
                return label.replace("xClass", '')
            else:
                # zakres
                if sensor['maxMeasSignal'] > 35:
                    return label.replace("xClass", "")
                else:
                    return label.replace("xClass", "")
        else:
            return label
    else:
        return label


def replaceErrorValue(label):
    if "xErrorValue" in label:
        # Czujnik ciśnienia
        if sensor['type'] == 5:
            # jendostka
            if "bar a" is sensor['unitMeasSignal'] or "mbar a" is sensor['unitMeasSignal']:
                return label.replace("xErrorValue", '')
            else:
                # zakres
                if sensor['maxMeasSignal'] > 35:
                    return label.replace("xErrorValue", "")
                else:
                    return label.replace("xErrorValue", "")
    else:
        return label


def replaceSqueezeClass(label):
    if "xSqueezeClass" in label:
        # Czujnik ciśnienia
        if sensor['type'] == 5:
            # jendostka
            if "bar a" is sensor['unitMeasSignal'] or "mbar a" is sensor['unitMeasSignal']:
                return label.replace("xSqueezeClass", "q0")
            else:
                # zakres
                if sensor['maxMeasSignal'] > 35:
                    return label.replace("xSqueezeClass", "q0")
                else:
                    return label.replace("xSqueezeClass", "q0")
    else:
        return label


def deleteLinesWitchQ0(label):
    a = label.splitlines()
    count = 0
    for char in a:
        if "q0" in char:
            a[count] = ''
        count = count + 1
    return '\n'.join(a)


print(sensor)
labelScheme = openLabelSheme(preperePathToLabelSheme())
labelScheme = replaceInventoryNumber(labelScheme)
labelScheme = replaceModel(labelScheme)
labelScheme = replaceSerialNumber(labelScheme)
labelScheme = replaceCalibrationDate(labelScheme)
labelScheme = replaceCalibrationPlace(labelScheme)
labelScheme = replaceMinAnalogSignal(labelScheme)
labelScheme = replaceMaxAnalogSignal(labelScheme)
labelScheme = replaceUnitAnalogSignal(labelScheme)
labelScheme = replaceMinMeasSignal(labelScheme)
labelScheme = replaceMaxMeasSignal(labelScheme)
labelScheme = replaceUnitMeasSignal(labelScheme)
labelScheme = replaceOperator(labelScheme)
labelScheme = replaceSqueezeOperator(labelScheme)
labelScheme = replaceSqueezeRange(labelScheme)
labelScheme = replaceClass(labelScheme)
labelScheme = replaceErrorValue(labelScheme)
labelScheme = replaceSqueezeClass(labelScheme)
labelScheme = deleteLinesWitchQ0(labelScheme)

print(labelScheme)
