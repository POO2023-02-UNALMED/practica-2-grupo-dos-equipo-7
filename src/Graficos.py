import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from uiMain.appMisc.misc import *

# ------------------------------------
# Backend (TEMPORAL)

from gestorAplicacion.Aerolinea.Asiento import Asiento
from gestorAplicacion.Aerolinea.Boleto import Boleto
from gestorAplicacion.Aerolinea.Maleta import Maleta
from gestorAplicacion.Aerolinea.Pasajero import Pasajero
from gestorAplicacion.Aerolinea.RestriccionesMaleta import RestriccionesMaleta
from gestorAplicacion.Aerolinea.ServiciosEspeciales import ServiciosEspeciales
from gestorAplicacion.Aerolinea.Vuelo import Vuelo

from gestorAplicacion.Cuenta.Usuario import Usuario
from gestorAplicacion.Cuenta.GestionUsuario import GestionUsuario

from gestorAplicacion.Descuentos.Descuento import Descuento
from gestorAplicacion.Descuentos.descuentoMaleta import descuentoMaleta
from gestorAplicacion.Descuentos.descuentoVuelo import descuentoVuelo
from gestorAplicacion.Descuentos.upgradeAsiento import upgradeAsiento

from gestorAplicacion.Mascotas.Animal import Animal
from gestorAplicacion.Mascotas.Perro import Perro
from gestorAplicacion.Mascotas.Gato import Gato
# ------------------------------------

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
    
    "Salir" : exitHandler
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
        submitButton.grid(row=index+2, column=0, padx=5, pady=5)
        marco.grid_rowconfigure(index+2, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        clearButton = tk.Button(marco, text="Clear", bg="white", borderwidth=0, command = lambda: self.clear())
        clearButton.grid(row=index+2, column=1, padx=5, pady=5)
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
    
    def clearZone(self):
        self.zonaForm.destroy()
        self.zonaForm = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        self.zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.zona.grid_rowconfigure(1, weight=1)
        self.zona.grid_columnconfigure(0, weight=1)
        
        self.ventana1()
        pass
    
class ComprarVuelo(VentanaBaseFuncionalidad):
    
    def ventana1(self):
        
        def callback(formData):
            
            vuelos = Vuelo.generarVuelos(5, formData[criterios[0]], formData[criterios[1]]) #Genera los vuelos 
            asientos = (vuelos[0]).generarAsientos(3, 5, 100)
            
            def selecAsientos(event):
                vuelo = vuelos[dropDownVuelos.current()] # Scope?
                asientos = vuelo.generarAsientos(3, 5, 100)
                dropDownAsientos["values"] = asientos
                pass
            
            # Seleccionar vuelo y asiento
            labelVuelo = tk.Label(formElement.marco, text = "Vuelo:")
            labelVuelo.grid(row=nextFreeRow, column=0, padx=5, pady=5)
            dropDownVuelos = ttk.Combobox(formElement.marco,state = "readonly", values = vuelos )
            dropDownVuelos.grid(row=nextFreeRow, column=1, padx=15, pady=15)
            dropDownVuelos.bind("<<ComboboxSelected>>", selecAsientos)
            
            labelAsiento = tk.Label(formElement.marco, text = "Asiento:")
            labelAsiento.grid(row=nextFreeRow+1, column=0, padx=5, pady=5)
            dropDownAsientos = ttk.Combobox(formElement.marco,state = "readonly",values = asientos )
            dropDownAsientos.grid(row=nextFreeRow + 1, column=1, padx=15, pady=15)
            
            labelMaletas = tk.Label(formElement.marco, text = "Cantidad de maletas:")
            labelMaletas.grid(row=nextFreeRow+2, column=0, padx=5, pady=5)
            dropDownMaletas = ttk.Combobox(formElement.marco,state = "readonly",values = [0, 1, 2, 3, 4])
            dropDownMaletas.grid(row=nextFreeRow+2, column=1, padx=15, pady=15)

            # Crea boton de siguiente y uno de cancelar  
            getBotonCancelar(formElement.marco, lambda: self.clearZone(), nextFreeRow+3, 0)
            getBotonContinuar(formElement.marco, lambda: self.ventana2(
                {
                    "vuelo": vuelos[dropDownVuelos.current()],
                    "asiento": asientos[dropDownAsientos.current()],
                    "maletas": int(dropDownMaletas.current()),
                    "boleto": ""
                }, formData # Origen, destino, cantidad maletas
            ),nextFreeRow+3, 1)
            
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
            # Agregar las maletas
            maletas = [Maleta(index+1, formData[key], 2, 2, 2) for index, key in enumerate(formData.keys())]
            #maleta.asignarBoleto(boleto)
            #boleto.addEquipaje(maleta)

            alertInfo("Previsualizacion del precio", f"Precio a pagar en total por {numMaletas} maletas: ${1}, Total: {2}")
            
            # Crea boton de siguiente y uno de cancelar  
            getBotonCancelar(formElement.marco, lambda: self.clearZone(), nextFreeRow+1, 0)
            getBotonContinuar(formElement.marco, lambda: self.ventana3(newData), nextFreeRow+1, 1)
            pass
        
        
        numMaletas = newData["maletas"]
        
        if (numMaletas == 0):
            self.ventana3(1, 2)
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

        
    def ventana3(self, newData, prevData):
        # Se muestra info del vuelo y previsualizacion de datos y se pide confirmacion
        def confirmarCompra(allData):
            pass
        
        resultFrame = ResultFrame(
            "Detalles del boleto",
            {"ok": "200"}, #boleto.getInfo()
            self.zonaForm
        )
        nextFreeRow = resultFrame.nextFreeRow
        
        getBotonCancelar(resultFrame.marco, lambda: self.clearZone(), nextFreeRow+1, 0)
        getBotonContinuar(resultFrame.marco, lambda: confirmarCompra(1), nextFreeRow+1, 1)
        pass
    

class ReasignarVuelo(VentanaBaseFuncionalidad):
    def ventana1(self):
        
        pass
    
    
class CancelarVuelo(VentanaBaseFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame(
            "Datos del Vuelo",
            [],
            "Ingrese los datos",
            [],
            None, self.zonaForm
        )
        pass

class CheckIn(VentanaBaseFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame(
            "Datos del Vuelo",
            [],
            "Ingrese los datos",
            [],
            None, self.zonaForm
        )
        pass

class GestionUsuario(VentanaBaseFuncionalidad):
    def ventana1(self):
        formElement = FieldFrame(
            "Datos del Vuelo",
            [],
            "Ingrese los datos",
            [],
            None, self.zonaForm
        )
        pass
    

def iniciar():
    usuario = 1
    pass

ventanaInicial = VentanaInicial()
ventanaInicial.generar()

App.mainloop()
