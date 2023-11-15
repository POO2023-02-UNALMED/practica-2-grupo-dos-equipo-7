import pickle
from gestorAplicacion.Cuenta.Usuario import Usuario

def serializarUsuario(instanciaUsuario):
    file = open("baseDatos/temp/mainUser.pickle","wb")
    serializacion = pickle.dump(instanciaUsuario, file)
    file.close()
    return

def deserializarUsuario():
    file = open("baseDatos/temp/mainUser.pickle","rb")
    instancia = pickle.load(file)
    return instancia
