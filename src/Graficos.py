import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from uiMain.appMisc.misc import *

# ------------------------------------
# Backend (TEMPORAL)

from gestorAplicacion.Aerolinea.Boleto import Boleto
from gestorAplicacion.Aerolinea.Maleta import Maleta
from gestorAplicacion.Aerolinea.Vuelo import Vuelo
from gestorAplicacion.Cuenta.Usuario import Usuario
from baseDatos.Serializador import *

# ------------------------------------

def createMainUser():
    mainUser = Usuario("Largod </>", "largod@unal.edu.co", 5000)
    
    baseData = [
        { "Origen": "Medellin", "Destino": "Codazzi",   "Maletas": 2, "Vuelo": 2, "Asiento": 3 },
        { "Origen": "Bogota",   "Destino": "Venezuela", "Maletas": 1, "Vuelo": 3, "Asiento": 4 },
        { "Origen": "de Mal",   "Destino": "a Peor",    "Maletas": 0, "Vuelo": 4, "Asiento": 5 },
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
App.title("Ventana de Inicio")
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
    
    "Salir" : lambda: exitHandler(user)
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
        marco = tk.Frame(parent, bg="green", borderwidth=1, relief="solid")
        marco.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        #Agregar el titulo de los criterios
        elementoTituloCriterio = tk.Label(marco, text=tituloCriterio)
        elementoTituloCriterio.grid(row=0, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)


        #Agregar el titulo de los valores
        elementoTituloValores = tk.Label(marco, text=tituloValores)
        elementoTituloValores.grid(row=0, column=1, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(1, weight=1)

        #Por cada criterio agregarlos y sus respectivas entradas
        for index, criterio in enumerate(criterios):
        
            #Crea el criterio y su valor y lo guarda
            elementoCriterio = tk.Label(marco, text=criterio)
            elementoCriterio.grid(row=index+1, column=0, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(0, weight=1)

            elementoInput = tk.Entry(marco)
            elementoInput.grid(row=index+1, column=1, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(1, weight=1)

            self.data[criterio] = {
                "elementos" : (elementoCriterio, elementoInput),
                "value" : None, 
            }

        
        submitButton = tk.Button(marco, text="Enviar", bg="white", borderwidth=0, command = lambda: self.submitForm(callback))
        submitButton.grid(row=index+2, column=1, padx=5, pady=5)
        marco.grid_rowconfigure(index+2, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        clearButton = tk.Button(marco, text="Clear", bg="white", borderwidth=0, command = lambda: self.clear())
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
        return self.data[criterio]["value"]

    def submitForm(self, callback):
        for criterio in self.criterios:
            value = (self.data[criterio]["elementos"][1]).get()
            self.data[criterio]["value"] = value
            self.formData[criterio] = value
            if value == "":
                alertWarn("Campos sin llenar", "Error, por favor llene todos los campos antes de continuar:3")
                return False
            
        if callback != None:
            callback(self.formData)
        
        

    def clear(self):
        #Limpiar todos los datos
        for criterio in self.criterios:
            (self.data[criterio]["elementos"][1]).delete(0 ,'end')
    
    
    def delete(self):
        self.marco.destroy()
        pass

class ResultFrame(tk.Frame):

    def __init__(self, tituloResultados, datos, parent):
        
        #Inicializar el diccionario que guardara los datos
        self.parent = parent
        
        #Crea el marco donde van a estar los elementos
        marco = tk.Frame(parent, bg="green", borderwidth=1, relief="solid")
        marco.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        #Agregar el titulo de los criterios
        elementoTituloResultados = tk.Label(marco, text=tituloResultados)
        elementoTituloResultados.grid(row=0, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        #Por cada criterio agregarlos y sus respectivas entradas
        for index, key in enumerate(datos.keys()):
        
            #Crea el criterio y su valor y lo guarda
            elementoKey = tk.Label(marco, text=key)
            elementoKey.grid(row=index+1, column=0, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(0, weight=1)

            elementoValue = tk.Label(marco, text=datos[key])
            elementoValue.grid(row=index+1, column=1, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(1, weight=1)

        self.nextFreeRow = index + 2
        self.marco = marco
        pass
    
    def delete(self):
        self.marco.destroy()
        pass

class ResultFrameSimple(tk.Frame):

    def __init__(self, titulo, resultados, parent):
        
        #Inicializar el diccionario que guardara los datos
        self.parent = parent
        self.titulo = titulo
        self.resultados = resultados
        self.resultadosElements = []
        #Crea el marco donde van a estar los elementos
        marco = tk.Frame(parent, bg="green", borderwidth=1, relief="solid")
        marco.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        #Agregar el titulo de los criterios
        elementoTituloResultados = tk.Label(marco, text=titulo)
        elementoTituloResultados.grid(row=0, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)


        """#Agregar el titulo de los valores
        elementoTituloValores = tk.Label(marco, text=tituloValores)
        elementoTituloValores.grid(row=0, column=1, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(1, weight=1)
        """
        
        #Por cada criterio agregarlos y sus respectivas entradas
        for index, resultado in enumerate(resultados):
            #Crea el criterio y su valor y lo guarda
            elementoResultado = tk.Label(marco, text=resultado)
            elementoResultado.grid(row=index+1, column=0, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(0, weight=1)
            self.resultadosElements.append(elementoResultado)
            
        pass

class ProcesoConsulta:
    def __init__(self, zona, nombre, descripcion, criterios):
        self.zona = zona
        self.nombre = nombre
        self.descripcion = descripcion
        
        self.criterios = criterios
        pass

    def generar(self):
        zonaInfo = tk.Frame(self.zona, bg="yellow", borderwidth=1, relief="solid")
        zonaInfo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(0, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)

        self.zonaForm = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)

        nombreProceso = tk.Label(zonaInfo, text= self.nombre)
        nombreProceso.grid(row=0, column=0, padx=5, pady=5)
        zonaInfo.grid_rowconfigure(0, weight=1)
        zonaInfo.grid_columnconfigure(0, weight=1)

        descripcionProceso = tk.Label(zonaInfo, text= self.descripcion)
        descripcionProceso.grid(row=1, column=0, padx=5, pady=5)
        zonaInfo.grid_rowconfigure(1, weight=1)
        zonaInfo.grid_columnconfigure(0, weight=1)

        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, self.zonaForm)

class MainMenu:
    def __init__(self):
        pass

    def generar(self):
        frame_grande = tk.Frame(App, bg="blue")
        frame_grande.grid(row=0, column=0, sticky="nsew")
        App.grid_rowconfigure(0, weight=1)
        App.grid_columnconfigure(0, weight=1)

        nombre_aplicacion = tk.Label(frame_grande, text="Nombre aplicacion",fg="red")
        nombre_aplicacion.grid(row=0,column=0,padx=5, pady=5,sticky="nw")

        marco = tk.Frame(frame_grande, bg="green", borderwidth=1, relief="solid")
        marco.grid(row=1, column=0, sticky="nsew", padx=5, pady=10)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(0, weight=1)

        zonaSuperior = tk.Frame(marco, bg="yellow", borderwidth=1, relief="solid")
        zonaSuperior.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)
        
        # ----------------------------------------------
        archivoSelec = tk.StringVar(zonaSuperior) 
        archivoSelec.set("Archivo") 

        archivoButton = tk.OptionMenu(zonaSuperior, archivoSelec, *["Aplicacion", "Salir"], command = lambda e : handlersProcesoConsulta[archivoSelec.get()]())
        archivoButton.grid(row=0, column=0, padx=5, pady=5)
        zonaSuperior.grid_rowconfigure(0, weight=1)
        zonaSuperior.grid_columnconfigure(0, weight=1)

        opciones = ["Comprar vuelo", "Reasignar Vuelo", "Cancelar Vuelo", "Check In", "Gestion usuario"]
        
        procesoSelec = tk.StringVar(zonaSuperior) 
        procesoSelec.set("Procesos y consultas") 

        listaProcesoConsulta = tk.OptionMenu(zonaSuperior, procesoSelec, *opciones, command = lambda e : handlersProcesoConsulta[procesoSelec.get()](self))
        listaProcesoConsulta.grid(row=0, column=1, padx=5, pady=5)
        zonaSuperior.grid_rowconfigure(0, weight=1)
        zonaSuperior.grid_columnconfigure(1, weight=1)

                
        ayudaButton = tk.Button(zonaSuperior, text="Ayuda")
        ayudaButton.grid(row=0, column=2, padx=5, pady=5)
        zonaSuperior.grid_rowconfigure(0, weight=1)
        zonaSuperior.grid_columnconfigure(2, weight=1)
        
        #Zona main --------------------
        zonaProceso = tk.Frame(marco, bg="orange", borderwidth=1, relief="solid")
        zonaProceso.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        marco.grid_rowconfigure(1, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        self.zona = zonaProceso
        
        # Ventana inicial del main menu
        InitMainMenu().generar(self, "Bievenido al sistema de vuelos, aqui podras ... bla bla bla", TEXT_DATA["breveDescripcionApp"])
        pass


class VentanaInicial:
    def __init__(self):
        pass

    def generar(self):
        frame_grande = tk.Frame(App, bg="#DAD8FF")
        frame_grande.grid(row=0, column=0, sticky="nsew")
        App.grid_rowconfigure(0, weight=1)
        App.grid_columnconfigure(0, weight=1)

        # Barra de menu        
        menuBar = tk.Menu(App)
        App.config(menu=menuBar)
        
        menuInicio = tk.Menu(menuBar, tearoff=False)
        menuBar.add_cascade(menu=menuInicio, label="Inicio")
    
        menuInicio.add_command( label="Salir", command = lambda: exitHandler(user) )
        menuInicio.add_command( label="Descripcion", command = lambda: p3Label.config(text = TEXT_DATA["breveDescripcionApp"]))

        # Diferentes paneles
        p1 = tk.Frame(frame_grande, bg="#E0B4E7", borderwidth=1, relief="flat")
        p1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(0, weight=1)
        self.p1 = p1
        
        p2 = tk.Frame(frame_grande, bg="#E0B4E7", borderwidth=1, relief="flat")
        p2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(1, weight=1)
        self.p2 = p2

        p3 = tk.Frame(p1, bg="#FFD8EC", borderwidth=1, highlightbackground="#9656B6",highlightthickness=2)
        p3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        #p1.grid_rowconfigure(0, weight=1)
        #p1.grid_columnconfigure(0, weight=1)
        self.p3 = p1
        
        p4 = tk.Frame(p1, bg="#FFD8EC", borderwidth=1,highlightbackground="#9656B6",highlightthickness=2)
        p4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        p1.grid_rowconfigure(1, weight=1)
        p1.grid_columnconfigure(0, weight=1)
        self.p4 = p4

        p5 = tk.Frame(p2, bg="#FFD8EC", borderwidth=1, highlightbackground="#9656B6",highlightthickness=2)
        p5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        p2.grid_rowconfigure(0, weight=1)
        p2.grid_columnconfigure(0, weight=1)
        self.p5 = p5

        p6 = tk.Frame(p2, bg="#FFD8EC", borderwidth=1, highlightbackground="#9656B6",highlightthickness=2)
        p6.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        #p2.grid_rowconfigure(1, weight=1)
        #p2.grid_columnconfigure(0, weight=1)
        self.p6 = p6
        #.............................

        # Corto saludo de bienvenida (P3)
        #monospace = tk.font.Font(family="monospace", size=12,file="src\imagenes\JetBrainsMono-Regular.ttf")
        p3Label = tk.Label(p3, text = TEXT_DATA["textoBienvenida"], anchor="w", justify="center", bg="#FFD8EC",fg="#5B2A73",font=("fixedsys",9))
        p3Label.grid(row=0,column=0,padx=5, pady=5, sticky="nsew")
        p3.grid_rowconfigure(0, weight=0)
        p3.grid_columnconfigure(0, weight=0)

        # Ingreso al sistema  y seccion de imagenes (P4)
        marcoImagenes = tk.Frame(p4)
        marcoImagenes.grid(row=0,column=0,padx=10,pady=10)
        p4.grid_rowconfigure(0,weight=1)
        p4.grid_columnconfigure(0,weight=1)
        
        # Lista de nombres de archivos de imágenes
        
        global indexImg
        indexImg = 0
        
        #sistemaPaths = [f"src\imagenes\ImagenesSistema\{i}.png" for i in range(1, maximo+1)]
        sistemaPaths = [ "src/imagenes/imagenS1.png", "src/imagenes/imagen1-1.png"]
        
        fotos = [
            ImageTk.PhotoImage(Image.open(path).resize((700, 550)))
            for path in sistemaPaths
        ]
        
        etiqueta = tk.Label(marcoImagenes, image=fotos[0],highlightbackground="#DAD8FF",highlightthickness=4)
        etiqueta.grid(row=0, column=0)    
        etiqueta.bind("<Enter>", lambda event: changeImage())
    
        def changeImage():
            global indexImg
            indexImg = 0 if indexImg == (len(fotos)-1) else indexImg + 1
            etiqueta.configure(image=fotos[indexImg])
        
        botonIngreso = tk.Button(p4,text="Ingreso al sistema",bg="#DAD8FF",font=("fixedsys",12),relief="groove",fg="#7768D2",height="2",width="25")
        botonIngreso.grid(row=1,column=0,padx=10,pady=10,sticky="ws")
        #p4.grid_rowconfigure(0,weight=0)
        #p4.grid_columnconfigure(0,weight=0)
        botonIngreso.bind("<Button-1>", lambda e : MainMenu().generar())
        
        # - - - Seccion informacion y hojas de vida - - -
        
        
        # Guardar datos de hojas de vida
        hojasVida = {}
        for i in range(1, 6):
            hojasVida[str(i)] = open(f"src/imagenes/hojaVida{i}.txt","r").read()
        hojasVida["Indice"] = 1
        
        imagenes = {}
        for i in range(1, 5 + 1):
            imagenes[str(i)] = []
            for j in range(1, 5):
                # Falta unificar formato !!!!
                if i != 1:
                    imagenes[str(i)].append(f"src/imagenes/imagen{i}-{j}.jpeg")
                else:
                    imagenes[str(i)].append(f"src/imagenes/imagen{i}-{j}.png")
                    
        #Funcion para mostrar imagenes segun la persona
        def showImages(index):
            for i, path in enumerate(imagenes.get(index, [])):
                img = getImage(p6, path, (220, 220),highlightbackground="#FFA7EE",highlightthickness=3)
                img.grid(row= (i//2), column=(i%2), padx=10, pady=10,sticky="nsew")
                
        #Definir funcion hojas vida
        def cambioHojaVida(index):
            if index == 5:
                hojasVida["Indice"] = 1
                #imagenes["imagenIndex"]=1
            else:
                hojasVida["Indice"] +=1
                #imagenes["imagenIndex"]+=1
            
            hojaVidaLabel.config(text=hojasVida[str(hojasVida["Indice"])])
            showImages(str(hojasVida["Indice"]))
            pass
        
        hojaVidaLabel = tk.Label(p5, text="", font=("fixedsys",12),bg="#FFD8EC",fg="#5B2A73")
        hojaVidaLabel.grid(row=0,column=0, padx=5, pady=5)
        hojaVidaLabel.bind("<Button-1>", lambda e: cambioHojaVida(hojasVida["Indice"]))
        cambioHojaVida(hojasVida["Indice"])
        pass


class VentanaBaseFuncionalidad(tk.Frame):
    
    def generar(self, mainMenu, nombre, descripcion):
        self.mainMenu = mainMenu
        self.zona = mainMenu.zona
        self.nombre = nombre
        self.descripcion = descripcion
        
        self.zonaInfo = tk.Frame(self.zona, bg="yellow", borderwidth=1, relief="solid")
        self.zonaInfo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(0, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)
        
        self.nombreProceso = tk.Label(self.zonaInfo, text= self.nombre)
        self.nombreProceso.grid(row=0, column=0, padx=5, pady=5)
        self.zonaInfo.grid_rowconfigure(0, weight=1)
        self.zonaInfo.grid_columnconfigure(0, weight=1)
        
        self.descripcionProceso = tk.Label(self.zonaInfo, text= self.descripcion)
        self.descripcionProceso.grid(row=1, column=0, padx=5, pady=5)
        self.zonaInfo.grid_rowconfigure(1, weight=1)
        self.zonaInfo.grid_columnconfigure(0, weight=1)
        
        self.zonaForm = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)
        
        self.ventana1()
        pass
    
    def showSelectHistorial(self, callback):
        historialBoletos = user.getHistorial()
        
        infoVuelos = ResultFrame(
            "Historial de vuelos",
            {f"Boleto #{i+1}" : boleto.getStr() for i, boleto in enumerate(historialBoletos) },
            self.zonaForm
        )
        nextFreeRow = infoVuelos.nextFreeRow

        separador = getSeparador(infoVuelos.marco, nextFreeRow, 2, 5)
        
        labelVuelo = tk.Label(infoVuelos.marco, text = "Vuelo:")
        labelVuelo.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)
        dropDownVuelos = ttk.Combobox(infoVuelos.marco,state = "readonly", values = [f"Boleto #{i+1}" for i in range(len(historialBoletos))] )
        dropDownVuelos.grid(row=nextFreeRow+1, column=1, padx=15, pady=15)
        
        getBotonCancelar(infoVuelos.marco, lambda: self.cancel(), nextFreeRow+2, 0)
        
        # Manda el index del boleto en el historial
        getBotonContinuar(infoVuelos.marco, lambda: callback(dropDownVuelos.current()), nextFreeRow+2, 1)
        pass
        
    
    def cancel(self):
        self.clearZone()
        self.ventana1()
        pass
    
    def clearZone(self):    
        self.zonaForm.destroy()
        self.zonaForm = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)
        pass

class InitMainMenu(VentanaBaseFuncionalidad):
    def ventana1(self):
        info = [
            "Como usar la aplicacion?",
            "Texto de como usar la aplicacion",
            "Que se puede hacer?",
            "Texto de que se puede hacer"
        ]
        labels = [
            tk.Label(self.zonaForm, text = texto, anchor="w", justify="left")
            .grid(row=row, column=0, padx=5, pady=5)
            for row, texto in enumerate(info)
        ]
        pass
    pass

class ComprarVuelo(VentanaBaseFuncionalidad):
    
    def ventana1(self):
        
        def callback(formData):
            
            vuelos = Vuelo.generarVuelos(5, formData[criterios[0]], formData[criterios[1]]) #Genera los vuelos 
            asientos = (vuelos[0]).generarAsientos(3, 5, 100) # Genera los asientos del primer vuelo
            
            def selecAsientos(event):
                vuelo = vuelos[dropDownVuelos.current()] # selecciona el vuelo seleccionado
                asientos = vuelo.generarAsientos(3, 5, 100) # Genera los asientos del vuelo
                dropDownAsientos["values"] = asientos # Muestralos asientos del vuelo seleccionado
                pass
            
            separador = getSeparador(formElement.marco, nextFreeRow, 2, 5) # Separador generico
            
            # Seleccionar vuelo y asiento
            labelVuelo = tk.Label(formElement.marco, text = "Vuelo:") 
            labelVuelo.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)            
            dropDownVuelos = ttk.Combobox(formElement.marco,state = "readonly", values = vuelos )
            dropDownVuelos.grid(row=nextFreeRow+1, column=1, padx=15, pady=15)
            dropDownVuelos.bind("<<ComboboxSelected>>", selecAsientos)
            
            labelAsiento = tk.Label(formElement.marco, text = "Asiento:")
            labelAsiento.grid(row=nextFreeRow+2, column=0, padx=5, pady=5)
            dropDownAsientos = ttk.Combobox(formElement.marco,state = "readonly",values = asientos )
            dropDownAsientos.grid(row=nextFreeRow+2, column=1, padx=15, pady=15)
            
            labelMaletas = tk.Label(formElement.marco, text = "Cantidad de maletas:")
            labelMaletas.grid(row=nextFreeRow+3, column=0, padx=5, pady=5)
            dropDownMaletas = ttk.Combobox(formElement.marco,state = "readonly",values = [0, 1, 2, 3, 4])
            dropDownMaletas.grid(row=nextFreeRow+3, column=1, padx=15, pady=15)

            # Crea boton de siguiente y uno de cancelar  
            getBotonCancelar(formElement.marco, lambda: self.cancel(), nextFreeRow+4, 0)
            getBotonContinuar(formElement.marco, lambda: self.ventana2(
                {
                    "vuelo": vuelos[dropDownVuelos.current()],
                    "asiento": asientos[dropDownAsientos.current()],
                    "maletas": int(dropDownMaletas.current()),
                }, formData # Origen, destino
            ),nextFreeRow+4, 1)
            
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
            
            separador = getSeparador(formElement.marco, nextFreeRow, 2, 5)
            
            # Crea boton de siguiente y uno de cancelar  
            getBotonCancelar(formElement.marco, lambda: self.cancel(), nextFreeRow+1, 0)
            getBotonContinuar(formElement.marco, lambda: self.ventana3(boleto), nextFreeRow+1, 1)
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
            
            if (user.dinero >= boleto.valor):
                user.comprarBoleto(boleto)
                alertInfo("Compra exitosa", "Boleto comprado con exito!, gracias por usar nuestra aplicacion.")
                self.cancel()
            else:
                alertWarn("Dinero Insuficiente", "Error, dinero insuficiente en la cuenta, compra cancelada")
                self.cancel()
                pass
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
        labelVuelo = tk.Label(vuelosDisponibles.marco, text = "Vuelo:")
        labelVuelo.grid(row=nextFreeRow, column=0, padx=5, pady=5)
        dropDownVuelos = ttk.Combobox(vuelosDisponibles.marco,state = "readonly", values = [f"Vuelo #{i+1}" for i in range(len(vuelos))] )
        dropDownVuelos.grid(row=nextFreeRow, column=1, padx=15, pady=15)
        dropDownVuelos.bind("<<ComboboxSelected>>", selecAsientos)
        
        labelAsiento = tk.Label(vuelosDisponibles.marco, text = "Asiento:")
        labelAsiento.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)
        dropDownAsientos = ttk.Combobox(vuelosDisponibles.marco,state = "readonly",values = asientos )
        dropDownAsientos.grid(row=nextFreeRow + 1, column=1, padx=15, pady=15)
        
        labelMaletas = tk.Label(vuelosDisponibles.marco, text = "Cantidad de maletas:")
        labelMaletas.grid(row=nextFreeRow+2, column=0, padx=5, pady=5)
        dropDownMaletas = ttk.Combobox(vuelosDisponibles.marco,state = "readonly",values = [0, 1, 2, 3, 4])
        dropDownMaletas.grid(row=nextFreeRow+2, column=1, padx=15, pady=15)
        
        # Crea boton de siguiente y uno de cancelar  
        getBotonCancelar(vuelosDisponibles.marco, lambda: self.cancel(), nextFreeRow+3, 0)
        getBotonContinuar(vuelosDisponibles.marco, lambda: self.ventana4(
            {
                "vuelo": vuelos[dropDownVuelos.current()],
                "asiento": asientos[dropDownAsientos.current()],
                "maletas": int(dropDownMaletas.current()),
                "indexBoleto": indexBoleto,
            }, {"Origen": boleto.origen, "Destino": boleto.destino} # Origen, destino, cantidad maletas
        ),nextFreeRow+3, 1)
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
            
            if (user.dinero >= valorReasignacion):
                user.reasignarBoleto(newBoleto, indexBoleto)
                
                alertInfo("Compra exitosa", "Boleto reasginado con exito, gracias por su atencion")
                self.cancel()
            else:
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
                alertConfirmacion("El boleto seleccionado ya tiene check in, pasando al menu de servicios")
                self.ventanaServicios(boleto)

            else:
                if boleto.status == "Cancelado":
                    alertWarn("Error", "El boleto es un boleto cancelado, no se puede hacer Check In")
                    self.cancel()
                else: 
                    # SI no tiene check se pide la verificacion para hacer check in, y se pasa a los servicios
                    ok = alertConfirmacion("El boleto seleccionado aun no tiene check in, desea confirmar el check in?")
                    if ok:
                        boleto.status = "Confirmado"
                        boleto.setCheckInRealizado = True
                        
                        # Backend check In
                        alertInfo("Check In", "Check In realizado con exito")
                        self.ventanaServicios(boleto)

    def ventanaServicios(self, boleto):
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
        labelOpciones = tk.Label(infoServicios.marco, text = "Seleccionar opcion")
        labelOpciones.grid(row=nextFreeRow, column=0, padx=5, pady=5)            
        dropDownOpciones = ttk.Combobox(infoServicios.marco, state = "readonly", values = [
            "Mejorar asiento", "Comprar servicios especiales"
        ])
        
        nextRow = nextFreeRow + 2
        dropDownOpciones.grid(row=nextFreeRow, column=1, padx=15, pady=15)
        dropDownOpciones.bind("<<ComboboxSelected>>", lambda e: handlersCheckIn[dropDownOpciones.get()](nextRow, boleto))
        
        separador = getSeparador(infoServicios.marco, nextFreeRow + 1, 2)

        self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
        self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)


        def mejoraSilla(nextRow, boleto):
            
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            def confirmar(asiento):
                pass
            
            labelAsiento = tk.Label(self.zonaResult, text = "Seleccionar nuevo asiento")
            labelAsiento.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownAsiento = ttk.Combobox(self.zonaResult, state = "readonly", values = boleto.vuelo.asientos)
            dropDownAsiento.grid(row=nextRow, column=1, padx=15, pady=15)

            b1 = getBotonCancelar(self.zonaResult, lambda: self.cancel(), nextRow+1, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar(
                boleto.vuelo.asientos[dropDownAsiento.current()]
            ), nextRow+1, 1)
            
            pass
        
        
        def comprarServicios(nextRow, boleto):
            self.zona3 = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
            self.zona3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
             
            def tempHandler(key, row, boleto):
                self.zona3.destroy()
                self.zona3 = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
                self.zona3.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
                handlersServicios[key](0, boleto)
                
            def servicioComida(nextRow, boleto):
                def confirmar(boleto):
                    pass
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de comprar comida tiene un costo de $1")
                labelAviso.grid(row=nextRow, column=0, padx=5, pady=5)
                
                labelDescripcion = tk.Label(self.zona3, text = "Descripcion del servicio...")
                labelDescripcion.grid(row=nextRow, column=1, padx=5, pady=5)
                
                b1 = getBotonCancelar(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                
                pass

            def servicioMascota(nextRow, boleto):
                
                def callback(data):
                    pass
                
            
                formMascota = FieldFrame(
                    "Datos mascota",
                    ["Nombre", "Raza", "Peso", "Perro/Gato"],
                    "Datos",
                    None, None, self.zona3,
                    callback=None
                )

                
                # Perro/Gato, Nombre, Peso
                
                pass

            def servicioMenor(nextRow, boleto):
                def confirmar(boleto):
                    pass
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de comprar comida tiene un costo de $1")
                labelAviso.grid(row=nextRow, column=0, padx=5, pady=5)
                
                labelDescripcion = tk.Label(self.zona3, text = "Descripcion del servicio...")
                labelDescripcion.grid(row=nextRow, column=1, padx=5, pady=5)
                
                b1 = getBotonCancelar(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                pass

            def servicioAsistencia(nextRow, boleto):
                def confirmar(boleto):
                    pass
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de comprar comida tiene un costo de $1")
                labelAviso.grid(row=nextRow, column=0, padx=5, pady=5)
                
                labelDescripcion = tk.Label(self.zona3, text = "Descripcion del servicio...")
                labelDescripcion.grid(row=nextRow, column=1, padx=5, pady=5)
                
                b1 = getBotonCancelar(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                pass

            def servicioTransporte(nextRow, boleto):
                def confirmar(boleto):
                    pass
                
                labelAviso = tk.Label(self.zona3, text = "El servicio de comprar comida tiene un costo de $1")
                labelAviso.grid(row=nextRow, column=0, padx=5, pady=5)
                
                labelDescripcion = tk.Label(self.zona3, text = "Descripcion del servicio...")
                labelDescripcion.grid(row=nextRow, column=1, padx=5, pady=5)
                
                b1 = getBotonCancelar(self.zona3, lambda: self.cancel(), nextRow+1, 0)
                b2 = getBotonContinuar(self.zona3, lambda: confirmar(boleto), nextRow+1, 1)
                pass

            def showServicios(nextRow, boleto):
                resultFrame = ResultFrame(
                    "Servicios contratados",
                    {f"Servicio #{i}": servicio for i, servicio in enumerate(boleto.serviciosContratados)},
                    self.zona3
                )
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
            self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            def confirmar():
                pass

            # Dropdown de la opcion
            
            labelOpciones = tk.Label(self.zonaResult, text = "Seleccionar servicio")
            labelOpciones.grid(row=nextRow, column=0, padx=5, pady=5)
            self.zonaResult.grid_rowconfigure(nextRow, weight=1)
            self.zonaResult.grid_columnconfigure(0, weight=1)
            
            dropDownOpciones = ttk.Combobox(self.zonaResult, state = "readonly", values = [
                "Comida a la carta", "Viaje con mascota", "Acompañante para menor de edad",
                "Asistencia para pasajero con necesidades especiales", "Transporte terrestre",
                "Ver servicios contratados"
            ])
            
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
        
        boton = tk.Button(resultFrame.marco, text="Volver", bg="white", borderwidth=0, command = lambda: self.ventana1())
        boton.grid(row=nextFreeRow, column=0, padx=5, pady=5)
        pass
    
    def ventanaDepositar(self, valor):
        user.depositarDinero(valor)
        alertInfo("Deposito realizado con exito", f"Se ha agregado ${valor} a tu cuenta, nuevo saldo: {user.dinero}")
        self.cancel()
        pass
    
    
    def ventana1(self):
        self.clearZone()
        
        infoCuenta = ResultFrame(
            "Detalles del boleto",
            user.getInfo(),
            self.zonaForm
        )
        nextFreeRow = infoCuenta.nextFreeRow
        
        separador = getSeparador(infoCuenta.marco, nextFreeRow, 2, 5)
        
        #..........................................
        # Seccion depositar dinero
        labelDepositar = tk.Label(infoCuenta.marco, text="Depositar")
        labelDepositar.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)
        
        inputDepositar = tk.Entry(infoCuenta.marco)
        inputDepositar.grid(row=nextFreeRow+1, column=1, padx=5, pady=5)
        
        # Depositar dinero
        botonDespositar = tk.Button(infoCuenta.marco, text="Depositar dinero", bg="white", borderwidth=0, command = lambda: self.ventanaDepositar(int(inputDepositar.get())))
        botonDespositar.grid(row=nextFreeRow+2, column=1, padx=5, pady=5) 
        #..........................................
        
        sep2 = getSeparador(infoCuenta.marco, nextFreeRow+3, 2, 5)
        
        # Ver historial de vuelos
        botonHistorial = tk.Button(infoCuenta.marco, text="Ver historial de vuelos", bg="white", borderwidth=0, command = self.ventanaHistorial)
        botonHistorial.grid(row=nextFreeRow+4, column=0, padx=5, pady=5)
        
        # Canjear Millas
        botonCanjearMillas = tk.Button(infoCuenta.marco, text="Canjear millas", bg="white", borderwidth=0, command = self.ventanaCanjearMillas)
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
        labelOpciones = tk.Label(infoMillas.marco, text = "Seleccionar opcion")
        labelOpciones.grid(row=nextFreeRow, column=0, padx=5, pady=5)            
        dropDownOpciones = ttk.Combobox(infoMillas.marco, state = "readonly", values = [
            "Mejora de silla", "Descuento vuelo",
            "Descuento maleta", "Ver descuentos del usuario"
        ])
        
        nextRow = nextFreeRow + 2
        dropDownOpciones.grid(row=nextFreeRow, column=1, padx=15, pady=15)
        dropDownOpciones.bind("<<ComboboxSelected>>", lambda e: handlersMillas[dropDownOpciones.get()](nextRow))
        
        separador = getSeparador(infoMillas.marco, nextFreeRow + 1, 2)
        
        self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
        self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # . . . Menu . . .
        
        #getBotonCancelar(self.zonaForm, lambda: self.cancel(), 1, 0)
        #getBotonContinuar(self.zonaForm, lambda: 1, 1, 1)
        
        # HandlersMillas
        
        def mejoraSilla(nextRow):
            
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            def selecAsientos():
                dropDownAsiento["values"] = ((user.getHistorial())[dropDownBoleto.current()]).vuelo.asientos
                pass
            
            def confirmar(boleto, newAsiento):
                pass
            
            labelBoleto = tk.Label(self.zonaResult, text = "Seleccionar vuelo")
            labelBoleto.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownBoleto = ttk.Combobox(self.zonaResult, state = "readonly", values = [boleto.getStr() for boleto in user.getHistorial()])
            dropDownBoleto.grid(row=nextRow, column=1, padx=15, pady=15)
            dropDownBoleto.bind("<<ComboboxSelected>>", lambda e: selecAsientos())
        
            labelAsiento = tk.Label(self.zonaResult, text = "Seleccionar asiento")
            labelAsiento.grid(row=nextRow+1, column=0, padx=5, pady=5)
            dropDownAsiento = ttk.Combobox(self.zonaResult, state = "readonly", values = ((user.getHistorial())[0]).vuelo.asientos)
            dropDownAsiento.grid(row=nextRow+1, column=1, padx=15, pady=15)

            b1 = getBotonCancelar(self.zonaResult, lambda: self.cancel(), nextRow+2, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar(
                (user.getHistorial())[dropDownBoleto.current()],
                ((user.getHistorial())[dropDownBoleto.current()]).vuelo.asientos[dropDownAsiento.current()]
            ), nextRow+2, 1)
            
            pass

        def descuentoVuelo(nextRow):
            
            #verificarMillas(user, upgradeAsiento.costoMillas) 
            #user.descontarMillas(upgradeAsiento.costoMillas)
            #f"Canjeado con éxito, millas restantes: {user.getMillas()}"
            #descuento = upgradeAsiento(user)
            #millasAsiento(user, descuento)
                
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            def confirmar(boleto):
                pass

            labelBoleto = tk.Label(self.zonaResult, text = "Seleccionar vuelo")
            labelBoleto.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownBoleto = ttk.Combobox(self.zonaResult, state = "readonly", values = [boleto.getStr() for boleto in user.getHistorial()])
            dropDownBoleto.grid(row=nextRow, column=1, padx=15, pady=15)
            
            b1 = getBotonCancelar(self.zonaResult, lambda: self.cancel(), nextRow+1, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar((user.getHistorial())[dropDownBoleto.current()]), nextRow+1, 1)
            
            pass

        def descuentoMaleta(nextRow):
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            def confirmar(boleto):
                pass
            
            labelBoleto = tk.Label(self.zonaResult, text = "Seleccionar vuelo")
            labelBoleto.grid(row=nextRow, column=0, padx=5, pady=5)
            dropDownBoleto = ttk.Combobox(self.zonaResult, state = "readonly", values = [boleto.getStr() for boleto in user.getHistorial()])
            dropDownBoleto.grid(row=nextRow, column=1, padx=15, pady=15)
            
            b1 = getBotonCancelar(self.zonaResult, lambda: self.cancel(), nextRow+1, 0)
            b2 = getBotonContinuar(self.zonaResult, lambda: confirmar((user.getHistorial())[dropDownBoleto.current()]), nextRow+1, 1)
            pass

        def showDescuento(nextRow):
            self.zonaResult.destroy()
            self.zonaResult = tk.Frame(self.zonaForm, bg="orange", borderwidth=1, relief="solid")
            self.zonaResult.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            resultFrame = ResultFrame(
                "Descuentos del usuario",
                {f"Descuento #{i}" : descuento for i, descuento in enumerate(user.descuentos)},
                self.zonaResult
            )
            pass

        handlersMillas = {
            "Mejora de silla": mejoraSilla,
            "Descuento vuelo": descuentoVuelo,
            "Descuento maleta": descuentoMaleta,
            "Ver descuentos del usuario": showDescuento
        }
        
        # Handlers continuar    
        pass
    



ventanaInicial = VentanaInicial()
ventanaInicial.generar()

App.mainloop()
