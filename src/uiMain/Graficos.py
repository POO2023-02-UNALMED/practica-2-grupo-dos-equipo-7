import tkinter as tk


App = tk.Tk()
App.title("Ventana de Inicio")
App.geometry("800x600")


#Implementar formulario generico
class FieldFrame(tk.Frame):
    """
    crea un nuevo objeto de tipo FieldFrame
    @arg tituloCriterios titulo para la columna "Criterio"
    @arg criterios array con los nombres de los criterios
    @arg tituloValores titulo para la columna "valor"
    @arg valores array con los valores iniciales; Si ‘None’, no hay valores iniciales
    @arg habilitado array con los campos no-editables por el usuario; Si ‘None’, todos son editables
    """

    def __init__(self, tituloCriterios, criterios, tituloValores, valores, habilitado, parent):
        
        #Inicializar el diccionario que guardara los datos
        self.data = {}
        self.formData = {}

        self.criterios = criterios

        #Crea el marco donde van a estar los elementos
        marco = tk.Frame(parent, bg="green", borderwidth=1, relief="solid")
        marco.grid(row=0, column=0, padx=5, pady=5)
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

            # !!!! Posicionenlos !!!!

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
        pass

class MainMenu:
    def __init__(self):
        pass

    def generar(self):

        #Botones de arriba:
        archivoButton = ""
        procesosconsultasButton = ""
        ayudaButton = ""

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

        zona1 = tk.Frame(marco, bg="yellow", borderwidth=1, relief="solid")
        zona1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        zona2 = tk.Frame(marco, bg="orange", borderwidth=1, relief="solid")
        zona2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        marco.grid_rowconfigure(1, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        self.marco = marco
        pass


class ProcesoConsulta:
    def __init__(self, zona):
        self.zona = zona
        self.nombre = "Nombre Proceso"
        self.descripcion = "Descripcion"
        
        self.criterios = []
        
        pass

    def generar(self):
        zona1 = tk.Frame(self.zona, bg="yellow", borderwidth=1, relief="solid")
        zona1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        marco.grid_rowconfigure(0, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        zona2 = tk.Frame(self.zona, bg="orange", borderwidth=1, relief="solid")
        zona2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        marco.grid_rowconfigure(1, weight=1)
        marco.grid_columnconfigure(0, weight=1)

        nombreProceso = tk.Label(zona1, text= self.nombre)
        nombreProceso.grid(row=0, column=0, padx=5, pady=5)
        zona1.grid_rowconfigure(0, weight=1)
        zona1.grid_columnconfigure(0, weight=1)

        descripcionProceso = tk.Label(zona1, text= self.descripcion)
        descripcionProceso.grid(row=1, column=0, padx=5, pady=5)
        zona1.grid_rowconfigure(1, weight=1)
        zona1.grid_columnconfigure(0, weight=1)

        formElement = FieldFrame("Preguntas", self.criterios, "Entradas", self.criterios, None, zona2)


def genComprarVuelo():
    pass

def genReasignarVuelo():
    pass


def genCancelarVuelo():
    pass


def genGestionUsuario():
    pass


def genCheckIn():
    pass


def makePopUp():
    pass



#ventanaInicial = VentanaInicial()
#ventanaInicial.generar()

mainMenu = MainMenu()
mainMenu.generar()


App.mainloop()
