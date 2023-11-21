from .Animal import Animal

class Gato(Animal):
    """
    Clase que representa a un gato.

    Atributos:
        PESO_MAXIMO_BODEGA (float): Peso máximo que un gato puede tener para viajar en la bodega.
        PESO_MAXIMO_CABINA (float): Peso máximo que un gato puede tener para viajar en la cabina.
        peso (float): Peso del gato.
    """

    PESO_MAXIMO_BODEGA = 20.0
    PESO_MAXIMO_CABINA = 6.0

    def __init__(self, nombre, raza, peso):
        """
        Inicializa un objeto de la clase Gato.
        """
        super().__init__(nombre, raza)
        self.peso = peso

    def puedeViajarEnCabina(self):
        """
        Determina si el gato puede viajar en la cabina basándose en su peso.
        """
        return self.peso <= Gato.PESO_MAXIMO_CABINA

    def puedeViajarEnBodega(self):
        """
        Determina si el gato puede viajar en la bodega basándose en su peso.
        """
        return self.peso <= Gato.PESO_MAXIMO_BODEGA

    def __str__(self):
        """
        Devuelve una representación en cadena de la información del gato.
        """
        return f"Nombre: {self.getNombre()}, Raza: {self.getRaza()}, Peso: {self.peso}, Especie: Gato"