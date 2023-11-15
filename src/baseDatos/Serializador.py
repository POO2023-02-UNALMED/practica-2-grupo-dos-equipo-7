import pickle

def serializarUsuario(instanciaUsuario):
    file = open("src/baseDatos/temp/mainUser.pickle","wb")
    pickle.dump(instanciaUsuario, file)
    file.close()
    print("Usuario guardado")
    

def deserializarUsuario():
    file = open("src/baseDatos/temp/mainUser.pickle","rb")
    instancia = pickle.load(file)
    print("Usuario cargado")
    return instancia