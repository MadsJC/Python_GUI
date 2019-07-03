from tkinter import *
import pandas as pd
import GUI_backend

def view_command():
    list1.delete(0, END)
    for row in sg_backend.view():
        list1.insert(END,row)

def download_command():
    sg_backend.download()

window = Tk()
window.geometry("1000x500")
window.wm_title("Korsika Transferliste")


Button1 = Button(window, text= 'Preview list', command = view_command)
Button1.grid(row = 1, column = 0, sticky = W, padx=10, pady=10)

Button2 = Button(window, text= 'Download list', command = download_command)
Button2.grid(row = 1, column = 1, sticky = W, padx=10, pady=10)

Button_close = Button(window, text= 'Close', command=window.destroy)
Button_close.grid(row = 1, column = 2, sticky = W, padx=10, pady=10)

list1 = Listbox(window, height = 25, width = 160)
list1.grid(row = 5, column = 0, columnspan = 3)

scrollb1 = Scrollbar(window)
scrollb1.grid(row = 5, column = 4, rowspan = 2, sticky=N+S+W)

list1.configure(yscrollcommand=scrollb1.set)
scrollb1.configure(command=list1.yview)

window.mainloop()
