import tkinter as tk


App = tk.Tk()
App.title("Ventana de Inicio")
App.geometry("800x600")


def genVentanaInicial():
    frame_grande = tk.Frame(App, bg="blue")
    frame_grande.grid(row=0, column=0, sticky="nsew")
    App.grid_rowconfigure(0, weight=1)
    App.grid_columnconfigure(0, weight=1)

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

    welcome_label = tk.Label(frame_grande, text="Inicio",fg="red")
    welcome_label.grid(row=0,column=0,padx=5, pady=5,sticky="nw")

    saludo = "Bienvenid@ al sistema de venta de vuelos"
    saludo_label = tk.Label(p3,text=saludo)
    saludo_label.grid(row=0,column=0,padx=5, pady=5)


    """bios = [
        "Juan Carlos Largo"
    ]

    
    for bio in bios:
        bio_label = tk.Label(right_bottom, text=bio, font=("Arial", 10))
        bio_label.pack(pady=5)

    # Botón para ingresar al sistema
    login_button = tk.Button(left_bottom, text="Ingresar al sistema")
    login_button.pack(pady=10)"""
    pass

def genMainMenu():
    pass


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

genVentanaInicial()
App.mainloop()
