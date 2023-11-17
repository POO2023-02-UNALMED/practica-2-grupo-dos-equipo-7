import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from baseDatos.Serializador import serializarUsuario, deserializarUsuario

# Archivo temporal para tener cierta organizacion con handlers y funcionalidades extra?

def exitHandler(USER):
    ok = messagebox.askokcancel("Confirmacion", "Desea salir del programa?")
    if ok:
        serializarUsuario(USER)
        exit()

def cancelarHandler(callback):
    ok = messagebox.askokcancel("Cancelar", "Esta seguro de cancelar el proceso?")
    if ok:
        callback()
    

def getBotonContinuar(parent, callback, row, col):
    boton = tk.Button(parent, text="Continuar", bg="#DAD8FF",font=("fixedsys",12),relief="groove",fg="#7768D2", command = callback)
    boton.grid(row=row, column=col, padx=5, pady=5)
    parent.grid_rowconfigure(row, weight=1)
    parent.grid_columnconfigure(col, weight=1)
    return boton
    pass

def getBotonCancelar(parent, callback, row, col):
    boton = tk.Button(parent, text="Cancelar", bg="#DAD8FF",font=("fixedsys",12),relief="groove",fg="#7768D2", command = lambda: cancelarHandler(callback))
    boton.grid(row=row, column=col, padx=5, pady=5)
    parent.grid_rowconfigure(row, weight=1)
    parent.grid_columnconfigure(col, weight=1)
    return boton
    pass

def getImage(parent, path, size, **kwargs):
    original = Image.open(path)
    resize = original.resize(size)
    imageTemp = ImageTk.PhotoImage(resize)
    imagen = tk.Label(parent, image=imageTemp, **kwargs)
    imagen.image = imageTemp
    return imagen

def getSeparador(parent, row, col, pad = 5):
    seps = []
    for i in range(col):
        separator = ttk.Separator(parent, orient="horizontal")
        separator.grid(row=row, column=i, sticky="ew", padx=0, pady=pad)
        seps.append(separator)
    return seps

#Pop up functions
def confirmarTransaccion(user, valor):
    return messagebox.askokcancel(f"Confirmar transaccion $({valor})", f"Por favor confirme la transaccion de ${valor}, saldo actual: {user.dinero}")

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
    
    "textoBienvenida": "Hola usuario, bienvenido al sistema de venta de vuelos, gracias por preferir nuestra aerolínea.\nEn esta ventana de inicio, tienes al lado derecho información acerca de los desarrolladores \ndel sistema con sus respectivas fotos,y en la parte inferior, se muestran imágenes del sistema\n y el botón para ingresar al mismo. Espero que disfrutes de la experiencia de comprar con nosotros :)",
    "breveDescripcionApp": "Hola, esta aplicacion es un sistema de vuelos, aqui podras ... bla bla bla",
}