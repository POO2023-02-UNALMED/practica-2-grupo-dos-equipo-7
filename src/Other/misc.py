from sys import exit
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from baseDatos.Serializador import serializarUsuario, deserializarUsuario

def exitHandler(USER):
    """
    Manejador de salida. Pregunta al usuario si desea salir y guarda los cambios automáticamente.
    """
    ok = messagebox.askokcancel("Confirmacion", "Desea salir del programa? (Se guardaran los cambios automaticamente)")
    if ok:
        serializarUsuario(USER)
        exit()

def cancelarHandler(callback):
    """
    Manejador de cancelación. Pregunta al usuario si desea cancelar el proceso.
    """
    ok = messagebox.askokcancel("Cancelar", "Esta seguro de cancelar el proceso?")
    if ok:
        callback()

def getBotonContinuar(parent, callback, row, col):
    """
    Crea y devuelve un botón de "Continuar".
    """
    boton = tk.Button(parent, text="Continuar", bg="#DAD8FF",font=("fixedsys",12),relief="groove",fg="#4a4699", command = callback)
    boton.grid(row=row, column=col, padx=5, pady=5)
    parent.grid_rowconfigure(row, weight=1)
    parent.grid_columnconfigure(col, weight=1)
    return boton

def getBotonCancelar(parent, callback, row, col):
    """
    Crea y devuelve un botón de "Cancelar".
    """
    boton = tk.Button(parent, text="Cancelar", bg="#DAD8FF",font=("fixedsys",12),relief="groove",fg="#4a4699", command = lambda: cancelarHandler(callback))
    boton.grid(row=row, column=col, padx=5, pady=5)
    parent.grid_rowconfigure(row, weight=1)
    parent.grid_columnconfigure(col, weight=1)
    return boton

def getBotonTemp(parent, callback, row, col):
    """
    Crea y devuelve un botón temporal de "Volver al menu".
    """
    boton = tk.Button(parent, text="Volver al menu", bg="#DAD8FF",font=("fixedsys",12),relief="groove",fg="#4a4699", command = lambda: cancelarHandler(callback))
    boton.grid(row=row, column=col, padx=5, pady=5)
    parent.grid_rowconfigure(row, weight=1)
    parent.grid_columnconfigure(col, weight=1)
    return boton

def getImage(parent, path, size, **kwargs):
    """
    Carga y devuelve una imagen.
    """
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
    "descripcionComprarVuelo": "En esta funcionalidad puedes hacer la compra de tu vuelo ingresando el lugar de origen y destino,\nal darle continuar se desplegarán las opciones de vuelo, asiento y cantidad de equipaje, seguidamente\n se pedirá el peso de su maleta y se calculará el nuevo precio del boleto. Finalmente,\n se le mostrará los detalles del vuelo y un mensaje de confirmación de compra.",
    "descripcionReasignarVuelo": "Si cambiaste de opinión o se te presentó algún imprevisto, no hay ningún problema porque aquí podrás\n reasignar tu vuelo. Elige el boleto que deseas reasignar, aparecerá los detalles del boleto y al darle\n continuar se le mostrará las opciones de vuelos disponibles con el mismo origen y destino, además\n del formulario de asiento y equipaje. Finalmente, saldrá el mensaje de confirmación del proceso.",
    "descripcionCancelarVuelo": "Si por alguna razón no puedes asistir a tu vuelo, tienes la opción de cancelarlo y obtendrás un 50% de\n reembolso de tu dinero. Nos caracterizamos por la flexibidad en estos procesos y tratamos de hacerlo\n de la manera más sencilla, solo tienes que seleccionar el vuelo a cancelar y darle en continuar,\n aceptar los mensajes de confirmación y voilá, tu vuelo se cancelará fácil y rápido.",
    "descripcionCheckIn": "Contamos con el servicio de check In online, para que puedas hacerlo desde cualquier lugar y así confirmar\n tu asistencia al vuelo. Además, tienes la oportunidad de contratar servicios especiales para que tengas una\n mayor comodidad durante el vuelo, entre estos servicios se encuentran la comida a la carta, la disponibilidad\n de viajar con tu querida mascota, contratar un acompañante para pasajeros menores de edad, entre otros.",
    "descripcionGestionUsuario": "¡Hola usuario! Aquí podrás consultar cuanto saldo de dinero posees y tus millas, las cuales podrás canjear\n por una mejora de silla, descuento en el asiento o maleta. Adicionalmente, podrás visualizar tu historial\n de vuelos y la lista de descuentos que hayas canjeado. Por último, tienes la opción de depositar el monto\n de dinero que quieras, para seguir comprando con nosotros :)",
    
    "textoBienvenida": "Hola usuario, bienvenido al sistema de venta de vuelos, gracias por preferir nuestra aerolínea.\nEn esta ventana de inicio, tienes al lado derecho información acerca de los desarrolladores \ndel sistema con sus respectivas fotos,y en la parte inferior, se muestran imágenes del sistema\n y el botón para ingresar al mismo. Espero que disfrutes de la experiencia de comprar con nosotros :)",
    "breveDescripcionApp": "En este sistema podrás interactuar con cinco funcionalidades, las cuales son comprar, \nreasignar y cancelar vuelos, hacer el check In y por último, consultar la información de tu\nusuario en gestión de usuario. Cada funcionalidad tiene sus respectivos formularios,\nlos cuales se hicieron de manera clara e intuitiva para que tu experiencia sea la mejor :)",
    "breveDescripcionMenu": "Si estás buscando la mejor oferta de vuelos y una buena relación calidad-precio, este es el lugar para ti. Aquí encontrarás\nvuelos desde solo $100 dólares, podrás contratar servicios especiales durante y después del vuelo, tendrás flexibilidad para\nreasignar o cancelar tu vuelo y como incentivo por tu fidelización contarás con millas que se podrán cambiar por muchos beneficios\nmás. Gracias por preferirnos, esperamos que tengas una grata experiencia usando nuestro sistema. En la parte inferior encontrarás\nla explicación de cómo usar la aplicación.",
}