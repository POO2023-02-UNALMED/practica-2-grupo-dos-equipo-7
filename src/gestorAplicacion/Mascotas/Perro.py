from .Animal import Animal

class Perro(Animal):

    razasExcluidasCabina = ["Bulldog", "Dóberman", "Pitbull", "Rottweiler"]
    razasExcluidasBodega = ["Pitbull", "Rottweiler"]

    PESO_MAXIMO_BODEGA = 30.0
    TAMANO_MAXIMO_BODEGA = 30.0
    PESO_MAXIMO_CABINA = 8.0
    TAMANO_MAXIMO_CABINA = 20.0

    def __init__(self, nombre, raza, tamano, peso):
        super(nombre, raza)
        self.tamano = tamano
        self.peso = peso

    def getPeso(self):
        return self.peso

    def setPeso(self, peso):
        self.peso = peso

    def getTamano(self):
        return self.tamano

    def setTamano(self, tamano):
        self.tamano = tamano

    def puedeViajarEnCabina(self):
        if ((not (self.raza in Perro.razasExcluidasCabina)) and self.getPeso() <= Perro.PESO_MAXIMO_CABINA
                and self.getTamano() <= Perro.TAMANO_MAXIMO_CABINA):
            return True
        return False

    def puedeViajarEnBodega(self):
        if ((not (self.raza in Perro.razasExcluidasBodega)) and self.getPeso() <= Perro.PESO_MAXIMO_BODEGA
                and self.getTamano() <= Perro.TAMANO_MAXIMO_BODEGA):
            return True
        return False

    def toString(self):
        return "nombre: " + self.getNombre() + ", raza: " + self.getRaza() + ", especie: Perro"
