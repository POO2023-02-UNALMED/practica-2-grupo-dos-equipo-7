import tkinter as tk
import os
from PIL import ImageTk, Image

def getImage(parent, path, size, **kwargs):
    original = Image.open(path)
    resize = original.resize(size)
    imageTemp = ImageTk.PhotoImage(resize)
    imagen = tk.Label(parent, image=imageTemp, **kwargs)
    imagen.image = imageTemp
    return imagen

#Pop up functions
def alertWarn(errMsg, msg):
    return tk.messagebox.showerror(errMsg, msg)

def alertConfirmacion(msg = "Escriba aceptar para confirmar el proceso"):
    return tk.messagebox.askokcancel("Confirmacion", msg)

def alertInfo(title, info):
    return tk.messagebox.showinfo(title, info)

def makePopUp():
    pass
