import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from uiMain.appMisc.misc import *

# Implementacion modular para el manejo de contenido en la apliaccion

App = tk.Tk()
App.title("Ventana de Inicio")
App.geometry("800x600")


"""
drowpDown = ttk.Combobox(
    state = "readonly",
    values=["Hola", "Largo"]
)"""



handlersProcesoConsulta = {
    "Comprar vuelo": lambda mainMenu: ComprarVuelo().generar(
        mainMenu.zona,
        "Comprar Vuelo",
        TEXT_DATA["descripcionComprarVuelo"],
        ["Origen", "Destino", "Numero Asiento"]
    ),
    
    "Reasignar Vuelo": lambda mainMenu: ReasignarVuelo().generar(
        mainMenu.zona,
        "Reasignar Vuelo",
        TEXT_DATA["descripcionReasignarVuelo"],
        ["ID del vuelo", "Pizza", "Secso"]
    ),
    
    "Cancelar Vuelo": lambda mainMenu: CancelarVuelo().generar(
        mainMenu.zona,
        "Cancelar Vuelo",
        TEXT_DATA["descripcionCancelarVuelo"],
        ["ID Vuelo", "Pizza", "Secso"]
    ),
    
    "Check In": lambda mainMenu: CheckIn().generar(
        mainMenu.zona,
        "Check In",
        TEXT_DATA["descripcionCheckIn"],
        ["Edad", "Pizza", "Secso"]
    ),
    
    "Gestion usuario": lambda mainMenu: GestionUsuario().generar(
        mainMenu.zona,
        "Gestion Usuario",
        TEXT_DATA["descripcionGestionUsuario"],
        ["Edad", "Pizza", "Secso"]
    ),
    
    "Salir" : exitHandler
}


#Implementar formulario generico
class FieldFrame(tk.Frame):
    """
    crea un nuevo objeto de tipo FieldFrame
    @arg tituloCriterios titulo para la columna "Criterio"
    @arg criterios array con los nombres de los criterios
    @arg tituloValores titulo para la columna "valor"
    @arg valores array con los valores iniciales; Si None, no hay valores iniciales
    @arg habilitado array con los campos no-editables por el usuario; Si None, todos son editables
    """

    def __init__(self, tituloCriterios, criterios, tituloValores, valores, habilitado, parent, callback = None):
        
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
        elementoTituloCriterio = tk.Label(marco, text=tituloCriterios)
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
        submitButton.grid(row=index+2, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(index+2, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        clearButton = tk.Button(marco, text="Clear", bg="white", borderwidth=0, command = lambda: self.clear())
        clearButton.grid(row=index+2, column=1, padx=5, pady=5)
        marco.grid_rowconfigure(index+2, weight=1)
        marco.grid_columnconfigure(1, weight=1)

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
        
        print(self.formData)
        if callback != None:
            callback(self.formData)
        
        

    def clear(self):
        #Limpiar todos los datos
        for criterio in self.criterios:
            (self.data[criterio]["elementos"][1]).delete(0 ,'end')
                

class ResultFrame(tk.Frame):

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
        pass

class VentanaInicial:
    def __init__(self):
        pass

    def generar(self):
        frame_grande = tk.Frame(App, bg="blue")
        frame_grande.grid(row=0, column=0, sticky="nsew")
        App.grid_rowconfigure(0, weight=1)
        App.grid_columnconfigure(0, weight=1)

        # Barra de menu        
        menuBar = tk.Menu(App)
        App.config(menu=menuBar)
        
        menuInicio = tk.Menu(menuBar, tearoff=False)
        menuBar.add_cascade(menu=menuInicio, label="Inicio")
    
        menuInicio.add_command( label="Salir", command = exitHandler )
        menuInicio.add_command( label="Descripcion", command = lambda: p3Label.config(text = TEXT_DATA["breveDescripcionApp"]))

        # Diferentes paneles
        p1 = tk.Frame(frame_grande, bg="green", borderwidth=1, relief="solid")
        p1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(0, weight=1)
        self.p1 = p1
        
        p2 = tk.Frame(frame_grande, bg="red", borderwidth=1, relief="solid")
        p2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(1, weight=1)
        self.p2 = p2

        p3 = tk.Frame(p1, bg="yellow", borderwidth=1, relief="solid")
        p3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        p1.grid_rowconfigure(0, weight=1)
        p1.grid_columnconfigure(0, weight=1)
        self.p3 = p1
        
        p4 = tk.Frame(p1, bg="orange", borderwidth=1, relief="solid")
        p4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        p1.grid_rowconfigure(1, weight=1)
        p1.grid_columnconfigure(0, weight=1)
        self.p4 = p4

        p5 = tk.Frame(p2, bg="purple", borderwidth=1, relief="solid")
        p5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        p2.grid_rowconfigure(0, weight=1)
        p2.grid_columnconfigure(0, weight=1)
        self.p5 = p5

        p6 = tk.Frame(p2, bg="pink", borderwidth=1, relief="solid")
        p6.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        p2.grid_rowconfigure(1, weight=1)
        p2.grid_columnconfigure(0, weight=1)
        self.p6 = p6
        #.............................

        # Corto saludo de bienvenida (P3)
        p3Label = tk.Label(p3, text = TEXT_DATA["textoBienvenida"])
        p3Label.grid(row=0,column=0,padx=5, pady=5)

        # Ingreso al sistema (P4)
        button_VentanaP = tk.Button(p4,text="Ingreso al sistema")
        button_VentanaP.grid(row=2,column=2,padx=5,pady=5)
        p4.grid_rowconfigure(1,weight=0)
        p4.grid_columnconfigure(1,weight=0)
        button_VentanaP.bind("<Button-1>", lambda e : MainMenu().generar())
        
        
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
                img = getImage(p6, path, (200, 200))
                img.grid(row= (i//2), column=(i%2), padx=10, pady=10)
                
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
        
        hojaVidaLabel = tk.Label(p5, text="", font=("timesNewRoman",10) )
        hojaVidaLabel.grid(row=0,column=0, padx=5, pady=5)
        hojaVidaLabel.bind("<Button-1>", lambda e: cambioHojaVida(hojasVida["Indice"]))
        cambioHojaVida(hojasVida["Indice"])             
        pass
    

class VentanaFuncionalidad(tk.Frame):
    
    def generar(self, zona, nombre, descripcion):
        self.zona = zona
        self.nombre = nombre
        self.descripcion = descripcion
        
        self.zonaInfo = tk.Frame(self.zona, bg="yellow", borderwidth=1, relief="solid")
        self.zonaInfo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(0, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)

        self.zonaForm = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)
        
        self.nombreProceso = tk.Label(self.zonaInfo, text= self.nombre)
        self.nombreProceso.grid(row=0, column=0, padx=5, pady=5)
        self.zonaInfo.grid_rowconfigure(0, weight=1)
        self.zonaInfo.grid_columnconfigure(0, weight=1)
        
        self.descripcionProceso = tk.Label(self.zonaInfo, text= self.descripcion)
        self.descripcionProceso.grid(row=1, column=0, padx=5, pady=5)
        self.zonaInfo.grid_rowconfigure(1, weight=1)
        self.zonaInfo.grid_columnconfigure(0, weight=1)
        
        self.ventana1()
        pass
    
class ComprarVuelo(VentanaFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, self.zonaForm)
        pass
    
    def ventana1(self):
        pass
    
    def ventana1(self):
        pass
    
    

class ReasignarVuelo(VentanaFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, self.zonaForm)
        pass
    
    
class CancelarVuelo(VentanaFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, self.zonaForm)
        pass

class CheckIn(VentanaFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, self.zonaForm)
        pass

class GestionUsuario(VentanaFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, self.zonaForm)
        pass

ventanaInicial = VentanaInicial()
ventanaInicial.generar()

App.mainloop()
