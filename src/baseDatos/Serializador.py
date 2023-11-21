# Descripción:
#       Este módulo proporciona funciones para la serialización y
#       deserialización del usuario.
# Nota:
#       Al salir de la aplicacion automaticamente se serializa el usuario y se guarda
 
import pickle

def serializarUsuario(instanciaUsuario):
    """
    Serializa un objeto Usuario y lo guarda en un archivo.
    Parámetros:
    - instanciaUsuario: La instancia del objeto Usuario a serializar.
    """
    file = open("src/baseDatos/temp/mainUser.pickle","wb")
    pickle.dump(instanciaUsuario, file)
    file.close()
    print("Usuario guardado")
    

def deserializarUsuario():
    """
    Deserializa un objeto Usuario desde un archivo y lo devuelve.
    Retorna:
    - instancia: La instancia del objeto Usuario deserializado.
    """
    file = open("src/baseDatos/temp/mainUser.pickle","rb")
    instancia = pickle.load(file)
    print("Usuario cargado")
    return instancia