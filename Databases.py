import pyodbc
import datetime
from calendar import monthrange


def _count_number_of_letters(text):
    result = 0
    for char in text:
        if char.isalpha():
            result += 1
    return result


class Database:
    def __init__(self, name):
        self._conn = pyodbc.connect(name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


class PE(Database):
    def __init__(self):
        dbc = 'Driver={ODBC Driver 17 for SQL Server};' \
              'Server=WPLSXSQL1;' \
              'Database=sensmandb;' \
              'uid=admuser;pwd=admu$er;'
        super().__init__(dbc)

    def if_exist(self, inventory_number):
        sql = "SELECT COUNT(1) FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_type(self, inventory_number):
        sql = "SELECT typ_id FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_type_name(self, inventory_number):
        sql = "SELECT Btc.lo FROM Baza_typ_czujnika AS Btc JOIN Baza_czujniki AS Bc ON Bc.typ_id = Btc.id AND " \
              "Bc.nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_procucent(self, inventory_number):
        sql = "SELECT prod FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_model(self, inventory_number):
        sql = "SELECT k_modelu FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_serial_number(self, inventory_number):
        sql = "SELECT n_seryjny FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_calibration_period(self, inventory_number):
        sql = "SELECT okres_k FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_calibration_date(self, inventory_number):
        sql = "SELECT kolejna_k FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_status(self, inventory_number):
        sql = "SELECT status FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_min_analog_signal(self, inventory_number):
        sql = "SELECT syg_ana_min FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        min_analog_signal = super().query(sql)[0][0]
        if min_analog_signal is not None and min_analog_signal % 1 == 0:
            return int(min_analog_signal)
        else:
            return min_analog_signal

    def get_max_analog_signal(self, inventory_number):
        sql = "SELECT syg_ana_max FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        max_analog_signal = super().query(sql)[0][0]
        if max_analog_signal is not None and max_analog_signal % 1 == 0:
            return int(max_analog_signal)
        else:
            return max_analog_signal

    def get_unit_analog_signal(self, inventory_number):
        sql = "SELECT jednostka_ana FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_min_meas_signal(self, inventory_number):
        sql = "SELECT syg_mierz_min FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        min_meas_signal = super().query(sql)[0][0]
        if min_meas_signal is not None and min_meas_signal % 1 == 0:
            return int(min_meas_signal)
        else:
            return min_meas_signal

    def get_max_meas_signal(self, inventory_number):
        sql = "SELECT syg_mierz_max FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        max_meas_signal = super().query(sql)[0][0]
        if max_meas_signal is not None and max_meas_signal % 1 == 0:
            return int(max_meas_signal)
        else:
            return max_meas_signal

    def get_unit_meas_signal(self, inventory_number):
        sql = "SELECT jednostka_mierz FROM Baza_czujniki WHERE nr_zd = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def add_new_measurement_instrument(self, inventory_number, model, serial_number, producent, calibration_period, calibration_date,
                     status, min_analog_signal, max_analog_signal, unit_analog_signal, min_meas_signal, max_meas_signal,
                     unit_meas_signal, type):
        sql = "INSERT INTO Baza_czujniki (nr_zd, k_modelu, n_seryjny, prod, okres_k, kolejna_k, status, syg_ana_min," \
              " syg_ana_max, jednostka_ana, syg_mierz_min, syg_mierz_max, jednostka_mierz, typ_id) " \
              "VALUES ('{}', '{}', '{}', '{}', {}, '{}', '{}', {}, {}, '{}', {}, {}, '{}', {})" \
            .format(inventory_number, model, serial_number, producent, calibration_period, calibration_date, status,
                    min_analog_signal, max_analog_signal, unit_analog_signal, min_meas_signal, max_meas_signal,
                    unit_meas_signal, type)
        super().execute(sql)

    def get_responsible_employee(self, inventory_number):
        if self.get_status(inventory_number) == "wp":
            sql = "SELECT akt_wyp_id FROM Baza_czujniki WHERE nr_zd = N'{}'".format(inventory_number)
            hire_id = super().query(sql)[0][0]
            if hire_id is None:
                return "-"
            else:
                sql = "SELECT id_pracownika_id FROM Baza_wypozyczenia WHERE id = N'{}'".format(hire_id)
                employee_id = super().query(sql)[0][0]
                if employee_id == -1:
                    return "-"
                else:
                    sql = "SELECT first_name FROM auth_user WHERE id = N'{}'".format(employee_id)
                    first_name = super().query(sql)[0][0]
                    sql = "SELECT last_name FROM auth_user WHERE id = N'{}'".format(employee_id)
                    last_name = super().query(sql)[0][0]
                    return first_name + " " + last_name
        else:
            return "-"

    def get_range(self, inventory_number):
        min_analog_signal = self.get_min_analog_signal(inventory_number)
        max_analog_signal = self.get_max_analog_signal(inventory_number)
        unit_analog_signal = self.get_unit_analog_signal(inventory_number)
        min_meas_signal = self.get_min_meas_signal(inventory_number)
        max_meas_signal = self.get_max_meas_signal(inventory_number)
        unit_meas_signal = self.get_unit_meas_signal(inventory_number)
        type_name = self.get_type_name(inventory_number)
        if "Komora" in type_name:
            return unit_meas_signal
        elif min_analog_signal is None and max_analog_signal is None and unit_analog_signal == "" and min_meas_signal is \
                None and max_meas_signal is None and unit_meas_signal == "":
            return "-"
        elif unit_meas_signal is not None and ("CL" or "CR" or "TS" or "TE") in unit_meas_signal:
            return unit_meas_signal
        elif min_analog_signal is None and max_analog_signal is None and unit_analog_signal == "":
            return str(min_meas_signal) + "_" + str(max_meas_signal) + unit_meas_signal
        elif (min_analog_signal and max_analog_signal and unit_analog_signal and min_meas_signal and max_meas_signal
              and unit_meas_signal) is None:
            return "-"
        else:
            return str(min_analog_signal) + "_" + str(max_analog_signal) + unit_analog_signal + "_" + \
                   str(min_meas_signal) + "_" + str(max_meas_signal) + unit_meas_signal



class MP2(Database):
    def __init__(self):
        dbc = 'Driver={ODBC Driver 17 for SQL Server};' \
              'Server=wplsxsql1;' \
              'Database=MP2_PRO;' \
              'uid=MP2_Read;pwd=Read_MP2;'
        super().__init__(dbc)

    def if_exist(self, inventory_number):
        sql = "SELECT COUNT(1) FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_last_measurement_instrument(self):
        sql = "SELECT EQUIP.EQNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.EQNUM LIKE 'LP[_]%' ORDER BY EQUIP.EQNUM DESC"
        return super().query(sql)[0][0]

    def get_object_code(self, inventory_number):
        sql = "SELECT EQUIP.EQNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_type(self, inventory_number):
        sql = "SELECT EQUIP.DESCRIPTION FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_model(self, inventory_number):
        sql = "SELECT EQUIP.MODELNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_serial_number(self, inventory_number):
        sql = "SELECT EQUIP.SERIALNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_producent(self, inventory_number):
        sql = "SELECT EQUIP.MANUFACTURER FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def get_calibration_period(self, inventory_number):
        sql = "SELECT EQUIP.UD7 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0].split(" ")[0]

    def get_calibration_date(self, inventory_number):
        sql = "SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        calibration_date = super().query(sql)[0][0]
        if calibration_date in ["w kalibracji", "archiwum"]:
            calibration_date = datetime.date.today()
        else:
            calibration_date = datetime.date(int(calibration_date[3:]), int(calibration_date[:2]),
                                             monthrange(int(calibration_date[3:]), int(calibration_date[:2]))[1])
        return calibration_date

    def get_status(self, inventory_number):
        sql = "SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        status = super().query(sql)[0][0]
        if status == "w kalibracji":
            return "wk"
        elif status == "archiwum":
            return "ar"
        elif datetime.date(int(status[3:]), int(status[:2]),
                           monthrange(int(status[3:]), int(status[:2]))[1]) > datetime.date.today():
            return "nn"
        else:
            return "nn"

    def get_min_analog_signal(self, inventory_number):
        sql = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        min_analog_signal = super().query(sql)[0][0]
        if min_analog_signal is None:
            pass
        else:
            if ("V" or "mA") in min_analog_signal:
                min_analog_signal = min_analog_signal.split("_")[0]
            else:
                min_analog_signal = None
        return min_analog_signal

    def get_max_analog_signal(self, inventory_number):
        sql = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        max_analog_signal = super().query(sql)[0][0]
        if max_analog_signal is None:
            pass
        else:
            if ("V" or "mA") in max_analog_signal:
                max_analog_signal = max_analog_signal.split("_")[1]
                max_analog_signal = max_analog_signal[:(len(max_analog_signal)
                                                        - _count_number_of_letters(max_analog_signal))]
            else:
                max_analog_signal = None
        return max_analog_signal

    def get_unit_analog_signal(self, inventory_number):
        sql = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        unit_analog_signal = super().query(sql)[0][0]
        if unit_analog_signal is None:
            pass
        else:
            if ("V" or "mA") in unit_analog_signal:
                unit_analog_signal = unit_analog_signal.split("_")[1]
                unit_analog_signal = unit_analog_signal[-_count_number_of_letters(unit_analog_signal):]
            else:
                unit_analog_signal = None
        return unit_analog_signal

    def get_min_meas_signal(self, inventory_number):
        sql = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        min_meas_signal = super().query(sql)[0][0]
        if min_meas_signal is None:
            pass
        else:
            if ("V" or "mA") in min_meas_signal:
                min_meas_signal = min_meas_signal.split("_")[2]
            elif "_" in min_meas_signal:
                min_meas_signal = min_meas_signal.split("_")[0]
            else:
                min_meas_signal = None
        return min_meas_signal

    def get_max_meas_signal(self, inventory_number):
        sql = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        max_meas_signal = super().query(sql)[0][0]
        if max_meas_signal is None:
            pass
        else:
            if ("V" or "mA") in max_meas_signal:
                max_meas_signal = max_meas_signal.split("_")[3]
                max_meas_signal = max_meas_signal[:len(max_meas_signal) - _count_number_of_letters(max_meas_signal)]
            elif "_" in max_meas_signal:
                max_meas_signal = max_meas_signal.split("_")[1]
                max_meas_signal = max_meas_signal[:len(max_meas_signal) - _count_number_of_letters(max_meas_signal)]
            else:
                max_meas_signal = None
        return max_meas_signal

    def get_unit_meas_signal(self, inventory_number):
        sql = "SELECT EQUIP.UD10 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        unit_meas_signal = super().query(sql)[0][0]
        if unit_meas_signal is None:
            pass
        else:
            if ("V" or "mA") in unit_meas_signal:
                unit_meas_signal = unit_meas_signal.split("_")[3]
                unit_meas_signal = unit_meas_signal[-_count_number_of_letters(unit_meas_signal):]
            elif "_" in unit_meas_signal:
                unit_meas_signal = unit_meas_signal.split("_")[1]
                unit_meas_signal = unit_meas_signal[-_count_number_of_letters(unit_meas_signal):]
        return unit_meas_signal

    def get_team(self, inventory_number):
        sql = "SELECT EQUIP.SUBLOCATION1 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '{}'".format(inventory_number)
        return super().query(sql)[0][0]

    def _get_calibration_years(self):
        sql = "SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.LOCATION ='VS_PDP'"
        calibration_dates = super().query(sql)
        calibration_years = []
        for calibration_date in calibration_dates:
            if calibration_date[0] is not None and len(calibration_date[0].split(".")[0]) == 2\
                    and len(calibration_date[0].split(".")[1]) == 4:
                if datetime.date.today().year >= int(calibration_date[0].split(".")[1]):
                    calibration_years.append(int(calibration_date[0].split(".")[1]))
        return sorted(list(set(calibration_years)))


    def _prepare_overdue_calibration_dates(self):
        overdue_dates_calibration = []
        for year in self._get_calibration_years():
            for month in range(1, 13):
                if month >= datetime.date.today().month and year == datetime.date.today().year:
                    pass
                else:
                    if month in range(0, 10):
                        overdue_dates_calibration.append("0" + str(month) + "." + str(year))
                    else:
                        overdue_dates_calibration.append(str(month) + "." + str(year))
        return overdue_dates_calibration

    # Przygotowanie numerów inwentarzowych z przeterminowaną datą kalibracji
    def get_inventory_number_overdue_measurement_instruments(self):
        overdue_measurement_instruments = []
        for dates in self._prepare_overdue_calibration_dates():
            sql = "SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.LOCATION ='VS_PDP' AND EQUIP.UD9 ='{}'"\
                .format(dates)
            measurement_instruments = super().query(sql)
            for measurement_instrument in measurement_instruments:
                overdue_measurement_instruments.append(measurement_instrument[0])
        return overdue_measurement_instruments

    # przygotowanie daty do warunku z aktualnymi kalibracjami
    def _prepare_current_calibration_date(self):
        if datetime.date.today().month in range(0, 10):
            current_date_calibration = "0" + str(datetime.date.today().month) + "." + str(datetime.date.today().year)
        else:
            current_date_calibration = str(datetime.date.today().month) + "." + str(datetime.date.today().year)
        return current_date_calibration

    # przygotowanie numerów inwentarzowych z przyrządami do kalibracji w tym miesiącu
    def get_inventory_number_current_measurement_instruments(self):
        current_measurement_instruments = []
        sql = "SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.LOCATION ='VS_PDP' AND EQUIP.UD9 ='{}'"\
            .format(self._prepare_current_calibration_date())
        measurement_instruments = super().query(sql)
        for measurement_instrument in measurement_instruments:
            current_measurement_instruments.append(measurement_instrument[0])
        return current_measurement_instruments

    def _prepare_next_calibration_date(self):
        current_month = datetime.date.today().replace(day=monthrange(datetime.date.today().year,
                                                                     datetime.date.today().month)[1])
        next_month = current_month + datetime.timedelta(days=1)
        if next_month.month in range(0, 10):
            next_date_calibration = "0" + str(next_month.month) + "." + str(next_month.year)
        else:
            next_date_calibration = str(next_month.month) + "." + str(next_month.year)
        return next_date_calibration

    # # przygotowanie numerów inwentarzowych z przyrządmi do kalibracji w przyszłym miesiącu
    def get_inventory_number_next_measurement_instruments(self):
        next_measurement_instruments = []
        sql = "SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.LOCATION ='VS_PDP' AND EQUIP.UD9 ='{}'"\
            .format(self._prepare_next_calibration_date())
        measurement_instruments = super().query(sql)
        for measurement_instrument in measurement_instruments:
            next_measurement_instruments.append(measurement_instrument[0])
        return next_measurement_instruments

    def get_object_code_all_measurement_instruments(self):
        objects_code = []
        sql = "SELECT EQUIP.EQNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.LOCATION = 'VS_PDP' AND EQUIP.EQNUM LIKE 'LP_%'"
        for object_code in super().query(sql):
            objects_code.append(object_code[0])
        return objects_code

    def get_inventory_number(self, object_code):
        sql = "SELECT EQUIP.UD4 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.EQNUM = '{}'".format(object_code)
        inventory_number = super().query(sql)[0][0]
        if inventory_number is None:
            return ""
        else:
            return inventory_number


#
# inventory_number = "ZD3331"
#
# with PE() as pe:
#      if pe.if_exist(inventory_number):
#          pass
#         print("istnieje")
#         print(pe.getType(inventory_number))
#         print(pe.getModel(inventory_number))
#         print(pe.getSerialNumber(inventory_number))
#         print(pe.getCalibrationPeriod(inventory_number))
#         print(pe.getCalibrationDate(inventory_number))
#         print(pe.getStatus(inventory_number))
#         print(pe.getMinAnalogSignal(inventory_number))
#         print(pe.getMaxAnalogSignal(inventory_number))
#         print(pe.getUnitAnalogSignal(inventory_number))
#         print(pe.getMinMeasSignal(inventory_number))
#         print(pe.getMaxMeasSignal(inventory_number))
#         print(pe.getUnitMeasSignal(inventory_number))
#         print(pe.getResponsibleEmployee(inventory_number))
#         print(pe.getRange(inventory_number))
#
#     if not pe.ifExist("test1"):
#         pass
#
# print(""
#       ""
#       "")
#
# with MP2() as mp2:
#     if mp2.ifExist(inventory_number):
#         # print(mp2.getLastMeasurementInstrument())
#         print(mp2.getObjectCode(inventory_number))
#         print(mp2.getType(inventory_number))
#         print(mp2.getModel(inventory_number))
#         print(mp2.getSerialNumber(inventory_number))
#         print(mp2.getProducent(inventory_number))
#         print(mp2.getCalibrationPeriod(inventory_number))
#         print(mp2.getCalibrationDate(inventory_number))
#         print(mp2.getMinAnalogSignal(inventory_number))
#         print(mp2.getMaxAnalogSignal(inventory_number))
#         print(mp2.getUnitAnalogSignal(inventory_number))
#         print(mp2.getMinMeasSignal(inventory_number))
#         print(mp2.getMaxMeasSignal(inventory_number))
#         print(mp2.getUnitMeasSignal(inventory_number))
#         print(mp2.getTeam(inventory_number))
#         print(mp2.getLowestYear())
#