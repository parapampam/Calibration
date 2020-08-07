import Databases as Db


mp2 = Db.MP2()
pe = Db.PE()

objects_code = mp2.get_object_code_all_measurement_instruments()

mp2_inventory_numbers = []

for object_code in objects_code:
    mp2_inventory_numbers.append(mp2.get_inventory_number(object_code))



with Db.PE() as pe:
    for inventory_number in mp2_inventory_numbers:
        if pe.if_exist(inventory_number):
           pass
        else:
            print(" ".join([inventory_number, "nie istnieje w bazie PE\nCzy chcesz skopiować przyrząd pomiarowy z bazy MP2 do PE?"]))
            if input("t/n?") == "t":

                type = mp2.get_type(inventory_number)
                model = mp2.get_model(inventory_number)
                serial_number = mp2.get_serial_number(inventory_number)
                producent = mp2.get_producent(inventory_number)
                calibration_period = mp2.get_calibration_period(inventory_number)
                calibration_date = mp2.get_calibration_date(inventory_number)
                status = mp2.get_status(inventory_number)
                min_analog_signal = mp2.get_min_analog_signal(inventory_number)
                if min_analog_signal == "":
                    min_analog_signal = "NULL"
                max_analog_signal = mp2.get_max_analog_signal(inventory_number)
                if max_analog_signal == "":
                    max_analog_signal = "NULL"
                unit_analog_signal = mp2.get_unit_analog_signal(inventory_number)
                min_meas_signal = mp2.get_min_meas_signal(inventory_number)
                if min_meas_signal == "":
                    min_meas_signal = "NULL"
                max_meas_signal = mp2.get_max_meas_signal(inventory_number)
                if max_meas_signal == "":
                    max_meas_signal = "NULL"
                unit_meas_signal = mp2.get_unit_meas_signal(inventory_number)


                print(" ".join(["Numer inwentarzowy:", inventory_number]))
                print(" ".join(["Typ przyrządu pomiarowego:", type]))
                # print(" ".join(["Numer typu:", pe.get_type_number(type)]))
                print(" ".join(["Model przyrządu pomiarowego ", model]))
                print(" ".join(["Numer seryjny przyrządu pomiarowego", serial_number]))
                print(" ".join(["Producent:", producent]))
                print(" ".join(["Czasookres kalibracji:", calibration_period]))
                print(" ".join(["Data kalibracji:", str(calibration_date)]))
                print(" ".join(["Status:", status]))
                print(" ".join(["Dolny zakres sygnału analogowego:", min_analog_signal]))
                print(" ".join(["Górny zakres sygnału analogowego:", max_analog_signal]))
                print(" ".join(["Jednosta sygnału analogowego:", unit_analog_signal]))
                print(" ".join(["Dolny zakres sygnału mierzonego:", min_meas_signal]))
                print(" ".join(["Górny zakres sygnału mierzonego:", max_meas_signal]))
                print(" ".join(["Jednosta sygnału mierzonego:", unit_meas_signal]))

                print("Na pewno dodać?\n")
                if input("t/n?") == "t":
                    pe.add_new_measurement_instrument(inventory_number, model, serial_number, producent,
                                                      calibration_period, calibration_date, status, min_analog_signal,
                                                      max_analog_signal, unit_analog_signal, min_meas_signal,
                                                      max_meas_signal, unit_meas_signal, pe.get_type_number(type))


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