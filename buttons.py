from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="Look! I clicked a Button!!!")
    myLabel.pack()

myButton = Button(root, text="Clik Me!", command=myClick, fg="blue", bg="#fffff1")
myButton.pack()

root.mainloop()