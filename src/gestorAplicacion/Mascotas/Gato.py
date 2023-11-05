from .Animal import Animal

class Gato(Animal):

    razasExcluidasCabina = ["Siamés", "Bengal", "Sphynx", "Persa"]
    razasExcluidasBodega = ["Bengal", "Siames"]

    PESO_MAXIMO_BODEGA = 20.0
    TAMANO_MAXIMO_BODEGA = 30.0
    PESO_MAXIMO_CABINA = 6.0
    TAMANO_MAXIMO_CABINA = 15.0

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
        if (not self.raza in Gato.razasExcluidasCabina and self.getPeso() <= Gato.PESO_MAXIMO_CABINA
                and self.getTamano() <= Gato.TAMANO_MAXIMO_CABINA):
            return True

        return False

    def puedeViajarEnBodega(self):
        if (not self.raza in Gato.razasExcluidasBodega and self.getPeso() <= Gato.PESO_MAXIMO_BODEGA
                and self.getTamano() <= Gato.TAMANO_MAXIMO_BODEGA):
            return True

        return False

    def toString(self):
        return "nombre: " + self.getNombre() + ", raza: " + self.getRaza() + ", especie: Gato"
