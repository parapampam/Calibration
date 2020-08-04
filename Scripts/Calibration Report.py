# -*- coding: utf-8 -*-
import datetime as datetime
import pyodbc
import datetime
import Databases
import sys
import calendar
import locale
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment

from openpyxl.utils import get_column_letter

from openpyxl.styles import PatternFill, Border, Side

locale.setlocale(locale.LC_ALL, "pl_PL")

overdue_measurement_instruments = Databases.MP2().get_inventory_number_overdue_measurement_instruments()
current_measurement_instruments = Databases.MP2().get_inventory_number_current_measurement_instruments()
next_measurement_instruments = Databases.MP2().get_inventory_number_next_measurement_instruments()

print(overdue_measurement_instruments)
print(current_measurement_instruments)
print(next_measurement_instruments)

thin_border = Border(left=Side(style='thin'),
                     right=Side(style='thin'),
                     top=Side(style='thin'),
                     bottom=Side(style='thin'))

pe = Databases.PE()
mp2 = Databases.MP2()
workbook = Workbook()
sheet = workbook.active
sheet.freeze_panes = 'B2'
sheet.title = calendar.month_name[datetime.date.today().month] + str(datetime.date.today().year)

sheet["A1"] = "Kod obiektu"
sheet["B1"] = "Typ przyrządu pomiarowego"
sheet["C1"] = "Numer inwenatrzowy"
sheet["D1"] = "Data kalibracji"
sheet["E1"] = "Osoba odpowiedzialna/zespół"
sheet["F1"] = "Numer seryjny"
sheet["G1"] = "Model"
sheet["H1"] = "Zakres pomiarowy"
sheet["I1"] = "Czasookres kalibracji"


def create_table(inventory_numbers):
    max_row = sheet.max_row
    for i in range(0, len(inventory_numbers)):
        # Kod obiektu
        sheet["A" + str(i + max_row + 1)] = mp2.get_object_code(inventory_numbers[i])
        # Typ przyrządu pomiarowego
        sheet["B" + str(i + max_row + 1)] = pe.get_type_name(inventory_numbers[i])
        # Numer inwentarzowy
        sheet["C" + str(i + max_row + 1)] = inventory_numbers[i]
        # Data kalibracji
        sheet["D" + str(i + max_row + 1)] = mp2.get_calibration_date(inventory_numbers[i]).strftime("%m.%Y")
        # Osoba odpowiedzialna/zespół za dostarczenie przyrządu pomiarowego do kalibracji
        if "wp" in pe.get_status(inventory_numbers[i]):
            responsible_employee = pe.get_responsible_employee(inventory_numbers[i])
        else:
            responsible_employee = mp2.get_team(inventory_numbers[i])
        sheet["E" + str(i + max_row + 1)] = responsible_employee
        # Numer seryjny
        sheet["F" + str(i + max_row + 1)] = pe.get_serial_number(inventory_numbers[i])
        # Model
        sheet["G" + str(i + max_row + 1)] = pe.get_model(inventory_numbers[i])
        # Zakres pomiarowy
        sheet["H" + str(i + max_row + 1)] = pe.get_range(inventory_numbers[i])
        # Czasookres kalibracji
        calibration_period = pe.get_calibration_period(inventory_numbers[i])
        if calibration_period == 1:
            calibration_period = str(calibration_period) + " rok"
        elif calibration_period in range(2, 5):
            calibration_period = str(calibration_period) + " lata"
        elif calibration_period == 5:
            calibration_period = str(calibration_period) + " lat"
        else:
            pass
        sheet["I" + str(i + max_row + 1)] = calibration_period


def fill_color(overdue_inventory_numbers, current_inventory_numbers):
    red = 'FF0000'
    yellow = 'FFFF00'
    green = '00FF00'
    max_row = sheet.max_row
    for column in range(sheet.min_column, sheet.max_column + 1):
        sheet.cell(1, column).border = thin_border
        for row in range(2, max_row + 1):
            sheet.cell(row, column).border = thin_border
            if row <= len(overdue_inventory_numbers) + 1:
                sheet.cell(row, column).fill = PatternFill(start_color=red, end_color=red, fill_type='solid')
            elif row <= len(overdue_inventory_numbers) + len(current_inventory_numbers) + 1:
                sheet.cell(row, column).fill = PatternFill(start_color=yellow, end_color=yellow, fill_type='solid')
            else:
                sheet.cell(row, column).fill = PatternFill(start_color=green, end_color=green, fill_type='solid')


def set_columns_width():
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    for column in range(sheet.min_column, sheet.max_column + 1):
        width = 0
        for row in range(sheet.min_row, sheet.max_row + 1):
            value = sheet.cell(row, column).value
            if value is not None:
                if len(value) > width:
                    width = len(value)
        sheet.column_dimensions[columns[column - 1]].width = width + 2


create_table(overdue_measurement_instruments)
create_table(current_measurement_instruments)
create_table(next_measurement_instruments)
fill_color(overdue_measurement_instruments, current_measurement_instruments)

set_columns_width()

report_name = "Raport kalibracyjny PE {} {}.xlsx".format(calendar.month_name[datetime.date.today().month],
                                                         datetime.date.today().year)
workbook.save(filename=report_name)


def test(inventory_numbers):
    for i in range(0, len(inventory_numbers)):
        print(str(inventory_numbers[i]) + ": " + str(pe.if_exist(inventory_numbers[i])))


test(next_measurement_instruments)
#
# # sprawdzenie czy dany czujnik znajduje się bazie danych PE
# for i in all_measurement_instrument:
#     query = "SELECT nr_zd FROM Baza_czujniki WHERE nr_zd = '{}'".format(i)
#     cursor_PE.execute(query)
#     PE = cursor_PE.fetchone()
#     if PE is None:
#         # print("Przyrzad " + i + " nie znajduje sie w bazie danych PE")
#         pass
#     else:
#         # print("Przyrzad " + i + " znajduje sie w bazie danych PE")
#         pass
#
# # ZD3331 - istnieje typ czujnika
# # ZD2694 - nie istnieje typ czujnika
#
# mp2 = Databases.MP2("ZD1992")
# pe = Databases.PE("ZD1992")
#
#
# # na podstawie opisu MP2 dodanie nowego typu czujnika w PE
# def checkTypeInPE():
#     try:
#         cursor_PE.execute("SELECT * FROM Baza_typ_czujnika WHERE lo = N'{}'".format(mp2.getType()))
#         if cursor_PE.fetchone()[0]:
#             exist = True
#         else:
#             exist = False
#     except TypeError:
#         exist = False
#
#     if exist is True:
#         cursor_PE.execute("SELECT * FROM Baza_typ_czujnika WHERE lo = N'{}'".format(mp2.getType()))
#         return cursor_PE.fetchone()[0]
#     else:
#         cursor_PE.execute("SELECT TOP 1 id FROM Baza_typ_czujnika ORDER BY ID DESC")
#         x = cursor_PE.fetchone()[0] + 1
#         cursor_PE.execute("SET IDENTITY_INSERT Baza_typ_czujnika ON")
#         cursor_PE.execute("INSERT INTO Baza_typ_czujnika (id, sh, lo, mw) VALUES (?, ?, ?, ?)",
#                           [x, str(mp2.getType()).lower(), mp2.getType(), 1])
#         cursor_PE.execute("SET IDENTITY_INSERT Baza_typ_czujnika OFF")
#         cursor_PE.commit()
#         return x
#
#
# def addNewSensor(inventory_number, model, serial_number, producent, calibration_period, calibration_date,
#                  status, min_analog_signal, max_analog_signal, unit_analog_signal, min_meas_signal, max_meas_signal,
#                  unit_meas_signal, type):
#     query = "INSERT INTO Baza_czujniki (nr_zd, k_modelu, n_seryjny, prod, okres_k, kolejna_k, status, syg_ana_min, syg_ana_max, jednostka_ana, syg_mierz_min, syg_mierz_max, jednostka_mierz, typ_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
#     cursor_PE.execute(query, (
#         inventory_number, model, serial_number, producent, calibration_period, calibration_date, status,
#         min_analog_signal, max_analog_signal, unit_analog_signal, min_meas_signal, max_meas_signal, unit_meas_signal,
#         type))
#     cursor_PE.commit()
#
#
# # sprawdzenie czy dany czujnik znajdue się bazie danych PE i jeśli trzeba kopiujemy:
# if pe.measurementInstrumentInDatabase() is True:
#     pass
# else:
#     print("mie ma")
#     pe.addNewSensor(mp2.getModel(), mp2.getSerialNumber(), mp2.getProducent(), mp2.getCalibrationPeriod(),
#                     mp2.getCalibrationDate(),
#                     mp2.getStatus(), mp2.getMinAnalogSignal(), mp2.getMaxAnalogSignal(), mp2.getUnitAnalogSignal(),
#                     mp2.getMinMeasSignal(),
#                     mp2.getMaxMeasSignal(), mp2.getUnitMeasSignal(), checkTypeInPE())
#
#
# # cursor_PE.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
# # print(cursor_PE.fetchall())
# # cursor_PE.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'auth_user'")
# # print(cursor_PE.fetchall())
#
# def cleanPEDAtabase():
#     cursor_PE.execute("SELECT nr_zd FROM Baza_czujniki")
#     instruments = cursor_PE.fetchall()
#
#     for i in range(0, len(instruments)):
#         pe = Databases.PE(instruments[i][0])
#
#         if pe.getUnitAnalogSignal() is None:
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET jednostka_ana = '' WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#
#         if pe.getUnitMeasSignal() is None:
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET jednostka_mierz = '' WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#
#         if pe.getMinAnalogSignal() == 0.0 and pe.getMaxAnalogSignal() == 0.0:
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET syg_ana_min = NULL WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET syg_ana_max = NULL WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#
#         if pe.getMinAnalogSignal() is None and pe.getMaxAnalogSignal() is None:
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET jednostka_ana = '' WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#
#         if pe.getMinMeasSignal() == 0.0 and pe.getMaxMeasSignal() == 0.0:
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET syg_mierz_min = NULL WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET syg_mierz_max = NULL WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#
#         if pe.getMinMeasSignal() is None and pe.getMaxMeasSignal() is None and "Komora" not in pe.getType():
#             cursor_PE.execute(
#                 "UPDATE Baza_czujniki SET jednostka_mierz = '' WHERE nr_zd = N'{}'".format(pe.getInventoryNumber()))
#             cursor_PE.commit()
#
#
# cleanPEDAtabase()
