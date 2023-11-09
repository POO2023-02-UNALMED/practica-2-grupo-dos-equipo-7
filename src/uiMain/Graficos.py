import tkinter as tk
import os
print(os.getcwd())
from PIL import Image,ImageTk


App = tk.Tk()
App.title("Ventana de Inicio")
App.geometry("800x600")


#Pop up functions

def alertWarn(errMsg, msg):
    ok = tk.messagebox.showerror(errMsg, msg)
    pass

def alertConfirmacion(msg = "Escriba aceptar para confirmar el proceso"):
    return = tk.messagebox.askokcancel("Confirmacion", msg)

def alertInfo(title, info):
    return = tk.messagebox.showinfo(title, info)




def genComprarVuelo(mainMenu):
    comprarVuelo = ProcesoConsulta(
        mainMenu.zona,
        "Comprar Vuelo",
        "En este menu el usuario podra comprar el vuelo",
        ["Origen", "Destino", "Numero Asiento"]
    )
    comprarVuelo.generar()
    pass

def genReasignarVuelo(mainMenu):
    comprarVuelo = ProcesoConsulta(
        mainMenu.zona,
        "Reasignar Vuelo",
        "Aqui el usuario podra reasignar algun vuelo anterior",
        ["ID del vuelo", "Pizza", "Secso"]
    )
    comprarVuelo.generar()
    return comprarVuelo


def genCancelarVuelo(mainMenu):
    comprarVuelo = ProcesoConsulta(
        mainMenu.zona,
        "Cancelar Vuelo",
        "En este menu el usuario podra cancelar su vuelo",
        ["ID Vuelo", "Pizza", "Secso"]
    )
    comprarVuelo.generar()
    return comprarVuelo


def genGestionUsuario(mainMenu):
    comprarVuelo = ProcesoConsulta(
        mainMenu.zona,
        "Gestion Usuario",
        "Consiste en la funcionalidad de comprar vuelo",
        ["Edad", "Pizza", "Secso"]
    )
    comprarVuelo.generar()
    return comprarVuelo


def genCheckIn(mainMenu):
    comprarVuelo = ProcesoConsulta(
        mainMenu.zona,
        "Check In",
        "Consiste en la funcionalidad de comprar vuelo",
        ["Edad", "Pizza", "Secso"]
    )
    comprarVuelo.generar()
    return comprarVuelo

handlersProcesoConsulta = {
    "Comprar vuelo": genComprarVuelo,
    "Reasignar Vuelo": genReasignarVuelo,
    "Cancelar Vuelo": genCancelarVuelo,
    "Check In": genCheckIn,
    "Gestion usuario": genGestionUsuario,
    "Salir" : lambda : exit()
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

    def __init__(self, tituloCriterios, criterios, tituloValores, valores, habilitado, parent):
        
        #Inicializar el diccionario que guardara los datos
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

        
        submitButton = tk.Button(marco, text="Enviar", bg="white", borderwidth=0, command = lambda: self.submitForm())
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

    def submitForm(self):
        for criterio in self.criterios:
            value = (self.data[criterio]["elementos"][1]).get()
            self.data[criterio]["value"] = value
            self.formData[criterio] = value

            if value == None:
                self.warnValoresFaltantes()

        print(self.formData)

    def clear(self):

        #Limpiar todos los datos
        for criterio in self.criterios:
            (self.data[criterio]["elementos"][1]).delete(0 ,'end')
                    
    def warnValoresFaltantes(self):
        #Genera la ventana y la muestra
        
        # usar ventanas emergentes automaticas de tkinter

        pass

class ResultFrame(tk.Frame):

    def __init__(self, titulo, resultados, parent):
        
        #Inicializar el diccionario que guardara los datos
        self.titulo = titulo
        self.resultados = resultados
        
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


        """#Agregar el titulo de los valores
        elementoTituloValores = tk.Label(marco, text=tituloValores)
        elementoTituloValores.grid(row=0, column=1, padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(1, weight=1)
        """
        
        #Por cada criterio agregarlos y sus respectivas entradas
        for index, resultado in enumerate(resultados):
        
            #Crea el criterio y su valor y lo guarda
            elementoCriterio = tk.Label(marco, text=resultado)
            elementoCriterio.grid(row=index+1, column=0, padx=5, pady=5)
            marco.grid_rowconfigure(index+1, weight=1)
            marco.grid_columnconfigure(0, weight=1)
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

        zonaForm = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        zonaForm.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
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

        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, zonaForm)

def makePopUp():
    pass

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

        welcome_label = tk.Label(frame_grande, text="Inicio",fg="red")
        welcome_label.grid(row=0,column=0,padx=5, pady=5,sticky="nw")

        p1 = tk.Frame(frame_grande, bg="green", borderwidth=1, relief="solid")
        p1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(0, weight=1)

        p2 = tk.Frame(frame_grande, bg="red", borderwidth=1, relief="solid")
        p2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        frame_grande.grid_rowconfigure(1, weight=1)
        frame_grande.grid_columnconfigure(1, weight=1)

        p3 = tk.Frame(p1, bg="yellow", borderwidth=1, relief="solid")
        p3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        p1.grid_rowconfigure(0, weight=1)
        p1.grid_columnconfigure(0, weight=1)

        p4 = tk.Frame(p1, bg="orange", borderwidth=1, relief="solid")
        p4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        p1.grid_rowconfigure(1, weight=1)
        p1.grid_columnconfigure(0, weight=1)

        p5 = tk.Frame(p2, bg="purple", borderwidth=1, relief="solid")
        p5.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        p2.grid_rowconfigure(0, weight=1)
        p2.grid_columnconfigure(0, weight=1)

        p6 = tk.Frame(p2, bg="pink", borderwidth=1, relief="solid")
        p6.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        p2.grid_rowconfigure(1, weight=1)
        p2.grid_columnconfigure(0, weight=1)

        saludo = "Bienvenid@ al sistema de venta de vuelos"
        saludo_label = tk.Label(p3,text=saludo)
        saludo_label.grid(row=0,column=0,padx=5, pady=5)

        
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Combinar el directorio actual con la ruta relativa a la carpeta de imágenes
        imagen_path = os.path.join(script_directory, "src\imagenes\imagen2-1.jpeg")

        # Combinar la ruta de la carpeta de imágenes con el nombre de la imagen
        #imagen_path = os.path.join(imagenes_directory, "aleja1.gif")

        def cambioVentana(evento):
            mainMenu = MainMenu()
            mainMenu.generar()

        button_VentanaP = tk.Button(p4,text="Ingreso al sistema")
        button_VentanaP.grid(row=2,column=2,padx=5,pady=5)
        p4.grid_rowconfigure(1,weight=0)
        p4.grid_columnconfigure(1,weight=0)
        button_VentanaP.bind("<Button-1>", cambioVentana)
            

        #Codigo hojas de vida

        # Guardar datos de hojas de vida
        hojasVida = {}
        for i in range(1, 6):
            hojasVida[str(i)] = open(f"src\imagenes\hojaVida{i}.txt","r").read()

        hojasVida["Indice"] = 1
        
        #Definir funcion hojas vida
        def cambioHojaVida(index):
            if index == 5:
                hojasVida["Indice"] = 1
                #imagenes["imagenIndex"]=1
            else:
                hojasVida["Indice"] +=1
                #imagenes["imagenIndex"]+=1
            
            hojaVidaLabel.config(text=hojasVida[str(hojasVida["Indice"])])
            #posicionImagen
            
        hojaVidaLabel = tk.Label(p5, text="", font=("timesNewRoman",10) )
        hojaVidaLabel.grid(row=0,column=0, padx=5, pady=5)
        hojaVidaLabel.bind("<Button-1>", lambda e: cambioHojaVida(hojasVida["Indice"]))
        hojaVidaLabel.config(text=hojasVida["1"])     

        #guardar imagenes
        """imagenes = {}
        for j in range(1,5):
            for i in range(1,5):
                imagenes[str(j)] = Image.open(f"src\imagenes\imagen{j}-{i}.jpeg")

        #Subir imagenes
        def posicionImagen(imagenIndex,a,b,numeroImagen):
            imagen_pil = Image.open(f"src\imagenes\imagen{numeroImagen}-{imagenIndex}.jpeg")
            imagen_redimensionada = imagen_pil.resize((200,200))
            imagen = ImageTk.PhotoImage(imagen_redimensionada)
            imagenLabel = tk.Label(p6,image=imagen)
            imagenLabel.grid(row=a,column=b,padx=10,pady=10)

        a,b= 0,0
        for i in range(1,5):
            if i == 2:
                a,b=0,1
            elif i ==3:
                a,b = 1,0
            elif i == 4:
                a,b = 1,1
            imagenes[str(i)] = posicionImagen(i,a,b,numeroImagen=1)"""           
        pass


ventanaInicial = VentanaInicial()
ventanaInicial.generar()

#mainMenu = MainMenu()
#mainMenu.generar()

App.mainloop()
