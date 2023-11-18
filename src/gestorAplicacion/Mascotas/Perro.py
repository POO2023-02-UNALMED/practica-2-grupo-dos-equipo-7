from .Animal import Animal

class Perro(Animal):
    PESO_MAXIMO_BODEGA = 30.0
    PESO_MAXIMO_CABINA = 8.0

    def __init__(self, nombre, raza, peso):
        super().__init__(nombre, raza)
        self.peso = peso

    def puedeViajarEnCabina(self):
        return self.peso <= Perro.PESO_MAXIMO_CABINA

    def puedeViajarEnBodega(self):
        return self.peso <= Perro.PESO_MAXIMO_BODEGA
    
    def toString(self):
        return f"Nombre: {self.getNombre()}, Raza: {self.getRaza()}, Peso: {self.peso}, Especie: Perro"
