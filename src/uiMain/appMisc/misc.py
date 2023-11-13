import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image

# Archivo temporal para tener cierta organizacion con handlers y funcionalidades extra?

def exitHandler():
    ok = messagebox.askokcancel("Confirmacion", "Desea salir del programa?")
    if ok:
        exit()
        

def getImage(parent, path, size, **kwargs):
    original = Image.open(path)
    resize = original.resize(size)
    imageTemp = ImageTk.PhotoImage(resize)
    imagen = tk.Label(parent, image=imageTemp, **kwargs)
    imagen.image = imageTemp
    return imagen

#Pop up functions
def alertWarn(errMsg, msg):
    return messagebox.showerror(errMsg, msg)

def alertConfirmacion(msg = "Escriba aceptar para confirmar el proceso"):
    return messagebox.askokcancel("Confirmacion", msg)

def alertInfo(title, info):
    return messagebox.showinfo(title, info)

def makePopUp():
    pass


TEXT_DATA = {
    "descripcionComprarVuelo": "Aqui puedes buscar y comprar vuelos a el destino que desees!",
    "descripcionReasignarVuelo": "Si cambiaste de opinion con respecto a algun detalle de tu vuelo, puedes reasignar tu ticket a otro vuelo!",
    "descripcionCancelarVuelo": "Si tuviste algun imprevisto o cambiaste de opinion, aqui puedes cancelar tu vuelo programado, nosotros entendemos y te regresamos el 10% de tu dinero!",
    "descripcionCheckIn": "Aqui puedes hacer check in y ademas de confirmar, agregar servicios adicionales para tu mayor comodidad en el vuelo!",
    "descripcionGestionUsuario": "Aqui puedes consultar informacion acerca de tu cuenta y hacer muchas cosas mas",
    
    "textoBienvenida": "Bienvenid@ al sistema de venta de vuelos, Largo-fly :3",
    "breveDescripcionApp": "Hola, esta aplicacion es un sistema de vuelos, aqui podras ... bla bla bla",
}