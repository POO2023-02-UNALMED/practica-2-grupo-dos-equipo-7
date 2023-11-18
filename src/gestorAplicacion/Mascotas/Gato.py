from .Animal import Animal

class Gato(Animal):

    PESO_MAXIMO_BODEGA = 20.0
    PESO_MAXIMO_CABINA = 6.0

    def __init__(self, nombre, raza, peso):
        super().__init__(nombre, raza)
        self.peso = peso

    def puedeViajarEnCabina(self):
        return self.peso <= Gato.PESO_MAXIMO_CABINA

    def puedeViajarEnBodega(self):
        return self.peso <= Gato.PESO_MAXIMO_BODEGA

    def __str__(self):
        return f"Nombre: {self.getNombre()}, Raza: {self.getRaza()}, Peso: {self.peso}, Especie: Gato"
