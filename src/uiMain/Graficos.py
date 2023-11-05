import tkinter as tk


App = tk.Tk()
App.title("Ventana de Inicio")


def genVentanaInicial():

    left_frame = tk.Frame(App, width=400, height=400)
    right_frame = tk.Frame(App, width=400, height=400)
    left_frame.grid(row=0, column=0)
    right_frame.grid(row=0, column=1)

    left_top = tk.Frame(left_frame, width=400, height=200)
    left_bottom = tk.Frame(left_frame, width=400, height=200)
    right_top = tk.Frame(right_frame, width=400, height=200)
    right_bottom = tk.Frame(right_frame, width=400, height=200)

    left_top.grid(row=0, column=0)
    left_bottom.grid(row=1, column=0)
    right_top.grid(row=0, column=0)
    right_bottom.grid(row=1, column=0)

    welcome_label = tk.Label(left_top, text="Inicio")
    welcome_label.pack(pady=10)

    bios = [
        "Juan Carlos Largo"
    ]

    
    for bio in bios:
        bio_label = tk.Label(right_bottom, text=bio, font=("Arial", 10))
        bio_label.pack(pady=5)

    # Botón para ingresar al sistema
    login_button = tk.Button(left_bottom, text="Ingresar al sistema")
    login_button.pack(pady=10)
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


App.mainloop()
