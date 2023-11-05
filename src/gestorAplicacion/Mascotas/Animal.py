class Animal:

    def __init__(self, nombre, raza):
        self.nombre = nombre
        self.raza = raza

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre = nombre

    def getRaza(self):
        return self.raza

    def setRaza(self, raza):
        self.raza = raza

    def puedeViajarEnCabina(self):
        pass

    def puedeViajarEnBodega(self):
        pass
