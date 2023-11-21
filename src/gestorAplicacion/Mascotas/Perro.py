from .Animal import Animal

class Perro(Animal):
    """
    Clase que representa a un perro.

    Atributos:
        PESO_MAXIMO_BODEGA (float): Peso máximo que un perro puede tener para viajar en la bodega.
        PESO_MAXIMO_CABINA (float): Peso máximo que un perro puede tener para viajar en la cabina.
        peso (float): Peso del perro.
    """

    PESO_MAXIMO_BODEGA = 30.0
    PESO_MAXIMO_CABINA = 8.0

    def __init__(self, nombre, raza, peso):
        """
        Inicializa un objeto de la clase Perro.
        """
        super().__init__(nombre, raza)
        self.peso = peso

    def puedeViajarEnCabina(self):
        """
        Determina si el perro puede viajar en la cabina basándose en su peso.
        """
        return self.peso <= Perro.PESO_MAXIMO_CABINA

    def puedeViajarEnBodega(self):
        """
        Determina si el perro puede viajar en la bodega basándose en su peso.
        """
        return self.peso <= Perro.PESO_MAXIMO_BODEGA
    
    def toString(self):
        """
        Devuelve una representación en cadena de la información del perro.
        """
        return f"Nombre: {self.getNombre()}, Raza: {self.getRaza()}, Peso: {self.peso}, Especie: Perro"