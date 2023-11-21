import os
import sys
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sys import exit

# ------------------------------------
# Backend (TEMPORAL)
from Other.misc import *
from Other.ErrorAplicacion import *
from baseDatos.Serializador import *

from gestorAplicacion.Aerolinea.Asiento import Asiento
from gestorAplicacion.Aerolinea.Boleto import Boleto
from gestorAplicacion.Aerolinea.Maleta import Maleta
from gestorAplicacion.Aerolinea.RestriccionesMaleta import RestriccionesMaleta
from gestorAplicacion.Aerolinea.ServiciosEspeciales import ServiciosEspeciales
from gestorAplicacion.Aerolinea.Vuelo import Vuelo

from gestorAplicacion.Cuenta.Usuario import Usuario

from gestorAplicacion.Descuentos.Descuento import Descuento
from gestorAplicacion.Descuentos.descuentoMaleta import descuentoMaleta
from gestorAplicacion.Descuentos.descuentoVuelo import descuentoVuelo
from gestorAplicacion.Descuentos.upgradeAsiento import upgradeAsiento

from gestorAplicacion.Mascotas.Animal import Animal
from gestorAplicacion.Mascotas.Perro import Perro
from gestorAplicacion.Mascotas.Gato import Gato


# ------------------------------------
color={"pink":"#FFD8EC","purple":"#D0A2F7","blue":"#DAD8FF","pinkpurple":"#FFD3FB","darkblue":"#4E3D6F"}

def createMainUser():
    mainUser = Usuario("Jaime Alberto Guzman", "jaguzman@unal.edu.co", 5000)
    
    baseData = [
        { "Origen": "Medellin", "Destino": "Nueva York",   "Maletas": 2, "Vuelo": 2, "Asiento": 3 },
        { "Origen": "Bogota",   "Destino": "Madrid", "Maletas": 1, "Vuelo": 3, "Asiento": 4 },
        { "Origen": "Medellin",   "Destino": "Cartagena",    "Maletas": 0, "Vuelo": 4, "Asiento": 5 },
        { "Origen": "Bogota",   "Destino": "Medellin",  "Maletas": 4, "Vuelo": 0, "Asiento": 2 },
    ]
    
    for data in baseData:
        vuelo = Vuelo.generarVuelos(5, data["Origen"], data["Destino"])[data["Vuelo"]] #Genera los vuelos 
        boleto = Boleto(
            data["Origen"],
            data["Destino"],
            vuelo,
            vuelo.generarAsientos(3, 5, 100)[data["Asiento"]],
            mainUser
        )
        maletas = [Maleta(i+1, 12, boleto) for i in range(data["Maletas"])]
        mainUser.comprarBoleto(boleto)
    return mainUser


App = tk.Tk()
App.title("Ventana Inicio - Aplicacion")
App.geometry("1400x800")

#serializarUsuario(createMainUser())
global user
user = deserializarUsuario()


handlersProcesoConsulta = {
    "Comprar vuelo": lambda mainMenu: ComprarVuelo().generar(
        mainMenu,
        "Comprar Vuelo",
        TEXT_DATA["descripcionComprarVuelo"],
    ),
    
    "Reasignar Vuelo": lambda mainMenu: ReasignarVuelo().generar(
        mainMenu,
        "Reasignar Vuelo",
        TEXT_DATA["descripcionReasignarVuelo"]
    ),
    
    "Cancelar Vuelo": lambda mainMenu: CancelarVuelo().generar(
        mainMenu,
        "Cancelar Vuelo",
        TEXT_DATA["descripcionCancelarVuelo"]
    ),
    
    "Check In": lambda mainMenu: CheckIn().generar(
        mainMenu,
        "Check In",
        TEXT_DATA["descripcionCheckIn"]
    ),
    
    "Gestion usuario": lambda mainMenu: GestionUsuario().generar(
        mainMenu,
        "Gestion Usuario",
        TEXT_DATA["descripcionGestionUsuario"]
    ),
    
    "Salir" : lambda: VentanaInicial().generar(),
}


#Implementar formulario generico
class FieldFrame(tk.Frame):
    """
    crea un nuevo objeto de tipo FieldFrame
    @arg tituloResultados titulo para la columna "Criterio"
    @arg criterios array con los nombres de los criterios
    @arg tituloValores titulo para la columna "valor"
    @arg valores array con los valores iniciales; Si None, no hay valores iniciales
    @arg habilitado array con los campos no-editables por el usuario; Si None, todos son editables
    """

    def __init__(self, tituloCriterio, criterios, tituloValores, valores, habilitado, parent, callback = None):
        
        #Inicializar el diccionario que guardara los datos
        self.parent = parent
        self.data = {}
        self.formData = {}

        self.criterios = criterios

        #Crea el marco donde van a estar los elementos
        marco = tk.Frame(parent, bg=color["pink"], highlightbackground="#9656B6",highlightthickness=2)
        marco.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        #Agregar el titulo de los criterios
        elementoTituloCriterio = tk.Label(marco, text=tituloCriterio,font=("fixedsys",12),bg=color["purple"])
        elementoTituloCriterio.grid(row=0, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)


        #Agregar el titulo de los valores
        elementoTituloValores = tk.Label(marco, text=tituloValores,font=("fixedsys",12),bg=color["purple"])
        elementoTituloValores.grid(row=0, column=1, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(1, weight=1)

        #Por cada criterio agregarlos y sus respectivas entradas
        index = 0
        for index, criterio in enumerate(criterios):
        
            #Crea el criterio y su valor y lo guarda
            elementoCriterio = tk.Label(marco, text=criterio,bg=color["pink"],font=("fixedsys",12))
            elementoCriterio.grid(row=index+1, column=0, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(0, weight=1)

            elementoInput = tk.Entry(marco,font=("fixedsys",12))
            elementoInput.grid(row=index+1, column=1, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(1, weight=1)

            self.data[criterio] = {
                "elementos" : (elementoCriterio, elementoInput),
                "value" : None, 
            }

        
        submitButton = tk.Button(marco, text="Enviar", bg=color["blue"],font=("fixedsys",12),relief="groove",fg=color["darkblue"], command = lambda: self.submitForm(callback))
        submitButton.grid(row=index+2, column=1, padx=5, pady=5)
        marco.grid_rowconfigure(index+2, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        clearButton = tk.Button(marco, text="Limpiar",bg=color["blue"],font=("fixedsys",12),relief="groove",fg=color["darkblue"],command = lambda: self.clear())
        clearButton.grid(row=index+2, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(index+2, weight=1)
        marco.grid_columnconfigure(1, weight=1)

        self.nextFreeRow = index + 3
        self.marco = marco
        pass

    """
    @arg criterio el criterio cuyo valor se quiere obtener
    @return el valor del criterio cuyo nombre es 'criterio'
    """
    def getValue(self, criterio):
        """
        Obtiene el valor de un criterio específico.

        Args:
            criterio (str): El criterio del que se quiere obtener el valor.

        Returns:
            El valor del criterio.
        """
        return self.data[criterio]["value"]

    def submitForm(self, callback):
        """
        Envía el formulario y llama a una función de devolución de llamada.

        Args:
            callback (function): La función de devolución de llamada a llamar después de enviar el formulario.

        Raises:
            ErrorSugeridoFieldFrame: Si hay campos vacíos en el formulario.
        """
        vacios = []
        
        for criterio in self.criterios:
            value = (self.data[criterio]["elementos"][1]).get()
            self.data[criterio]["value"] = value
            self.formData[criterio] = value
            
            if value == "":
                vacios.append(criterio)
                
        try:
            if len(vacios) > 0:
                raise ErrorSugeridoFieldFrame(vacios)
            
            if callback != None:
                callback(self.formData)

        except ErrorSugeridoFieldFrame:
            alertWarn("Campos sin llenar", f"Error, por favor llene todos los campos antes de continuar (Campos faltantes: {', '.join(vacios)})")
            return False

    def clear(self):
        """
        Limpia todos los campos del formulario.
        """
        for criterio in self.criterios:
            (self.data[criterio]["elementos"][1]).delete(0 ,'end')
    
    
    def delete(self):
        """
        Destruye el marco del formulario.
        """
        self.marco.destroy()
        pass

class ResultFrame(tk.Frame):
    """
    Clase que representa un marco de resultados en la interfaz de usuario.

    Atributos:
        parent (tkinter.Tk): La ventana principal de la aplicación.
        nextFreeRow (int): La próxima fila libre en el marco.
        marco (tkinter.Frame): El marco que contiene los elementos de la interfaz de usuario.
    """

    def __init__(self, tituloResultados, datos, parent):
        """
        Inicializa un objeto de la clase ResultFrame.

        Args:
            tituloResultados (str): El título de los resultados.
            datos (dict): Los datos a mostrar en el marco.
            parent (tkinter.Tk): La ventana principal de la aplicación.
        """
        
        #Inicializar el diccionario que guardara los datos
        self.parent = parent
        
        #Crea el marco donde van a estar los elementos
        marco = tk.Frame(parent, bg=color["pink"], relief="flat")
        marco.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        #Agregar el titulo de los criterios
        elementoTituloResultados = tk.Label(marco, text=tituloResultados,font=("fixedsys",12),bg=color["purple"])
        elementoTituloResultados.grid(row=0, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        index = 0
        #Por cada criterio agregarlos y sus respectivas entradas
        for index, key in enumerate(datos.keys()):
        
            #Crea el criterio y su valor y lo guarda
            elementoKey = tk.Label(marco, text=key,font=("fixedsys",10),bg=color["pink"])
            elementoKey.grid(row=index+1, column=0, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(0, weight=1)

            elementoValue = tk.Label(marco, text=datos[key],font=("fixedsys",10),bg=color["pink"])
            elementoValue.grid(row=index+1, column=1, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(1, weight=1)

        self.nextFreeRow = index + 2
        self.marco = marco
    
    def delete(self):
        """
        Destruye el marco de resultados.
        """
        self.marco.destroy()

class ProcesoConsulta:
    """
    Clase que representa un proceso de consulta en la interfaz de usuario.

    Atributos:
        zona (tkinter.Tk): La ventana principal de la aplicación.
        nombre (str): El nombre del proceso de consulta.
        descripcion (str): La descripción del proceso de consulta.
        criterios (list): Los criterios del proceso de consulta.
        zonaForm (tkinter.Frame): El marco que contiene los elementos del formulario.
    """

    def __init__(self, zona, nombre, descripcion, criterios):
        """
        Inicializa un objeto de la clase ProcesoConsulta.

        Args:
            zona (tkinter.Tk): La ventana principal de la aplicación.
            nombre (str): El nombre del proceso de consulta.
            descripcion (str): La descripción del proceso de consulta.
            criterios (list): Los criterios del proceso de consulta.
        """
        self.zona = zona
        self.nombre = nombre
        self.descripcion = descripcion
        self.criterios = criterios

    def generar(self):
        """
        Genera la interfaz de usuario para el proceso de consulta.
        """
        # Crea un marco para la información de la zona
        zonaInfo = tk.Frame(self.zona, bg="yellow", borderwidth=1, relief="solid")
        zonaInfo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(0, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)

        # Crea un marco para el formulario
        self.zonaForm = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)

        # Crea una etiqueta para el nombre del proceso
        nombreProceso = tk.Label(zonaInfo, text= self.nombre)
        nombreProceso.grid(row=0, column=0, padx=5, pady=5)
        zonaInfo.grid_rowconfigure(0, weight=1)
        zonaInfo.grid_columnconfigure(0, weight=1)

        # Crea una etiqueta para la descripción del proceso
        descripcionProceso = tk.Label(zonaInfo, text= self.descripcion)
        descripcionProceso.grid(row=1, column=0, padx=5, pady=5)
        zonaInfo.grid_rowconfigure(1, weight=1)
        zonaInfo.grid_columnconfigure(0, weight=1)

        # Crea un marco de campo para las preguntas
        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, self.zonaForm)

class MainMenu:
    """
    Clase que representa el menú principal de la aplicación.

    Atributos:
        zona (tkinter.Tk): La ventana principal de la aplicación.
    """

    def __init__(self):
        """
        Inicializa un objeto de la clase MainMenu.
        """
        pass

    def generar(self):
        """
        Genera la interfaz de usuario para el menú principal.
        """
        # Crea un marco grande para la aplicación
        frame_grande = tk.Frame(App, bg=color["blue"])
        frame_grande.grid(row=0, column=0, sticky="nsew")
        App.grid_rowconfigure(0, weight=1)
        App.grid_columnconfigure(0, weight=1)

        # Crea un marco para el menú principal
        marco = tk.Frame(frame_grande, bg=color["blue"], borderwidth=1, relief="flat")
        marco.grid(row=1, column=0, sticky="nsew", padx=5, pady=10)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(0, weight=1)
        
        # Crea la barra de menú
        menuBar = tk.Menu(App)
        App.config(menu=menuBar)
        App.title("Sistema de venta de vuelos")
        
        
        menuArchivo = tk.Menu(menuBar, tearoff=False,bg=color["blue"])
        menuBar.add_cascade(menu=menuArchivo, label="Archivo")
        menuArchivo.add_command(label="Aplicacion",command= lambda : alertInfo("Información de la aplicación","En esta aplicación podrás realizar la compra, reasignación y cancelación de vuelos, así como su respectivo check in donde a su vez podrás contratar servicios especiales que mejoren tu bienestar en el vuelo. Por último, puedes consultar tus datos de usuario y canjear millas por muchos beneficios. Gracias por usar nuestra aplicación :)"))
        menuArchivo.add_command(label="Salir", command = lambda : handlersProcesoConsulta["Salir"]())

        menuConsultas = tk.Menu(menuBar, tearoff=False,bg=color["blue"])
        menuBar.add_cascade(menu=menuConsultas, label="Procesos y Consultas")
        menuConsultas.add_command(label="Comprar vuelo", command = lambda : handlersProcesoConsulta["Comprar vuelo"](self))
        menuConsultas.add_command(label="Reasignar vuelo",command = lambda : handlersProcesoConsulta["Reasignar Vuelo"](self))
        menuConsultas.add_command(label="Cancelar vuelo",command = lambda : handlersProcesoConsulta["Cancelar Vuelo"](self))
        menuConsultas.add_command(label="Check In",command = lambda : handlersProcesoConsulta["Check In"](self))
        menuConsultas.add_command(label="Gestion usuario",command = lambda : handlersProcesoConsulta["Gestion usuario"](self))

        menuAyuda = tk.Menu(menuBar, tearoff=False,bg=color["blue"])
        menuBar.add_cascade(menu=menuAyuda, label="Ayuda")
        menuAyuda.add_command(label="Acerca de:",command= lambda : alertInfo("Información de los desarrolladores","Juan Carlos Largo B. - jlargob@unal.edu.co\n\nMaría Alejandra Muñoz G. - mamunozgo@unal.edu.co\n\nHarrison Zuleta M. - hzuletam@unal.edu.co"))
        
        #Zona main --------------------
        zonaProceso = tk.Frame(marco, bg=color["purple"], relief="flat")
        zonaProceso.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        marco.grid_rowconfigure(1, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        self.zona = zonaProceso
        
        # Ventana inicial del main menu
        InitMainMenu().generar(self, "Bienvenido al sistema de venta de vuelos", TEXT_DATA["breveDescripcionMenu"])
        
        pass


class VentanaInicial:
    def __init__(self):
        pass

    def generar(self):
        frame_grande = tk.Frame(App, bg=color["blue"])
        frame_grande.grid(row=0, column=0, sticky="nsew")
        App.grid_rowconfigure(0, weight=1)
        App.grid_columnconfigure(0, weight=1)

        # Barra de menu        
        menuBar = tk.Menu(App)
        App.config(menu=menuBar)
        
        menuInicio = tk.Menu(menuBar, tearoff=False,bg=color["blue"])
        menuBar.add_cascade(menu=menuInicio, label="Inicio")
    
        menuInicio.add_command( label="Salir", command = lambda: exitHandler(user))
        menuInicio.add_command( label="Descripcion", command = lambda: p3Label.config(text = TEXT_DATA["breveDescripcionApp"]))

        # Diferentes paneles
        p1 = tk.Frame(frame_grande, bg=color["purple"], borderwidth=1, relief="flat")
        p1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(0, weight=1)
        self.p1 = p1
        
        p2 = tk.Frame(frame_grande, bg=color["purple"], borderwidth=1, relief="flat")
        p2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(1, weight=1)
        self.p2 = p2

        p3 = tk.Frame(p1, bg=color["pink"], borderwidth=1, highlightbackground="#9656B6",highlightthickness=2)
        p3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        #p1.grid_rowconfigure(0, weight=1)
        #p1.grid_columnconfigure(0, weight=1)
        self.p3 = p1
        
        p4 = tk.Frame(p1, bg=color["pink"], borderwidth=1,highlightbackground="#9656B6",highlightthickness=2)
        p4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        p1.grid_rowconfigure(1, weight=1)
        p1.grid_columnconfigure(0, weight=1)
        self.p4 = p4

        p5 = tk.Frame(p2, bg=color["pink"], borderwidth=1, highlightbackground="#9656B6",highlightthickness=2)
        p5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        p2.grid_rowconfigure(0, weight=1)
        p2.grid_columnconfigure(0, weight=1)
        self.p5 = p5

        p6 = tk.Frame(p2, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
        p6.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        #p2.grid_rowconfigure(1, weight=1)
        #p2.grid_columnconfigure(0, weight=1)
        self.p6 = p6
        #.............................

        # Corto saludo de bienvenida (P3)
        #monospace = tk.font.Font(family="monospace", size=12,file="src\imagenes\JetBrainsMono-Regular.ttf")
        p3Label = tk.Label(p3, text = TEXT_DATA["textoBienvenida"], anchor="w", justify="center", bg=color["pink"],fg="#5B2A73",font=("fixedsys",12))
        p3Label.grid(row=0,column=0,padx=5, pady=5, sticky="nsew")
        p3.grid_rowconfigure(0, weight=1)
        p3.grid_columnconfigure(0, weight=1)

        # Ingreso al sistema  y seccion de imagenes (P4)
        marcoImagenes = tk.Frame(p4)
        marcoImagenes.grid(row=0,column=0,padx=10,pady=10)
        p4.grid_rowconfigure(0,weight=1)
        p4.grid_columnconfigure(0,weight=1)
        # Lista de nombres de archivos de imágenes
        global indexImg
        indexImg = 0
        
        # Lista de rutas a las imágenes del sistema
        sistemaPaths = [ "src/data/imagenS1.png", "src/data/imagenS2.png","src/data/imagenS3.png","src/data/imagenS4.png","src/data/imagenS5.png"]
        
        # Crea una lista de objetos PhotoImage a partir de las rutas de las imágenes
        fotos = [
            ImageTk.PhotoImage(Image.open(path).resize((700, 550)))
            for path in sistemaPaths
        ]
        
        # Crea una etiqueta con la primera imagen
        etiqueta = tk.Label(marcoImagenes, image=fotos[0],highlightbackground=color["blue"],highlightthickness=4)
        etiqueta.grid(row=0, column=0)    
        etiqueta.bind("<Enter>", lambda event: changeImage())
    
        def changeImage():
            """
            Cambia la imagen mostrada en la etiqueta.
            """
            global indexImg
            indexImg = 0 if indexImg == (len(fotos)-1) else indexImg + 1
            etiqueta.configure(image=fotos[indexImg])
        
        # Crea un botón para ingresar al sistema
        botonIngreso = tk.Button(p4,text="Ingreso al sistema",bg=color["blue"],font=("fixedsys",12),relief="groove",fg=color["darkblue"],height="2",width="25")
        botonIngreso.grid(row=1,column=0,padx=15,pady=10,sticky="s")
        botonIngreso.bind("<Button-1>", lambda e : MainMenu().generar())
        # - - - Seccion informacion y hojas de vida - - -
        
        
        # Guardar datos de hojas de vida
        hojasVida = {}
        for i in range(1, 3 + 1):
            file = open(f"src/data/desarrolladores/hojaVida{i}.txt","r")
            hojasVida[str(i)] = file.read()
            file.close()
            
        hojasVida["Indice"] = 1
        
        imagenes = {}
        for i in range(1, 3 + 1):
            imagenes[str(i)] = []
            for j in range(1, 5):
                # Falta unificar formato !!!!
                imagenes[str(i)].append(f"src/data/desarrolladores/imagen{i}-{j}.jpg")
                    
        #Funcion para mostrar imagenes segun la persona
        def showImages(index):
            i=1
            for i, path in enumerate(imagenes.get(index, [])):
                img = getImage(p6, path, (200, 200),highlightbackground="#FFA7EE",highlightthickness=3)
                img.grid(row= (i//2), column=(i%2), padx=10, pady=10)
        p6.grid_rowconfigure(0,weight=1)
        p6.grid_columnconfigure(0,weight=1)
        p6.grid_rowconfigure(1,weight=1)
        p6.grid_columnconfigure(1,weight=1)

                
        #Definir funcion hojas vida
        def cambioHojaVida(index):
            if index == 3:
                hojasVida["Indice"] = 1
                #imagenes["imagenIndex"]=1
            else:
                hojasVida["Indice"] +=1
                #imagenes["imagenIndex"]+=1
            
            hojaVidaLabel.config(text=hojasVida[str(hojasVida["Indice"])])
            showImages(str(hojasVida["Indice"]))
            pass
        
        hojaVidaLabel = tk.Label(p5, text="", font=("fixedsys",14),bg=color["pink"],fg="#5B2A73",justify="center")
        hojaVidaLabel.grid(row=1,column=0, padx=5, pady=5,sticky="nsew")
        p5.grid_rowconfigure(0,weight=1)
        p5.grid_columnconfigure(0,weight=1)
        hojaVidaLabel.bind("<Button-1>", lambda e: cambioHojaVida(hojasVida["Indice"]))
        cambioHojaVida(hojasVida["Indice"])

        tituloBios = tk.Label(p5,text="Biografía de los desarrolladores",font=("fixedsys",15,"bold"),bg=color["pink"],fg="#431b57",justify="center")
        tituloBios.grid(row=0,column=0,padx=5, pady=5,sticky="nsew")
        p5.grid_rowconfigure(1,weight=1)

        clickLabel = tituloBios = tk.Label(p5,text="Click sobre la biografía para cambiar de desarrollador",font=("fixedsys",10),bg=color["pink"],fg="#cf488d",justify="center")
        clickLabel.grid(row=2,column=0,padx=5, pady=5,sticky="nsew")
        p5.grid_rowconfigure(2,weight=1)
        pass


class VentanaBaseFuncionalidad(tk.Frame):
    """
    Clase base que representa una ventana de funcionalidad en la interfaz de usuario.

    Atributos:
        parent (tkinter.Tk): La ventana principal de la aplicación.
        zona (tkinter.Frame): El marco que contiene los elementos de la interfaz de usuario.
        zonaForm (tkinter.Frame): El marco que contiene los elementos del formulario.
    """
    
    def generar(self, mainMenu, nombre, descripcion):
        self.mainMenu = mainMenu
        self.zona = mainMenu.zona
        self.nombre = nombre
        self.descripcion = descripcion
        
        self.zonaInfo = tk.Frame(self.zona, bg=color["pinkpurple"], highlightbackground="#9656B6",highlightthickness=2)
        self.zonaInfo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(0, weight=0)
        self.zona.grid_columnconfigure(0, weight=0)
        
        self.nombreProceso = tk.Label(self.zonaInfo, text= self.nombre, bg=color["pinkpurple"],font=("fixedsys",22,"bold"),fg="#5B2A73")
        self.nombreProceso.grid(row=0, column=0, padx=10, pady=10)
        self.zonaInfo.grid_rowconfigure(0, weight=0)
        self.zonaInfo.grid_columnconfigure(0, weight=1)
        
        self.descripcionProceso = tk.Label(self.zonaInfo, text= self.descripcion,bg=color["pinkpurple"],font=("fixedsys",15),fg="#5B2A73")
        self.descripcionProceso.grid(row=1, column=0, padx=15, pady=15)
        self.zonaInfo.grid_rowconfigure(0, weight=0)
        self.zonaInfo.grid_columnconfigure(0, weight=1)

        avion = getImage(self.zonaInfo, "src/data/iconoAvion.png",(80,80))
        avion.grid(row=0, column=0, padx=5, pady=5,sticky="e")
        
        self.zonaForm = tk.Frame(self.zona, bg=color["pinkpurple"], highlightbackground="#9656B6",highlightthickness=2)
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)
        
        self.ventana1()
        pass
    
    def showSelectHistorial(self, callback):
        """
        Muestra el historial de boletos del usuario y permite seleccionar uno.

        Args:
            callback (function): Función a llamar cuando se selecciona un boleto.
        """
        # Obtiene el historial de boletos del usuario
        historialBoletos = user.getHistorial()
        
        # Crea un marco de resultados con el historial de boletos
        infoVuelos = ResultFrame(
            "Historial de vuelos",
            {f"Boleto #{i+1}" : boleto.getStr() for i, boleto in enumerate(historialBoletos) },
            self.zonaForm
        )
        nextFreeRow = infoVuelos.nextFreeRow

        # Crea un separador
        separador = getSeparador(infoVuelos.marco, nextFreeRow, 2, 5)
        
        # Crea una etiqueta y un dropdown para seleccionar un vuelo
        labelVuelo = tk.Label(infoVuelos.marco, text = "Vuelo:",font=("fixedsys",12),bg="#E1BEFF")
        labelVuelo.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)
        dropDownVuelos = ttk.Combobox(infoVuelos.marco,state = "readonly", values = [f"Boleto #{i+1}" for i in range(len(historialBoletos))],font="fixedsys" )
        dropDownVuelos.grid(row=nextFreeRow+1, column=1, padx=15, pady=15)
        
        # Crea un botón para cancelar la operación
        getBotonCancelar(infoVuelos.marco, lambda: self.cancel(), nextFreeRow+2, 0)
        
        def verify():
            """
            Verifica que se haya seleccionado un boleto y llama a la función de callback.
            """
            try:
                if dropDownVuelos.current() != -1:
                    callback(dropDownVuelos.current())
                else:
                    raise ErrorSeleccionarDropdown()
                
            except ErrorSeleccionarDropdown:
                alertWarn("Campos sin seleccionar", "Error, por favor seleccione todos los campos antes de continuar :3")
            pass
        
        # Crea un botón para continuar con la operación
        getBotonContinuar(infoVuelos.marco, lambda: verify(), nextFreeRow+2, 1)
        pass
    
    def cancel(self):
        """
        Cancela la operación actual y vuelve a la ventana principal.
        """
        self.clearZone()
        self.ventana1()
        pass
    
    def clearZone(self):    
        """
        Limpia la zona de formulario actual.
        """
        # Destruye el marco del formulario actual
        self.zonaForm.destroy()
        
        # Crea un nuevo marco de formulario vacío
        self.zonaForm = tk.Frame(self.zona, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)
        pass

class InitMainMenu(VentanaBaseFuncionalidad):
    """
    Clase que representa el menú principal de la aplicación.

    Hereda de VentanaBaseFuncionalidad.
    """

    def ventana1(self):
        """
        Genera la interfaz de usuario para la ventana principal.
        """
        # Crea las etiquetas de título
        labelTitulo1 = tk.Label(self.zonaForm, text="¿Cómo usar la aplicación?",font=("fixedsys",16),anchor="center" ,justify="center",bg=color["purple"],fg="#310944")
        labelTitulo1.grid(row=0,column=0)
        labelTitulo2 = tk.Label(self.zonaForm, text="¿Qué se puede hacer?",font=("fixedsys",16),anchor="center" ,justify="center",bg=color["purple"],fg="#310944")
        labelTitulo2.grid(row=2,column=0)

        # Texto de las etiquetas
        texto1 = "Bienvenido a la aplicación de la aerolínea, en esta podrás hacer uso de los diferentes servicios\n que te proporcionamos como usuario. En la esquina superior izquierda encontrarás tres opciones de\n menú. En Archivo tienes las opciones de Aplicación y Salir, en las cuales encontrarás información\n de la aplicación y te redirigirá a la ventana de Inicio respectivamente. En el menú de Procesos y\n Consultas se desplegarán las funcionalidades de la aplicación, las cuales son: Comprar, reasignar\n y cancelar vuelo, hacer Check In y Gestión de Usuario; al elegir alguna de las opciones anteriores\n te redirigirá a la interfaz de dicha funcionalidad, en la cual se presentará una breve descripción\n de lo que se hace allí y los formularios necesarios para ello."
        texto2="Entre las acciones que podrás realizar se encuentran comprar y definir su boleto, reasignar el\nmismo junto con su asiento y maleta, cancelarlo con un 50% de reembolso, confirmar su asistencia\n haciendo check in, tener la disponibilidad de contratar servicios especiales durante y después\n del vuelo para mejorar tu comodidad, y por último, gestionar tu dinero, consultar historial\n de vuelos y canjear millas por nuevos beneficios. Finalmente, en la parte de Ayuda,\n aparecerá información sobre los desarrolladores del programa."

        # Crea las etiquetas de texto
        labelTexto1 = tk.Label(self.zonaForm, text = texto1, font=("fixedsys",16),anchor="center" ,justify="center",bg=color["pinkpurple"],fg="#310944")
        labelTexto1.grid(row=1, column=0)
        labelTexto2 = tk.Label(self.zonaForm, text = texto2, font=("fixedsys",16),anchor="center" ,justify="center",bg=color["pinkpurple"],fg="#310944")
        labelTexto2.grid(row=3, column=0)

        imgMenu = getImage(self.zonaForm,"src\data\imgMenu.png",(180,180))
        imgMenu.grid(row=1, column=1)

        self.zonaForm.grid_columnconfigure(0,weight=1)
        self.zonaForm.grid_rowconfigure(0,weight=1)
        self.zonaForm.grid_columnconfigure(1,weight=1)
        self.zonaForm.grid_rowconfigure(2,weight=1)
        self.zonaForm.grid_rowconfigure(3,weight=1)
        pass
    pass

class ComprarVuelo(VentanaBaseFuncionalidad):
    """
    Clase que representa la funcionalidad de compra de vuelos en la aplicación.

    Hereda de VentanaBaseFuncionalidad.
    """
    def ventana1(self):
        
        def callback(formData):
            
            vuelos = Vuelo.generarVuelos(5, formData[criterios[0]], formData[criterios[1]]) #Genera los vuelos 
            asientos = (vuelos[0]).generarAsientos(3, 5, 100) # Genera los asientos del primer vuelo
            
            def selecAsientos(event):
                vuelo = vuelos[dropDownVuelos.current()] # selecciona el vuelo seleccionado
                asientos = vuelo.generarAsientos(3, 5, 100) # Genera los asientos del vuelo
                dropDownAsientos["values"] = asientos # Muestralos asientos del vuelo seleccionado
                pass
            
            def verify():
                newData = {
                    "vuelo": vuelos[dropDownVuelos.current()],
                    "asiento": asientos[dropDownAsientos.current()],
                    "maletas": int(dropDownMaletas.current()),
                }
                verificado = (
                    dropDownVuelos.current() != -1 and
                    dropDownAsientos.current() != -1 and
                    dropDownMaletas.current() != -1
                )
                
                try:
                    if verificado:
                        self.ventana2(newData, formData) # Origen, destino
                    else:
                        raise ErrorSeleccionarDropdown()
                    
                except ErrorSeleccionarDropdown:
                    alertWarn("Campos sin seleccionar", "Error, por favor seleccione todos los campos antes de continuar :3")
                pass
            
            separador = getSeparador(formElement.marco, nextFreeRow, 2, 5) # Separador generico
            
            # Seleccionar vuelo y asiento
            labelVuelo = tk.Label(formElement.marco, text = "Vuelo:",bg=color["pink"],font=("fixedsys",10)) 
            labelVuelo.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)            
            dropDownVuelos = ttk.Combobox(formElement.marco,state = "readonly", values = vuelos, font="fixedsys")
            dropDownVuelos.grid(row=nextFreeRow+1, column=1, padx=15, pady=15)
            dropDownVuelos.bind("<<ComboboxSelected>>", selecAsientos)
            
            labelAsiento = tk.Label(formElement.marco, text = "Asiento:",bg=color["pink"],font=("fixedsys",10))
            labelAsiento.grid(row=nextFreeRow+2, column=0, padx=5, pady=5)
            dropDownAsientos = ttk.Combobox(formElement.marco,state = "readonly",values = asientos,font="fixedsys" )
            dropDownAsientos.grid(row=nextFreeRow+2, column=1, padx=15, pady=15)
            
            labelMaletas = tk.Label(formElement.marco, text = "Cantidad de maletas:",bg=color["pink"],font=("fixedsys",10))
            labelMaletas.grid(row=nextFreeRow+3, column=0, padx=5, pady=5)
            dropDownMaletas = ttk.Combobox(formElement.marco,state = "readonly",values = [0, 1, 2, 3, 4],font="fixedsys")
            dropDownMaletas.grid(row=nextFreeRow+3, column=1, padx=15, pady=15)

            # Crea boton de siguiente y uno de cancelar  
            getBotonCancelar(formElement.marco, lambda: self.cancel(), nextFreeRow+4, 0)
            getBotonContinuar(formElement.marco, lambda: verify(), nextFreeRow+4, 1)
            
            pass
        
        criterios = ["Origen", "Destino"]
        formElement = FieldFrame(
            "Datos del Vuelo",
            criterios,
            "Ingrese los datos",
            criterios,
            None, self.zonaForm,
            callback = callback
        )

        nextFreeRow = formElement.nextFreeRow
        pass
    
    def ventana2(self, newData, prevData):
        self.clearZone()
        
        def callback(formData):
            maletas = [ 
                Maleta( index+1, float(formData[key]), boleto )
                for index, key in enumerate(formData.keys())
            ]
            
            alertInfo("Previsualizacion del precio", f"Precio a pagar en total por {numMaletas} maletas: ${sum(maleta.calcularPrecio() for maleta in maletas)}, Total boleto: {boleto.valor}")
            
            # Crea boton de siguiente y uno de cancelar  
            self.ventana3(boleto)
            pass
        
        
        boleto = Boleto(
            prevData["Origen"],
            prevData["Destino"],
            newData["vuelo"],
            newData["asiento"],
            user
        )
        
        numMaletas = newData["maletas"]
        
        if (numMaletas == 0):
            self.ventana3(boleto)
        else:
            # Inputs de maletas
            criterios = [
                f"Maleta #{i}"
                for i in range(1, numMaletas + 1)
            ]
            
            formElement = FieldFrame(
                "Maleta",
                criterios,
                "Peso de la maleta",
                None,
                None, self.zonaForm,
                callback = callback
            )
            nextFreeRow = formElement.nextFreeRow
        pass

        
    def ventana3(self, boleto):
        self.clearZone()
        # Se muestra info del vuelo y previsualizacion de datos y se pide confirmacion
        def confirmarCompra():
            ok = alertConfirmacion(f"Confirmacion de compra, valor final: ${boleto.valor}")
            
            if ok:
                try:
                    if (user.dinero >= boleto.valor):
                        user.comprarBoleto(boleto)
                        alertInfo("Compra exitosa", "Boleto comprado con exito!, gracias por usar nuestra aplicacion.")
                        self.cancel()
                    else:
                        raise ErrorDineroInsuficiente()    
                
                except ErrorDineroInsuficiente:
                    alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")
                    self.cancel()
            pass
        
        resultFrame = ResultFrame(
            "Detalles del boleto",
            boleto.getInfo(),
            self.zonaForm
        )
        nextFreeRow = resultFrame.nextFreeRow
        
        separador = getSeparador(resultFrame.marco, nextFreeRow, 2, 5)
        
        getBotonCancelar(resultFrame.marco, lambda: self.cancel(), nextFreeRow+1, 0)
        getBotonContinuar(resultFrame.marco, lambda: confirmarCompra(), nextFreeRow+1, 1)
        pass

class ReasignarVuelo(VentanaBaseFuncionalidad):
    
    
    def ventana1(self):
        self.showSelectHistorial(self.ventana2)
        pass
    
    def ventana2(self, indexBoleto):
        self.clearZone()
        boleto = user.getHistorial()[indexBoleto]
        
        def confirmarReasignacion(boleto, indexBoleto):
            ok = alertConfirmacion("Esta seguro de reasignar el vuelo? se cobrara un 10% adicional por el proceso")
            
            # Verificar si no es un boleto cancelado o reasignado
            if ok:
                if boleto.status == "Cancelado":
                    alertWarn("Boleto cancelado", "Error, el boleto ya fue cancelado, no se puede reasignar")
                    self.cancel()
                else:
                    self.ventana3(boleto, indexBoleto)
                
        resultFrame = ResultFrame(
            "Detalles del boleto",
            boleto.getInfo(),
            self.zonaForm
        )
        nextFreeRow = resultFrame.nextFreeRow
        
        separador = getSeparador(resultFrame.marco, nextFreeRow, 2, 5)
        
        getBotonCancelar(resultFrame.marco, lambda: self.cancel(), nextFreeRow+1, 0)
        getBotonContinuar(resultFrame.marco, lambda: confirmarReasignacion(boleto, indexBoleto), nextFreeRow+1, 1)
        pass
    
    def ventana3(self, boleto, indexBoleto):
        vuelos = Vuelo.generarVuelos(5, boleto.origen, boleto.destino) #Genera los vuelos 
        asientos = (vuelos[0]).generarAsientos(3, 5, 100)
        
        vuelosDisponibles = ResultFrame(
            f"Vuelos disponibles (Origen: {boleto.origen}, Destino: {boleto.destino})",
            { f"Vuelo #{i+1}" : vuelo for i, vuelo in enumerate(vuelos) },
            self.zonaForm
        )
        nextFreeRow = vuelosDisponibles.nextFreeRow

        def selecAsientos(event):
            vuelo = vuelos[dropDownVuelos.current()]
            asientos = vuelo.generarAsientos(3, 5, 100)
            dropDownAsientos["values"] = asientos
            pass
        
        
        # Seleccionar vuelo y asiento
        labelVuelo = tk.Label(vuelosDisponibles.marco, text = "Vuelo:",bg=color["pink"], font=("fixedsys",10))
        labelVuelo.grid(row=nextFreeRow, column=0, padx=5, pady=5)
        dropDownVuelos = ttk.Combobox(vuelosDisponibles.marco,state = "readonly", values = [f"Vuelo #{i+1}" for i in range(len(vuelos))],font="fixedsys" )
        dropDownVuelos.grid(row=nextFreeRow, column=1, padx=15, pady=15)
        dropDownVuelos.bind("<<ComboboxSelected>>", selecAsientos)
        
        labelAsiento = tk.Label(vuelosDisponibles.marco, text = "Asiento:",bg=color["pink"], font=("fixedsys",10))
        labelAsiento.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)
        dropDownAsientos = ttk.Combobox(vuelosDisponibles.marco,state = "readonly",values = asientos,font="fixedsys" )
        dropDownAsientos.grid(row=nextFreeRow + 1, column=1, padx=15, pady=15)
        
        labelMaletas = tk.Label(vuelosDisponibles.marco, text = "Cantidad de maletas:",bg=color["pink"], font=("fixedsys",10))
        labelMaletas.grid(row=nextFreeRow+2, column=0, padx=5, pady=5)
        dropDownMaletas = ttk.Combobox(vuelosDisponibles.marco,state = "readonly",values = [0, 1, 2, 3, 4],font="fixedsys")
        dropDownMaletas.grid(row=nextFreeRow+2, column=1, padx=15, pady=15)
        
        def verify():
            verificado = (
                dropDownVuelos.current() != -1 and
                dropDownAsientos.current() != -1 and
                dropDownMaletas.current() != -1
            )
            try:
                if verificado:
                    self.ventana4(
                        {
                            "vuelo": vuelos[dropDownVuelos.current()],
                            "asiento": asientos[dropDownAsientos.current()],
                            "maletas": int(dropDownMaletas.current()),
                            "indexBoleto": indexBoleto,
                        }, {"Origen": boleto.origen, "Destino": boleto.destino} # Origen, destino, cantidad maletas
                    )
                else:
                    raise ErrorSeleccionarDropdown()
                
            except ErrorSeleccionarDropdown:
                alertWarn("Campos sin seleccionar", "Error, por favor seleccione todos los campos antes de continuar :3")
            pass
        
        # Crea boton de siguiente y uno de cancelar  
        getBotonCancelar(vuelosDisponibles.marco, lambda: self.cancel(), nextFreeRow+3, 0)
        getBotonContinuar(vuelosDisponibles.marco, lambda: verify(),nextFreeRow+3, 1)
        pass

        
    def ventana4(self, newData, prevData):
        self.clearZone()
        
        def callback(formData):  
            maletas = [ 
                Maleta( index+1, float(formData[key]), newBoleto )
                for index, key in enumerate(formData.keys())
            ]
            
            alertInfo("Previsualizacion del precio", f"Precio a pagar en total por {numMaletas} maletas: ${sum(maleta.calcularPrecio() for maleta in maletas)}")
            
            separador = getSeparador(formElement.marco, nextFreeRow, 2, 5)
        
            # Crea boton de siguiente y uno de cancelar
            getBotonCancelar(formElement.marco, lambda: self.cancel(), nextFreeRow+1, 0)
            getBotonContinuar(formElement.marco, lambda: self.ventana5(newBoleto, newData["indexBoleto"]), nextFreeRow+1, 1)
            pass
        
        newBoleto = Boleto(
            prevData["Origen"],
            prevData["Destino"],
            newData["vuelo"],
            newData["asiento"],
            user
        )
        
        numMaletas = newData["maletas"]
        
        if (numMaletas == 0):
            self.ventana5(newBoleto, newData["indexBoleto"])
        else:
            # Inputs de maletas
            criterios = [f"Maleta #{i}" for i in range(1, numMaletas + 1)]
            formElement = FieldFrame(
                "Maleta",
                criterios,
                "Peso de la maleta",
                criterios,
                None, self.zonaForm,
                callback = callback
            )
            nextFreeRow = formElement.nextFreeRow
        pass

        
    def ventana5(self, newBoleto, indexBoleto):
        self.clearZone()
        # Se muestra info del vuelo y previsualizacion de datos y se pide confirmacion
        def confirmarCompra():
            valorReasignacion = newBoleto.calcularReasignacion(user.getHistorial()[indexBoleto])
            
            ok = alertConfirmacion(f"Esta seguro de reasignar su vuelo?, se cobrara el restante del vuelo anterior + 10% del valor del boleto adicional. Total: {valorReasignacion}")
            
            if ok:
                try:
                    if (user.dinero >= valorReasignacion):
                        user.reasignarBoleto(newBoleto, indexBoleto)
                        alertInfo("Compra exitosa", "Boleto reasginado con exito, gracias por su atencion")
                        self.cancel()
                    else:
                        raise ErrorDineroInsuficiente()
            
                except ErrorDineroInsuficiente:
                    alertWarn("Dinero Insuficiente", "Error, dinero en la cuenta insuficiente, compra cancelada")
                    self.cancel()
                    pass
                      
            pass
        
        resultFrame = ResultFrame(
            "Detalles del boleto",
            newBoleto.getInfo(),
            self.zonaForm
        )
        nextFreeRow = resultFrame.nextFreeRow
        
        separador = getSeparador(resultFrame.marco, nextFreeRow, 2, 5)
        
        getBotonCancelar(resultFrame.marco, lambda: self.cancel(), nextFreeRow+1, 0)
        getBotonContinuar(resultFrame.marco, lambda: confirmarCompra(), nextFreeRow+1, 1)
        pass

class CancelarVuelo(VentanaBaseFuncionalidad):

    def ventana1(self):
        self.showSelectHistorial(self.ventana2)
        pass

    def ventana2(self, indexBoleto):
        self.clearZone()
        boleto = user.getHistorial()[indexBoleto]
        
        def confirmarCancelar(boleto):
            ok = alertConfirmacion(f"Esta seguro de cancelar el vuelo? se regresara solo un 50% de su valor original (${boleto.valor})")
            
            if ok:
                if boleto.status == "Cancelado":
                    alertWarn("Error", "El boleto ya se encuentra cancelado")
                    self.cancel()
                else:
                    retorno = user.cancelarBoleto(boleto)
                    alertInfo("Proceso exitoso", f"Boleto cancelado con exito, se han regresado ${retorno} a su cuenta (Al cancelar un boleto se regresa un 50%)")
                    self.cancel()
            pass
        
        resultFrame = ResultFrame(
            "Detalles del boleto",
            boleto.getInfo(),
            self.zonaForm
        )
        nextFreeRow = resultFrame.nextFreeRow
        
        getBotonCancelar(resultFrame.marco, lambda: self.cancel(), nextFreeRow, 0)
        getBotonContinuar(resultFrame.marco, lambda: confirmarCancelar(boleto), nextFreeRow, 1)
        pass


class CheckIn(VentanaBaseFuncionalidad):
    
    def ventana1(self):
        self.clearZone()
        self.showSelectHistorial(self.ventana2)
        pass
    
    def ventana2(self, indexBoleto):
        
        self.clearZone()
        boleto = user.getHistorial()[indexBoleto]
                
        resultFrame = ResultFrame(
            "Detalles del boleto",
            boleto.getInfo(),
            self.zonaForm
        )
        
        nextFreeRow = resultFrame.nextFreeRow
        
        getBotonCancelar(resultFrame.marco, lambda: self.cancel(), nextFreeRow, 0)
        getBotonContinuar(resultFrame.marco, lambda: confirmacion(boleto), nextFreeRow, 1)

        def confirmacion(boleto):
            
            # SI el boleto ya tiene check in pasa a los servicios
            if (boleto.checkInRealizado):
                alertInfo("Check In", "El boleto seleccionado ya tiene check in, pasando al menu de servicios")
                self.ventanaServicios(boleto)

            else:
                if boleto.status == "Cancelado":
                    alertWarn("Error", "El boleto es un boleto cancelado, no se puede hacer Check In")
                    self.cancel()
                else: 
                    # SI no tiene check se pide la verificacion para hacer check in, y se pasa a los servicios
                    ok = alertConfirmacion("El boleto seleccionado aun no tiene check in, desea confirmar el check in?")
                    if ok:
                        # Backend check In
                        boleto.makeCheckIn()

                        alertInfo("Check In", "Check In realizado con exito!")
                        self.ventanaServicios(boleto)

    def ventanaServicios(self, boleto):
        self.zona3 = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
        self.zona3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
            
        self.clearZone()
        
        # Mostrar millas disponibles
        infoServicios = ResultFrame(
            "Informacion del boleto",
            {
                "Origen - Destino": boleto.getOrigenDestino(),
                "Tipo asiento": boleto.tipo,
                "Cantidad maletas": len(boleto.equipaje), 
                "Servicios contratados": len(boleto.serviciosContratados) 
            },
            self.zonaForm
        )
        nextFreeRow = infoServicios.nextFreeRow
        
        # Dropdown de la opcion
        labelOpciones = tk.Label(infoServicios.marco, text = "Seleccionar opcion",font=("fixedsys",12),bg="#E1BEFF")
        labelOpciones.grid(row=nextFreeRow, column=0, padx=5, pady=5)            
        dropDownOpciones = ttk.Combobox(infoServicios.marco, state = "readonly", values = [
            "Mejorar asiento", "Comprar servicios especiales"
        ],font="fixedsys")
        
        nextRow = nextFreeRow + 2
        dropDownOpciones.grid(row=nextFreeRow, column=1, padx=15, pady=15)
        dropDownOpciones.bind("<<ComboboxSelected>>", lambda e: handlersCheckIn[dropDownOpciones.get()](nextRow, boleto))
        
        separador = getSeparador(infoServicios.marco, nextFreeRow + 1, 2)

        self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
        self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)


        def mejoraSilla(nextRow, boleto):
            self.zona3.destroy()
            self.zona3 = tk.Frame(self.zonaForm,bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zona3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
                
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            def confirmar(boleto, asiento):
                ok = alertConfirmacion(f"Desea hacer una mejora de su asiento por $35")
                
                try:
                    if dropDownAsiento.current() == -1:
                        raise ErrorSeleccionarDropdown()
                except ErrorSeleccionarDropdown:
                    alertWarn("Campos sin seleccionar", "Error, por favor seleccione todos los campos antes de continuar :3")
                pass
        
                if ok:
                    try:
                        if (boleto.tipo == "Vip"):
                            alertWarn("Error", "Error, el boleto ya es de tipo VIP, no se puede mejorar mas")
                        else:
                            if (user.dinero >= 35):
                                boleto.upgradeAsiento(asiento)
                                alertInfo("Transaccion exitosa", "Mejora de asiento realizada con exito!")
                                self.clearZone()
                                self.ventanaServicios(boleto)
                            else:
                                raise ErrorDineroInsuficiente()
                            
                    except ErrorDineroInsuficiente:
                        alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")
                        
                pass
            
            labelAsiento = tk.Label(self.zonaResult, text = "Seleccionar nuevo asiento",font=("fixedsys",12),bg=color["pink"])
            labelAsiento.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownAsiento = ttk.Combobox(self.zonaResult, state = "readonly", values = [
                asiento for asiento in boleto.vuelo.asientos
                if asiento.tipo == "Vip"
            ], font="fixedsys")
            dropDownAsiento.grid(row=nextRow, column=1, padx=15, pady=15)

            b1 = getBotonTemp(self.zonaResult, lambda: self.cancel(), nextRow+1, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar(
                boleto,
                boleto.vuelo.asientos[dropDownAsiento.current()]
            ), nextRow+1, 1)
            
            pass
        
        
        def comprarServicios(nextRow, boleto):
            self.zona3.destroy()
            self.zona3 = tk.Frame(self.zonaForm,bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zona3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
             
            def tempHandler(key, row, boleto):
                self.zona3.destroy()
                self.zona3 = tk.Frame(self.zonaForm,bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
                self.zona3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
                handlersServicios[key](0, boleto)
                
                
            def servicioComida(nextRow, boleto):
                def confirmar(boleto):
                    servicio = ServiciosEspeciales.COMIDA_A_LA_CARTA

                    ok = alertConfirmacion(f"¿Desea comprar el servicio de comida a la carta durante el vuelo? Este tiene un costo de ${servicio.precio}")
                
                    if ok:
                        try:
                            if (user.dinero >= servicio.precio):                            
                                boleto.comprarServicio(servicio)
                                alertInfo("Transaccion exitosa", "Mejora de asiento realizada con exito!")
                                self.clearZone()
                                self.ventanaServicios(boleto)
                            else:
                                raise ErrorDineroInsuficiente()
                            
                        except ErrorDineroInsuficiente:
                            alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")
                    pass
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de comprar comida a la carta tiene un costo de $40,\npresione el botón de continuar si desea adquirirlo.",bg=color["pink"],font=("fixedsys",12))
                labelAviso.grid(row=0, column=0, padx=10, pady=5)
                
                avion = getImage(self.zona3, "src\data\comidaCarta.png",(90,90))
                avion.grid(row=0, column=1, padx=10, pady=5)
                
                b1 = getBotonTemp(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                
                pass

            def servicioMascota(nextRow, boleto):
                
                def confirmar(formData):
                    servicio = ServiciosEspeciales.MASCOTA_EN_CABINA
                    ok = alertConfirmacion(f"¿Desea contratar el servicio de transporte de mascota? Tiene un costo de ${servicio.precio}")
                
                    if ok:
                        mascota = None
                        if (formData["Perro/Gato"].lower() == "perro"):
                            mascota = Perro(formData["Nombre"], formData["Raza"], float(formData["Peso"]))
                        elif (formData["Perro/Gato"].lower() == "gato"):
                            mascota = Gato(formData["Nombre"], formData["Raza"], float(formData["Peso"]))            
                        else:
                            alertWarn("Error", "Error, tipo de mascota no valido, solo se admite Perro o Gato")
                            pass
                            
                        if mascota != None:
                            try:
                                if (user.dinero >= servicio.precio):          
                                    boleto.comprarServicioMascota(mascota)
                                    alertInfo("Transaccion exitosa", f"Servicio agregado con exito, ahora {mascota.nombre} podra viajar contigo!")
                                    self.clearZone()
                                    self.ventanaServicios(boleto)
                                else:
                                    raise ErrorDineroInsuficiente()
                                
                            except ErrorDineroInsuficiente:
                                alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")
                                
                        self.zona3.destroy()
                        self.zona3 = tk.Frame(self.zonaForm,bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
                        self.zona3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
                    pass
            
                formMascota = FieldFrame(
                    "Datos mascota",
                    ["Nombre", "Raza", "Peso", "Perro/Gato"],
                    "Datos",
                    None, None, self.zona3,
                    callback=confirmar
                )
                
                pass

            def servicioMenor(nextRow, boleto):
                
                def confirmar(boleto):
                    servicio = ServiciosEspeciales.ACOMPANANTE_PARA_MENOR
                    ok = alertConfirmacion(f"¿Desea contratar un acompañante para el pasajero menor de edad? Esto tiene un costo de ${servicio.precio}")

                    if ok:
                        try:
                            if (user.dinero >= servicio.precio):                            
                                boleto.comprarServicio(servicio)
                                alertInfo("Transaccion exitosa", "Servicio contratado con exito!")
                                self.clearZone()
                                self.ventanaServicios(boleto)
                            else:
                                raise ErrorDineroInsuficiente()
                        
                        except ErrorDineroInsuficiente:
                            alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")    
                    pass
                
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de contratar un acompañante para el pasajero menor de edad tiene un costo de $15",bg=color["pink"],font=("fixedsys",10))
                labelAviso.grid(row=nextRow, column=0, padx=5, pady=5)
                
                menorEdad = getImage(self.zona3, "src\data\menorEdad.png",(90,90))
                menorEdad.grid(row=0, column=1, padx=10, pady=5)
                
                b1 = getBotonTemp(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                pass

            def servicioAsistencia(nextRow, boleto):
                
                def confirmar(boleto):
                    servicio = ServiciosEspeciales.ASISTENCIA_NECESIDADES_ESPECIALES
                    ok = alertConfirmacion(f"¿Desea contratar asistencia para pasajero con necesidades especiales? Este servicio no tiene ningun costo")

                    if ok:
                        try:
                            if (user.dinero >= servicio.precio):                            
                                boleto.comprarServicio(servicio)
                                alertInfo("Transaccion exitosa", "Servicio contratado con exito!")
                                self.clearZone()
                                self.ventanaServicios(boleto)
                            else:
                                raise ErrorDineroInsuficiente()
                            
                        except ErrorDineroInsuficiente:
                            alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")
                    pass
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de contratar asistencia para pasajero con necesidades especiales no tiene ningun costo",bg=color["pink"],font=("fixedsys",12))
                labelAviso.grid(row=nextRow, column=0, padx=5, pady=5)
                
                discapacidad = getImage(self.zona3, "src\data\discapacidad.png",(90,90))
                discapacidad.grid(row=0, column=1, padx=10, pady=5)
                
                b1 = getBotonTemp(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                pass

            def servicioTransporte(nextRow, boleto):
                def confirmar(boleto):
                    servicio = ServiciosEspeciales.TRANSPORTE_TERRESTRE
                    ok = alertConfirmacion(f"¿Desea contratar el servicio de transporte terrestre? Este tiene un costo de ${servicio.precio}")

                    if ok:
                        try:
                            if (user.dinero >= servicio.precio):                            
                                boleto.comprarServicio(servicio)
                                alertInfo("Transaccion exitosa", "Servicio contratado con exito!")
                                self.clearZone()
                                self.ventanaServicios(boleto)
                            else:
                                raise ErrorDineroInsuficiente()
                        
                        except ErrorDineroInsuficiente:
                            alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")
                    pass
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de transporte terrestre tiene un costo de $70.\nUna van te recogerá en el aeropuerto y te llevará a tu hotel o lugar de destino.",bg=color["pink"],font=("fixedsys",10))
                labelAviso.grid(row=nextRow, column=0, padx=5, pady=5)
                
                transporte = getImage(self.zona3, "src\data\dvan.png",(90,90))
                transporte.grid(row=0, column=1, padx=10, pady=5)
                
                b1 = getBotonTemp(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                pass

            def showServicios(nextRow, boleto):
                if len(boleto.serviciosContratados) != 0:
                    data = {f"Servicio #{i+1}": servicio for i, servicio in enumerate(boleto.serviciosContratados)}
                else:
                    data = {"Servicios": "No hay servicios contratados para el boleto de momento"}

                resultFrame = ResultFrame(
                    "Servicios contratados",
                    data,
                    self.zona3
                )
                
                b1 = getBotonTemp(resultFrame.marco, lambda: self.cancel(), resultFrame.nextFreeRow, 1)
                pass
            
            # Servicios especiales:
            handlersServicios = {
                "Comida a la carta": servicioComida,
                "Viaje con mascota": servicioMascota,
                "Acompañante para menor de edad": servicioMenor,
                "Asistencia para pasajero con necesidades especiales": servicioAsistencia,
                "Transporte terrestre": servicioTransporte,
                "Ver servicios contratados": showServicios,
            }
            
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            # Dropdown de la opcion
            
            labelOpciones = tk.Label(self.zonaResult, text = "Seleccionar servicio",bg=color["pink"],font=("fixedsys",12))
            labelOpciones.grid(row=nextRow, column=0, padx=5, pady=5)
            self.zonaResult.grid_rowconfigure(nextRow, weight=1)
            self.zonaResult.grid_columnconfigure(0, weight=1)
            
            dropDownOpciones = ttk.Combobox(self.zonaResult, state = "readonly", values = [
                "Comida a la carta", "Viaje con mascota", "Acompañante para menor de edad",
                "Asistencia para pasajero con necesidades especiales", "Transporte terrestre",
                "Ver servicios contratados"
            ],font="fixedsys")
            
            
            dropDownOpciones.grid(row=nextRow, column=1, padx=15, pady=15)
            dropDownOpciones.bind("<<ComboboxSelected>>", lambda e: tempHandler(dropDownOpciones.get(), nextRow+1, boleto))
            self.zonaResult.grid_rowconfigure(nextRow, weight=1)
            self.zonaResult.grid_columnconfigure(1, weight=1)
            pass
        
        handlersCheckIn = {
            "Mejorar asiento": mejoraSilla,
            "Comprar servicios especiales": comprarServicios,
        }
        pass
    
class GestionUsuario(VentanaBaseFuncionalidad):
        
    def ventanaHistorial(self):
        self.clearZone()
        
        resultFrame = ResultFrame(
            "Historial de vuelos",
            {f"Vuelo #{i+1}" : boleto.getStr() for i, boleto in enumerate(user.historial)},
            self.zonaForm
        )
        nextFreeRow = resultFrame.nextFreeRow
        
        boton = tk.Button(resultFrame.marco, text="Volver",bg=color["blue"],font=("fixedsys",12),relief="groove",fg=color["darkblue"], command = lambda: self.ventana1())
        boton.grid(row=nextFreeRow, column=0, padx=5, pady=5)
        
        frame2 = tk.Frame(self.zonaForm, bg=color["pink"], highlightbackground="#9656B6",highlightthickness=2)
        frame2.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        def handleBuscarVuelo(formData):
            try:
                index = int(formData["Numero del vuelo"])
                if (index-1 >= 0) and (index-1 <= len(user.historial)-1):
                    self.clearZone()
                    resultFrame = ResultFrame(
                        "Detalles del boleto",
                        user.historial[index-1].getInfo(),
                        self.zonaForm
                    )
                    volver = getBotonTemp(resultFrame.marco, lambda: self.cancel(), resultFrame.nextFreeRow, 0)
                else:
                    raise ErrorBusquedaInvalida()
            except:
                alertWarn("Error", "Error, numero de vuelo invalido, no se encontraron resultados para la busqueda")
            pass
        
        FieldFrame("Buscar vuelo", ["Numero del vuelo"], "Numero del vuelo", None, None, frame2, callback= handleBuscarVuelo)
        pass
    
    def ventanaDepositar(self, valor):
        try:
            valor = float(valor)
            if valor >= 0:
                user.depositarDinero(valor)
                alertInfo("Deposito realizado con exito", f"Se ha agregado ${valor} a tu cuenta, nuevo saldo: {user.dinero}")    
                self.cancel()
            else:
                raise ErrorDepositoInvalido()
        except:
            alertWarn("Error", "Error, valor de deposito invalido")
        pass
    
    def ventana1(self):
        self.clearZone()
        
        infoCuenta = ResultFrame(
            "Informacion de la cuenta",
            user.getInfo(),
            self.zonaForm
        )
        nextFreeRow = infoCuenta.nextFreeRow
        
        separador = getSeparador(infoCuenta.marco, nextFreeRow, 2, 5)
        
        #..........................................
        # Seccion depositar dinero
        labelDepositar = tk.Label(infoCuenta.marco, text="Depositar",font=("fixedsys",12),bg="#E1BEFF")
        labelDepositar.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)
        
        inputDepositar = tk.Entry(infoCuenta.marco)
        inputDepositar.grid(row=nextFreeRow+1, column=1, padx=5, pady=5)
        
        # Depositar dinero
        botonDespositar = tk.Button(infoCuenta.marco, text="Depositar dinero",bg="#EBD3FF",font=("fixedsys",12),relief="groove",fg="#7A37B3", command = lambda: self.ventanaDepositar((inputDepositar.get())))
        botonDespositar.grid(row=nextFreeRow+2, column=1, padx=5, pady=5) 
        #..........................................
        
        sep2 = getSeparador(infoCuenta.marco, nextFreeRow+3, 2, 5)
        
        # Ver historial de vuelos
        botonHistorial = tk.Button(infoCuenta.marco, text="Ver historial de vuelos",bg=color["blue"],font=("fixedsys",12),relief="groove",fg=color["darkblue"], command = self.ventanaHistorial)
        botonHistorial.grid(row=nextFreeRow+4, column=0, padx=5, pady=5)
        
        # Canjear Millas
        botonCanjearMillas = tk.Button(infoCuenta.marco, text="Canjear millas",bg=color["blue"],font=("fixedsys",12),relief="groove",fg=color["darkblue"],command = self.ventanaCanjearMillas)
        botonCanjearMillas.grid(row=nextFreeRow+4, column=1, padx=5, pady=5)    
        pass
    
    def ventanaCanjearMillas(self):
        self.clearZone()
        
        # Mostrar millas disponibles
        infoMillas = ResultFrame(
            "Informacion de la Cuenta:",
            {"Millas disponibles": user.millas},
            self.zonaForm
        )
        nextFreeRow = infoMillas.nextFreeRow
        
        # Dropdown de la opcion
        labelOpciones = tk.Label(infoMillas.marco, text = "Seleccionar opcion",bg=color["pink"],font=("fixedsys",12))
        labelOpciones.grid(row=nextFreeRow, column=0, padx=5, pady=5)            
        dropDownOpciones = ttk.Combobox(infoMillas.marco, state = "readonly", values = [
            "Mejora de silla", "Descuento vuelo",
            "Descuento maleta", "Ver descuentos del usuario"
        ],font="fixedsys")
        
        nextRow = nextFreeRow + 2
        dropDownOpciones.grid(row=nextFreeRow, column=1, padx=15, pady=15)
        dropDownOpciones.bind("<<ComboboxSelected>>", lambda e: handlersMillas[dropDownOpciones.get()](nextRow))
        
        separador = getSeparador(infoMillas.marco, nextFreeRow + 1, 2)
        
        self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
        self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # . . . Menu . . .
        
        #getBotonCancelar(self.zonaForm, lambda: self.cancel(), 1, 0)
        #getBotonContinuar(self.zonaForm, lambda: 1, 1, 1)
        
        # HandlersMillas
        
        def mejoraSilla(nextRow):
            
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            def selecAsientos():
                dropDownAsiento["values"] = [
                    asiento
                    for asiento in ((user.getHistorial())[dropDownBoleto.current()]).vuelo.asientos
                    if asiento.tipo == "Vip"
                ]
                pass
            
            def confirmar(boleto, asiento):
                descuento = upgradeAsiento(asiento)
                ok = alertConfirmacion(f"Acepta para canjear {descuento.getCostoMillas()} millas por una mejora de asiento?.")
                
                if ok:
                    if (boleto.tipo == "Vip"):
                        alertWarn("Error", "Error, el boleto ya es de tipo VIP, no se puede mejorar mas")
                    else:
                        try:
                            if (user.verificarMillas(descuento.getCostoMillas())):
                                ahorrado = user.canjearMillas(boleto, descuento)
                                alertInfo("Millas canjeadas con exito", f"Se han descontado {descuento.getCostoMillas()} millas de su cuenta, y se ha realizado una mejora de asiento a su boleto! Felicidades!")
                                self.cancel()
                                pass
                            else:
                                raise ErrorMillasInsuficientes()
                        except ErrorMillasInsuficientes:
                            alertWarn("Error", "No tiene suficientes millas para canjear por una mejora de asiento")
                pass
            
            labelBoleto = tk.Label(self.zonaResult, text = "Seleccionar boleto",font=("fixedsys",12),bg=color["pink"])
            labelBoleto.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownBoleto = ttk.Combobox(self.zonaResult, state = "readonly", values = [boleto.getStr() for boleto in user.getHistorial()],font="fixedsys")
            dropDownBoleto.grid(row=nextRow, column=1, padx=15, pady=15)
            dropDownBoleto.bind("<<ComboboxSelected>>", lambda e: selecAsientos())
        
            labelAsiento = tk.Label(self.zonaResult, text = "Seleccionar asiento",font=("fixedsys",12),bg=color["pink"])
            labelAsiento.grid(row=nextRow+1, column=0, padx=5, pady=5)
            dropDownAsiento = ttk.Combobox(self.zonaResult, state = "readonly", values = ((user.getHistorial())[0]).vuelo.asientos,font="fixedsys")
            dropDownAsiento.grid(row=nextRow+1, column=1, padx=15, pady=15)

            b1 = getBotonCancelar(self.zonaResult, lambda: self.cancel(), nextRow+2, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar(
                (user.getHistorial())[dropDownBoleto.current()],
                ((user.getHistorial())[dropDownBoleto.current()]).vuelo.asientos[dropDownAsiento.current()]
            ), nextRow+2, 1)
            pass

        def descuentoVueloVentana(nextRow):
                
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            def confirmar(boleto):
                descuento = descuentoVuelo()
                ok = alertConfirmacion(f"Acepta canjear {descuento.getCostoMillas()} millas por un descuento de vuelo?.")
                if ok:
                    try:
                        if (user.verificarMillas(descuento.getCostoMillas())):
                            ahorrado = user.canjearMillas(boleto, descuento)
                            alertInfo("Millas canjeadas con exito", f"Se han descontado {descuento.getCostoMillas()} millas de su cuenta por un descuento en el vuelo, y se ha reembolazado ${ahorrado} a su cuenta, felicidades!")
                            self.cancel()
                            pass
                        else: 
                            raise ErrorMillasInsuficientes()
                    
                    except ErrorMillasInsuficientes:
                        alertWarn("Error", "No tiene suficientes millas para canjear por un descuento de vuelo")
                
                pass

            labelBoleto = tk.Label(self.zonaResult, text = "Seleccionar vuelo",font=("fixedsys",12),bg=color["pink"])
            labelBoleto.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownBoleto = ttk.Combobox(self.zonaResult, state = "readonly", values = [boleto.getStr() for boleto in user.getHistorial()])
            dropDownBoleto.grid(row=nextRow, column=1, padx=15, pady=15)
            
            b1 = getBotonCancelar(self.zonaResult, lambda: self.cancel(), nextRow+1, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar((user.getHistorial())[dropDownBoleto.current()]), nextRow+1, 1)
            
            pass

        def descuentoMaletaVentana(nextRow):
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            def confirmar(boleto):
                descuento = descuentoMaleta()
                ok = alertConfirmacion(f"Acepta canjear {descuento.getCostoMillas()} millas por un descuento en el costo total de las maletas?.")
            
                if ok:
                    try:
                        if (user.verificarMillas(descuento.getCostoMillas())):
                            ahorrado = user.canjearMillas(boleto, descuento)
                            alertInfo("Millas canjeadas con exito", f"Se han descontado {descuento.getCostoMillas()} millas de su cuenta, y se ha realizado un descuento de ${ahorrado} a su boleto, dinero reembolsado a su cuenta.")
                            self.cancel()
                            pass
                        else:
                            raise ErrorMillasInsuficientes()
                    except ErrorMillasInsuficientes:
                        alertWarn("Error", "No tiene suficientes millas para canjear por un descuento de maleta")
                pass

            
            labelBoleto = tk.Label(self.zonaResult, text = "Seleccionar vuelo",font=("fixedsys",12),bg=color["pink"])
            labelBoleto.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownBoleto = ttk.Combobox(self.zonaResult, state = "readonly", values = [boleto.getStr() for boleto in user.getHistorial()])
            dropDownBoleto.grid(row=nextRow, column=1, padx=15, pady=15)
            
            b1 = getBotonCancelar(self.zonaResult, lambda: self.cancel(), nextRow+1, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar((user.getHistorial())[dropDownBoleto.current()]), nextRow+1, 1)
            pass

        def showDescuento(nextRow):
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg=color["pink"],highlightbackground="#9656B6",highlightthickness=2)
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            resultFrame = ResultFrame(
                "Descuentos del usuario",
                {f"Descuento #{i+1}" : descuento for i, descuento in enumerate(user.descuentos)},
                self.zonaResult
            )
            pass

        handlersMillas = {
            "Mejora de silla": mejoraSilla,
            "Descuento vuelo": descuentoVueloVentana,
            "Descuento maleta": descuentoMaletaVentana,
            "Ver descuentos del usuario": showDescuento
        }
        
        # Handlers continuar    
        pass
    



ventanaInicial = VentanaInicial()
ventanaInicial.generar()

App.mainloop()
serializarUsuario(user)
exit()