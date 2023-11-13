import tkinter.messagebox as messagebox

# Archivo temporal para tener cierta organizacion con handlers de funcionalidades?


def exitHandler():
    ok = messagebox.askokcancel("Confirmacion", "Desea salir del programa?")
    if ok:
        exit()