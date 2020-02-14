import pyodbc
from tkinter import *

root = Tk()
connMP2 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                         'Server=wplsxsql1;'
                         'Database=MP2_PRO;'
                         'uid=MP2_Read;pwd=Read_MP2;'
                         )
cursorMP2 = connMP2.cursor()
cursorMP2.execute("SELECT EQUIP.EQNUM FROM MP2_PRO.dbo.EQUIP EQUIP WHERE EQUIP.EQNUM LIKE 'LP[_]%' ORDER BY EQUIP.EQNUM DESC")
myLabel = Label(root, text=str(cursorMP2.fetchone()[0]))
myLabel.pack()
root.mainloop()
