import PE_Database as PE
import MP2_Database as MP2
from tkinter import *

cursorPE = PE.connectWithDatabase()
cursorMP2 = MP2.connectWithDatabase()

# Porównanie dat kalibracji dla baz danych PE i MP2. Powrównuje tylko te przyrządy pomiarowe, które są w PE.
cursorPE.execute("SELECT nr_zd FROM Baza_czujniki")
czujnikiPE = cursorPE.fetchall()
for row in czujnikiPE:
    try:
        cursorPE.execute("SELECT kolejna_k, status FROM Baza_czujniki WHERE nr_zd = '" + str(row[0]) + "'")
        datePE = cursorPE.fetchone()
        cursorMP2.execute("SELECT EQUIP.UD9 FROM MP2_PRO.dbo.EQUIP EQUIP WHERE UD4 = '" + str(row[0]) + "'")
        dateMP2 = cursorMP2.fetchone()
        if datePE[0].strftime("%m.%Y") == dateMP2[0] and (datePE[1] == 'wp' or datePE[1] == 'ns'):
            pass
        elif dateMP2[0] == "w kalibracji" and (datePE[1] == 'wk' or datePE[1] == 'zk'):
            pass
        elif "archiwum" in dateMP2[0] and (datePE[1] == 'wn' or datePE[1] == 'nn'):
            pass
        elif dateMP2[0] == "do wizualizacji":
            pass
            #print("Przyrząd pomiarowy " + str(row[0]) + " jest przeznaczony do wizualizacji")
        elif str(row[0]) == 'ZD2537' or str(row[0]) == 'ZD5493' or str(row[0]) == 'ZD4960':
            pass
        else:
            print("Coś jest nie tak z czujnikiem: " + str(row[0]))
    except TypeError:
        print("Przyrząd pomiarowy " + str(row[0]) + " nie znajduje się w bazie MP2")


#Porównanie numerów inwentarzowych dla baz danych PE i MP2. Powrównuje tylko te przyrządy pomiarowe, które są w PE
cursorPE.execute("SELECT nr_zd FROM Baza_czujniki")
czujnikiPE = cursorPE.fetchall()
for row in czujnikiPE:
    try:
        
    except: